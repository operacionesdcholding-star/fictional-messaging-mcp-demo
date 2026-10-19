"""Run an actual SDK client against the local HTTP server; no external requests."""
import asyncio
import json
import os
import socket
import subprocess
import sys
from pathlib import Path
import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def exercise(url):
    async with httpx.AsyncClient(trust_env=False) as http:
        health = await http.get(url.replace('/mcp','/healthz'))
        assert health.json()['real_whatsapp'] is False
        # Fail closed for unexpected Host values (DNS-rebinding protection).
        bad_host = await http.post(url, headers={'Host':'untrusted.example'}, json={})
        assert bad_host.status_code == 421, bad_host.status_code
    async with httpx.AsyncClient(trust_env=False) as local_http, streamable_http_client(url, http_client=local_http) as (read, write, _):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            listing = await session.list_tools()
            assert {t.name for t in listing.tools} == {'list_demo_accounts','read_demo_messages'}
            for t in listing.tools:
                assert t.annotations.readOnlyHint and not t.annotations.destructiveHint
            accounts = await session.call_tool('list_demo_accounts',{})
            assert accounts.isError is False
            assert accounts.structuredContent['synthetic'] is True
            assert accounts.structuredContent['accounts'] == ['demo_alpha','demo_beta']
            for account, prefix in [('demo_alpha','alpha_'),('demo_beta','beta_')]:
                result = await session.call_tool('read_demo_messages',{'account':account})
                assert result.isError is False
                data = result.structuredContent
                assert data['account'] == account and data['synthetic'] is True
                assert all(m['id'].startswith(prefix) for m in data['messages'])
                assert {m['direction'] for m in data['messages']} == {'incoming','echo'}
            denied = await session.call_tool('read_demo_messages',{'account':'real-account'})
            assert denied.isError is True
            absent = await session.call_tool('send_message',{})
            assert absent.isError is True
            print(json.dumps({'status':'PASS','protocol':init.protocolVersion,
                'transport':'local HTTP','tools':[t.name for t in listing.tools],
                'checks':['health','untrusted host rejected','initialize','list_tools',
                          'read annotations','call list accounts','read alpha','read beta',
                          'invalid account rejected','send tool absent'],
                'chatgpt_connection_tested':False,'events_supported':False},indent=2))

async def main():
    with socket.socket() as s:
        s.bind(('127.0.0.1',0)); port=s.getsockname()[1]
    env={**os.environ,'PORT':str(port)}
    env.pop('RENDER_EXTERNAL_HOSTNAME',None)
    log=Path('server-test.log').open('w')
    process=subprocess.Popen([sys.executable,'server.py'],env=env,stdout=log,stderr=log)
    try:
        async with httpx.AsyncClient(trust_env=False) as http:
            for _ in range(100):
                if process.poll() is not None: raise RuntimeError('Server exited; see server-test.log')
                try:
                    if (await http.get(f'http://127.0.0.1:{port}/healthz')).status_code==200: break
                except httpx.ConnectError: pass
                await asyncio.sleep(.1)
            else: raise TimeoutError('Server startup timeout')
        await exercise(f'http://127.0.0.1:{port}/mcp')
    finally:
        process.terminate()
        try: process.wait(timeout=5)
        except subprocess.TimeoutExpired: process.kill(); process.wait()
        log.close()

if __name__=='__main__': asyncio.run(main())

"""Public fictional read-only MCP demo. Never connect this app to real data."""
import os
from typing import Literal, Any
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import ToolAnnotations
from starlette.responses import JSONResponse

# RENDER_EXTERNAL_HOSTNAME is supplied by Render. No wildcard host allowlist.
allowed_hosts = ['127.0.0.1:*', 'localhost:*']
render_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')
if render_host:
    if not render_host.endswith('.onrender.com') or '/' in render_host or ':' in render_host:
        raise ValueError('Unexpected deployment hostname')
    allowed_hosts.append(render_host)

mcp = FastMCP(
    'Public fictional messaging demo',
    instructions='All records are public synthetic fixtures. This server has no WhatsApp connection, personal data, sending capability, or event subscriptions.',
    host='0.0.0.0', port=int(os.environ.get('PORT', '8000')),
    streamable_http_path='/mcp', stateless_http=True, json_response=True,
    max_request_body_size=65536,
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=True,
        allowed_hosts=allowed_hosts,
        allowed_origins=['http://127.0.0.1:*', 'http://localhost:*'] +
                        ([f'https://{render_host}'] if render_host else []),
    ),
)
ANNOTATIONS = ToolAnnotations(readOnlyHint=True, destructiveHint=False,
                              idempotentHint=True, openWorldHint=False)
FIXTURES = {
    'demo_alpha': [
        {'id': 'alpha_001', 'direction': 'incoming', 'timestamp': '2026-01-01T10:00:00Z',
         'text': 'Fictional customer asks about a fictional appointment.'},
        {'id': 'alpha_002', 'direction': 'echo', 'timestamp': '2026-01-01T10:05:00Z',
         'text': 'Fictional operator replies that the example appointment is confirmed.'},
    ],
    'demo_beta': [
        {'id': 'beta_001', 'direction': 'incoming', 'timestamp': '2026-01-01T11:00:00Z',
         'text': 'Fictional customer asks about a fictional product.'},
        {'id': 'beta_002', 'direction': 'echo', 'timestamp': '2026-01-01T11:05:00Z',
         'text': 'Fictional operator replies that the example product is available.'},
    ],
}

@mcp.tool(annotations=ANNOTATIONS, structured_output=True)
def list_demo_accounts() -> dict[str, Any]:
    """List two public fictional account IDs. No real accounts or private information."""
    return {'synthetic': True, 'accounts': sorted(FIXTURES)}

@mcp.tool(annotations=ANNOTATIONS, structured_output=True)
def read_demo_messages(account: Literal['demo_alpha', 'demo_beta']) -> dict[str, Any]:
    """Read static public fictional messages for exactly one demo account. Does not access WhatsApp."""
    return {'synthetic': True, 'account': account, 'messages': FIXTURES[account]}

@mcp.custom_route('/healthz', methods=['GET'])
async def health(request):
    return JSONResponse({'status':'ok', 'mode':'public-synthetic-read-only', 'real_whatsapp':False})

if __name__ == '__main__':
    mcp.run(transport='streamable-http')

# Public fictional MCP HTTP demo

## Status
Working local HTTP MCP server using official Python MCP SDK 1.29.0.
Independent client process performed initialize, tools/list and tools/call successfully.
Negotiated protocol: 2025-11-25. This is NOT an MCP Events implementation.
No deployment, actual ChatGPT installation, OAuth, Meta connection or real WhatsApp test has been performed.

## Boundaries
Only hard-coded fictional public records. Names are demo_alpha and demo_beta; there are no user names, telephone numbers, contacts, actual messages or credentials.
The two tools are list_demo_accounts and read_demo_messages. No write/send tool exists. No database or external API is used. Authentication is intentionally absent because everything exposed is public fictional demonstration data. This setup MUST NOT be used for real data.
A HTTP MCP request uses POST even for read-only tools; it does not change source data.
Host allowlist and 64 KiB request-body limit are enabled. This is a functional demo, not a production security certification. Standard server logs may contain HTTP client metadata, so do not submit personal information in requests.

## Local verification
Python 3.12.14 was used here. Dependencies: pip install -r requirements.txt
Run: python test_client.py
The client starts and stops a local server subprocess and verifies health, denied foreign Host, initialize, tool discovery, read-only annotations, both accounts, invalid account rejection and absence of send tool.
See test-results.json. Only local loopback requests bypass environment proxy settings; no external network is used by the test.

## Render deployment contract
Publish these files as the root of a dedicated demo source repository, or use an equivalent officially supported source-upload route if the connected Render tool exposes it. Do not publish an existing user repository or unrelated workspace files.
render.yaml explicitly requests plan: free. Do not remove that field and accept a platform default. No database, persistent disk, worker, cron job, custom domain or paid service.
Build: pip install -r requirements.txt
Start: python server.py
Health: /healthz
MCP endpoint: /mcp
Render supplies PORT and RENDER_EXTERNAL_HOSTNAME. The server validates the exact onrender.com hostname. Automatic redeploy is disabled.
If Render cannot offer the Free service, stop. Do not substitute a paid instance or authorize payment.
Python version support and dependency installation still need verification in the actual Render build; local success is not a cloud-build pass.
Source-repository publication and connection require an authorized route. A ZIP in Library is not itself a supported Render deployment source. No repository or image has been published.

## Acceptance after authorized deployment
1. Confirm actual plan is Free and no ancillary paid resources were created.
2. GET the returned HTTPS /healthz and verify real_whatsapp=false.
3. Run the SDK client read sequence against the exact returned HTTPS /mcp URL using normal network settings.
4. Create/install the custom MCP plugin with the user's required approval. Use No authentication ONLY for this fictional public demo.
5. Read both fictional accounts from the intended dot and confirm tool outputs are labeled synthetic.
6. Report installation and reading as verified only after success in that dot. Do not claim event monitoring.

Render Free sleeps after inactivity. This is acceptable for a short manual demonstration but not continuous monitoring. No periodic keep-alive jobs should be created to disguise this limitation.

## Sources
- Official SDK guidance: https://developers.openai.com/plugins/build/mcp-server
- Custom plugin installation: https://developers.openai.com/api/docs/guides/custom-mcp-server
- Render Blueprint specification: https://render.com/docs/blueprint-spec
- Free-plan limitations: https://render.com/docs/free

## Next phase, outside this demo
Actual account authentication and per-account authorization, secured persistent storage, MCP Events protocol compatibility, provider webhook validation, explicit data-sharing approvals, and WhatsApp coexistence remain separate work. None are enabled by this package.

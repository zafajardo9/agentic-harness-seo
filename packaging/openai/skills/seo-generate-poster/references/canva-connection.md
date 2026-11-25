# Connect Canva for poster generation

Each user signs in to their own Canva account and authorizes their host. The
host handles credentials and the poster profile stores creative settings.

## Codex

1. Install the **Canva** connector from the desktop Plugins Directory and
   follow its prompts to connect your Canva account.
2. Enable Canva in your chat and start a new chat if the connector or skill
   was just installed. Invoke `seo-generate-poster` from the installed
   Agentic Harness SEO Planner plugin or ask for that skill by name.

## Claude Code

Reuse an authenticated Canva MCP server if one is already configured. For a
new direct connection, create an app in the Canva Developer Portal and enable
Canva MCP for that app. Register `http://localhost:8765/callback` as an OAuth
redirect URI, then run the following with the app's client ID. If you select
another callback port, use the same port in Canva and Claude Code.

```bash
claude mcp add --scope user --transport http \
  --client-id YOUR_CANVA_CLIENT_ID --client-secret --callback-port 8765 \
  canva https://api.canva.com/connect/v1/mcp
```

Enter the client secret at Claude Code's masked terminal prompt and use
`/mcp` in Claude Code to finish browser sign-in. If authorization expires, use
the same host connection to sign in again.

[Canva MCP access](https://www.canva.dev/docs/apps/mcp/access/) · [Claude Code OAuth configuration](https://code.claude.com/docs/en/mcp#use-pre-configured-oauth-credentials)

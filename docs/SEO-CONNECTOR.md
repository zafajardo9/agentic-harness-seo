# Connect Agentic Harness SEO

## Codex planner marketplace

Install the planner from the [repository marketplace](../README.md#codex).
The catalog points to the self-contained plugin in `packaging/openai/`. Refresh
the checked-in package when the planning workflow, templates, poster skill,
starter profiles, notices, or version change:

```bash
./scripts/agentic-harness-seo run package_openai_plugin.py --sync-repo
```

## ChatGPT planning plugin without hosting

Download `agentic-harness-seo-planner.zip` from a successful **Build SEO planner
packages** run in GitHub Actions, or build it from a checkout using the
commands below. The ZIP includes the roadmap skill, shared planning workflow, and six industry
templates. It uses the evidence available to the chat, such as accessible web
pages and supplied project materials.

```bash
bash ./scripts/agentic-harness-seo setup --skip-browser
bash ./scripts/agentic-harness-seo run package_openai_plugin.py dist/agentic-harness-seo-planner.zip
```

Upload the ZIP in the OpenAI Plugins dashboard as a **Skills only** plugin.
Public directory publication requires developer verification and review.
OpenAI currently requires a separate submission for a version with MCP if the
original plugin was submitted as skills only. [OpenAI plugin submission guide](https://developers.openai.com/plugins/deploy/submission)

## Claude chat planning skill without hosting

Download `seo-roadmap.zip` from the **Build SEO planner packages** workflow or
build it locally:

```bash
bash ./scripts/agentic-harness-seo setup --skip-browser
bash ./scripts/agentic-harness-seo run package_openai_plugin.py dist/seo-roadmap.zip --claude-skill
```

In Claude, open **Customize → Skills → Create skill → Upload a skill** and
upload the ZIP. With the skill enabled, ask Claude to use the SEO roadmap
skill for a deployed URL or an unpublished project. It uses available chat
evidence and the bundled templates. [Claude custom skills](https://support.claude.com/en/articles/12512180-use-skills-in-claude)

## SEO tools over MCP

The MCP server provides three tools for SEO planning.

| Tool | Input | Result |
| --- | --- | --- |
| `seo_audit_page` | One public HTTP(S) page URL | Findings and evidence from the toolkit's deterministic on-page checks |
| `seo_check_html` | Rendered HTML and the intended URL | The same checks on supplied HTML, without fetching the URL |
| `seo_planning_framework` | An industry such as `saas`, `local-service`, or `ecommerce` | The existing planning workflow and an industry template for the assistant to use |

The live tool checks raw HTML, including server-rendered markup. For a
JavaScript-rendered project, open the page in the browser and provide rendered
HTML. Site-wide audits, browser rendering, and credentialed analytics are
available through the [coding-agent toolkit](HARNESSES.md).

## ChatGPT and Claude chat

GitHub distributes the code and the Claude Code marketplace manifest. ChatGPT
and Claude chat connect to the running MCP server at an HTTPS URL.

Deploy the repository's Dockerfile to a container host and expose its port
through HTTPS. The container listens on port 8000 or the host's `PORT` value.
Set `SEO_MCP_HOSTS` to the hostname forwarded in the HTTP Host header, for
example `seo.example.com`. Use spaces to separate multiple permitted hosts.
The server exposes `/mcp` over Streamable HTTP. The endpoint accepts unauthenticated
requests, so use host-level rate limits and expose it only when that access is
appropriate. It serves public-page checks and HTML submitted by the client.

1. In ChatGPT developer mode, create a custom app with
   `https://seo.example.com/mcp` as the MCP server URL and select no
   authentication. Enable the app in a chat. App availability and permissions
   depend on the workspace. [ChatGPT custom app setup](https://help.openai.com/en/articles/12584461-developer-mode-and-full-mcp-connectors-in-chatgpt-beta)
2. In Claude, add a custom connector with the same HTTPS URL and enable it in a
   chat. [Claude custom connector setup](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)

To bundle the planning skill and deployed MCP tools for OpenAI plugin
distribution, build the **Agentic Harness SEO Live** ZIP with your actual
endpoint:

```bash
bash ./scripts/agentic-harness-seo run package_openai_plugin.py dist/agentic-harness-seo-live.zip --mcp-url https://seo.example.com/mcp
```

Upload this ZIP using **With MCP** when you create the plugin draft. Complete
domain verification and provide the listing and review materials requested by
the dashboard. [OpenAI plugin submission guide](https://developers.openai.com/plugins/deploy/submission)

## Codex and local MCP clients

From a checkout, initialize the managed runtime and register the server. On
Windows, use Git Bash for the commands below and supply the absolute path to
Git's `bash.exe` and the checkout's launcher when configuring a desktop client.

```bash
bash ./scripts/agentic-harness-seo setup --skip-browser
codex mcp add agentic-harness-seo -- bash "$PWD/scripts/agentic-harness-seo" run seo_mcp.py
codex mcp get agentic-harness-seo
```

Start a new Codex chat after registration. Other local MCP clients can use the
same command and arguments with the stdio transport. Remote MCP clients can use
the HTTPS endpoint. Claude Code can also use the
[native marketplace plugin](../README.md#install) for the full toolkit.

## Try both workflows

- Deployed site: “Use Agentic Harness SEO to check these live pages, then build
  a 90-day SEO roadmap with priorities and success metrics.”
- Project in development: “Use Agentic Harness SEO to check my homepage's
  rendered HTML and build a launch plan for a SaaS site.”

Confirm the assistant calls the matching page-check tool and the planning tool.
The roadmap should cite page findings and identify which metrics still need
data from sources such as Search Console.

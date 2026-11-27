# Connect Agentic Harness SEO

## Codex and Claude Code

Install from the [repository marketplace](../README.md#install). Both native
manifests register the same core skills, optional extension workflows, and
`seo-roadmap` entry. Run `claude plugin validate .` to see the Claude Code
commands. In Codex, select a workflow by its skill name in the composer.

When adding a skill or changing a planning template, refresh both manifests
and the bundled roadmap references:

```bash
./scripts/agentic-harness-seo run package_openai_plugin.py --sync-repo
```

## Hosted plugin packages

Download the ZIP for your host from the **Build SEO plugin packages** GitHub
Actions workflow, or build both from a clean checkout:

```bash
./scripts/agentic-harness-seo setup --skip-browser
./scripts/agentic-harness-seo run package_openai_plugin.py dist/agentic-harness-seo-planner.zip
./scripts/agentic-harness-seo run package_openai_plugin.py dist/agentic-harness-seo-claude.zip --claude-plugin
```

- **ChatGPT** uses `agentic-harness-seo-planner.zip`. Upload it as a skills-only
  plugin in the OpenAI Plugins dashboard. Enable the uploaded plugin in ChatGPT,
  then search the skill picker for entries such as `seo-audit` or `seo-roadmap`.
  Public listings require submission and review. [OpenAI upload guide](https://developers.openai.com/plugins/deploy/submission)
- **Claude chat and Cowork** use `agentic-harness-seo-claude.zip`. Upload it as a
  custom **plugin** in Claude. Use `/` or the `+` menu to find the installed
  workflows. The separate `seo-roadmap.zip` remains available for accounts
  that want a standalone planning skill. [Claude plugin guide](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)

The hosted packages include the same workflow names. They use the host's
available browsing, connectors, and supplied evidence. Features that require
a local shell, Chromium, credentials, or persistent storage depend on the
host's runtime and connected services. Each workflow identifies evidence gaps
when those capabilities are unavailable.

## SEO tools over MCP

The MCP server lists and loads the same workflows for clients with MCP tools.
Clients that support MCP prompts can also select each workflow by name in their
prompt picker.

| Tool | Input | Result |
| --- | --- | --- |
| `seo_audit_page` | One public HTTP(S) page URL | Findings and evidence from the toolkit's deterministic on-page checks |
| `seo_check_html` | Rendered HTML and the intended URL | The same checks on supplied HTML, without fetching the URL |
| `seo_list_workflows` | None | Names of all packaged workflows |
| `seo_workflow` | Skill name and optional bundled resource path | Workflow instructions, resource list, or one bundled resource |
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

Start a new Codex chat after registration. Ask for `seo_list_workflows` to browse the catalog. Other local MCP clients can use the
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

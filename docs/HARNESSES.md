# Using Agentic Harness SEO in other AI harnesses

The native Codex and Claude Code plugins expose the same SEO workflows.
The [hosted builds](SEO-CONNECTOR.md) carry the same catalog into ChatGPT
and Claude chat. Use the portable installer for workspace registration in
other coding agents or to install locally without a marketplace.

The installer copies the toolkit to a stable location, rewrites launcher
paths, adds a PATH-ready wrapper, and registers each workflow with the
host. Re-running the installer updates managed entries. If a project
already defines a skill with the same name, the installer preserves the
existing skill and reports the conflicting path.

## Support matrix

| Harness | Where workflows appear |
|---|---|
| **Claude Code** | Native marketplace plugin. Type `/agentic-harness-seo:` for skills. |
| **OpenAI Codex** | Native marketplace plugin or project `.agents/skills/`. Select a skill in the composer. |
| **Google Antigravity** | Project `.agents/skills/`. Select or request a skill by name. |
| **Gemini CLI** | Project `.agents/skills/`. Run `/skills list` to browse. |
| **Cursor** | Project `.agents/skills/`. Select a skill from the Agent menu. |
| **Grok Build** | Project `.grok/skills/`. Run `/skills` or select a workflow by name. |
| **Cline** | Project `.cline/skills/`. Enable Skills in Cline and browse its Skills panel. |
| **Aider** | `CONVENTIONS.md` contains the workflow catalog. Read it in the session and ask for a workflow by name. |
| **ChatGPT** | Hosted plugin. Find the workflows in the skill picker. |
| **Claude chat and Cowork** | Hosted plugin. Open the `/` or `+` picker. |
| **Other MCP clients** | `seo_list_workflows` catalogs workflows and `seo_workflow` loads them. |

## Install

Run this from a checkout of this repository, with Python 3.11 to 3.14 on PATH:

```bash
git clone https://github.com/zafajardo9/agentic-harness-seo.git
cd agentic-harness-seo
python3 scripts/portable_install.py --project ~/my-site --harnesses all
```

`--harnesses` takes one or more of `codex`, `antigravity`, `grok`, `gemini`,
`cursor`, `cline`, `aider`, or `all`. The installer also writes each host's workspace instruction file. On machines
with a native Codex or Claude plugin, use the matching marketplace install to
keep a single set of skill entries.

Then build the managed environment once and put the launcher on PATH:

```bash
export PATH="$HOME/.agentic-harness-seo/bin:$PATH"
"$HOME/.agentic-harness-seo/scripts/agentic-harness-seo" setup
"$HOME/.agentic-harness-seo/scripts/agentic-harness-seo" doctor --json
```

Windows: the launcher is a bash script, so run it from Git Bash or WSL. The
environment build and every audit then work the same way. `install.ps1` path and
`AGENTIC_HARNESS_SEO_PYTHON` still apply.

## How the launcher is resolved

Every skill says to run `"${CLAUDE_PLUGIN_ROOT}/scripts/agentic-harness-seo"`.
Outside Claude Code that variable is unset, so resolve the launcher in this order
and use the same subcommands:

1. `"${CLAUDE_PLUGIN_ROOT}/scripts/agentic-harness-seo"` when the variable is set.
2. `"$AGENTIC_HARNESS_SEO_ROOT/scripts/agentic-harness-seo"` when that variable is set.
3. `"$HOME/.agentic-harness-seo/scripts/agentic-harness-seo"` for a portable install.
4. `"./scripts/agentic-harness-seo"` when this repository is the workspace.

Never invoke the bundled Python with a bare interpreter, and never run the
scripts through a system `pip install`. The launcher owns the environment.

## What the model gets

The managed block points the model at `skills/harness-seo/SKILL.md` for routing and at
`agents/` for the 20 specialists. The skills are the same files Claude Code
loads, so the audit logic, the scoring, and the JSON contracts do not change.
The bundled scripts do the work in every harness: fetch, parse, call APIs, and
score.

## What differs from Claude Code

| Capability | Claude Code | Other harnesses |
|---|---|---|
| Schema validation hook | Runs on every `Edit`/`Write` | Not available; run `hooks/validate-schema.py` yourself |
| Sub-agent fan-out | Parallel, separate contexts | Sequential or in one context, depending on harness |
| Model tiering (`model: sonnet`) | Honoured | Ignored; the harness picks the model |
| Workflow invocation | Native plugin skills and slash commands | Host skill picker or ask by name |
| MCP extensions | Via the plugin's MCP config | Only where the harness supports MCP servers |
| Drift baselines | SQLite under the data dir | Same, in the portable install's data dir |

None of this changes the analysis itself. It changes how much runs in parallel
and which integrations are reachable.

## Troubleshooting

- `doctor --json` reports whether the managed environment and Chromium are ready.
  It never prints absolute paths or environment values.
- If an instruction still shows `${CLAUDE_PLUGIN_ROOT}` in a project you edited
  by hand, replace the token with the toolkit root, or re-run the installer.
- `command not found` for the launcher means `<root>/bin` is not on PATH. Use the
  absolute launcher path instead.
- Hosts without a local shell can use the [SEO connector](SEO-CONNECTOR.md) for
  deterministic page checks and workflow resources. The coding-agent runtime
  provides site-wide shell checks and browser automation.

# Using Agentic Harness SEO in other AI harnesses

Claude Code is the full-featured path. It installs the toolkit as a plugin,
expands `${CLAUDE_PLUGIN_ROOT}` inside skill bodies, runs the schema hook, and
fans work out to sub-agents with their own tool allowlists.

Codex also supports a [native install for the SEO Planner](../README.md#codex).
For the full toolkit, Cursor, Google Antigravity, Gemini CLI, OpenAI Codex CLI,
Cline, Aider and Grok Build read workspace instructions and give the model a
shell. The portable installer sets up the full toolkit for those harnesses:

1. It copies the toolkit to a stable directory, `~/.agentic-harness-seo` by default.
2. It rewrites the `${CLAUDE_PLUGIN_ROOT}` token in the installed Markdown to that
   absolute path, exactly as the manual Claude installer does.
3. It writes a launcher wrapper under `<root>/bin` so the toolkit is one PATH
   entry away.
4. It writes the harness's own instruction file into your project, inside a
   managed block that a later run replaces instead of duplicating.

## Support matrix

| Harness | File the installer writes | Notes |
|---|---|---|
| **Claude Code** | plugin marketplace (native) | Hooks, sub-agents, MCP extensions. Use the plugin path in the README |
| **OpenAI Codex** | Native marketplace or portable `AGENTS.md` | Install the planner through the marketplace. Use the portable install for full audits and shell tools |
| **Google Antigravity** | `AGENTS.md` | Reads `AGENTS.md` first, falls back to `skills/`. Skills appear as workspace knowledge |
| **Grok Build** | `AGENTS.md` | Reads `AGENTS.md` and Claude-compatible skill layouts |
| **Gemini CLI** | `GEMINI.md` | Reads `GEMINI.md`. Skills are activated in conversation, not as slash commands |
| **Cursor** | `.cursor/rules/agentic-harness-seo.mdc` | Agent Requested rule. Symlink `skills/` into `.cursor/rules/` if you want per-skill rules |
| **Cline** | `.clinerules/agentic-harness-seo.md` | Loads rules from `.clinerules/`. Sub-agent delegation happens in one context |
| **Aider** | `CONVENTIONS.md` | Add `read: CONVENTIONS.md` to `.aider.conf.yml`, or use the `AGENTS.md` block. Aider has no sub-agent dispatch |
| **ChatGPT** | Skills-only plugin or custom app | Use the [planning plugin or hosted SEO MCP tools](SEO-CONNECTOR.md) |
| **Claude chat** | Custom skill or connector | Use the [planning skill or hosted SEO MCP tools](SEO-CONNECTOR.md) |
| **Other MCP clients** | Local or remote MCP configuration | See [SEO connector setup](SEO-CONNECTOR.md) |

## Install

Run this from a checkout of this repository, with Python 3.11 to 3.14 on PATH:

```bash
git clone https://github.com/zafajardo9/agentic-harness-seo.git
cd agentic-harness-seo
python3 scripts/portable_install.py --project ~/my-site --harnesses all
```

`--harnesses` takes one or more of `codex`, `antigravity`, `grok`, `gemini`,
`cursor`, `cline`, `aider`, or `all`. The same `.md` block is written for every
harness that reads markdown; Cursor gets the `.mdc` frontmatter it requires.

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
| `/harness-seo` slash commands | Native | Ask in plain language; the model reads `AGENTS.md` or `SKILL.md` |
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
- A harness that cannot run a shell cannot run the audits. It can still read
  SKILL.md files as context, but every deterministic check needs the scripts.

# Agentic Harness SEO: Multi-Platform Agent Instructions

> For **Cursor**, **Cursor Cloud Agents**, **Google Antigravity**, **Gemini CLI**,
> **Grok Build**,
> **OpenAI Codex CLI**, **Cline**, **Aider**, and any other agent harness that
> reads project-root agent instructions.
>
> Claude Code users: see `CLAUDE.md` instead.

## Cross-platform portability (v2.0.0)

Every skill in `skills/*/SKILL.md` is authored to a portable subset of the
Claude Code skill spec. Validate compatibility with your harness via:

```bash
./scripts/agentic-harness-seo run portability_check.py
```

The check confirms each `SKILL.md` has the minimum frontmatter every harness
expects (`name`, `description`, optional `model`, optional `tools`) and warns
on Claude-Code-specific features (`maxTurns`, multi-line tool list with
descriptive comments) that other harnesses may ignore but do not reject.

### Install for any harness

Claude Code installs the native plugin from the marketplace. ChatGPT, Claude
chat, and other MCP clients can connect to the [SEO MCP server](docs/SEO-CONNECTOR.md).
For coding agents that load workspace instructions, `scripts/portable_install.py`
writes the right file and installs the local toolkit:

```bash
python3 scripts/portable_install.py --project ~/my-site --harnesses all
```

It copies the toolkit to `~/.agentic-harness-seo`, rewrites the launcher token in
the installed Markdown, adds a wrapper under `bin/`, and writes a managed block
into `AGENTS.md` (Codex, Antigravity, Grok), `GEMINI.md` (Gemini CLI),
`.cursor/rules/agentic-harness-seo.mdc` (Cursor), `.clinerules/` (Cline) or
`CONVENTIONS.md` (Aider). The full matrix, including what each harness loses
against Claude Code, is in `docs/HARNESSES.md`.

### Resolving the launcher outside Claude Code

Claude Code expands `${CLAUDE_PLUGIN_ROOT}`; other harnesses do not. Resolve the
launcher in this order and use the same subcommands:

1. `"${CLAUDE_PLUGIN_ROOT}/scripts/agentic-harness-seo"` when the variable is set.
2. `"$AGENTIC_HARNESS_SEO_ROOT/scripts/agentic-harness-seo"` when that variable is set.
3. `"$HOME/.agentic-harness-seo/scripts/agentic-harness-seo"` for a portable install.
4. `"./scripts/agentic-harness-seo"` when this repository is the workspace.

Never invoke the bundled Python with a bare interpreter: the launcher owns the
managed environment.

### Per-harness notes

| Harness | Instruction file | How it loads Agentic Harness SEO |
|---|---|---|
| **Cursor** | `.cursor/rules/agentic-harness-seo.mdc` | The portable install writes the rule; symlink `skills/` and `agents/` into `.cursor/rules/` for per-skill rules. Commands are text prompts |
| **Cursor Cloud Agents** | `AGENTS.md` | Push the repo; Cloud Agents read `AGENTS.md` at session start |
| **Google Antigravity** | `AGENTS.md` | Reads `AGENTS.md` first, falls back to `skills/` |
| **Gemini CLI** | `GEMINI.md` | `gemini init` loads `GEMINI.md`; skills are activated in conversation |
| **Grok Build** | `AGENTS.md` | Reads `AGENTS.md` and Claude-compatible skill layouts; `grok inspect` verifies discovery. See the [official compatibility guide](https://docs.x.ai/build/features/skills-plugins-marketplaces) |
| **OpenAI Codex CLI** | `AGENTS.md` | Reads project-root `AGENTS.md`; Claude-specific tool names are aliased to Codex equivalents |
| **Cline** | `.clinerules/agentic-harness-seo.md` | Loads `.clinerules/`; sub-agent delegation happens in one context |
| **Aider** | `CONVENTIONS.md` or `AGENTS.md` | No sub-agent dispatch; the seo-* skills run inline |

### Tool-name compatibility

Where agentic-harness-seo skills mention Claude Code tools (`Read`, `Write`, `Edit`,
`Bash`, `Glob`, `Grep`, `WebFetch`), each harness typically has an equivalent:

| Claude Code | Codex | Cline | Aider | Cursor / Antigravity |
|---|---|---|---|---|
| Read       | read_file        | read_file       | (inline)        | read |
| Write      | write_file       | write_file      | /add then edit  | write |
| Edit       | apply_diff       | replace_in_file | /edit           | edit |
| Bash       | bash             | execute_command | /run            | shell |
| Glob       | glob             | search_files    | (inline)        | find |
| Grep       | grep             | search_files    | /grep           | grep |
| WebFetch   | fetch / browse   | (browser tool)  | (n/a)           | fetch |

These mappings are automatic in most harnesses; we list them for transparency
in case a recipe needs a specific call.

## Overview

Agentic Harness SEO is a Tier 4 SEO analysis skill with 30 sub-skills (23 core + 1 orchestrator +
1 framework integration + 5 extension mirrors), 20 sub-agents (16 core + 1 framework
integration + 3 extension mirrors), and 70 Python execution scripts.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/harness-seo audit <url>` | Full website audit with parallel subagent delegation |
| `/harness-seo page <url>` | Deep single-page analysis |
| `/harness-seo technical <url>` | Technical SEO audit (9 categories) |
| `/harness-seo content <url>` | E-E-A-T and content quality analysis |
| `/harness-seo content-brief <topic>` | Generate a content brief for a topic |
| `/harness-seo schema <url>` | Schema.org detection, validation, generation |
| `/harness-seo sitemap <url>` | XML sitemap analysis or generation |
| `/harness-seo images <url>` | Image SEO: on-page audit, SERP analysis, file optimization |
| `/harness-seo geo <url>` | AI Overviews / Generative Engine Optimization |
| `/harness-seo plan <type>` | Strategic SEO planning |
| `/harness-seo cluster <keyword>` | SERP-based semantic clustering and content architecture |
| `/harness-seo sxo <url>` | Search Experience Optimization: page-type analysis, personas |
| `/harness-seo drift baseline <url>` | Capture SEO baseline for change monitoring |
| `/harness-seo drift compare <url>` | Compare current state to stored baseline |
| `/harness-seo drift history <url>` | Show drift history over time |
| `/harness-seo ecommerce <url>` | E-commerce SEO: product schema, marketplace intelligence |
| `/harness-seo programmatic [url]` | Programmatic SEO at scale |
| `/harness-seo competitor-pages [url]` | Competitor comparison pages |
| `/harness-seo flow [stage]` | FLOW framework prompts (Find, Leverage, Optimize, Win, Local; prompts/sync utilities.) |
| `/harness-seo local <url>` | Local SEO analysis (GBP, citations, reviews) |
| `/harness-seo maps [cmd] [args]` | Maps intelligence (geo-grid, GBP audit, competitors) |
| `/harness-seo hreflang <url>` | Hreflang/i18n SEO audit, cultural profiles, content parity |
| `/harness-seo google [cmd] [url]` | Google SEO APIs (GSC, PageSpeed, CrUX, Indexing, GA4) |
| `/harness-seo backlinks <url>` | Backlink profile analysis |
| `/harness-seo backlinks setup` | Setup free backlink APIs |
| `/harness-seo backlinks verify <url>` | Verify known backlinks still exist |
| `/harness-seo dataforseo [cmd]` | Live SEO data via DataForSEO (extension) |
| `/harness-seo image-gen [use-case]` | AI image generation for SEO assets (extension) |
| `/harness-seo generate-poster <profile> [brief]` | Editable Canva social poster or creative profile setup |
| `/harness-seo firecrawl [cmd] <url>` | Full-site crawling and site mapping (extension) |
| `/harness-seo ahrefs [cmd] <target>` | Ahrefs backlink and keyword data (extension) |
| `/harness-seo bing [cmd] <url>` | Bing Webmaster data and IndexNow (extension) |
| `/harness-seo profound [cmd]` | LLM brand-citation tracking (extension) |
| `/harness-seo seranking [cmd]` | AI share-of-voice tracking (extension) |
| `/harness-seo matomo [cmd] [args]` | Matomo Reporting API: GA4 alternative or supplement (extension) |
| `/harness-seo posthog [cmd]` | PostHog via MCP: GA4 alternative or supplement (extension) |
| `/harness-seo unlighthouse <url>` | Multi-page Lighthouse audits (extension) |
| `/harness-seo shopify [crawl\|check] <url>` | Signed crawl of a Shopify store you administer, then the audit (extension) |

## Using with Cursor / Cursor Cloud

Cursor reads this file automatically. All SKILL.md files contain the full
analysis logic as natural language instructions. Python scripts in `scripts/`
provide execution capabilities.

**Running scripts directly** (Cursor doesn't have MCP):
```bash
# Page fetching with SSRF protection
./scripts/agentic-harness-seo run fetch_page.py https://example.com

# HTML parsing for SEO elements
./scripts/agentic-harness-seo run parse_html.py --url https://example.com

# PageSpeed Insights
./scripts/agentic-harness-seo run pagespeed_check.py https://example.com --json

# Drift baseline
./scripts/agentic-harness-seo run drift_baseline.py https://example.com

# DataForSEO (requires credentials)
DATAFORSEO_USERNAME=user DATAFORSEO_PASSWORD=pass ./scripts/agentic-harness-seo run dataforseo_merchant.py search "keyword"
```

**Cursor Cloud gotchas:**
- SSL certificates may not resolve for some domains. Investigate the certificate issue rather than disabling verification.
- Run bundled tools through `agentic-harness-seo`; never call the venv interpreter directly.
- Screenshots save to `/tmp/` not CWD. Check absolute paths.

## Using with Google Antigravity

Antigravity discovers this project via `.claude-plugin/plugin.json`.
Place the repo in `~/.gemini/antigravity/plugins/agentic-harness-seo/` or install via:

```bash
bash install.sh
```

## Architecture

```
skills/                    # 30 sub-skills (auto-discovered)
  harness-seo/SKILL.md    # Main orchestrator + routing
  seo-cluster/            # Semantic clustering (v1.9.0)
  seo-sxo/                # Search Experience Optimization (v1.9.0)
  seo-drift/              # SEO drift monitoring (v1.9.0)
  seo-ecommerce/          # E-commerce SEO (v1.9.0)
  seo-audit/              # Full site audit
  seo-page/               # Single-page analysis
  seo-technical/          # Technical SEO
  seo-content/            # E-E-A-T quality
  seo-content-brief/      # Content brief generation
  seo-schema/             # Schema.org markup
  seo-sitemap/            # XML sitemaps
  seo-images/             # Image optimization
  seo-geo/                # AI search / GEO
  seo-agentic/            # Agent readiness (Lighthouse Agentic Browsing, WebMCP)
  seo-local/              # Local SEO
  seo-maps/               # Maps intelligence
  seo-plan/               # Strategic planning
  seo-hreflang/           # International SEO
  seo-google/             # Google APIs
  seo-backlinks/          # Backlink analysis
  seo-programmatic/       # Programmatic SEO
  seo-competitor-pages/   # Competitor pages
  seo-flow/               # FLOW framework integration
  seo-dataforseo/         # DataForSEO (extension)
  seo-image-gen/          # AI images (extension)
  seo-generate-poster/   # Editable Canva posters and creative profiles
  seo-bing/               # Bing Webmaster and IndexNow (extension)
  seo-shopify/            # Shopify Crawler Access signed crawl (extension)
  seo-posthog/            # PostHog analytics via MCP (extension)
agents/                    # 20 subagents
scripts/                   # 70 Python scripts, including the managed runtime
schema/                    # JSON-LD templates
extensions/                # 11 extensions. 5 MCP: DataForSEO, Firecrawl, Banana, Ahrefs, PostHog. 6 non-MCP: SE Ranking, Profound, Bing Webmaster, Matomo, Unlighthouse, Shopify
```

## Key Principles

1. **Progressive Disclosure**: Read SKILL.md for routing, load references on demand
2. **Industry Detection**: Auto-detect SaaS, e-commerce, local, publisher, agency
3. **Security**: All scripts call `validate_url()` for SSRF protection
4. **Config location**: `~/.config/agentic-harness-seo/` for API credentials, or the directory in `AGENTIC_HARNESS_SEO_PROFILE_DIR`

## Maintenance and licensing

Maintained by [@zafajardo9](https://github.com/zafajardo9). See [LICENSE](LICENSE)
and [NOTICE](NOTICE) for licensing and copyright notices.

<!--
  Agentic Harness SEO (agentic-harness-seo): open-source SEO audits for agent
  harnesses. Maintained by zafajardo9 and distributed under the MIT License.
-->

<h1 align="center">Agentic Harness SEO</h1>

<p align="center">
  <b>Run a full SEO audit from your agent harness.</b><br />
  Claude Code, OpenAI Codex CLI, Google Antigravity, Gemini CLI, Cursor, Cline, Aider and Grok Build.
</p>

<p align="center">
  <a href="#what-it-does">What it does</a> ·
  <a href="#how-an-audit-works">How it works</a> ·
  <a href="#commands">Commands</a> ·
  <a href="#install">Install</a> ·
  <a href="#configuration">Configuration</a> ·
  <a href="#security-and-privacy">Security</a> ·
  <a href="#faq">FAQ</a>
</p>

Agentic Harness SEO is an SEO analysis toolkit that runs inside an agent harness.
Point it at a site and it performs the technical, content, schema, local and
AI-search checks a consultant would, then returns a prioritized action plan.

It runs locally. The harness calls bundled Python tools, the tools return JSON,
and the model synthesizes the findings into a report. Nothing is uploaded to an
SEO vendor. Optional extensions call third-party APIs only when you configure
credentials for them.

The toolkit contains **30 sub-skills**, **20 specialist sub-agents** and **68
Python scripts**, plus 11 optional extensions.

## What it does

| Area | Checks and outputs |
|---|---|
| **Technical SEO** | Crawlability, robots.txt, canonicals, indexability, redirects, URL structure, mobile, HTTPS and security headers, JavaScript rendering |
| **Core Web Vitals** | PageSpeed Insights and CrUX field data, LCP subparts, INP and CLS thresholds, preload, bfcache and speculation-rule review |
| **Content quality** | E-E-A-T signals, thin and duplicated content, readability, keyword coverage, claim verification, humanization |
| **Structured data** | Detects, validates and generates JSON-LD for Organization, Product, Article, FAQ, LocalBusiness, breadcrumbs, e-commerce and more |
| **Sitemaps and images** | XML sitemap analysis and generation, image audit, ALT text, image SERP analysis, file-size optimization |
| **AI search (GEO)** | Citability for AI Overviews, AI Mode, ChatGPT, Gemini and Perplexity, AI crawler access, brand presence, llms.txt |
| **Agent readiness** | Lighthouse Agentic Browsing X/N, accessibility tree, Markdown availability, WebMCP, AI agent access |
| **Local SEO** | Google Business Profile signals, NAP consistency, citations, reviews, map pack, geo-grid and competitor radius |
| **Backlinks** | Common Crawl domain metrics for free, plus Moz and Bing Webmaster when keys exist, and link verification |
| **International** | Hreflang and i18n audit, cultural profiles, content parity |
| **E-commerce** | Product and Offer schema, marketplace intelligence, Google Shopping signals |
| **Strategy** | Semantic clustering, SXO and personas, content briefs, programmatic SEO, competitor comparison pages, the FLOW framework |
| **Change monitoring** | Drift baselines in SQLite, comparison across runs, history, regression reports |
| **Google APIs** | Search Console, PageSpeed, CrUX, Indexing, GA4, Cloud NLP, Ads Keyword Planner and YouTube, when credentials are present |
| **Reporting** | Markdown findings, JSON for every script, and PDF reports through `google_report.py` |

## How an audit works

1. **Learn the site.** The orchestrator detects the business type (SaaS, local,
   e-commerce, publisher, agency) and the signals present: blog, topic clusters,
   product pages, existing drift baselines.
2. **Probe the data sources.** It checks for Google, Matomo and PostHog
   credentials and for available MCP tools, then spawns only the agents whose data
   exists. A site with no Search Console access runs a leaner audit.
3. **Fan out.** Specialist agents work in parallel, each with its own context and
   tool budget. They call the bundled scripts and read the JSON.
4. **Synthesize.** Findings go through PERCEIVE, ANALYZE, VALIDATE and ACT, then
   into Critical, High, Medium and Low buckets with a 0 to 100 health score.
5. **Recommend.** Each item states why it matters, what it depends on, and how to
   verify the fix worked. Reports are saved as Markdown, and `/harness-seo google report`
   produces a PDF.

## Commands

Commands are available as `/harness-seo <command>` in Claude Code. In other harnesses,
ask in plain language and the agent reads `AGENTS.md` and the matching skill.

### Runtime

| Command | What it does |
|---|---|
| `/harness-seo setup` | Create or repair the isolated Python environment and Chromium |
| `/harness-seo doctor` | Report runtime readiness without changing anything |

### Audits and planning

| Command | What it does |
|---|---|
| `/harness-seo audit <url>` | Full site audit with parallel agents and a prioritized plan |
| `/harness-seo page <url>` | Deep single-page analysis |
| `/harness-seo plan <type>` | Strategic SEO plan for SaaS, local, e-commerce, publisher or agency |

### Technical SEO

| Command | What it does |
|---|---|
| `/harness-seo technical <url>` | Technical audit across nine categories |
| `/harness-seo sitemap <url \| generate>` | Analyze or generate XML sitemaps |
| `/harness-seo images <url>` | Image SEO audit and optimization advice |
| `/harness-seo hreflang <url>` | Hreflang and international SEO audit and generation |
| `/harness-seo programmatic <url>` | Programmatic SEO analysis and planning |
| `/harness-seo google <command>` | Google APIs: GSC, PageSpeed, CrUX, Indexing, GA4, PDF reports |
| `/harness-seo drift baseline \| compare \| history <url>` | Capture, compare and review drift snapshots |

### Content and strategy

| Command | What it does |
|---|---|
| `/harness-seo content <url>` | E-E-A-T and content quality analysis |
| `/harness-seo content-brief <topic>` | Content brief with target keywords, outline and internal links |
| `/harness-seo cluster <keyword>` | SERP-based semantic clustering and content architecture |
| `/harness-seo sxo <url>` | Search Experience Optimization: page types, user stories, personas |
| `/harness-seo flow [stage]` | FLOW framework prompts for Find, Leverage, Optimize, Win or Local |
| `/harness-seo competitor-pages <url>` | Competitor comparison page generation |

### Schema and AI search

| Command | What it does |
|---|---|
| `/harness-seo schema <url>` | Detect, validate and generate Schema.org markup |
| `/harness-seo geo <url>` | AI Overviews and Generative Engine Optimization |
| `/harness-seo agentic <url>` | Agent readiness: Lighthouse Agentic Browsing, llms.txt, WebMCP |

### Social posters

| Command | What it does |
|---|---|
| `/harness-seo generate-poster <profile> [brief]` | Develop an idea and make an editable Canva draft |
| `/harness-seo generate-poster setup [profile]` | Create or update a reusable creative profile |
| `/harness-seo generate-poster version [count] [direction]` | Create alternatives to a Canva draft |

### Local, links and commerce

| Command | What it does |
|---|---|
| `/harness-seo local <url>` | Local SEO: GBP, citations, reviews, map pack |
| `/harness-seo maps <command>` | Maps intelligence: geo-grid, GBP audit, reviews, competitors |
| `/harness-seo backlinks <url>` | Backlink profile analysis across free and configured sources |
| `/harness-seo ecommerce <url>` | E-commerce SEO, product schema and marketplace intelligence |

### Extensions

| Command | What it does |
|---|---|
| `/harness-seo dataforseo <command>` | Live SERP, keyword and merchant data (MCP) |
| `/harness-seo firecrawl <command> <url>` | Full-site crawling and site mapping (MCP) |
| `/harness-seo ahrefs <command> <target>` | Backlinks and organic keywords (MCP) |
| `/harness-seo seranking <command>` | AI share of voice and SERP data (API) |
| `/harness-seo profound <command>` | LLM citation tracking (API) |
| `/harness-seo bing <command> <url>` | Bing Webmaster data and IndexNow submission (API) |
| `/harness-seo image-gen <use-case>` | AI image generation for SEO assets (MCP) |
| `/harness-seo matomo <command>` | Matomo Reporting API as a GA4 alternative (API) |
| `/harness-seo posthog <command>` | PostHog analytics through MCP (MCP) |
| `/harness-seo unlighthouse <url>` | Multi-page Lighthouse audit, runs locally |
| `/harness-seo shopify <crawl \| check> <url>` | Signed crawl of a Shopify store you administer |

## Install

### Codex

To install the **Agentic Harness SEO Planner** from a local checkout, run these
commands from the repository root.

```bash
codex plugin marketplace add .
codex plugin add agentic-harness-seo-planner@agentic-harness-seo
```

To install from GitHub, the repository's published branch must include the
marketplace files.

```bash
codex plugin marketplace add zafajardo9/agentic-harness-seo
codex plugin add agentic-harness-seo-planner@agentic-harness-seo
```

After adding the marketplace, you can also select **Agentic Harness SEO** in
the desktop Plugins Directory and install the planner there.

Start a new chat and ask for an SEO launch plan, a 90-day roadmap, or the
`seo-generate-poster` skill. The package includes six planning templates and
two poster profiles and requires no Python setup. For live page checks, see
[MCP setup](docs/SEO-CONNECTOR.md#codex-and-local-mcp-clients).
For full site audits, use the portable toolkit below.

### Generate social posters in Canva

In Claude Code, select a profile and describe the post. Use `setup` to change
the profile's tone, palette, format, or recurring ideas.

```text
/harness-seo generate-poster setup dds
/harness-seo generate-poster dds Create an Instagram post about our upcoming workshop
/harness-seo generate-poster filepino
/harness-seo generate-poster version 2 Try different layouts and keep the copy
```

Before Canva creates a draft, the skill extracts the facts, data, tone, and
ideas from your brief and any material you supply. It proposes three layout
and format ideas with text wireframes and recommends one, then asks about open
choices for size, colors, photos or illustrations, vector-style graphics or
supplied SVGs, and heading and body fonts. Reply **Use defaults** or change the
settings you want. It then shows a final brief with the exact poster copy, and
creates nothing in Canva until you reply **Approve**. Use `version` when you want more options based on a draft you like. Each
alternative gets its own edit link, and the original stays available.

In Codex, choose the installed `seo-generate-poster` skill and ask, for example,
“Use FilePino to propose an Instagram checklist” or “Make two more versions of
this poster with the same colors and text.”
The starter profiles are draft creative directions. Your updates are saved under
`~/.config/agentic-harness-seo/poster-profiles/`.

Connect your own Canva account in your host before generating a design.
Codex uses the Canva connector from the desktop Plugins Directory. Claude Code
uses an authenticated Canva MCP server. Each completed draft includes an
**Open in Canva** edit link. A revision includes its own edit link and keeps the
original link available in the same chat.
[Canva connection steps](skills/seo-generate-poster/references/canva-connection.md)

### ChatGPT

**SEO planning without hosting.** Download `agentic-harness-seo-planner.zip`
from a successful [Build SEO planner packages run](https://github.com/zafajardo9/agentic-harness-seo/actions/workflows/openai-planner.yml)
or build it from your checkout. On Windows, run these commands in Git Bash.

```bash
bash ./scripts/agentic-harness-seo setup --skip-browser
bash ./scripts/agentic-harness-seo run package_openai_plugin.py dist/agentic-harness-seo-planner.zip
```

Upload the ZIP as **Skills only** in the [OpenAI Plugins dashboard](https://platform.openai.com/plugins).
This is the developer upload path. A public Plugins Directory listing requires
developer verification and review.

**Live checks in ChatGPT.** Deploy the SEO MCP server and add its HTTPS URL as
a custom app in ChatGPT. The connector can check deployed pages and draft HTML.
[ChatGPT connector setup](docs/SEO-CONNECTOR.md#chatgpt-and-claude-chat)

### Claude Code

Requires Claude Code 1.0.33 or newer. Run these inside it:

```bash
/plugin marketplace add zafajardo9/agentic-harness-seo
/plugin install agentic-harness-seo@zafajardo9-agentic-harness-seo
/harness-seo setup
```

`/harness-seo setup` builds a private Python environment and downloads Chromium for the
plugin. It does not touch your global Python packages. Run `/harness-seo doctor` at any
time to check it.

### Manual install

macOS and Linux:

```bash
git clone --depth 1 https://github.com/zafajardo9/agentic-harness-seo.git
bash agentic-harness-seo/install.sh
```

Windows (PowerShell):

```powershell
git clone --depth 1 https://github.com/zafajardo9/agentic-harness-seo.git
powershell -ExecutionPolicy Bypass -File agentic-harness-seo\install.ps1
```

Clone rather than piping a remote script into a shell, so you can read the
installer first.

### Other AI harnesses

For the full toolkit in Codex CLI, Antigravity, Grok Build, Gemini CLI, Cursor,
Cline or Aider, use the portable installer. It writes the harness's workspace
instructions and installs the toolkit:

```bash
git clone https://github.com/zafajardo9/agentic-harness-seo.git
cd agentic-harness-seo
python3 scripts/portable_install.py --project ~/my-site --harnesses all
```

Then build the environment once and put the wrapper on PATH:

```bash
export PATH="$HOME/.agentic-harness-seo/bin:$PATH"
"$HOME/.agentic-harness-seo/scripts/agentic-harness-seo" setup
"$HOME/.agentic-harness-seo/scripts/agentic-harness-seo" doctor --json
```

`--harnesses` accepts `codex`, `antigravity`, `grok`, `gemini`, `cursor`,
`cline`, `aider` or `all`. What each harness keeps and loses against Claude Code
(sub-agent fan-out, hooks, MCP, model tiering) is in
[docs/HARNESSES.md](docs/HARNESSES.md). ChatGPT and Claude chat can run
on-page checks and load SEO planning workflows through the
[MCP connector](docs/SEO-CONNECTOR.md).

### First audit

```bash
/harness-seo audit https://example.com           # full audit with a prioritized plan
/harness-seo page https://example.com/pricing    # one page, in depth
/harness-seo technical https://example.com       # crawl, index, headers, rendering
/harness-seo geo https://example.com             # readiness for AI search
/harness-seo schema https://example.com          # structured data check and generation
/harness-seo local https://example.com           # local SEO and Google Business Profile
```

## Configuration

Everything works without credentials. Keys only add field data and paid sources.

| Source | How to configure |
|---|---|
| Google APIs (GSC, PSI, CrUX, Indexing, GA4, NLP, Ads, YouTube) | `/harness-seo google setup` |
| Moz and Bing Webmaster backlinks | `/harness-seo backlinks setup` |
| Extensions | Each guide under [`extensions/`](extensions/); credentials stay in the config directory |

| Environment variable | Purpose |
|---|---|
| `AGENTIC_HARNESS_SEO_PYTHON` | Absolute path to a supported interpreter (3.11 to 3.14) |
| `AGENTIC_HARNESS_SEO_PROFILE_DIR` | Credential directory, default `~/.config/agentic-harness-seo` |
| `AGENTIC_HARNESS_SEO_CONFIG_DIR` | Overrides the config and ledger location |
| `AGENTIC_HARNESS_SEO_LOCAL_TARGETS` | Opt in to auditing loopback or private addresses |
| `AGENTIC_HARNESS_SEO_TRUSTED_PROXIES` | Opt in to a trusted egress proxy on a private address |
| `AGENTIC_HARNESS_SEO_CHROMIUM_REQUIRE_SANDBOX` | Strict mode: fail instead of falling back to an unsandboxed browser |
| `AGENTIC_HARNESS_SEO_CHROMIUM_NO_SANDBOX` | Skip the sandbox attempt entirely |
| `AGENTIC_HARNESS_SEO_DATA_DIR` | Runtime data directory override |
| `AGENTIC_HARNESS_SEO_TAG` | Release tag or branch the installer clones |

Local state lives in `~/.config/agentic-harness-seo` for credentials and
`~/.cache/agentic-harness-seo` for drift baselines and the managed environment.

## Requirements and limits

- **Claude Code** 1.0.33 or newer for the plugin path. **Python** 3.11 to 3.14,
  with 3.11 as the floor and 3.14 as the ceiling.
- **Cost.** Five agents that need the most judgment run on Opus and the rest on
  Sonnet, so a full audit uses more of your plan than a single-page check. Every
  agent's model is set in its file under [`agents/`](agents/).
- **Field data.** Without Google keys, Core Web Vitals are lab estimates and
  indexing status is inferred from the page.
- **Interactive pages.** Content that appears only after scrolling or clicking
  can produce noisy results, even with automatic SPA rendering.
- **Concurrency.** Other harnesses often run agents sequentially, so the same
  audit takes longer than it does in Claude Code.
- **Uninstall.** Plugin: `/plugin uninstall agentic-harness-seo@zafajardo9-agentic-harness-seo`.
  Manual: run the matching `uninstall.sh` or `uninstall.ps1`.

## Sub-agents

| Agent | Role | Command |
|---|---|---|
| `seo-technical` | Technical SEO lead | `/harness-seo technical` |
| `seo-content` | Content editor and E-E-A-T | `/harness-seo content` |
| `seo-schema` | Structured data engineer | `/harness-seo schema` |
| `seo-sitemap` | Sitemap architect | `/harness-seo sitemap` |
| `seo-performance` | Performance engineer | `/harness-seo audit` |
| `seo-visual` | Visual and mobile QA | `/harness-seo audit` |
| `seo-geo` | AI search analyst | `/harness-seo geo` |
| `seo-agentic` | Agent readiness analyst | `/harness-seo agentic` |
| `seo-local` | Local SEO specialist | `/harness-seo local` |
| `seo-maps` | Maps and geo-grid analyst | `/harness-seo maps` |
| `seo-google` | Google data analyst | `/harness-seo google` |
| `seo-backlinks` | Link analyst | `/harness-seo backlinks` |
| `seo-cluster` | Topic strategist | `/harness-seo cluster` |
| `seo-sxo` | Search experience designer | `/harness-seo sxo` |
| `seo-drift` | Change monitor | `/harness-seo drift` |
| `seo-ecommerce` | E-commerce specialist | `/harness-seo ecommerce` |
| `seo-flow` | FLOW strategist | `/harness-seo flow` |
| `seo-dataforseo` | Live data analyst (extension) | `/harness-seo dataforseo` |
| `seo-image-gen` | Image producer (extension) | `/harness-seo image-gen` |
| `seo-posthog` | PostHog analyst (extension) | `/harness-seo posthog` |

## Extensions

Optional add-ons. The toolkit works fully without them.

| Extension | What it adds | Type |
|---|---|---|
| DataForSEO | SERP, keyword, merchant and AI-visibility data | MCP |
| Firecrawl | Full-site crawl and URL discovery | MCP |
| Ahrefs | Backlinks and organic keywords | MCP |
| Banana | AI image generation for SEO assets | MCP |
| PostHog | Organic traffic and landing-page analytics | MCP |
| SE Ranking | AI share of voice and SERP positions | API |
| Profound | LLM citation tracking over time | API |
| Bing Webmaster | Bing link data and IndexNow | API |
| Matomo | Reporting API as a GA4 alternative | API |
| Unlighthouse | Multi-page Lighthouse runs | Local |
| Shopify Crawler Access | Signed crawl of a store you administer | Local |

Setup guides live under [`extensions/`](extensions/). Integrations maintained by
other people are listed in
[docs/COMMUNITY-INTEGRATIONS.md](docs/COMMUNITY-INTEGRATIONS.md).

## Security and privacy

- **SSRF and DNS rebinding.** Every user-supplied URL passes through
  `validate_url()` in [`scripts/url_safety.py`](scripts/url_safety.py), which
  refuses private, loopback, link-local and cloud metadata addresses, and pins
  the resolved address for the request.
- **Browser egress guard.** Chromium runs behind a local proxy that validates
  every connection, including redirects and subresources. The sandbox is used
  where the host allows it and the fallback is reported.
- **Untrusted content.** Fetched pages are data, never instructions. The agent
  prompts say so explicitly.
- **No telemetry.** Reports stay on disk. Third-party calls happen only for
  configured extensions and APIs.

See [SECURITY.md](SECURITY.md) for the threat model and [PRIVACY.md](PRIVACY.md)
for the full list of outbound endpoints.

## Repository layout

```
skills/        30 sub-skills, each a SKILL.md with its own references
agents/        20 sub-agents with their own context and tool budgets
scripts/       68 Python tools, plus the managed runtime and launcher
schema/        JSON-LD templates
data/          Google update ledger and reference data
hooks/         PostToolUse schema validation (Claude Code)
extensions/    11 optional integrations
docs/          command reference, architecture, installation, harness matrix
tests/         test suite, including the documentation invariant gates
```

## Development

```bash
# Portability lint across every SKILL.md
./scripts/agentic-harness-seo run portability_check.py

# Reference graph and manifest consistency
./scripts/agentic-harness-seo run consistency_check.py

# Full test suite
python -m pytest tests/ -v
```

The suite pins behaviour that is easy to break silently: manifest counts, the
Python range across every copy, the script inventory in `CLAUDE.md`, canonical
phrasing in the user-facing docs, and the no-em-dash house style.

## License and contributing

Distributed under the [MIT License](LICENSE). This project is a fork of
[claude-seo](https://github.com/AgriciDaniel/claude-seo), where upstream
contributor credits are maintained. The [FLOW framework](https://github.com/AgriciDaniel/flow)
references are distributed under CC BY 4.0.

Contributions are welcome. Open an issue using one of the templates and
mention the checks you ran in your pull request.

## Maintainer

Maintained by [zafajardo9](https://github.com/zafajardo9).

## FAQ

**Do I need API keys?**
No. The toolkit works out of the box with raw fetching and heuristics. Keys add
field metrics (PSI, CrUX, Search Console, GA4) and paid sources (Moz, Bing,
DataForSEO and others).

**Does it work on JavaScript sites?**
Yes. When a page needs JavaScript, the renderer opens it in headless Chromium and
the audit sees what a visitor sees.

**How is it different from a crawler?**
Crawlers are faster at scale and have their own link indexes. This toolkit
explains findings, ranks them by impact, and covers AI search readiness. Many
teams use both.

**Does my data leave my machine?**
The audited pages are sent to your model provider, the same as any other content
you work with in that harness. Reports stay on disk. No SEO vendor is contacted
unless you configure an extension.

**Which harnesses are supported?**
Claude Code natively, and Codex CLI, Antigravity, Grok Build, Gemini CLI, Cursor,
Cline and Aider through the portable install. See
[docs/HARNESSES.md](docs/HARNESSES.md).

**Where do I read more?**
[Installation](docs/INSTALLATION.md), [Commands](docs/COMMANDS.md),
[Architecture](docs/ARCHITECTURE.md), [Troubleshooting](docs/TROUBLESHOOTING.md)
and [Extensions setup](docs/MCP-INTEGRATION.md).

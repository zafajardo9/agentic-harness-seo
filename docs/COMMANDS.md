# Commands Reference

## Overview

In Claude Code, use `/harness-seo` followed by a subcommand. If another skill
uses that name, use the plugin-qualified command, such as
`/agentic-harness-seo:harness-seo audit https://example.com`.

## Page-fetching script

Use `"${CLAUDE_PLUGIN_ROOT}/scripts/agentic-harness-seo" run fetch_page.py https://example.com --json` for structured
retrieval. Both the raw path (default, `--render never`) and the rendered path
(`--render auto` or `--render always`) emit JSON through the same
`render_page._json_summary` contract, so the two share one key set: `url`,
`status_code`, `content`, `raw_content`, `is_spa`, `extracted_text`,
`publication_date`, `accessibility_tree`, `accessibility_error`,
`accessibility_partial`, `headers`, `redirect_chain`, `console_errors`,
`render_diagnostics`, `render_engine`, `render_ms`, `mode_used`, `error`,
`structured_data`, and `truncation`. The raw path fills renderer-only fields
(`is_spa`, `extracted_text`, `render_engine`, ...) with `None`/empty defaults.
Fetch errors still emit JSON and exit 1; successful fetches exit 0. HTTP status
codes are reported without changing this behavior.

Pass `--max-text N` to cap the `content`, `raw_content`, and `extracted_text`
fields at N characters each; `truncation.fields` reports the original and
returned character counts per field. `--max-text 0` (default) keeps full text.

Combine `--json --output page.html` to save successful HTML while keeping JSON
on stdout. `output_written` indicates whether HTML was saved. On fetch errors,
the output file is left untouched. Without `--json`, existing text output is
unchanged.

## Command List

### `/harness-seo setup`

Explicitly create or refresh the isolated Python runtime and Playwright Chromium.
This is required once after a marketplace plugin install. Manual installers run
the same setup automatically. It never installs packages globally.

### `/harness-seo doctor`

Check runtime, dependency, and Chromium readiness without changing the system.
Diagnostic output omits absolute paths and environment values.

### `/harness-seo audit <url>`

Full website SEO audit with parallel analysis.

**Example:**
```
/harness-seo audit https://example.com
```

**What it does:**
1. Crawls up to 500 pages
2. Detects business type
3. Delegates to up to 17 specialist subagents in parallel (9 always-on + 8 conditional)
4. Generates SEO Health Score (0-100)
5. Creates prioritized action plan

**Output:**
- `FULL-AUDIT-REPORT.md`
- `ACTION-PLAN.md`
- `screenshots/` (if Playwright available)

---

### `/harness-seo page <url>`

Deep single-page analysis.

**Example:**
```
/harness-seo page https://example.com/about
```

**What it analyzes:**
- On-page SEO (title, meta, headings, URLs)
- Content quality (word count, readability, E-E-A-T)
- Technical elements (canonical, robots, Open Graph)
- Schema markup
- Images (alt text, sizes, formats)
- Core Web Vitals potential issues

---

### `/harness-seo technical <url>`

Technical SEO audit across 9 categories.

**Example:**
```
/harness-seo technical https://example.com
```

**Categories:**
1. Crawlability
2. Indexability
3. Security
4. URL Structure
5. Mobile Optimization
6. Core Web Vitals (LCP, INP, CLS)
7. Structured Data
8. JavaScript Rendering
9. IndexNow Protocol

---

### `/harness-seo content <url>`

E-E-A-T and content quality analysis.

**Example:**
```
/harness-seo content https://example.com/blog/post
```

**What it evaluates:**
- Experience signals (first-hand knowledge)
- Expertise (author credentials)
- Authoritativeness (external recognition)
- Trustworthiness (transparency, security)
- AI citation readiness
- Content freshness

---

### `/harness-seo content-brief <topic or url>`

Generate a detailed SEO content brief: target keywords, search intent, heading outline, internal link targets, and competitor angle.

**Example:**
```
/harness-seo content-brief "best running shoes for flat feet"
```

**What it produces:**
- Primary and secondary target keywords
- Search intent and audience
- Section-by-section heading outline
- Internal link recommendations
- Competitor content angles to beat

---

### `/harness-seo schema <url>`

Schema markup detection, validation, and generation.

**Example:**
```
/harness-seo schema https://example.com
```

**What it does:**
- Detects existing schema (JSON-LD, Microdata, RDFa)
- Validates against Google's requirements
- Identifies missing opportunities
- Generates ready-to-use JSON-LD

---

### `/harness-seo geo <url>`

AI Overviews / Generative Engine Optimization.

**Example:**
```
/harness-seo geo https://example.com/blog/guide
```

**What it analyzes:**
- Citability score (quotable facts, statistics)
- Structural readability (headings, lists, tables)
- Entity clarity (definitions, context)
- Authority signals (credentials, sources)
- Structured data support

---

### `/harness-seo agentic [audit|fix|lighthouse|refresh] <url>`

Agent readiness: how well AI agents that browse and act for people can read and use the site.

**Examples:**
```
/harness-seo agentic https://example.com
/harness-seo agentic lighthouse https://example.com
/harness-seo agentic fix https://example.com
```

**What it analyzes:**
- Lighthouse Agentic Browsing result as Lighthouse computes it (X of N, N/A and informative audits excluded)
- Accessibility tree for agents (the 33 axe rules Lighthouse uses, plus the local Agent-UX heuristic)
- robots.txt groups per AI purpose (training, search, user-triggered) and Content-Signal
- llms.txt, Markdown delivery (`Accept: text/markdown`, `.md` alternates), ai-catalog.json, `/.well-known` files
- WebMCP tools and form annotations, labelled as a W3C Community Group draft

`fix` drafts robots.txt Content-Signal lines, llms.txt, ai-catalog.json and WebMCP scaffolds for review; nothing is deployed.

---

### `/harness-seo images <url>`

Image optimization analysis. Subcommands: `serp <keyword>` (image SERP / visual-search analysis), `optimize <path>` (local file optimization + IPTC AI labeling).

**Examples:**
```
/harness-seo images https://example.com
/harness-seo images serp "running shoes"
/harness-seo images optimize ./hero.webp
```

**What it checks:**
- Alt text presence and quality
- File sizes (flag >200KB)
- Formats (WebP/AVIF recommendations)
- Responsive images (srcset, sizes)
- Lazy loading
- CLS prevention (dimensions)

---

### `/harness-seo sitemap <url>`

Analyze existing XML sitemap.

**Example:**
```
/harness-seo sitemap https://example.com/sitemap.xml
```

**What it validates:**
- XML format
- URL count (<50k per file)
- URL status codes
- lastmod accuracy
- Deprecated tags (priority, changefreq)
- Coverage vs crawled pages

---

### `/harness-seo sitemap generate`

Generate new sitemap with industry templates.

**Example:**
```
/harness-seo sitemap generate
```

**Process:**
1. Select or auto-detect business type
2. Interactive structure planning
3. Apply quality gates (30/50 location page limits)
4. Generate valid XML
5. Create documentation

---

### `/harness-seo plan <type>`

Strategic SEO planning.

**Types:** `saas`, `local`, `ecommerce`, `publisher`, `agency`

**Example:**
```
/harness-seo plan saas
```

**What it creates:**
- Complete SEO strategy
- Competitive analysis
- Content calendar
- Implementation roadmap (4 phases)
- Site architecture design

---

### `/harness-seo competitor-pages [url|generate]`

Competitor comparison page generation.

**Examples:**
```
/harness-seo competitor-pages https://example.com/vs/competitor
/harness-seo competitor-pages generate
```

**Capabilities:**
- Generate "X vs Y" comparison page layouts
- Create "Alternatives to X" page structures
- Build feature comparison matrices with scoring
- Generate Product + AggregateRating schema markup
- Apply conversion-optimized CTA placement
- Enforce fairness guidelines (accurate data, source citations)

---

### `/harness-seo hreflang [url]`

Hreflang and international SEO audit and generation. Subcommand: `audit <directory-or-url>` (audit hreflang across a local build directory or a live URL set).

**Examples:**
```
/harness-seo hreflang https://example.com
/harness-seo hreflang audit ./dist
```

**Capabilities:**
- Validate self-referencing hreflang tags
- Check return tag reciprocity (A→B requires B→A)
- Verify x-default tag presence
- Validate ISO 639-1 language and ISO 3166-1 region codes
- Check canonical URL alignment with hreflang
- Detect protocol mismatches (HTTP vs HTTPS)
- Generate correct hreflang link tags and sitemap XML

---

### `/harness-seo programmatic [url|plan]`

Programmatic SEO analysis and planning for pages generated at scale.

**Examples:**
```
/harness-seo programmatic https://example.com/tools/
/harness-seo programmatic plan
```

**Capabilities:**
- Assess data source quality (CSV, JSON, API, database)
- Plan template engines with unique content per page
- Design URL pattern strategies (`/tools/[tool-name]`, `/[city]/[service]`)
- Automate internal linking (hub/spoke, related items, breadcrumbs)
- Enforce thin content safeguards (quality gates, word count thresholds)
- Prevent index bloat (noindex low-value, pagination, faceted nav)

---

### `/harness-seo local <url>`

Local SEO analysis covering Google Business Profile, citations, reviews, and the map pack.

**Example:**
```
/harness-seo local https://example.com
```

**What it analyzes:**
- Google Business Profile signals (categories, hours, photos, posts)
- NAP (Name, Address, Phone) consistency across the page and external citations
- Review velocity, response rate, and sentiment
- Local schema markup (LocalBusiness, Restaurant, Service-specific types)
- Industry-specific local factors (brick-and-mortar, SAB, hybrid)
- Map pack visibility signals

---

### `/harness-seo maps [command] [args]`

Maps intelligence: geo-grid rank tracking, GBP profile audits, review intelligence, cross-platform NAP verification, competitor radius mapping.

**Examples:**
```
/harness-seo maps "Joe's Coffee" "austin tx"
/harness-seo maps grid "coffee shop" "austin tx"
/harness-seo maps gbp "Joe's Coffee" "austin tx"
/harness-seo maps reviews "Joe's Coffee" "austin tx"
/harness-seo maps competitors "auto repair" "denver"
/harness-seo maps nap "Joe's Coffee" "austin tx"
/harness-seo maps schema "Joe's Coffee" "austin tx"
```

**Capabilities:**
- Rank tracking on a geographic grid (typically 49 points)
- GBP profile audit with completeness scoring
- Review aggregation across Google, Yelp, Facebook, Bing
- Competitor discovery within a configurable radius

---

### `/harness-seo backlinks <url>`

Backlink profile analysis with a 3-tier data cascade: free (Common Crawl + verification), free with signup (Moz, Bing Webmaster Tools), paid (DataForSEO).

**Examples:**
```
/harness-seo backlinks https://example.com
/harness-seo backlinks gap https://example.com https://competitor.com
/harness-seo backlinks toxic https://example.com
/harness-seo backlinks new https://example.com
/harness-seo backlinks verify https://example.com --links known-links.txt
/harness-seo backlinks setup
```

**What it analyzes:**
- Domain Authority and Page Authority (Moz)
- Referring domain count and growth
- Anchor text distribution (branded, exact, partial, naked URL)
- Toxic / spammy backlink detection
- Lost backlinks
- Competitor link gap

---

### `/harness-seo cluster [command] <seed-keyword>`

SERP-based semantic topic clustering for content architecture planning. Built on the Pro Hub Challenge Semantic Cluster Engine. Subcommands: `plan <seed>` (full planning workflow; also `plan --from strategy` to import a `/harness-seo plan` output), `execute` (create content via claude-blog or output briefs), `map` (regenerate the interactive visualization). Bare `/harness-seo cluster <seed>` is shorthand for `plan`.

**Examples:**
```
/harness-seo cluster plan "claude code skills"
/harness-seo cluster plan --from strategy
/harness-seo cluster execute
/harness-seo cluster map
```

**What it produces:**
- Keyword expansion from the seed (50-200 candidates)
- Pairwise SERP overlap comparison to detect semantic clusters
- Intent classification per cluster (informational, commercial, transactional, navigational)
- Hub-and-spoke content architecture proposal
- Internal link matrix between cluster pages
- Interactive `cluster-map.html` visualization

---

### `/harness-seo sxo <url>`

Search Experience Optimization: SERP backwards analysis, page-type mismatch detection, persona scoring. Subcommands: `<url> <keyword>` (analyze for a specific keyword), `wireframe <url>` (IST/SOLL wireframe), `personas <url>` (persona-only scoring, skips SERP).

**Examples:**
```
/harness-seo sxo https://example.com/blog/how-to-x
/harness-seo sxo https://example.com/page "target keyword"
/harness-seo sxo wireframe https://example.com/page
/harness-seo sxo personas https://example.com/page
```

**What it produces:**
- Page-type taxonomy classification (article, landing, product, tool, listing)
- SERP intent vs page-type alignment check
- User stories derived from SERP signals
- Multi-persona scoring (researcher, buyer, expert, casual visitor)
- Wireframe-level recommendations for fixing mismatches

---

### `/harness-seo drift baseline|compare|history <url>`

SEO drift monitoring. Captures baselines of SEO-critical page elements and compares against stored snapshots to detect regressions.

**Examples:**
```
/harness-seo drift baseline https://example.com
/harness-seo drift compare https://example.com
/harness-seo drift history https://example.com
```

**What it tracks:** title, meta description, canonical, hreflang, Open Graph, schema, headings, internal links, robots, sitemap entry, indexability, Core Web Vitals, response status, redirect chain.

**17 comparison rules** classify changes by severity (CRITICAL, HIGH, MEDIUM). SQLite-backed baselines.

---

### `/harness-seo ecommerce <url>`

E-commerce SEO covering product schema, marketplace intelligence, and pricing gap analysis. Subcommands: `products <keyword>` (Google Shopping competitive analysis), `gaps <domain>` (organic-vs-Shopping visibility gap), `schema <url>` (product schema validation + enhancement).

**Examples:**
```
/harness-seo ecommerce https://shop.example.com/product/x
/harness-seo ecommerce products "running shoes"
/harness-seo ecommerce gaps shop.example.com
/harness-seo ecommerce schema https://shop.example.com/product/x
```

**What it analyzes:**
- Product schema (Product, Offer, AggregateRating, Review)
- Google Shopping visibility
- Amazon marketplace presence
- Pricing gap vs competitors
- Out-of-stock and availability signals
- Faceted navigation crawl traps

---

### `/harness-seo flow [stage] [url|topic]`

FLOW framework integration: evidence-led prompts for the Find, Leverage, Optimize, Win, and Local stages of a content campaign.

**Examples:**
```
/harness-seo flow find "topic"
/harness-seo flow leverage https://example.com
/harness-seo flow optimize https://example.com/page
/harness-seo flow win https://example.com/page
/harness-seo flow local https://example.com
/harness-seo flow prompts
/harness-seo flow sync
```

**41 prompts** sourced from FLOW (CC BY 4.0). Each prompt is grounded in a specific evidence source (SERP data, GSC, GA4, customer interviews) with attribution preserved.

---

### `/harness-seo google [command] [url]`

Google SEO APIs. 4-tier credential system covering PageSpeed Insights, CrUX, CrUX History, Search Console, URL Inspection, Indexing API, GA4, and Keyword Planner.

**Setup & reporting:**
```
/harness-seo google setup                      # Configure/check credentials
/harness-seo google quotas                     # Show per-API quota usage
/harness-seo google report full                # Generate full PDF/HTML report
/harness-seo google report cwv-audit           # CWV-focused report
/harness-seo google report gsc-performance     # Search performance report
/harness-seo google report indexation          # Indexation status report
```

**PageSpeed / CrUX (Tier 0):**
```
/harness-seo google pagespeed <url>            # PageSpeed Insights (lab) + CWV
/harness-seo google crux <url>                 # CrUX field data
/harness-seo google crux-history <url>         # 25-week CrUX history
```

**Search Console / Indexing (Tier 1):**
```
/harness-seo google gsc <property>             # Search Analytics (clicks/impressions/CTR/position)
/harness-seo google inspect <url>              # URL Inspection (indexation status)
/harness-seo google inspect-batch <file>       # Batch URL inspection
/harness-seo google sitemaps <property>        # List submitted sitemaps + status
/harness-seo google index <url>                # Indexing API notify
/harness-seo google index-batch <file>         # Batch indexing notify
```
Use Indexing API commands only for pages with JobPosting or BroadcastEvent embedded in VideoObject. Route ordinary URLs to URL Inspection or sitemaps; `URL_UPDATED` does not guarantee indexing.

**GA4 (Tier 2):**
```
/harness-seo google ga4 [property-id]          # Organic traffic report
/harness-seo google ga4-pages [property-id]    # Top organic landing pages
```

**NLP / Keywords / YouTube:**
```
/harness-seo google nlp <url-or-text>          # NLP content analysis
/harness-seo google entities <url-or-text>     # Entity extraction
/harness-seo google entity <query>             # Entity lookup
/harness-seo google keywords <seed>            # Keyword Planner ideas (Tier 3)
/harness-seo google volume <keywords>          # Keyword search volume (Tier 3)
/harness-seo google youtube <query>            # YouTube search
/harness-seo google youtube-video <video_id>   # YouTube video analysis
/harness-seo google safety <url>               # Safe Browsing check
```

**Tiers:**
- Tier 0 (API key only): PSI, CrUX, CrUX History
- Tier 1 (+ OAuth or Service Account): GSC, URL Inspection, Indexing API
  (an OAuth sign-in is read-only by default; add `--indexing` to `google_auth.py --auth` for the Indexing API)
- Tier 2 (+ GA4 property config): GA4 organic traffic
- Tier 3 (+ Google Ads developer token): Keyword Planner

PDF and HTML reports generated via WeasyPrint and matplotlib.

---

### `/harness-seo generate-poster [setup [profile] | profile [brief]]`

Develop a social media concept and turn it into an editable Canva design. Supply
a profile and brief, or choose a profile and ask for an idea. Use `setup` to
create or update a saved creative profile. Follow-up feedback in the same
chat creates a new draft and keeps the previous Canva link available.

See [poster examples and Canva setup](../README.md#generate-social-posters-in-canva).

### `/harness-seo image-gen [use-case] <description>`

AI image generation for SEO assets (extension). Powered by Gemini via nanobanana-mcp.

**Prerequisites:** Banana extension installed (`./extensions/banana/install.sh`)

**Use Cases:**
```
/harness-seo image-gen og <description>          # OG/social preview image (16:9, 1K)
/harness-seo image-gen hero <description>        # Blog hero image (16:9, 2K)
/harness-seo image-gen product <description>     # Product photography (4:3, 2K)
/harness-seo image-gen infographic <description> # Infographic visual (2:3, 4K)
/harness-seo image-gen custom <description>      # Custom with full Creative Director pipeline
/harness-seo image-gen batch <description> [N]   # Generate N variations (default: 3)
```

**What it does:**
1. Maps SEO use case to optimized domain mode, aspect ratio, and resolution
2. Constructs 6-component Reasoning Brief (Creative Director pipeline)
3. Generates image via Gemini API
4. Provides SEO checklist (alt text, file naming, WebP, schema markup)

---

### `/harness-seo firecrawl [command] <url>`

Full-site crawling and URL discovery via Firecrawl MCP (extension).

**Prerequisites:** Firecrawl extension installed (`./extensions/firecrawl/install.sh`)

**Examples:**
```
/harness-seo firecrawl crawl https://example.com
/harness-seo firecrawl map https://example.com
/harness-seo firecrawl scrape https://example.com/page
/harness-seo firecrawl search "query" https://example.com
```

**What it does:**
- `crawl` walks the site discovering URLs and capturing content
- `map` returns the full URL inventory for a domain
- `scrape` extracts a single page in a model-friendly format
- `search` searches within a crawled site for a query

---

### `/harness-seo dataforseo [command]`

Live SEO data via DataForSEO MCP server (extension). 23 data commands across 9 API modules, plus cost-tracking commands.

**Prerequisites:** DataForSEO extension installed (`./extensions/dataforseo/install.sh`)

**SERP Analysis:**
```
/harness-seo dataforseo serp <keyword>              # Google organic results (also Bing/Yahoo)
/harness-seo dataforseo serp-images <keyword>       # Image elements in the organic SERP (no Images tool on the pinned server)
/harness-seo dataforseo serp-youtube <keyword>      # YouTube search results
/harness-seo dataforseo youtube <video_id>          # YouTube video deep analysis
```

**Keyword Research:**
```
/harness-seo dataforseo keywords <seed>             # Keyword ideas and suggestions
/harness-seo dataforseo volume <keywords>           # Search volume metrics
/harness-seo dataforseo difficulty <keywords>       # Keyword difficulty scores
/harness-seo dataforseo intent <keywords>           # Search intent classification
/harness-seo dataforseo trends <keyword>            # Google Trends data
```

**Domain & Competitors:**
```
/harness-seo dataforseo backlinks <domain>          # Full backlink profile
/harness-seo dataforseo competitors <domain>        # Competitor analysis
/harness-seo dataforseo ranked <domain>             # Ranked keywords
/harness-seo dataforseo intersection <domains>      # Keyword/backlink overlap
/harness-seo dataforseo traffic <domains>           # Traffic estimation
/harness-seo dataforseo subdomains <domain>         # Subdomains with ranking data
/harness-seo dataforseo top-searches <domain>       # Top queries mentioning domain
```

**Technical / On-Page:**
```
/harness-seo dataforseo onpage <url>                # On-page analysis (Lighthouse)
/harness-seo dataforseo tech <domain>               # Technology detection
/harness-seo dataforseo whois <domain>              # WHOIS data
```

**Content & Business Data:**
```
/harness-seo dataforseo content <keyword/url>       # Content analysis and trends
/harness-seo dataforseo listings <keyword>          # Business listings search
```

**AI Visibility / GEO:**
```
/harness-seo dataforseo ai-scrape <query>           # ChatGPT web scraper for GEO
/harness-seo dataforseo ai-mentions <keyword>       # LLM mention tracking
```

**Cost Tracking:**
```
/harness-seo dataforseo costs today                            # Today's DataForSEO spend
/harness-seo dataforseo costs summary                          # Spend summary across periods
/harness-seo dataforseo costs config --mode threshold --threshold 0.50   # Set cost-control mode/threshold
```

---

### `/harness-seo ahrefs [command] <url|topic>`

Ahrefs API metrics (extension). **Prerequisites:** Ahrefs extension installed (`./extensions/ahrefs/install.sh`).
```
/harness-seo ahrefs metrics <url>       # DR/UR, referring-domain count, organic traffic estimate
/harness-seo ahrefs backlinks <url>     # Top referring domains, anchor distribution, follow/nofollow ratio
/harness-seo ahrefs organic <url>       # Organic keywords, ranking distribution, traffic by country
/harness-seo ahrefs content <topic>     # Content Explorer top results, social shares, referring domains
```

---

### `/harness-seo bing [command]`

Bing Webmaster Tools + IndexNow (extension). The `seo-bing` skill ships with the plugin. **Prerequisites:** keys stored once with `./extensions/bing-webmaster/install.sh` (or `install.ps1`).
```
/harness-seo bing links <url>                 # Inbound links from Bing Webmaster
/harness-seo bing compare <urlA> <urlB>       # Compare two URLs' Bing link profiles
/harness-seo bing submit <url> --host <host>                # IndexNow single-URL submit (requires key)
/harness-seo bing submit-batch <file> --host <host>         # IndexNow batch submit (requires key)
/harness-seo bing verify-indexnow --host <host>             # Verify the IndexNow key is published
```

---

### `/harness-seo matomo [command] [site-id]`

Matomo Reporting API (extension). **Prerequisites:** Matomo extension installed (`./extensions/matomo/install.sh`), which writes the instance URL, API token, and optional default site ID to `~/.config/agentic-harness-seo/matomo.json` (0600), or to `matomo.json` in `AGENTIC_HARNESS_SEO_PROFILE_DIR` when it is set. `MATOMO_URL`, `MATOMO_API_TOKEN`, and `MATOMO_SITE_ID` in the environment override the file. Works against self-hosted Matomo or Matomo Cloud; an instance on a private address must be named in `AGENTIC_HARNESS_SEO_LOCAL_TARGETS`.

Use as a GA4 alternative or supplement when you want full data ownership, no Google dependency, or privacy-first analytics.
```
/harness-seo matomo check                  # Probe credentials and confirm Matomo version
/harness-seo matomo organic [site-id]      # Organic traffic trend (28d) + top landing pages
/harness-seo matomo top-pages              # Top organic landing pages only
/harness-seo matomo device                 # Visits by device type
/harness-seo matomo country                # Visits by country
/harness-seo matomo referrers              # Channel + search-engine breakdown
/harness-seo matomo keywords               # Organic search keywords (often "(not provided)")
```

All commands accept `--days` (default 28), `--limit` (default 50),
`--site-id`, and `--json`. The audit orchestrator spawns the
`seo-matomo` agent automatically when credentials are present.

---

### `/harness-seo posthog [command]`

PostHog analytics via the PostHog MCP server (extension). The `seo-posthog` skill and agent ship with the plugin. **Prerequisites:** the PostHog MCP server registered (`./extensions/posthog/install.sh` or `install.ps1` offers to do it), connected and authenticated (`/mcp`). No credentials are stored by agentic-harness-seo. Queries run as HogQL through the MCP `exec` tool (`call execute-sql`).

Use as a GA4 alternative or supplement when the site already sends `$pageview` events to PostHog. PostHog has no keyword data; use `/harness-seo google` for Search Console.
```
/harness-seo posthog check                 # Confirm the MCP is connected and $pageview events exist
/harness-seo posthog organic               # Organic search visits per day (28d)
/harness-seo posthog top-pages             # Top organic landing pages
/harness-seo posthog device                # Organic traffic by device type
/harness-seo posthog country               # Organic traffic by country
/harness-seo posthog referrers             # Referrer / channel breakdown
```

Options: days (default 28) and limit (default 50). The audit orchestrator
spawns the `seo-posthog` agent automatically when the MCP is connected.

---

### `/harness-seo profound [command] <brand>`

LLM brand-citation tracking via Profound (extension). **Prerequisites:** Profound extension installed.
```
/harness-seo profound citations <brand>     # Citation rate per LLM + 30-day trend
/harness-seo profound prompts <brand>       # Top prompts that surface (or miss) the brand
/harness-seo profound competitors <brand>   # Brands cited alongside yours for the same prompts
/harness-seo profound alerts <brand>        # Spike/drop alerts vs 7-day baseline
```

---

### `/harness-seo seranking [command] <brand|keyword|url>`

AI-visibility + SERP via SE Ranking (extension). **Prerequisites:** SE Ranking extension installed.
```
/harness-seo seranking ai-visibility <brand>   # Share-of-voice across ChatGPT/Gemini/Perplexity/AI Overviews/AI Mode
/harness-seo seranking serp <keyword>          # Top 100 organic positions + SERP features
/harness-seo seranking backlinks <url>         # Backlink profile (free-tier alternative to Ahrefs/DataForSEO)
/harness-seo seranking competitors <url>       # Top 10 organic competitors + shared-keyword gaps
```

---

### `/harness-seo unlighthouse <url>`

Multi-page Lighthouse audit via Unlighthouse (extension, MIT, no API quota). **Prerequisites:** Node 18+ and the unlighthouse npm package (`./extensions/unlighthouse/install.sh`).
```
/harness-seo unlighthouse https://example.com
/harness-seo unlighthouse https://example.com --device desktop
/harness-seo unlighthouse https://example.com --max-routes 50 --output-dir ./reports
```

---

### `/harness-seo shopify [crawl|check] <url>`

Uncapped, sitemap-complete crawl of a Shopify store you administer, signed with the store's Crawler Access signature from a project-local `.shopify-env`, then the `seo-audit` pipeline on the crawl artifacts (extension, no API keys). The `seo-shopify` skill ships with the plugin. Without a valid signature for the host, `seo-audit` runs unchanged. **Prerequisites:** a signature from the Shopify admin (Online Store > Preferences > Crawler access) in `.shopify-env` (`./extensions/shopify/install.sh` or `install.ps1` can create the file from the template; see `extensions/shopify/docs/SHOPIFY-SETUP.md`).
```
/harness-seo shopify https://shop.example              # precheck, signed crawl, full audit
/harness-seo shopify crawl https://shop.example        # crawl only, artifacts in ./crawl
/harness-seo shopify check https://shop.example        # is there a valid signature for this host?
```

---

## Quick Reference

| Command | Use Case |
|---------|----------|
| `/harness-seo audit <url>` | Full website audit with parallel subagents |
| `/harness-seo shopify <url>` | Uncapped signed crawl of a Shopify store you administer, then the audit (extension) |
| `/harness-seo page <url>` | Single page analysis |
| `/harness-seo technical <url>` | Technical SEO across 9 categories |
| `/harness-seo content <url>` | E-E-A-T and content quality |
| `/harness-seo content-brief <topic>` | Detailed content brief: keywords, outline, internal links |
| `/harness-seo schema <url>` | Schema markup detection, validation, generation |
| `/harness-seo sitemap <url>` | Sitemap validation |
| `/harness-seo sitemap generate` | Create new sitemap with industry templates |
| `/harness-seo images <url>` | Image optimization |
| `/harness-seo geo <url>` | AI search optimization (GEO) |
| `/harness-seo agentic <url>` | Agent readiness (Lighthouse Agentic Browsing, AI agent access, WebMCP) |
| `/harness-seo local <url>` | Local SEO (GBP, citations, reviews) |
| `/harness-seo maps [command]` | Maps intelligence (geo-grid, GBP audit, competitors) |
| `/harness-seo backlinks <url>` | Backlink profile analysis |
| `/harness-seo cluster <seed>` | SERP-based semantic clustering |
| `/harness-seo sxo <url>` | Search Experience Optimization |
| `/harness-seo drift baseline\|compare\|history <url>` | SEO drift monitoring |
| `/harness-seo ecommerce <url>` | E-commerce SEO |
| `/harness-seo hreflang [url]` | Hreflang and international SEO |
| `/harness-seo plan <type>` | Strategic planning by industry |
| `/harness-seo programmatic [url\|plan]` | Programmatic SEO analysis |
| `/harness-seo competitor-pages [url\|generate]` | Competitor comparison pages |
| `/harness-seo flow [stage] [url\|topic]` | FLOW framework prompts |
| `/harness-seo google [command] [url]` | Google SEO APIs (GSC, PSI, CrUX, GA4) |
| `/harness-seo dataforseo [command]` | Live SEO data (extension) |
| `/harness-seo image-gen [use-case] <desc>` | AI image generation (extension) |
| `/harness-seo generate-poster <profile> [brief]` | Editable Canva social poster |
| `/harness-seo firecrawl [command] <url>` | Full-site crawling (extension) |
| `/harness-seo ahrefs [command] <url>` | Backlinks, organic keywords, and content data via the official Ahrefs MCP (extension) |
| `/harness-seo seranking [command]` | AI Share-of-Voice across ChatGPT, Gemini, Perplexity, AI Overviews, AI Mode (extension) |
| `/harness-seo profound [command]` | LLM citation tracking with time-series data (extension) |
| `/harness-seo bing [command] <url>` | Bing Webmaster Tools + IndexNow URL submission (extension) |
| `/harness-seo matomo [command] [args]` | Matomo Reporting API: GA4 alternative or complement (extension) |
| `/harness-seo posthog [command]` | PostHog via MCP: GA4 alternative or complement (extension) |
| `/harness-seo unlighthouse <url>` | Multi-page Lighthouse runner, runs locally (extension) |

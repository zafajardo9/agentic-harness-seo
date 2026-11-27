#!/usr/bin/env python3
"""
Cross-platform portability lint for SKILL.md files.

agentic-harness-seo skills run under Claude Code, but also Cursor / Cursor Cloud
Agents / Google Antigravity / Gemini CLI / OpenAI Codex CLI / Cline /
Aider. Most harnesses share a minimum frontmatter contract:

  - ``name``        (string, kebab-case, < 64 chars)
  - ``description`` (string, < 1024 chars, ends with a period or noun phrase)

Claude-Code-specific fields are tolerated by other harnesses (they are
ignored, not rejected):

  - ``model``        (e.g. sonnet, haiku, opus)
  - ``maxTurns``     (int)
  - ``tools``        (comma-separated list with optional inline comments)
  - ``compatibility`` (free text, e.g. "Requires the @ahrefs/mcp MCP server")
  - ``metadata``     (a dict; metadata.version is read by the consistency tests)

The check walks every ``SKILL.md`` under ``skills/`` and ``extensions/``
and reports portability findings. It also checks the catalog as a whole:
every skill's ``name`` matches its folder, a skill that calls the
``${CLAUDE_PLUGIN_ROOT}`` launcher says how to resolve it in hosts that do
not expand it, and both native plugin manifests (Claude Code and Codex)
expose every workflow exactly once. Severity:

  - ``error``: a harness will outright reject the file (missing required
              field, malformed YAML, name not kebab-case).
  - ``warning``: the file works but loses information in a non-Claude
              harness (e.g. tools list with inline comments may be
              parsed differently).
  - ``info``: noteworthy but harmless (e.g. very long description).

Exit code 0 if no errors; 1 otherwise. Warnings + info do not fail the
build but are surfaced in the report.

Usage::

    python scripts/portability_check.py
    python scripts/portability_check.py --json
    python scripts/portability_check.py --strict   # warnings also fail
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


_NAME_RE = re.compile(r"^[a-z][a-z0-9-]{1,62}[a-z0-9]$")
_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)

LAUNCHER_TOKEN = "${CLAUDE_PLUGIN_ROOT}"
LAUNCHER_FALLBACK = "do not expand the launcher placeholder"

# Native plugin manifests. Each must expose every workflow exactly once.
# Claude Code always loads ./skills/ and adds the manifest's "skills" paths;
# Codex loads only the paths its manifest lists.
MANIFESTS = {
    "claude": (".claude-plugin/plugin.json", ["./skills/"]),
    "codex": (".codex-plugin/plugin.json", []),
}


def _find_skill_files() -> list[Path]:
    """Every SKILL.md under skills/ and extensions/."""
    paths: list[Path] = []
    for root in ("skills", "extensions"):
        base = REPO_ROOT / root
        if not base.is_dir():
            continue
        paths.extend(base.rglob("SKILL.md"))
    return sorted(paths)


def _parse_frontmatter(text: str) -> dict[str, str] | None:
    """Light YAML-ish parser. Doesn't require PyYAML: we accept the
    documented subset (scalar string values, no nested mappings except
    for the metadata: block which we treat as opaque)."""
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return None

    body = m.group(1)
    fields: dict[str, str] = {}
    in_metadata = False
    metadata_buf: list[str] = []
    for line in body.splitlines():
        if not line.strip():
            continue
        if line.startswith(" ") or line.startswith("\t"):
            if in_metadata:
                metadata_buf.append(line)
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if key == "metadata":
            in_metadata = True
            metadata_buf = []
            fields["metadata"] = ""  # placeholder; we fill below
        else:
            in_metadata = False
            fields[key] = value.strip("'\"")

    if metadata_buf:
        fields["metadata"] = "\n".join(metadata_buf).strip()

    return fields


def check_one(path: Path) -> list[dict]:
    findings: list[dict] = []
    try:
        relpath = str(path.relative_to(REPO_ROOT))
    except ValueError:
        # Path is outside the repo (e.g. unit tests use tmp_path).
        relpath = str(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        findings.append({
            "severity": "error", "path": relpath,
            "rule": "io-error", "message": f"cannot read: {exc}",
        })
        return findings

    frontmatter = _parse_frontmatter(text)
    if frontmatter is None:
        findings.append({
            "severity": "error", "path": relpath,
            "rule": "no-frontmatter",
            "message": "SKILL.md must open with a YAML --- block",
        })
        return findings

    name = frontmatter.get("name", "").strip()
    if not name:
        findings.append({
            "severity": "error", "path": relpath,
            "rule": "missing-name",
            "message": "frontmatter must declare a 'name'",
        })
    elif not _NAME_RE.match(name):
        findings.append({
            "severity": "error", "path": relpath,
            "rule": "name-not-kebab-case",
            "message": f"name {name!r} must be kebab-case "
                       "(lowercase, hyphens, no leading/trailing dash)",
        })

    description = frontmatter.get("description", "").strip()
    if not description:
        findings.append({
            "severity": "error", "path": relpath,
            "rule": "missing-description",
            "message": "frontmatter must declare a 'description'",
        })
    elif len(description) > 1024:
        findings.append({
            "severity": "warning", "path": relpath,
            "rule": "long-description",
            "message": f"description is {len(description)} chars "
                       "(Codex truncates above 1024; Cursor truncates "
                       "above 2048)",
        })

    # tools is optional. If present, Cline and Codex parse the list more
    # strictly than Claude Code: warn if there are inline comments
    # (e.g., "Read, Bash # for analyse").
    tools = frontmatter.get("tools", "")
    if tools and "#" in tools:
        findings.append({
            "severity": "warning", "path": relpath,
            "rule": "tools-has-inline-comment",
            "message": "Cline + Codex may include the comment in the "
                       "tool name. Move comments below the frontmatter.",
        })

    # Only Claude Code expands the launcher token. Codex, Antigravity and
    # the other hosts load the same file, so it must say how to find the
    # toolkit root when the token stays literal.
    if LAUNCHER_TOKEN in text and LAUNCHER_FALLBACK not in text:
        findings.append({
            "severity": "error", "path": relpath,
            "rule": "launcher-without-fallback",
            "message": f"uses {LAUNCHER_TOKEN} but lacks the paragraph for "
                       "hosts that do not expand it (Codex, Antigravity, "
                       f"Gemini CLI, Cursor). Add the sentence containing "
                       f"'{LAUNCHER_FALLBACK}' that the other skills use.",
        })

    # metadata.version is referenced by the consistency tests but is
    # purely informational for non-Claude harnesses.
    if frontmatter.get("metadata", ""):
        if 'version' not in frontmatter["metadata"]:
            findings.append({
                "severity": "info", "path": relpath,
                "rule": "metadata-without-version",
                "message": "metadata block present but no version field; "
                           "agentic-harness-seo's manifest test expects "
                           "metadata.version on every skill",
            })

    return findings


def _workflow_names(root: Path) -> set[str]:
    """Unique workflow names: core skills plus every extension skill."""
    paths = list((root / "skills").glob("*/SKILL.md"))
    paths += list((root / "extensions").glob("*/skills/*/SKILL.md"))
    return {p.parent.name for p in paths}


def check_catalog(root: Path = REPO_ROOT) -> list[dict]:
    """Repo-wide checks that make every workflow load on every platform.

    - ``name-dir-mismatch``: Codex, Antigravity and Gemini CLI follow the
      Agent Skills spec, which requires ``name`` to equal the folder name.
    - ``not-exposed``: a native plugin manifest leaves a workflow out, so
      that platform never shows the command.
    - ``duplicate-skill``: a manifest loads two folders with one name.
    - ``manifest-*``: a manifest is missing, unreadable, or lists a path
      that does not exist.
    """
    findings: list[dict] = []
    for path in sorted(list((root / "skills").glob("*/SKILL.md"))
                       + list((root / "extensions").glob("*/skills/*/SKILL.md"))):
        fm = _parse_frontmatter(path.read_text(encoding="utf-8")) or {}
        name = fm.get("name", "").strip()
        if name and name != path.parent.name:
            findings.append({
                "severity": "error", "path": str(path.relative_to(root)),
                "rule": "name-dir-mismatch",
                "message": f"name {name!r} must match its folder "
                           f"{path.parent.name!r} (Agent Skills spec; Codex "
                           "and Antigravity key skills on the folder)",
            })

    expected = _workflow_names(root)
    for platform, (manifest_rel, implicit) in MANIFESTS.items():
        manifest_path = root / manifest_rel
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            findings.append({
                "severity": "error", "path": manifest_rel,
                "rule": "manifest-unreadable", "message": str(exc),
            })
            continue
        listed = manifest.get("skills", [])
        if isinstance(listed, str):
            listed = [listed]
        seen: dict[str, Path] = {}
        for rel in [*implicit, *listed]:
            base = root / rel
            if not base.is_dir():
                findings.append({
                    "severity": "error", "path": manifest_rel,
                    "rule": "manifest-missing-path",
                    "message": f"{platform} manifest lists {rel!r}, which "
                               "is not a directory",
                })
                continue
            for skill in sorted(base.glob("*/SKILL.md")):
                name = skill.parent.name
                if name in seen and seen[name] != skill:
                    findings.append({
                        "severity": "error", "path": manifest_rel,
                        "rule": "duplicate-skill",
                        "message": f"{platform} loads {name!r} twice: "
                                   f"{seen[name].relative_to(root)} and "
                                   f"{skill.relative_to(root)}",
                    })
                seen.setdefault(name, skill)
        for name in sorted(expected - set(seen)):
            findings.append({
                "severity": "error", "path": manifest_rel,
                "rule": "not-exposed",
                "message": f"{platform} plugin does not expose {name!r}; "
                           "add its skills/ folder to the manifest",
            })
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Cross-platform portability lint for agentic-harness-seo SKILL.md files."
    )
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true",
                        help="Treat warnings as errors (exit 1).")
    args = parser.parse_args()

    paths = _find_skill_files()
    all_findings: list[dict] = []
    for path in paths:
        all_findings.extend(check_one(path))
    all_findings.extend(check_catalog())

    error_count = sum(1 for f in all_findings if f["severity"] == "error")
    warning_count = sum(1 for f in all_findings if f["severity"] == "warning")
    info_count = sum(1 for f in all_findings if f["severity"] == "info")

    if args.json:
        json.dump({
            "skills_checked": len(paths),
            "errors": error_count,
            "warnings": warning_count,
            "info": info_count,
            "findings": all_findings,
        }, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"Portability lint: {len(paths)} SKILL.md files checked")
        print(f"  errors:   {error_count}")
        print(f"  warnings: {warning_count}")
        print(f"  info:     {info_count}")
        for f in all_findings:
            print(f"  [{f['severity']:<8}] {f['path']} :: {f['rule']}")
            print(f"           {f['message']}")

    fail = error_count > 0 or (args.strict and warning_count > 0)
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())

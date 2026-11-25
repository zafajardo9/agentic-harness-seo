"""Sync the Codex planner package or build a plugin or skill ZIP."""

import argparse
import json
from pathlib import Path
from shutil import copyfile, copytree
from urllib.parse import urlsplit
from zipfile import ZIP_DEFLATED, ZipFile

from runtime import _plugin_version


def mcp_endpoint(value: str) -> str:
    try:
        url = urlsplit(value)
        valid = (
            url.scheme == "https"
            and url.hostname
            and url.username is None
            and not any(char.isspace() or char in "?#\\" for char in value)
            and url.port != 0
        )
    except ValueError:
        valid = False
    if not valid:
        raise argparse.ArgumentTypeError("provide an HTTPS MCP URL without credentials, query, or fragment")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, nargs="?", help="Path for the plugin ZIP")
    variant = parser.add_mutually_exclusive_group()
    variant.add_argument("--mcp-url", type=mcp_endpoint, help="Deployed HTTPS MCP endpoint")
    variant.add_argument("--claude-skill", action="store_true", help="Build a Claude chat skill ZIP")
    variant.add_argument("--sync-repo", action="store_true", help="Refresh the checked-in Codex plugin")
    args = parser.parse_args()
    if args.sync_repo and args.output is not None:
        parser.error("--sync-repo does not take an output path")
    if not args.sync_repo and args.output is None:
        parser.error("provide an output ZIP path or --sync-repo")

    root = Path(__file__).resolve().parents[1]
    package = root / "packaging" / "openai"
    planning = root / "skills" / "seo-plan"
    manifest_path = package / ".codex-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["version"] = _plugin_version(root)

    references = {
        "workflow.md": planning / "SKILL.md",
        **{f"industries/{path.name}": path for path in sorted((planning / "assets").glob("*.md"))},
    }
    notices = {name: root / name for name in ("LICENSE", "NOTICE")}
    if args.sync_repo:
        for name, source in references.items():
            destination = package / "skills" / "seo-roadmap" / "references" / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            copyfile(source, destination)
        for name, source in notices.items():
            copyfile(source, package / name)
        poster_skill = "seo-generate-poster"
        copytree(root / "skills" / poster_skill, package / "skills" / poster_skill, dirs_exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(package)
        return

    if args.mcp_url:
        manifest["name"] = "agentic-harness-seo-live"
        manifest["description"] = "Check live pages and draft HTML with Agentic Harness SEO and build a roadmap."
        manifest["mcpServers"] = "./.mcp.json"
        interface = manifest["interface"]
        interface["displayName"] = "Agentic Harness SEO Live"
        interface["shortDescription"] = "Live SEO checks and plans"
        interface["longDescription"] = (
            "Check public URLs and supplied HTML using read-only SEO tools. Build a roadmap "
            "from the findings and industry templates."
        )
        interface["capabilities"].extend(["Live page checks", "Draft HTML checks"])

    skill_root = "seo-roadmap" if args.claude_skill else "skills/seo-roadmap"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(args.output, "w", compression=ZIP_DEFLATED) as archive:
        if not args.claude_skill:
            archive.writestr(".codex-plugin/plugin.json", json.dumps(manifest, indent=2) + "\n")
            archive.write(package / "assets" / "icon.svg", "assets/icon.svg")
            if args.mcp_url:
                config = {"mcpServers": {"agentic-harness-seo": {"url": args.mcp_url}}}
                archive.writestr(".mcp.json", json.dumps(config, indent=2) + "\n")
        archive.write(package / "skills" / "seo-roadmap" / "SKILL.md", f"{skill_root}/SKILL.md")
        for name, source in references.items():
            archive.write(source, f"{skill_root}/references/{name}")
        for name, source in notices.items():
            archive.write(source, f"{skill_root}/{name}" if args.claude_skill else name)
    print(args.output.resolve())


if __name__ == "__main__":
    main()

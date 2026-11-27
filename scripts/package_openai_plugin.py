"""Sync native plugin manifests or build a hosted plugin or skill ZIP."""

import argparse
import json
from pathlib import Path
from shutil import copyfile
from urllib.parse import urlsplit
from zipfile import ZIP_DEFLATED, ZipFile

from runtime import _plugin_version
from workflow_catalog import hosted_body, split_skill, workflows

CLAUDE_PACKAGE_README = """# Agentic Harness SEO

Audit websites, check structured data and content, and build SEO roadmaps.
Open the Claude skill picker and choose a workflow such as `seo-audit`,
`seo-technical`, or `seo-roadmap`. Use `harness-seo` for the full command menu.

In hosted chat, workflows use the available browsing and connected tools. Local
shell checks require the managed toolkit runtime, and provider workflows need the
corresponding account or connector.

[Install and setup guide](https://github.com/zafajardo9/agentic-harness-seo#install)
"""


def sync_native(root: Path, references: dict[str, Path]) -> None:
    skill_paths = list(dict.fromkeys(
        f"./{skill.parent.parent.relative_to(root).as_posix()}/"
        for skill in workflows(root).values()
        if skill.parent.parent != root / "skills"
    ))
    for host, paths in (("codex", ["./skills/", *skill_paths]), ("claude", skill_paths)):
        manifest_path = root / f".{host}-plugin/plugin.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["version"] = _plugin_version(root)
        manifest["skills"] = paths
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    roadmap = workflows(root)["seo-roadmap"].parent
    for name, source in references.items():
        destination = roadmap / "references" / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        copyfile(source, destination)


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
    variant.add_argument("--claude-plugin", action="store_true", help="Build a Claude chat plugin ZIP")
    variant.add_argument("--sync-repo", action="store_true", help="Refresh the native plugin manifests")
    args = parser.parse_args()
    if args.sync_repo and args.output is not None:
        parser.error("--sync-repo does not take an output path")
    if not args.sync_repo and args.output is None:
        parser.error("provide an output ZIP path or --sync-repo")

    root = Path(__file__).resolve().parents[1]
    package = root / "packaging" / "openai"
    planning = root / "skills" / "seo-plan"
    references = {
        "workflow.md": planning / "SKILL.md",
        **{f"industries/{path.name}": path for path in sorted((planning / "assets").glob("*.md"))},
    }
    license_file = root / "LICENSE"
    if args.sync_repo:
        sync_native(root, references)
        print(root)
        return

    host = "claude" if args.claude_plugin else "codex"
    manifest_path = f".{host}-plugin/plugin.json"
    manifest = json.loads((root / manifest_path).read_text(encoding="utf-8"))
    manifest["version"] = _plugin_version(root)
    manifest["skills"] = "./skills/"
    if host == "codex":
        manifest["interface"].update(logo="./assets/icon.svg", composerIcon="./assets/icon.svg")
    else:
        manifest["description"] = "Audit websites, analyze search performance, and build SEO roadmaps."
        manifest.pop("skills")  # Claude scans skills/ by default.

    if args.mcp_url:
        manifest["name"] = "agentic-harness-seo-live"
        manifest["description"] = "Run SEO workflows with live page and draft HTML checks."
        manifest["mcpServers"] = "./.mcp.json"
        interface = manifest["interface"]
        interface["displayName"] = "Agentic Harness SEO Live"
        interface["shortDescription"] = "Live SEO checks and plans"
        interface["longDescription"] += " Check public pages and draft HTML with the SEO connector."
        interface["capabilities"].extend(["Live page checks", "Draft HTML checks"])

    args.output.parent.mkdir(parents=True, exist_ok=True)
    catalog = workflows(root)
    with ZipFile(args.output, "w", compression=ZIP_DEFLATED) as archive:
        if args.claude_skill:
            catalog = {"seo-roadmap": catalog["seo-roadmap"]}
            archive.write(license_file, "seo-roadmap/LICENSE")
        else:
            archive.writestr(manifest_path, json.dumps(manifest, indent=2) + "\n")
            archive.write(package / "assets" / "icon.svg", "assets/icon.svg")
            archive.write(license_file, "LICENSE")
            if args.claude_plugin:
                archive.writestr("README.md", CLAUDE_PACKAGE_README)
                archive.write(root / "requirements.txt", "requirements.txt")
                for folder in ("scripts", "agents", "hooks", "schema", "data", "extensions", "assets"):
                    for path in sorted((root / folder).rglob("*")):
                        relative = path.relative_to(root)
                        if (
                            path.is_file() and not path.is_symlink()
                            and not any(part.startswith(".") or part in {"__pycache__", "node_modules"} for part in relative.parts)
                            and path.suffix in {"", ".py", ".js", ".cjs", ".json", ".md", ".txt", ".sh", ".ps1", ".svg", ".png", ".html", ".csv"}
                        ):
                            archive.write(path, relative.as_posix())
            if args.mcp_url:
                config = {"mcpServers": {"agentic-harness-seo": {"url": args.mcp_url}}}
                archive.writestr(".mcp.json", json.dumps(config, indent=2) + "\n")
        for name, skill in catalog.items():
            skill_root = name if args.claude_skill else f"skills/{name}"
            frontmatter, _ = split_skill(skill)
            archive.writestr(f"{skill_root}/SKILL.md", f"---\n{frontmatter}\n---\n\n{hosted_body(skill)}")
            for path in sorted(skill.parent.rglob("*")):
                relative = path.relative_to(skill.parent)
                if name == "seo-roadmap" and relative.parts[0] == "references":
                    continue
                if path.is_file() and path != skill and not path.is_symlink() and not any(part.startswith(".") for part in relative.parts):
                    archive.write(path, f"{skill_root}/{relative.as_posix()}")
            if name == "seo-roadmap":
                for reference, source in references.items():
                    archive.write(source, f"{skill_root}/references/{reference}")
    print(args.output.resolve())


if __name__ == "__main__":
    main()

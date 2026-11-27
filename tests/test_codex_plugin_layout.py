"""Verify every package advertises the same canonical SEO workflows."""

import json
import sys
from pathlib import Path
from zipfile import ZipFile

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from package_openai_plugin import main  # noqa: E402
from workflow_catalog import workflows  # noqa: E402


def test_native_marketplaces_cover_the_shared_catalog() -> None:
    marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    (entry,) = marketplace["plugins"]
    package = ROOT / entry["source"]["path"]
    codex = json.loads((package / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    claude = json.loads((package / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    assert codex["name"] == entry["name"]
    assert codex["version"] == claude["version"]
    assert (package / codex["interface"]["logo"]).is_file()
    assert (package / "scripts/agentic-harness-seo").is_file()

    catalog = workflows(ROOT)
    assert {"harness-seo", "seo-audit", "seo-roadmap", "seo-generate-poster",
            "seo-firecrawl", "seo-ahrefs", "seo-seranking"} <= set(catalog)
    for paths in (codex["skills"], ["./skills/", *claude["skills"]]):
        skills = [skill for path in paths for skill in (package / path).glob("*/SKILL.md")]
        assert len(skills) == len(catalog)
        assert set(skills) == set(catalog.values())


def test_roadmap_references_match_planning_sources() -> None:
    references = ROOT / "skills/seo-roadmap/references"
    planning = ROOT / "skills/seo-plan"
    assert (references / "workflow.md").read_bytes() == (planning / "SKILL.md").read_bytes()
    template_names = {path.name for path in (planning / "assets").glob("*.md")}
    assert {"saas.md", "local-service.md", "ecommerce.md", "publisher.md", "agency.md", "generic.md"} <= template_names
    assert {path.name for path in (references / "industries").glob("*.md")} == template_names
    for name in template_names:
        assert (references / "industries" / name).read_bytes() == (planning / "assets" / name).read_bytes()


@pytest.mark.parametrize(("args", "manifest_path"), [
    ([], ".codex-plugin/plugin.json"),
    (["--mcp-url", "https://example.com/mcp"], ".codex-plugin/plugin.json"),
    (["--claude-plugin"], ".claude-plugin/plugin.json"),
])
def test_hosted_packages_offer_the_shared_catalog(tmp_path, monkeypatch, args, manifest_path):
    destination = tmp_path / "plugin.zip"
    monkeypatch.setattr(sys, "argv", ["package_openai_plugin.py", str(destination), *args])
    main()

    with ZipFile(destination) as archive:
        files = set(archive.namelist())
        assert archive.testzip() is None
        assert {name for name in files if name.startswith("skills/") and name.endswith("/SKILL.md")} == {
            f"skills/{name}/SKILL.md" for name in workflows(ROOT)
        }
        assert b"Working in hosted chat" in archive.read("skills/seo-audit/SKILL.md")
        assert "skills/seo-generate-poster/references/profiles/filepino.md" in files
        assert "skills/seo-roadmap/references/industries/saas.md" in files
        assert "skills/seo-cluster/templates/cluster-map.html" in files
        manifest = json.loads(archive.read(manifest_path))
        if "--claude-plugin" in args:
            assert {"README.md", "scripts/agentic-harness-seo", "requirements.txt", "hooks/hooks.json"} <= files
            assert "skills" not in manifest
        else:
            assert manifest["skills"] == "./skills/"
            assert manifest["interface"]["logo"].removeprefix("./") in files
        assert (".mcp.json" in files) == ("--mcp-url" in args)

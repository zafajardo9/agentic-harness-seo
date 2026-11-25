"""Keep the installable Codex planner in sync with the ZIP package inputs."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_marketplace_points_to_a_complete_planner() -> None:
    marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
    (entry,) = marketplace["plugins"]
    package = ROOT / entry["source"]["path"]
    manifest = json.loads((package / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    release = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    assert manifest["name"] == entry["name"]
    assert manifest["version"] == release["version"]
    assert (package / manifest["interface"]["logo"]).is_file()
    skill = package / manifest["skills"] / "seo-roadmap"
    assert (skill / "SKILL.md").is_file()

    planning = ROOT / "skills" / "seo-plan"
    references = skill / "references"
    assert (references / "workflow.md").read_bytes() == (planning / "SKILL.md").read_bytes()
    template_names = {path.name for path in (planning / "assets").glob("*.md")}
    assert {"saas.md", "local-service.md", "ecommerce.md", "publisher.md", "agency.md", "generic.md"} <= template_names
    industries = references / "industries"
    assert {path.name for path in industries.glob("*.md")} == template_names
    for name in template_names:
        assert (industries / name).read_bytes() == (planning / "assets" / name).read_bytes()
    for name in ("LICENSE", "NOTICE"):
        assert (package / name).read_bytes() == (ROOT / name).read_bytes()


def test_marketplace_bundles_the_shared_poster_skill() -> None:
    source = ROOT / "skills" / "seo-generate-poster"
    bundled = ROOT / "packaging" / "openai" / "skills" / source.name
    files = {path.relative_to(source) for path in source.rglob("*") if path.is_file()}
    assert {
        Path("SKILL.md"),
        Path("references/canva-connection.md"),
        Path("references/profiles/dds.md"),
        Path("references/profiles/filepino.md"),
    } <= files
    assert {path.relative_to(bundled) for path in bundled.rglob("*") if path.is_file()} == files
    for path in files:
        assert (source / path).read_bytes() == (bundled / path).read_bytes()

"""Portable install for harnesses that have no plugin marketplace.

The installer is the only bundled tool that runs under a plain interpreter, so
these tests drive it as a module against a synthetic checkout. No network, no
managed venv, no real home directory.
"""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "portable_install", ROOT / "scripts" / "portable_install.py"
)
portable_install = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(portable_install)

BARE_INVOCATION = re.compile(r"(?<![A-Za-z0-9_/])agentic-harness-seo (?:run|setup|doctor)\b")


def _checkout(tmp_path: Path) -> Path:
    """A minimal checkout: one skill carrying the canonical token, plus a launcher."""
    source = tmp_path / "checkout"
    (source / "scripts").mkdir(parents=True)
    (source / "scripts" / "agentic-harness-seo").write_text("#!/usr/bin/env bash\n", encoding="utf-8")
    (source / "scripts" / "runtime.py").write_text("# runtime\n", encoding="utf-8")
    (source / "skills" / "harness-seo").mkdir(parents=True)
    (source / "skills" / "harness-seo" / "SKILL.md").write_text(
        'Run:\n\n    "${CLAUDE_PLUGIN_ROOT}/scripts/agentic-harness-seo" run parse_html.py\n',
        encoding="utf-8",
    )
    (source / "agents").mkdir()
    (source / "agents" / "seo-technical.md").write_text("# technical\n", encoding="utf-8")
    (source / "requirements.txt").write_text("requests>=2,<3\n", encoding="utf-8")
    (source / "LICENSE").write_text("license\n", encoding="utf-8")
    (source / ".claude-plugin").mkdir()
    (source / ".claude-plugin" / "plugin.json").write_text('{"version": "0.0.0"}\n', encoding="utf-8")
    return source


def test_resolve_harnesses_expands_all_and_dedupes() -> None:
    names = portable_install.resolve_harnesses("codex, cursor,codex,all")
    assert names[0] == "codex"
    assert names[1] == "cursor"
    assert set(names) == set(portable_install.HARNESS_TARGETS)
    assert len(names) == len(set(names))


def test_resolve_harnesses_rejects_unknown() -> None:
    with pytest.raises(ValueError, match="unknown harness"):
        portable_install.resolve_harnesses("codex,windsurf")


def test_install_copies_layout_and_rewrites_the_token(tmp_path: Path) -> None:
    source = _checkout(tmp_path)
    destination = tmp_path / "install"
    result = portable_install.install(source, destination)

    assert Path(str(result["launcher"])).is_file()
    assert (destination / "agents" / "seo-technical.md").is_file()
    assert (destination / "requirements.txt").is_file()
    assert (destination / "LICENSE").is_file()
    assert (destination / "runtime-plugin.json").is_file()
    assert result["rewritten_docs"] == 1

    skill = (destination / "skills" / "harness-seo" / "SKILL.md").read_text(encoding="utf-8")
    assert "${CLAUDE_PLUGIN_ROOT}" not in skill
    assert destination.as_posix() in skill


def test_install_writes_each_harness_instruction_file(tmp_path: Path) -> None:
    source = _checkout(tmp_path)
    destination = tmp_path / "install"
    project = tmp_path / "site"
    project.mkdir()

    harnesses = portable_install.resolve_harnesses("all")
    result = portable_install.install(source, destination, harnesses, project)

    assert len(result["adapters"]) == len(set(portable_install.HARNESS_TARGETS.values()))
    for relative in ("AGENTS.md", "GEMINI.md", "CONVENTIONS.md"):
        text = (project / relative).read_text(encoding="utf-8")
        assert destination.as_posix() in text
        assert "$" + "{CLAUDE_PLUGIN_ROOT}" not in text

    cursor = (project / ".cursor" / "rules" / "agentic-harness-seo.mdc").read_text(encoding="utf-8")
    assert cursor.startswith("---\n")
    assert "alwaysApply: false" in cursor
    assert (project / ".clinerules" / "agentic-harness-seo.md").is_file()


def test_install_is_idempotent_and_keeps_one_block(tmp_path: Path) -> None:
    source = _checkout(tmp_path)
    destination = tmp_path / "install"
    project = tmp_path / "site"
    project.mkdir()
    agents = project / "AGENTS.md"
    agents.write_text("# My project\n\nExisting instructions.\n", encoding="utf-8")

    portable_install.install(source, destination, ["codex"], project)
    portable_install.install(source, destination, ["codex"], project)

    text = agents.read_text(encoding="utf-8")
    assert text.count(portable_install.BEGIN) == 1
    assert text.count(portable_install.END) == 1
    assert text.startswith("# My project")
    assert "Existing instructions." in text


def test_install_block_never_uses_a_bare_launcher_invocation(tmp_path: Path) -> None:
    block = portable_install.instruction_block(tmp_path / "install")
    assert not BARE_INVOCATION.search(block)


def test_install_refuses_a_destination_inside_the_checkout(tmp_path: Path) -> None:
    source = _checkout(tmp_path)
    with pytest.raises(ValueError, match="outside the source checkout"):
        portable_install.install(source, source / "nested")


def test_install_requires_force_for_an_unrelated_directory(tmp_path: Path) -> None:
    source = _checkout(tmp_path)
    destination = tmp_path / "occupied"
    destination.mkdir()
    (destination / "keep.txt").write_text("mine\n", encoding="utf-8")

    with pytest.raises(FileExistsError, match="pass --force"):
        portable_install.install(source, destination)

    portable_install.install(source, destination, force=True)
    assert (destination / "keep.txt").is_file()
    assert (destination / "scripts" / "agentic-harness-seo").is_file()

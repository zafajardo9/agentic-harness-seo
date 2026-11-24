"""Test the hosted MCP entry point with the official client."""

import sys
from pathlib import Path

import anyio
import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from seo_mcp import server  # noqa: E402


def test_connector_is_launchable_through_managed_runtime():
    from runtime import _resolve_script

    root = Path(__file__).resolve().parents[1]
    assert _resolve_script(root, "seo_mcp.py", extension=None) == root / "scripts" / "seo_mcp.py"


def test_connector_workflows(monkeypatch):
    import fetch_page

    def fetch(url, *, timeout, public_only, max_time, max_bytes):
        assert public_only and timeout == 5 and max_time == 10 and max_bytes == 1_000_000
        return {
            "url": url,
            "content": "<title>Example storefront</title><h1>Example storefront</h1>",
            "status_code": 200,
            "headers": {"Content-Type": "text/html"},
        }

    monkeypatch.setattr(fetch_page, "fetch_page", fetch)

    async def run():
        app = server.streamable_http_app()
        async with app.router.lifespan_context(app):
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport) as client:
                async with streamable_http_client(
                    "http://localhost:8000/mcp", http_client=client,
                ) as (read, write, _):
                    async with ClientSession(read, write) as session:
                        await session.initialize()
                        tools = {tool.name: tool for tool in (await session.list_tools()).tools}
                        assert set(tools) == {
                            "seo_audit_page", "seo_check_html", "seo_planning_framework",
                        }
                        assert all(tool.annotations.readOnlyHint is True for tool in tools.values())

                        url = "https://example.com/"
                        audit = await session.call_tool("seo_audit_page", {"url": url})
                        assert not audit.isError
                        assert audit.structuredContent["facts"]["title"] == "Example storefront"

                        html_result = await session.call_tool(
                            "seo_check_html", {"page_url": url, "html": "<title>Draft site</title>"},
                        )
                        assert not html_result.isError
                        assert html_result.structuredContent["facts"]["title"] == "Draft site"

                        plan = await session.call_tool("seo_planning_framework", {"industry": "saas"})
                        assert not plan.isError
                        assert "Implementation Roadmap" in plan.structuredContent["workflow"]
                        assert plan.structuredContent["template"]

                        invalid = await session.call_tool("seo_planning_framework", {"industry": "../robots"})
                        assert invalid.isError

    anyio.run(run)

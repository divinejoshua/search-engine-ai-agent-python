# serp.py
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def search_duckduckgo(query: str) -> list[str]:
    params = StdioServerParameters(
        command="npx",
        args=["@modelcontextprotocol/serp", "--provider", "duckduckgo"],
        env=None
    )
    async with stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            response = await session.call_tool("search", arguments={"query": query})

    results = []
    for r in response.get("results", []):
        title = r.get("title", "")
        snippet = r.get("snippet", "")
        link = r.get("link", "")
        results.append(f"{title}\n{snippet}\n{link}")

    return results

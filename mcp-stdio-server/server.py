#!/usr/bin/env python3
import asyncio
import subprocess
import sys
import os  # Added for environment variables
from typing import Any, Sequence

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
)

app = Server("mac-memory-checker")


@app.list_tools()
async def handle_list_tools() -> list[Tool]:
    return [
        Tool(
            name="check_mac_memory",
            description="Check Mac free memory using top command",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        )
    ]


@app.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[TextContent]:
    if name != "check_mac_memory":
        # Validate tool name first
        raise ValueError(f"Unknown tool: {name}")

    try:
        # Force English output for consistent parsing
        env = os.environ.copy()
        env["LANG"] = "C"

        # Run the top command to get memory info
        result = subprocess.run(
            ["top", "-l", "1", "-s", "0"],
            capture_output=True,
            text=True,
            timeout=10,
            env=env  # Use modified environment
        )

        if result.returncode != 0:
            return [TextContent(type="text", text=f"Error running top command: {result.stderr}")]

        # Find memory line (works for both "PhysMem" and "Physical Memory")
        for line in result.stdout.splitlines():
            if "PhysMem" in line or "Physical Memory" in line:
                return [TextContent(type="text", text=f"Mac Memory Status:\n{line.strip()}")]

        return [TextContent(type="text", text="Memory information not found in top output")]

    except subprocess.TimeoutExpired:
        return [TextContent(type="text", text="Command timed out")]
    except Exception as e:
        return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="mac-memory-checker",
                server_version="1.0.0",
                capabilities={
                    "tools": {},
                    "prompts": {}
                },
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
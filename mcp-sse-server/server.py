#!/usr/bin/env python3

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
)

app = Server("calculator-server")

logger = logging.getLogger(__name__)

@dataclass
class CalculatorArgs:
    a: float
    b: float

def validate_numbers(a: Union[str, int, float], b: Union[str, int, float]) -> tuple[float, float]:
    try:
        num_a = float(a)
        num_b = float(b)
        return num_a, num_b
    except (ValueError, TypeError):
        raise ValueError("Both arguments must be valid numbers")

@app.list_tools()
async def handle_list_tools() -> list[Tool]:
    return [
        Tool(
            name="add",
            description="Add two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="subtract",
            description="Subtract second number from first number",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="multiply",
            description="Multiply two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="divide",
            description="Divide first number by second number",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number (dividend)"},
                    "b": {"type": "number", "description": "Second number (divisor)"},
                },
                "required": ["a", "b"],
            },
        ),
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "add":
            a, b = validate_numbers(arguments.get("a"), arguments.get("b"))
            result = a + b
            return [TextContent(type="text", text=f"Result: {result}")]
        
        elif name == "subtract":
            a, b = validate_numbers(arguments.get("a"), arguments.get("b"))
            result = a - b
            return [TextContent(type="text", text=f"Result: {result}")]
        
        elif name == "multiply":
            a, b = validate_numbers(arguments.get("a"), arguments.get("b"))
            result = a * b
            return [TextContent(type="text", text=f"Result: {result}")]
        
        elif name == "divide":
            a, b = validate_numbers(arguments.get("a"), arguments.get("b"))
            if b == 0:
                return [TextContent(type="text", text="Error: Division by zero is not allowed")]
            result = a / b
            return [TextContent(type="text", text=f"Result: {result}")]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except ValueError as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="calculator-server",
                server_version="0.1.0",
                capabilities={
                    "tools": {},
                    "prompts": {}
                },
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
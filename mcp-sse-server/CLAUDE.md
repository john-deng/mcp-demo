# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Model Context Protocol (MCP) server implementation written in Python that provides a calculator service with basic arithmetic operations. The server uses the `mcp` library and communicates via stdio to expose calculator tools to MCP clients.

## Development Commands

### Installation & Setup
```bash
# Or create and activate the shared virtual environment first
uv venv ../.venv
source ../.venv/bin/activate  # On Windows: ..\.venv\Scripts\activate
uv pip install -r requirements.txt
```

### Running the Server
```bash
# Run the MCP server
python3 server.py

# The server communicates via stdio - it's designed to be used by MCP clients
# For testing, you can run it directly but it expects JSON-RPC communication
```

### Testing
```bash
# No formal test suite is configured
# Test by integrating with an MCP client or using manual JSON-RPC calls
```

## Architecture

### Single-File Structure
- `server.py` - Main MCP server implementation containing:
  - Server initialization using the `mcp` library
  - Tool definitions for calculator operations (add, subtract, multiply, divide)
  - Tool handlers with input validation and error handling
  - Async stdio server setup

### Key Components

1. **Server Setup**: Uses `mcp.server.server.Server` class with stdio communication
2. **Tool Registration**: Decorators `@app.list_tools()` and `@app.call_tool()` register available tools
3. **Input Validation**: `validate_numbers()` function ensures proper numeric input
4. **Error Handling**: Comprehensive error handling for invalid inputs and division by zero
5. **Protocol Compliance**: Implements MCP protocol version "2024-11-05"

### MCP Protocol Implementation
- Implements standard MCP tool listing and execution
- Uses JSON Schema for tool input validation
- Returns `TextContent` responses for all operations
- Handles both expected errors (division by zero) and unexpected errors gracefully

## Key Files
- `server.py` - Complete MCP server implementation
- `requirements.txt` - Python dependencies (only `mcp>=1.0.0`)
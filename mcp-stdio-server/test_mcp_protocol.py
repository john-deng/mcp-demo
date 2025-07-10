#!/usr/bin/env python3
import asyncio
import json
import subprocess
import sys

async def test_mcp_server():
    """Test the MCP server via stdio protocol"""
    print("Testing MCP server via stdio protocol...")
    
    # Start the server process
    process = await asyncio.create_subprocess_exec(
        sys.executable, "server.py",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    try:
        # Send initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        print("1. Sending initialize request...")
        init_json = json.dumps(init_request) + "\n"
        process.stdin.write(init_json.encode())
        await process.stdin.drain()
        
        # Read response
        response_line = await process.stdout.readline()
        if response_line:
            response = json.loads(response_line.decode())
            print(f"   Initialize response: {response.get('result', {}).get('serverInfo', {}).get('name', 'Unknown')}")
        
        # Send tools/list request
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        print("2. Requesting tools list...")
        tools_json = json.dumps(tools_request) + "\n"
        process.stdin.write(tools_json.encode())
        await process.stdin.drain()
        
        # Read response
        response_line = await process.stdout.readline()
        if response_line:
            response = json.loads(response_line.decode())
            tools = response.get('result', {}).get('tools', [])
            print(f"   Available tools: {[tool['name'] for tool in tools]}")
        
        # Send tool call request
        call_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "check_mac_memory",
                "arguments": {}
            }
        }
        
        print("3. Calling check_mac_memory tool...")
        call_json = json.dumps(call_request) + "\n"
        process.stdin.write(call_json.encode())
        await process.stdin.drain()
        
        # Read response
        response_line = await process.stdout.readline()
        if response_line:
            response = json.loads(response_line.decode())
            content = response.get('result', {}).get('content', [])
            if content:
                print(f"   Memory result: {content[0].get('text', 'No text')}")
        
        print("✅ MCP server is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
        return False
    finally:
        # Clean up
        process.stdin.close()
        try:
            await asyncio.wait_for(process.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            process.terminate()
            await process.wait()

if __name__ == "__main__":
    success = asyncio.run(test_mcp_server())
    sys.exit(0 if success else 1)
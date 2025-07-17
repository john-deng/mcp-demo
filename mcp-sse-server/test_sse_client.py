#!/usr/bin/env python3

import asyncio
import aiohttp
import json
import sys

async def test_sse_server():
    """Test the SSE MCP server"""
    
    print("Testing SSE MCP Server...")
    
    # Test 1: Connect to SSE endpoint
    print("\n1. Testing SSE connection...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:8000/sse',
                                 headers={'Accept': 'text/event-stream'}) as resp:
                if resp.status == 200:
                    print("✓ SSE connection successful")
                    
                    # Read the first event (should be endpoint info)
                    async for line in resp.content:
                        line_str = line.decode('utf-8').strip()
                        if line_str.startswith('event: endpoint'):
                            print(f"✓ Received endpoint event: {line_str}")
                        elif line_str.startswith('data: '):
                            endpoint_data = line_str[6:]  # Remove 'data: '
                            print(f"✓ Endpoint data: {endpoint_data}")
                            session_url = f"http://localhost:8000{endpoint_data}"
                            print(f"✓ Session URL: {session_url}")
                            break
                else:
                    print(f"✗ SSE connection failed: {resp.status}")
                    return False
    except Exception as e:
        print(f"✗ SSE connection error: {e}")
        return False
    
    # Test 2: Try to send an initialize message
    print("\n2. Testing MCP initialization...")
    try:
        init_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(session_url, 
                                  json=init_message,
                                  headers={'Content-Type': 'application/json'}) as resp:
                if resp.status == 200:
                    print("✓ Initialize message sent successfully")
                    result = await resp.text()
                    print(f"✓ Response: {result}")
                else:
                    print(f"✗ Initialize failed: {resp.status}")
                    error_text = await resp.text()
                    print(f"Error: {error_text}")
                    return False
                    
    except Exception as e:
        print(f"✗ Initialize error: {e}")
        return False
    
    print("\n✓ SSE server test completed successfully!")
    return True

if __name__ == "__main__":
    print("Make sure your SSE server is running on http://localhost:8000")
    print("Run: python handler.py")
    print("\nStarting test in 3 seconds...")
    
    import time
    time.sleep(3)
    
    success = asyncio.run(test_sse_server())
    sys.exit(0 if success else 1)
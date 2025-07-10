#!/usr/bin/env python3
import asyncio
import subprocess
import sys
import os

async def test_memory_command():
    """Test the memory checking command directly"""
    print("Testing memory command...")
    
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
            env=env
        )
        
        if result.returncode != 0:
            print(f"❌ Error running top command: {result.stderr}")
            return False
            
        # Find memory line
        memory_line = None
        for line in result.stdout.splitlines():
            if "PhysMem" in line or "Physical Memory" in line:
                memory_line = line.strip()
                break
                
        if memory_line:
            print(f"✅ Memory command works!")
            print(f"Result: {memory_line}")
            return True
        else:
            print("❌ Memory information not found in top output")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def test_mcp_imports():
    """Test that MCP imports work"""
    print("Testing MCP imports...")
    try:
        from server import app, handle_list_tools, handle_call_tool
        print("✅ MCP server imports work!")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

async def main():
    print("=== Testing MCP Server Components ===")
    
    success1 = await test_mcp_imports()
    success2 = await test_memory_command()
    
    if success1 and success2:
        print("\n✅ All tests passed! MCP server should work correctly.")
        return True
    else:
        print("\n❌ Some tests failed.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
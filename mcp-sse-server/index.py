
import logging
import os
from mcp.server.models import InitializationOptions
from mcp.server.sse import SseServerTransport
from calculator.handler import app

try:
    from starlette.applications import Starlette
    from starlette.routing import Route, Mount
    from starlette.responses import Response
    import uvicorn
except ImportError:
    print("Please install starlette and uvicorn: uv pip install starlette uvicorn")
    exit(1)

logger = logging.getLogger(__name__)


public_path = os.getenv("PUBLIC_PATH", "")
uri_sse = os.path.join(public_path, 'sse')
uri_message = os.path.join(public_path, 'message')

sse = SseServerTransport(uri_message)

async def handle_sse(request):
    """Handle SSE connections"""
    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await app.run(
            streams[0], 
            streams[1], 
            InitializationOptions(
                server_name="calculator-server",
                server_version="0.1.0",
                capabilities={
                    "tools": {},
                    "prompts": {}
                },
            )
        )
    return Response()

def main():
    # Create Starlette routes
    routes = [
        Route(uri_sse, endpoint=handle_sse, methods=["GET"]),
        Mount(uri_message, app=sse.handle_post_message),
    ]
    
    # Create Starlette app
    starlette_app = Starlette(routes=routes)

    # Start server
    uvicorn.run(starlette_app, host="0.0.0.0", port=8000, log_level="info")

if __name__ == "__main__":
    main()
"""Main module for the MCP server."""

import os

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.routing import Mount
import uvicorn

import app.data


load_dotenv()

mcp = FastMCP("FastMCP Boilerplate")

app.data.mcp = mcp


import app.tools # pylint: disable = W0611, C0413



async def authorization_middleware(request: Request, call_next):
    """Enforce Bearer token auth."""

    authorization_header = request.headers.get("Authorization")

    if not authorization_header or not authorization_header.startswith("Bearer "):
        raise HTTPException(status_code = 401, detail = "Missing or invalid Authorization header.")

    if os.getenv("API_KEY_TOKEN") != authorization_header.split(" ", 1)[1]:
        raise HTTPException(status_code = 401, detail = "Invalid API key token.")

    return await call_next(request)


sse_starlette_app = mcp.sse_app()

starlette_app = Starlette(
    routes = [
        Mount("/", app = sse_starlette_app),
    ]
)

starlette_app.add_middleware(BaseHTTPMiddleware, dispatch = authorization_middleware)



if __name__ == "__main__":

    print(f"Starting MCP server on port {os.getenv('PORT', '8000')}.")
    uvicorn.run(starlette_app, port = int(os.getenv("PORT", "8000")), log_level = "error")
    
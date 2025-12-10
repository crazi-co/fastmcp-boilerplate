"""Tools for miscellaneous operations."""

import os
from typing import Dict, Any

import app.data



class Misc:
    """Misc tools."""

    @staticmethod
    @app.data.mcp.tool(name = "misc.health")
    def health() -> Dict[str, Any]:
        """
        This tool lets a user check the current health status of the MCP server.
        
        Returns:
            Dict containing:
                - data: Health object with fields:
                    - service (string): Service name
                    - status (string): Health status
                - message (string): Response message
                - status (string): Response status (success/error)
        """
        return {
            "status": "success",
            "message": "Health check successful.",
            "data": {
                "status": "healthy",
                "service": "fastmcp-boilerplate",
            }
        }

    @staticmethod
    @app.data.mcp.tool(name = "misc.version")
    def version() -> Dict[str, Any]:
        """
        This endpoint lets a user check the current version of the MCP server.
        
        Returns:
            Dict containing:
                - data: Version object with fields:
                    - version (string): API version
                - message (string): Response message
                - status (string): Response status (success/error)
        """
        return {
            "status": "success",
            "message": "Version check successful.",
            "data": {
                "version": os.getenv("VERSION"),
            }
        }

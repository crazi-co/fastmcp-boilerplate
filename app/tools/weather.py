"""Tools for weather operations."""

from typing import Dict, Any

import app.data
from app.utils import make_request



class Weather:

    """Weather tools."""

    @staticmethod
    @app.data.mcp.tool(name = "weather.alerts")
    def alerts(state: str) -> Dict[str, Any]:
        """
        Get weather alerts for a US state.

        Args:
            state: Two-letter US state code (e.g. "CA", "NY")
        
        Returns:
            Dict containing weather alerts for the state.
        """
        return make_request(
            method = "GET",
            url = f"{app.data.BASE_URL}/alerts/active/area/{state}",
            headers = app.data.headers
        )

    @staticmethod
    @app.data.mcp.tool(name = "weather.forecast")
    def forecast(latitude: float, longitude: float) -> Dict[str, Any]:
        """
        Get weather forecast for a location.

        Args:
            latitude: Latitude of the location
            longitude: Longitude of the location
        
        Returns:
            Dict containing weather forecast for the location.
        """
        return make_request(
            method = "GET",
            url = f"{app.data.BASE_URL}/points/{latitude},{longitude}",
            headers = app.data.headers
        )

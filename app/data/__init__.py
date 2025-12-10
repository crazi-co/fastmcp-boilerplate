"""Data package."""

from mcp.server.fastmcp import FastMCP
from requests import Session



BASE_URL: str = "https://api.weather.gov"

headers = {
    "User-Agent": "weather-app/1.0",
    "Accept": "application/geo+json",
}

mcp: FastMCP = None

session: Session = None

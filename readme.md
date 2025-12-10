# FastMCP Boilerplate

A production-ready FastMCP server boilerplate with tool registration, HTTP request utilities, authentication middleware, and SSE (Server-Sent Events) support for AI agent communication.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Technology Stack

- **Language:** Python 3.11+
- **MCP Framework:** FastMCP
- **Web Framework:** Starlette (for SSE endpoint)
- **HTTP Client:** requests (with session management and retry strategy)
- **Server:** Uvicorn
- **Other:** python-dotenv, httpx, urllib3

## Project Structure

```
fastmcp-boilerplate/
├── app/                          # Main application package
│   ├── data/                    # Global data and configuration
│   │   └── __init__.py          # MCP instance, base URL, headers, session
│   ├── logs/                    # Application log files
│   ├── tools/                   # MCP tool implementations
│   │   ├── __init__.py          # Tool module exports
│   │   ├── misc.py              # Miscellaneous tools (health, version)
│   │   └── weather.py           # Weather API tools (alerts, forecast)
│   └── utils/                   # Utility functions
│       ├── __init__.py          # Utility exports
│       └── request.py           # HTTP request helper with retry strategy
├── tests/                       # Test suite
├── run.py                       # Server entry point
├── requirements.txt             # Python dependencies
└── .env.example                 # Environment variables template (if exists)
```

## Prerequisites

- **Python 3.11+** (required)
- **API Key Token** (for authentication)

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd fastmcp-boilerplate
```

### 2. Set Up Environment Variables

```bash
# Copy the example environment file (if exists)
cp .env.example .env

# Edit .env and fill in required variables:
# - API_KEY_TOKEN: Your API key token for authentication
# - PORT: Server port (default: 8000)
# - VERSION: API version (optional)
```

### 3. Install Dependencies

```bash
# Create virtual environment (recommended)
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python run.py
```

The application will start on the port specified in `PORT` environment variable (default: 8000).

### 5. Verify Installation

The server exposes an SSE endpoint at `/sse` for MCP agent communication. You can verify it's running by checking the server logs.

## Authentication

### API Key Authentication

- **Header:** `Authorization: Bearer <api-key-token>`

The `API_KEY_TOKEN` environment variable must match the Bearer token in the Authorization header.

### Request Flow

1. Client sends request with `Authorization: Bearer <token>` header
2. Middleware validates:
   - Authorization header must start with "Bearer "
   - Token must match `API_KEY_TOKEN` environment variable
3. If validation fails → returns `401 Unauthorized`
4. If valid → request proceeds to MCP server

## Available Tools

The MCP server exposes the following tools:

### Weather Tools (`weather.*`)

- **`weather.alerts`**
  - Get weather alerts for a US state
  - Parameters: `state` (string) - Two-letter US state code (e.g. "CA", "NY")
  - Returns: Weather alerts for the specified state

- **`weather.forecast`**
  - Get weather forecast for a location
  - Parameters: `latitude` (float), `longitude` (float)
  - Returns: Weather forecast for the specified coordinates

### Misc Tools (`misc.*`)

- **`misc.health`**
  - Check API health status
  - Returns: Service status information

- **`misc.version`**
  - Get API version
  - Returns: Current API version

## Environment Variables

All environment variables are defined in `.env` file. Key variables include:

- **`API_KEY_TOKEN`**: API key token for authentication (required)
- **`PORT`**: Server port (default: 8000)
- **`VERSION`**: API version (optional)

## Features

- **FastMCP Integration** - Standardized MCP tool interface
- **Tool Registration** - Easy tool registration with decorators
- **HTTP Request Utilities** - Centralized HTTP client with session management
- **Retry Strategy** - Automatic retry for transient errors (429, 502, 503, 504)
- **Authentication Middleware** - Bearer token authentication
- **SSE Support** - Server-Sent Events for real-time agent communication
- **Error Handling** - Comprehensive error logging
- **Session Management** - Efficient HTTP session reuse

## MCP Protocol

### Endpoints

- **`GET /sse`**: Server-Sent Events stream for agent communication
- **`POST /messages`**: MCP message endpoint

### Tool Naming Convention

Tools are named using dot notation: `<module>.<action>`

Examples:
- `weather.alerts`
- `weather.forecast`
- `misc.health`

## Development

### Adding New Tools

1. Create or update the appropriate tool file in `app/tools/`
2. Define a static method with the `@app.data.mcp.tool(name = "module.action")` decorator
3. Use `make_request()` from `app.utils` for HTTP calls
4. Include proper type hints and docstrings

Example:

```python
from typing import Dict, Any
import app.data
from app.utils import make_request

class MyModule:
    """My module tools."""

    @staticmethod
    @app.data.mcp.tool(name = "mymodule.action")
    def action(param: str) -> Dict[str, Any]:
        """Tool description."""
        return make_request(
            method = "GET",
            url = f"{app.data.BASE_URL}/endpoint",
            headers = app.data.headers
        )
```

### Running Tests

```bash
# Run test suite (when implemented)
python -m pytest tests/
```

### Code Style

The project uses pylint for code quality. Run:

```bash
pylint app/
```

## API Response Handling

### Response Format

All tools return JSON responses. The format depends on the external API being called.

### Error Handling

- **API Errors (4xx, 5xx)**: Returned as-is in the response (not treated as exceptions)
- **Network/Connection Errors**: Logged and re-raised as exceptions
- **Authentication Errors**: Returned as 401 HTTP responses by middleware

### Retry Strategy

The request utility includes automatic retry for:
- Status codes: 429, 502, 503, 504
- Max retries: 3
- Backoff factor: 1

## Summary

This FastMCP boilerplate provides a standardized interface for AI agents to interact with external APIs through MCP tools. It:

- Exposes external API endpoints as MCP tools
- Handles authentication and authorization
- Provides robust error handling and retry logic
- Maintains session management for efficient HTTP requests
- Supports SSE for real-time agent communication

The server is designed to be:
- **Stateless**: Each request is self-contained
- **Extensible**: Easy to add new tools by implementing API endpoints
- **Reliable**: Automatic retries and comprehensive error handling

## Support

For issues and questions, please open an issue in the repository.

"""Requests utility."""

import logging
from typing import Dict, Any, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import app.data



logger = logging.getLogger(__name__)

def get_session() -> requests.Session:
    """Get or create a requests session with retry strategy."""

    if not app.data.session:

        app.data.session = requests.Session()

        retry_strategy = Retry(
            total = 3,
            backoff_factor = 1,
            status_forcelist = [429, 502, 503, 504],
            allowed_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
        )

        adapter = HTTPAdapter(max_retries = retry_strategy)
        app.data.session.mount("http://", adapter)
        app.data.session.mount("https://", adapter)

    return app.data.session


def make_request(
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    json: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    files: Optional[Dict[str, Any]] = None,
    timeout: int = 30
) -> Dict[str, Any]:
    """Make an HTTP request and return the JSON response."""

    session = get_session()

    try:
        response = session.request(
            method = method,
            url = url,
            headers = headers,
            json = json,
            params = params,
            data = data,
            files = files,
            timeout = timeout
        )

        return response.json()

    except Exception as e:

        logger.error("Unexpected error making %s request to %s: %s", method, url, e, exc_info = True)
        raise

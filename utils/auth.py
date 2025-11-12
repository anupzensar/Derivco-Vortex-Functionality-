"""
Authentication utilities for Canvas API
"""
from config.settings import settings
import time
import logging
import httpx

logger = logging.getLogger(__name__)


def get_auth_token() -> str:
    """
    Get the Bearer token for Canvas API authentication.
    
    Currently retrieves the token from environment variables.
    In the future, this function can be extended to fetch tokens
    from other sources (e.g., token refresh logic, external auth services).
    
    Returns:
        str: The Bearer token
    """
    # Prefer an explicitly configured static token
    # if settings.CANVAS_BEARER_TOKEN:
    #     return settings.CANVAS_BEARER_TOKEN

    # If no static token, attempt to obtain one from Okta using settings
    # Cache token until expiry to avoid frequent requests
    global _cached_token, _token_expires_at

    try:
        _cached_token
    except NameError:
        _cached_token = None
        _token_expires_at = 0

    if _cached_token and time.time() < _token_expires_at:
        return _cached_token

    # Validate required settings
    if not settings.OKTA_TOKEN_URL or not settings.OKTA_BASIC_AUTH:
        logger.error("OKTA_TOKEN_URL or OKTA_BASIC_AUTH not configured; cannot fetch token")
        raise RuntimeError("No Canvas bearer token configured and Okta token configuration is missing")

    # Build request
    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {settings.OKTA_BASIC_AUTH}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "password",
        "username": settings.OKTA_USERNAME,
        "password": settings.OKTA_PASSWORD,
        "scope": settings.OKTA_SCOPE or "openid roles",
    }

    try:
        with httpx.Client(verify=False, timeout=15.0) as client:
            resp = client.post(settings.OKTA_TOKEN_URL, headers=headers, data=data)
            resp.raise_for_status()
            body = resp.json()

            print("Okta token response:", body)

            access_token = body.get("access_token")
            expires_in = int(body.get("expires_in", 0))

            if not access_token:
                logger.error("Okta token endpoint did not return access_token: %s", body)
                raise RuntimeError("Failed to obtain access token from Okta")

            # Cache token for slightly less than expiry
            _cached_token = access_token
            _token_expires_at = time.time() + max(0, expires_in - 60)
            return _cached_token
    except httpx.HTTPStatusError as e:
        logger.error("Okta token request failed: %s", e.response.text)
        raise RuntimeError(f"Failed to obtain token from Okta: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        logger.error("Okta token request error: %s", str(e))
        raise RuntimeError(f"Failed to obtain token from Okta: {e}")


def get_auth_headers() -> dict:
    """
    Get the authentication headers for Canvas API requests.
    
    Returns:
        dict: Headers dictionary with Bearer token
    """
    token = get_auth_token()
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

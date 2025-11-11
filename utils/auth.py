"""
Authentication utilities for Canvas API
"""
from config.settings import settings


def get_auth_token() -> str:
    """
    Get the Bearer token for Canvas API authentication.
    
    Currently retrieves the token from environment variables.
    In the future, this function can be extended to fetch tokens
    from other sources (e.g., token refresh logic, external auth services).
    
    Returns:
        str: The Bearer token
    """
    return settings.CANVAS_BEARER_TOKEN


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

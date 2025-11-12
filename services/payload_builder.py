"""Build payloads for Pydantic models from normalized input."""
from typing import Any, Dict

from .config import ALIAS_CANDIDATES
from .normalizer import normalize_dict


def build_payload_from_raw(raw: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize raw dict and return alias-keyed payload suitable for models.

    The function checks ALIAS_CANDIDATES and picks the first candidate
    present in the normalized dict for each alias.
    """
    norm = normalize_dict(raw)
    payload: Dict[str, Any] = {}
    for alias, candidates in ALIAS_CANDIDATES.items():
        for cand in candidates:
            if cand in norm:
                payload[alias] = norm[cand]
                break
    return payload


__all__ = ["build_payload_from_raw"]

"""Normalization helpers for extractor modules."""
from typing import Any, Dict


def _normalize_key(k: str) -> str:
    return " ".join(k.strip().lower().split())


def normalize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Return a dict of normalized-key -> value.

    Non-string keys are ignored.
    """
    out: Dict[str, Any] = {}
    for k, v in data.items():
        if not isinstance(k, str):
            continue
        out[_normalize_key(k)] = v
    return out


__all__ = ["normalize_dict", "_normalize_key"]

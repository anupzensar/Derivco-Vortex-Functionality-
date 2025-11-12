"""Ticket type detection logic.

This module focuses on turning a raw input dict into the canonical
ticket type string (lowercased), or returning None when detection fails.
"""
from typing import Any, Dict, Optional

from .config import CHANNEL_MAP
from .normalizer import normalize_dict


def detect_ticket_type(data: Dict[str, Any]) -> Optional[str]:
    norm = normalize_dict(data)

    # 1) channel takes precedence
    if "channel" in norm:
        val = norm["channel"]
        if isinstance(val, str):
            mapped = CHANNEL_MAP.get(val.strip().lower())
            if mapped:
                return mapped

    # 2) explicit detection
    for explicit in ("ticket_type", "ticket type", "issue_type", "issue type", "type"):
        if explicit in norm:
            val = norm[explicit]
            if isinstance(val, str):
                maybe = CHANNEL_MAP.get(val.strip().lower())
                return maybe or val.strip().lower()

    # 3) heuristics similar to previous implementation
    if "test login id" in norm or "test login password" in norm:
        return "game launch issue"
    if "player name" in norm and "game launch url" in norm:
        return "player game launch issue"
    if ("mid" in norm or "module id" in norm) and "round id" in norm:
        return "eti games"
    if "event date & time" in norm or "event date" in norm:
        joined = " ".join(str(v).lower() for v in norm.values() if isinstance(v, (str, int, float)))
        if "stuck" in joined:
            return "stuck open round"
        if "player id" in norm or "player name" in norm:
            return "round outcome"
    if "round id" in norm and "player id" in norm:
        return "stuck open round"

    return None


__all__ = ["detect_ticket_type"]

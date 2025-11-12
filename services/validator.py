"""Validation and extraction helpers that produce structured results.

This module uses Pydantic models and the payload builder to validate and
return uniform results including missing field lists and validation errors.
"""
from typing import Any, Dict, Optional

from pydantic import ValidationError

from .config import TICKET_TYPE_MAP, ALIAS_CANDIDATES, REQUIRED_ALIASES
from .payload_builder import build_payload_from_raw
from .normalizer import normalize_dict


def extract_via_model(model_cls: type, raw: Dict[str, Any]) -> Dict[str, Any]:
    """Parse raw dict into model and return a structured dict.

    The return dict has keys: success, missing_fields, errors, model.
    """
    norm = normalize_dict(raw)
    payload = build_payload_from_raw(raw)

    # Determine canonical name for model
    rev_map = {v: k for k, v in TICKET_TYPE_MAP.items()}
    canon = rev_map.get(model_cls)

    missing = []
    if canon and canon in REQUIRED_ALIASES:
        for alias in REQUIRED_ALIASES[canon]:
            present = False
            if alias in payload and payload.get(alias) not in (None, ""):
                present = True
            else:
                for cand in ALIAS_CANDIDATES.get(alias, []):
                    if cand in norm and norm[cand] not in (None, ""):
                        present = True
                        break
            if not present:
                missing.append(alias)

    if missing:
        return {"success": False, "missing_fields": missing, "errors": None, "model": None}

    try:
        obj = model_cls.model_validate(payload)
    except ValidationError as e:
        return {"success": False, "missing_fields": None, "errors": e.errors(), "model": None}

    model_field_names = list(obj.__class__.model_fields.keys())
    model_data = obj.model_dump(include=set(model_field_names), exclude_none=True)
    return {"success": True, "missing_fields": None, "errors": None, "model": model_data}


__all__ = ["extract_via_model"]

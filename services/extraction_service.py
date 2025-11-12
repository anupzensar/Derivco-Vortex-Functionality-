"""
Top-level extraction service that orchestrates the modular components.

This module intentionally stays small: it handles import path setup for
direct execution, wires together detector/validator/payload builders and
exposes `ExtractionService` and a backward compatible `extract_ticket`.
"""
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# The extraction service supports two ways of being executed/imported:
# 1) as a package (recommended): `python -m services.extraction_service`
#    which makes relative imports work normally.
# 2) as a direct script: `python services/extraction_service.py --sample`.
#    Running as a direct script means relative imports fail; handle this
#    by attempting relative imports first and falling back to fixing
#    sys.path and importing via the package name.

try:
    # Preferred package-style (works when imported as a module)
    from .config import TICKET_TYPE_MAP
    from .detector import detect_ticket_type
    from .validator import extract_via_model
except Exception:
    # Fallback when running the file directly: add project root to sys.path
    project_root = str(Path(__file__).resolve().parent.parent)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    # Import using package-qualified names
    from services.config import TICKET_TYPE_MAP
    from services.detector import detect_ticket_type
    from services.validator import extract_via_model


# Extractors are discovered at runtime via the extractor registry so that
# adding new ticket types doesn't require editing this module. The registry
# dynamically imports modules under `services.extractors` and finds classes
# that inherit `BaseExtractor`.


class ExtractionService:
    """Service wrapper providing a clean API for extraction.

    Usage:
        svc = ExtractionService()
        result = svc.extract(data)

    The result is a dict with the following keys:
      - success: bool
      - ticket_type: canonical ticket type string or None
      - missing_fields: list of missing alias names (if any)
      - errors: list of validation errors (if any)
      - model: extracted model data (dict) on success
    """

    def __init__(self) -> None:
        # dispatch now handled dynamically via the extractor registry
        self.dispatch = None
        try:
            # expose a list of registered ticket types for callers/debugging
            from services.extractor_registry import list_registered_types

            self.registered_types = list_registered_types()
        except Exception:
            self.registered_types = []

    def extract(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(data, dict):
            return {"success": False, "ticket_type": None, "missing_fields": None, "errors": ["data must be a dict"], "model": None}

        ttype = detect_ticket_type(data)
        if not ttype:
            return {"success": False, "ticket_type": None, "missing_fields": None, "errors": ["could not detect ticket type"], "model": None}

        canon = ttype.lower()
        # Use the dynamic registry to find an extractor instance
        from services.extractor_registry import get_extractor_for

        extractor_inst = get_extractor_for(canon)
        if not extractor_inst:
            return {"success": False, "ticket_type": canon, "missing_fields": None, "errors": ["no extractor for ticket type"], "model": None}

        extracted = extractor_inst.extract(data)

        # extractor returns structured dict with success/missing/errors/model
        if isinstance(extracted, dict) and set(extracted.keys()) >= {"success", "model"}:
            return {"success": extracted.get("success", False), "ticket_type": canon, "missing_fields": extracted.get("missing_fields"), "errors": extracted.get("errors"), "model": extracted.get("model")}

        # fallback for legacy extractor which returned model dict or None
        if extracted is None:
            return {"success": False, "ticket_type": canon, "missing_fields": None, "errors": ["parsing failed or invalid input"], "model": None}
        return {"success": True, "ticket_type": canon, "missing_fields": None, "errors": None, "model": extracted}


def extract_ticket(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Backward-compatible simple function that returns the model dict or None.

    This wraps the service for callers that expect the old behaviour.
    """
    svc = ExtractionService()
    res = svc.extract(data)
    return res.get("model") if res.get("success") else None


__all__ = ["extract_ticket", "detect_ticket_type", "ExtractionService"]


def _sample_input() -> dict:
    """Return a representative sample input (contains all fields).

    Use this when the script is executed without external JSON.
    """
    return {
        "channel": "Game Launch Issue",
        "Test Login ID": "test_user_temp",
        "Test Login Password": "p@ssw0rd",
        "Game Launch URL": "https://casino.example/launch",
        "VPN": "vpn-prod",
        "Brand / Casino Company Name": "Example Casino Ltd",
        "Player Name": "Alice Smith",
        "Round ID": "RND-98765",
        "Game Name": "Roulette VIP Temporary",
        "Brand Name": "VIP Brand Temporary",
        "MID": "MID-55",
        "Player ID": "PID-123",
        "Event Date & Time": "2025-11-11 14:30:00",
        "Casino ID": "CAS-001",
    }


def _run_cli():
    import argparse
    import json
    parser = argparse.ArgumentParser(description="Run extractor on JSON input")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--file", "-f", help="Path to JSON file containing the input dict")
    group.add_argument("--json", "-j", help="Inline JSON string as input")
    group.add_argument("--sample", "-s", action="store_true", help="Use built-in sample input")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    elif args.json:
        data = json.loads(args.json)
    elif args.sample:
        data = _sample_input()
    else:
        # If nothing provided, use sample by default
        data = _sample_input()

    service = ExtractionService()
    res = service.extract(data)
    print(json.dumps(res, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    _run_cli()

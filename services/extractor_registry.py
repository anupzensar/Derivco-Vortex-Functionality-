"""Dynamic registry for extractor classes.

This module discovers classes inheriting `BaseExtractor` under
`services.extractors` and registers them by their canonical `ticket_type`.

New extractor modules are picked up automatically (no registry edit needed).
"""
import importlib
import inspect
import pkgutil
from typing import Dict

from services.extractors import base as _base_pkg
from services import extractors as _extractors_pkg


def discover_extractors() -> Dict[str, _base_pkg.BaseExtractor]:
    registry: Dict[str, _base_pkg.BaseExtractor] = {}

    for finder, name, ispkg in pkgutil.iter_modules(_extractors_pkg.__path__):
        # skip base module itself
        if name == "base":
            continue
        module = importlib.import_module(f"services.extractors.{name}")
        for _, obj in inspect.getmembers(module, inspect.isclass):
            try:
                if issubclass(obj, _base_pkg.BaseExtractor) and obj is not _base_pkg.BaseExtractor:
                    inst = obj()
                    registry[inst.ticket_type.lower()] = inst
            except Exception:
                # ignore classes that fail to initialize or are not proper extractors
                continue

    return registry


_REGISTRY = discover_extractors()


def get_extractor_for(ticket_type: str):
    if not ticket_type:
        return None
    return _REGISTRY.get(ticket_type.lower())


def list_registered_types():
    return list(_REGISTRY.keys())


__all__ = ["get_extractor_for", "list_registered_types", "discover_extractors"]

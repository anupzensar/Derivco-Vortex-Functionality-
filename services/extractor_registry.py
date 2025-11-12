"""Dynamic registry for extractor classes.

This module discovers classes inheriting `BaseExtractor` under
`services.extractors` and registers them by their canonical `ticket_type`.

New extractor modules are picked up automatically (no registry edit needed).
"""
import importlib
import inspect
import pkgutil
import os
from typing import Dict

from services.extractors.base import BaseExtractor


def discover_extractors() -> Dict[str, BaseExtractor]:
    registry: Dict[str, BaseExtractor] = {}

    # Get the extractors directory path
    extractors_path = os.path.join(os.path.dirname(__file__), "extractors")
    
    # Find all Python files in the extractors directory
    for filename in os.listdir(extractors_path):
        if filename.endswith('.py') and filename != 'base.py' and not filename.startswith('__'):
            module_name = filename[:-3]  # Remove .py extension
            module = importlib.import_module(f"services.extractors.{module_name}")
            for _, obj in inspect.getmembers(module, inspect.isclass):
                try:
                    if issubclass(obj, BaseExtractor) and obj is not BaseExtractor:
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

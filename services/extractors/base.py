from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseExtractor(ABC):
    """Abstract base class for per-ticket extractors.

    Subclasses must set the `ticket_type` class attribute to the canonical
    ticket type string (e.g. 'game launch issue') and either set `model_cls`
    or override `extract`.
    """
    ticket_type: str = ""
    model_cls = None

    def __init__(self) -> None:
        if not self.ticket_type:
            raise ValueError("Extractor must set ticket_type")

    def extract(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """Default extract implementation: delegate to validator using model_cls.

        Override in subclasses for custom behaviour.
        """
        if self.model_cls is None:
            raise NotImplementedError("Extractor must define model_cls or override extract")
        # Import locally to avoid circular imports at module import time
        from services.validator import extract_via_model

        return extract_via_model(self.model_cls, raw)

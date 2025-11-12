from typing import Dict, Any

from services.extractors.base import BaseExtractor
from services.config import TICKET_TYPE_MAP


class RoundOutcomeExtractor(BaseExtractor):
    ticket_type = "round outcome"
    model_cls = TICKET_TYPE_MAP.get(ticket_type)


__all__ = ["RoundOutcomeExtractor"]

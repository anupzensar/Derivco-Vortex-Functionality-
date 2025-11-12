from typing import Dict, Any

from services.extractors.base import BaseExtractor
from services.config import TICKET_TYPE_MAP


class StuckOpenRoundExtractor(BaseExtractor):
    ticket_type = "stuck open round"
    model_cls = TICKET_TYPE_MAP.get(ticket_type)


__all__ = ["StuckOpenRoundExtractor"]

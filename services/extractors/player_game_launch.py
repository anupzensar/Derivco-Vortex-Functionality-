from typing import Dict, Any

from services.extractors.base import BaseExtractor
from services.config import TICKET_TYPE_MAP


class PlayerGameLaunchExtractor(BaseExtractor):
    ticket_type = "player game launch issue"
    model_cls = TICKET_TYPE_MAP.get(ticket_type)


__all__ = ["PlayerGameLaunchExtractor"]

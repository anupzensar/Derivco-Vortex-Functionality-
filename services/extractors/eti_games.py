from typing import Dict, Any

from services.extractors.base import BaseExtractor
from services.config import TICKET_TYPE_MAP


class ETIGamesExtractor(BaseExtractor):
    ticket_type = "eti games"
    model_cls = TICKET_TYPE_MAP.get(ticket_type)

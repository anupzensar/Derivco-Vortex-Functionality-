from pydantic import BaseModel, Field
from typing import Optional


class StuckOpenRound(BaseModel):
    player_id: Optional[str] = Field(None, alias="Player ID")
    player_name: Optional[str] = Field(None, alias="Player Name")
    casino_id: Optional[str] = Field(None, alias="Casino ID")
    round_id: Optional[str] = Field(None, alias="Round ID")
    event_datetime: Optional[str] = Field(None, alias="Event Date & Time")
    game_name: Optional[str] = Field(None, alias="Game Name")

    class Config:
        populate_by_name = True
        extra = "allow"

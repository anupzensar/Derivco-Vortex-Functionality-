from pydantic import BaseModel, Field
from typing import Optional


class ETIGameIssue(BaseModel):
    player_name: Optional[str] = Field(None, alias="Player Name")
    casino_id: Optional[str] = Field(None, alias="Casino ID")
    round_id: Optional[str] = Field(None, alias="Round ID")
    game_name: Optional[str] = Field(None, alias="Game Name")
    brand_name: Optional[str] = Field(None, alias="Brand Name")
    mid: Optional[str] = Field(None, alias="MID")

    class Config:
        populate_by_name = True
        extra = "allow"

"""
Pydantic models for the ticket types described by the user.

Each field uses an alias that matches the incoming JSON labels so the
extractor can pass alias-keyed dicts directly to the models.
"""
from pydantic import BaseModel, Field
from typing import Optional


class GameLaunchIssue(BaseModel):
    test_login_id: Optional[str] = Field(None, alias="Test Login ID")
    test_login_password: Optional[str] = Field(None, alias="Test Login Password")
    casino_id: Optional[str] = Field(None, alias="Casino ID")
    module_id: Optional[str] = Field(None, alias="Module ID")
    game_launch_url: Optional[str] = Field(None, alias="Game Launch URL")
    vpn: Optional[str] = Field(None, alias="VPN")
    brand_company_name: Optional[str] = Field(None, alias="Brand / Casino Company Name")

    class Config:
        # Pydantic v2 renamed this setting
        populate_by_name = True
        extra = "allow"


class PlayerGameLaunchIssue(BaseModel):
    player_name: Optional[str] = Field(None, alias="Player Name")
    casino_id: Optional[str] = Field(None, alias="Casino ID")
    module_id: Optional[str] = Field(None, alias="Module ID")
    game_launch_url: Optional[str] = Field(None, alias="Game Launch URL")
    vpn: Optional[str] = Field(None, alias="VPN")
    brand_company_name: Optional[str] = Field(None, alias="Brand / Casino Company Name")

    class Config:
        populate_by_name = True
        extra = "allow"


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


class RoundOutcome(BaseModel):
    player_id: Optional[str] = Field(None, alias="Player ID")
    player_name: Optional[str] = Field(None, alias="Player Name")
    casino_id: Optional[str] = Field(None, alias="Casino ID")
    round_id: Optional[str] = Field(None, alias="Round ID")
    event_datetime: Optional[str] = Field(None, alias="Event Date & Time")
    game_name: Optional[str] = Field(None, alias="Game Name")

    class Config:
        populate_by_name = True
        extra = "allow"


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

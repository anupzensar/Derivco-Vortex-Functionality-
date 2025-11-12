from pydantic import BaseModel, Field
from typing import Optional


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

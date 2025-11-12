"""
Central configuration for the extractor: canonical ticket maps, channel map,
alias candidates and required aliases. Kept separate to make the extractor
modules smaller and easier to test.
"""
from typing import Dict, List

from models.game_launch_issue import GameLaunchIssue
from models.player_game_launch_issue import PlayerGameLaunchIssue
from models.eti_game_issue import ETIGameIssue
from models.round_outcome import RoundOutcome
from models.stuck_open_round import StuckOpenRound


# map canonical lowercase ticket type -> model class
TICKET_TYPE_MAP: Dict[str, type] = {
    "game launch issue": GameLaunchIssue,
    "player game launch issue": PlayerGameLaunchIssue,
    "eti games": ETIGameIssue,
    "round outcome": RoundOutcome,
    "stuck open round": StuckOpenRound,
}


# channel value -> canonical ticket type
CHANNEL_MAP: Dict[str, str] = {
    "game launch issue": "game launch issue",
    "game launch": "game launch issue",
    "gli": "game launch issue",
    "player game launch issue": "player game launch issue",
    "player launch": "player game launch issue",
    "eti games": "eti games",
    "eti": "eti games",
    "round outcome": "round outcome",
    "round": "round outcome",
    "stuck open round": "stuck open round",
    "stuck": "stuck open round",
}


# central alias -> normalized candidate keys mapping (normalized form)
ALIAS_CANDIDATES: Dict[str, List[str]] = {
    "Test Login ID": ["test login id", "test_login_id", "testloginid"],
    "Test Login Password": ["test login password", "test_login_password"],
    "Casino ID": ["casino id", "casino_id", "casinoid"],
    # accept 'mid' as a synonym for Module ID
    "Module ID": ["module id", "module_id", "m i d", "mid"],
    "Game Launch URL": ["game launch url", "game_launch_url"],
    "VPN": ["vpn"],
    "Brand / Casino Company Name": ["brand / casino company name", "brand name", "brand_company_name"],
    "Player Name": ["player name", "player_name"],
    "Round ID": ["round id", "round_id"],
    "Game Name": ["game name", "game_name"],
    "Brand Name": ["brand name", "brand_name"],
    "MID": ["mid", "m i d", "module id"],
    "Player ID": ["player id", "player_id"],
    "Event Date & Time": ["event date & time", "event date", "event_datetime", "event date time"],
}


# required alias fields per ticket type (these are aliases as defined in models)
REQUIRED_ALIASES: Dict[str, List[str]] = {
    "game launch issue": [
        "Test Login ID",
        "Test Login Password",
        "Casino ID",
        "Module ID",
        "Game Launch URL",
    ],
    "player game launch issue": [
        "Player Name",
        "Casino ID",
        "Module ID",
        "Game Launch URL",
    ],
    "eti games": ["Player Name", "Casino ID", "Round ID", "Game Name", "Brand Name", "MID"],
    "round outcome": ["Player ID", "Player Name", "Casino ID", "Round ID", "Event Date & Time", "Game Name"],
    "stuck open round": ["Player ID", "Player Name", "Casino ID", "Round ID", "Event Date & Time", "Game Name"],
}




"""
Pydantic schemas for data extraction
"""
from pydantic import BaseModel, Field

class ExtractedNotes(BaseModel):
    """Schema for extracted incident notes"""
    customer_reference: str = Field(default="N/A", alias="Your Reference")
    urgency_level: str = Field(default="N/A", alias="Urgency")
    affected_market: str = Field(default="N/A", alias="Market")
    related_to: str = Field(default="N/A")
    assistance_needed: str = Field(default="N/A", alias="I need assistance with")
    player_login: str = Field(default="N/A", alias="Player Login")
    round_id: str = Field(default="N/A", alias="Round ID")
    round_date_utc: str = Field(default="N/A", alias="Round date (UTC)")
    game_name: str = Field(default="N/A", alias="Game Name + Variant")
    casino_id: str = Field(default="N/A", alias="Casino ID")
    error_description: str = Field(default="N/A", alias="Description")

class FlattenedIncidentResponse(BaseModel):
    """Schema for final extracted incident data"""
    # Top-level fields
    id: str = "N/A"
    summary: str = "N/A"
    status: str = "N/A"
    priority: str = "N/A"
    customer: str = "N/A"
    assigned_group: str = "N/A"
    
    # LLM-extracted fields
    customer_reference: str = "N/A"
    urgency_level: str = "N/A"
    affected_market: str = "N/A"
    related_to: str = "N/A"
    assistance_needed: str = "N/A"
    player_login: str = "N/A"
    round_id: str = "N/A"
    round_date_utc: str = "N/A"
    game_name: str = "N/A"
    casino_id: str = "N/A"
    error_description: str = "N/A"
    full_user_identifier: str = "N/A"

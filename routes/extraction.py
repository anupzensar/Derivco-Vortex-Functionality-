"""Extraction-related API routes separated from `incidents.py`.

Provides endpoints that call the extraction service to map raw incident
JSON into typed ticket payloads.
"""
from fastapi import APIRouter, HTTPException, Body
from typing import Any, Dict

router = APIRouter()


@router.post("/incidents/extract")
async def extract_incident_fields(payload: Dict[str, Any] = Body(..., description="Raw incident data as a JSON object")):
    """
    Extract fields from an incident dict based on detected ticket type.

    Returns a structured dict: { success, ticket_type, missing_fields, errors, model }
    """
    try:
        from services.extraction_service import ExtractionService

        svc = ExtractionService()
        return svc.extract(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")


__all__ = ["router"]

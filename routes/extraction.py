"""Extraction-related API routes separated from `incidents.py`.

Provides endpoints that call the extraction service to map raw incident
JSON into typed ticket payloads.
"""

"""
LLM extraction routes
"""
import logging
from services.llm_service import process_incident, is_llm_available
from fastapi import APIRouter, HTTPException, Body
from typing import Any, Dict

logger = logging.getLogger(__name__)

router = APIRouter()

# router = APIRouter(prefix="/api/extract", tags=["LLM Extraction"])


@router.get("/health")
def extraction_health_check():
    """Check if LLM extraction service is available"""
    llm_status = is_llm_available()
    
    return {
        "service": "LLM Extraction Service",
        "status": "available" if llm_status else "unavailable",
        "llm_configured": llm_status,
        "message": "Service is ready" if llm_status else "OpenAI API key not configured"
    }


# Extract structured data from incident JSON
@router.post("/extract_Structured_Data_LLM")
def extract_from_json(incident_data: Dict[str, Any]):
    """Extract structured data from incident JSON"""
    
    if not is_llm_available():
        raise HTTPException(
            status_code=503,
            detail="LLM service not available. Configure OPENAI_API_KEY in .env"
        )
    
    try:
        logger.info(f"Processing incident: {incident_data.get('id', 'Unknown')}")
        extracted_data = process_incident(incident_data)
        
        return {
            "success": True,
            "message": "Data extracted successfully",
            "data": extracted_data
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=f"LLM service error: {str(e)}")
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"LLM processing error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")



@router.post("/incidents/verify_fields")
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




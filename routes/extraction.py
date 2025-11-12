"""
LLM extraction routes
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import logging

from services.llm_service import process_incident, is_llm_available

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/extract", tags=["LLM Extraction"])

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

@router.post("/from-json")
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


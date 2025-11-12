"""
LLM extraction service
"""
import os
import json
import re
from typing import Dict, Any
from pydantic import ValidationError
from openai import AzureOpenAI, APIError, APIConnectionError, APITimeoutError
import logging


from config.settings import settings
from schemas.extraction import ExtractedNotes, FlattenedIncidentResponse
 
logger = logging.getLogger(__name__)
 
# Initialize OpenAI client
try:
    client = AzureOpenAI(
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        api_key=settings.AZURE_OPENAI_API_KEY,  
        api_version=settings.AZURE_OPENAI_API_VERSION
    )
    
    if not settings.AZURE_OPENAI_API_KEY:
        logger.warning("AZURE_OPENAI_API_KEY not found. LLM functions will fail.")
        print("WARNING: AZURE_OPENAI_API_KEY not found. LLM functions will fail.")
except Exception as e:
    logger.error(f"Error initializing Azure OpenAI client: {e}")
    print(f"Error initializing Azure OpenAI client: {e}")
    client = None
 
def is_llm_available() -> bool:
    """Check if LLM is properly configured"""
    return client is not None and settings.AZURE_OPENAI_API_KEY != ""

def test_llm_connection() -> bool:
    """Test the connection to Azure OpenAI"""
    if not client:
        logger.error("Azure OpenAI client not initialized")
        return False
    
    try:
        # Simple test request
        response = client.chat.completions.create(
            model=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        logger.info("Azure OpenAI connection test successful")
        return True
    except Exception as e:
        logger.error(f"Azure OpenAI connection test failed: {e}")
        return False
 
def extract_notes_with_llm(notes_content: str) -> ExtractedNotes:
    """Extract structured data from notes using LLM"""
   
    tools = [{
        "type": "function",
        "function": {
            "name": "extract_incident_details",
            "description": "Extracts structured incident data from unstructured notes text.",
            "parameters": ExtractedNotes.model_json_schema(),
        },
    }]
 
    try:
        completion = client.chat.completions.create(
            model=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=[
                {"role": "system", "content": "You are an expert parser. Extract all details from the user's notes using the provided tool."},
                {"role": "user", "content": f"Extract data from the following incident notes:\n\n{notes_content}"}
            ],
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "extract_incident_details"}},
        )
 
        if not completion.choices or not completion.choices[0].message.tool_calls:
            raise RuntimeError("LLM did not return a tool call as required.")
 
        tool_call = completion.choices[0].message.tool_calls[0]
        if tool_call.function.name != "extract_incident_details":
            raise RuntimeError("LLM returned an unexpected tool call name.")
             
        extracted_data_json = tool_call.function.arguments
        extracted_data_dict = json.loads(extracted_data_json)
 
        return ExtractedNotes.model_validate(extracted_data_dict)
 
    except APIConnectionError as e:
        raise RuntimeError(f"OpenAI Connection Error: {str(e)}")
    except APITimeoutError as e:
        raise RuntimeError(f"OpenAI Timeout Error: {str(e)}")
    except APIError as e:
        status_code = getattr(e, 'status_code', 'Unknown')
        raise RuntimeError(f"OpenAI API Error: {status_code} - {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to process LLM output: {e}")
 
 
 
 
def process_incident(incident_data: Dict[str, Any]) -> Dict[str, Any]:
    """Process incident data and extract structured information"""
   
    if not client:
        raise ConnectionError("Azure OpenAI client not initialized. Check API key.")
 
    # Get notes content
    notes_content = incident_data.get("notes", "")
    if not notes_content:
        raise ValueError("Incident data is missing the 'notes' field.")
       
    incident_id = incident_data.get('id', incident_data.get('Id', 'Unknown'))
    logger.info(f"Processing incident: {incident_id}")
    logger.info(f"Notes content length: {len(notes_content)} characters")
   
    try:
        # Extract with LLM
        extracted_notes = extract_notes_with_llm(notes_content)
        logger.info("LLM extraction completed successfully")
    except Exception as e:
        logger.error(f"LLM extraction failed: {str(e)}")
        raise
   
    # Get top-level fields
    top_level_data = {
        "id": incident_data.get("id", "N/A"),
        "summary": incident_data.get("summary", "N/A"),
        "status": incident_data.get("status", "N/A"),
        "priority": incident_data.get("priority", "N/A"),
        "customer": incident_data.get("customer", "N/A"),
        "assigned_group": incident_data.get("assignedGroup", "N/A"),
    }
   
    # Get LLM-extracted fields
    llm_data = extracted_notes.model_dump(by_alias=False)
   
    # Extract nested user identifier
    desc_content = llm_data.get("error_description", "")
    user_id_match = re.search(r"Full User Identifier:\s*([0-9-a-zA-Z\s,;]+)", desc_content)
    full_user_id = user_id_match.group(1).strip() if user_id_match else "N/A"
   
    # Consolidate all data
    final_data = {
        **top_level_data,
        **llm_data,
        "full_user_identifier": full_user_id
    }
   
    # Validate
    try:
        FlattenedIncidentResponse.model_validate(final_data)
    except ValidationError as e:
        logger.error(f"Validation Error: {e}")
        raise
       
    logger.info(f"Successfully extracted data for incident: {top_level_data['id']}")
    return final_data
 
 
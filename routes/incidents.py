"""
API routes for incident management
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
import httpx
from config.settings import settings
from utils.auth import get_auth_headers
from models.incident import IncidentListResponse, Incident, SupportGroupListResponse

router = APIRouter()


# Helper function to make Canvas API requests
async def _make_canvas_request(url: str, params: dict = None):
    """Helper function to make requests to Canvas API with error handling"""
    headers = get_auth_headers()
    
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(url, headers=headers, params=params, timeout=30.0)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Canvas API error: {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Failed to connect to Canvas API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/incidents/all-by-support-group", response_model=IncidentListResponse)
async def get_all_incidents_by_support_group_basic(
    support_group_name: str = Query(..., description="Name of the support group to filter by")
):
    """
    1. Get All Incidents by Support Group (Basic)
    
    Retrieves all incidents assigned to a specific support group.
    This is the simplest query with just the support group filter.
    
    - **support_group_name**: The name of the support group (e.g., 'Gaming Services')
    """
    query_params = {
        "$filter": f"assignedGroup eq '{support_group_name}'"
    }
    
    url = f"{settings.CANVAS_API_BASE_URL}/incidents"
    return await _make_canvas_request(url, query_params)


@router.get("/incidents/key-fields", response_model=IncidentListResponse)
async def get_incidents_with_key_fields_only(
    support_group_name: str = Query(..., description="Name of the support group to filter by")
):
    """
    2. Get Incidents with Key Fields Only
    
    Retrieves incidents with only the most commonly needed fields to reduce response size.
    
    - **support_group_name**: The name of the support group
    
    Returns: id, summary, status, severity, assignedGroup, assignee, created, lastModified, priority, customer, notes
    """
    query_params = {
        "$filter": f"assignedGroup eq '{support_group_name}'",
        "$select": "id,summary,status,severity,assignedGroup,assignee,created,lastModified,priority,customer,notes"
    }
    
    url = f"{settings.CANVAS_API_BASE_URL}/incidents"
    return await _make_canvas_request(url, query_params)


@router.get("/incidents/sorted-by-created", response_model=IncidentListResponse)
async def get_incidents_sorted_by_created_date(
    support_group_name: str = Query(..., description="Name of the support group to filter by")
):
    """
    3. Get Incidents - Sorted by Created Date (Newest First)
    
    Retrieves incidents sorted by creation date (newest first) for better chronological viewing.
    
    - **support_group_name**: The name of the support group
    """
    query_params = {
        "$filter": f"assignedGroup eq '{support_group_name}'",
        "$orderby": "created desc",
        "$select": "id,summary,status,severity,assignedGroup,created,lastModified"
    }
    
    url = f"{settings.CANVAS_API_BASE_URL}/incidents"
    return await _make_canvas_request(url, query_params)


@router.get("/incidents/active-only", response_model=IncidentListResponse)
async def get_active_incidents_only(
    support_group_name: str = Query(..., description="Name of the support group to filter by")
):
    """
    4. Get Active Incidents Only
    
    Retrieves only active (open) incidents for the specified support group.
    
    - **support_group_name**: The name of the support group
    """
    query_params = {
        "$filter": f"assignedGroup eq '{support_group_name}' and isActive eq true",
        "$select": "id,summary,status,severity,assignedGroup,assignee,isActive,created"
    }
    
    url = f"{settings.CANVAS_API_BASE_URL}/incidents"
    return await _make_canvas_request(url, query_params)


@router.get("/incidents/paginated", response_model=IncidentListResponse)
async def get_incidents_with_pagination(
    support_group_name: str = Query(..., description="Name of the support group to filter by"),
    top: int = Query(10, description="Number of results to return", ge=1, le=1000),
    skip: int = Query(0, description="Number of results to skip", ge=0)
):
    """
    5. Get Incidents with Pagination (First N)
    
    Retrieves incidents with pagination support. Useful for large datasets.
    
    - **support_group_name**: The name of the support group
    - **top**: Number of results to return (default: 10)
    - **skip**: Number of results to skip (default: 0)
    """
    query_params = {
        "$filter": f"assignedGroup eq '{support_group_name}'",
        "$top": top,
        "$skip": skip,
        "$select": "id,summary,status,assignedGroup,created"
    }
    
    url = f"{settings.CANVAS_API_BASE_URL}/incidents"
    return await _make_canvas_request(url, query_params)


@router.get("/incidents/count-only")
async def get_incidents_count_only(
    support_group_name: str = Query(..., description="Name of the support group to filter by")
):
    """
    6. Get Incidents Count Only
    
    Gets only the count of incidents for the support group without returning the actual data.
    
    - **support_group_name**: The name of the support group
    """
    query_params = {
        "$filter": f"assignedGroup eq '{support_group_name}'",
        "$count": "true",
        "$top": 0
    }
    
    url = f"{settings.CANVAS_API_BASE_URL}/incidents"
    return await _make_canvas_request(url, query_params)


@router.get("/incidents/high-priority", response_model=IncidentListResponse)
async def get_high_priority_incidents(
    support_group_name: str = Query(..., description="Name of the support group to filter by")
):
    """
    7. Get High Priority Incidents
    
    Retrieves only high priority or high severity incidents for the support group.
    Filters for: Priority = High/Critical OR Severity = Severity A/Severity B
    
    - **support_group_name**: The name of the support group
    """
    query_params = {
        "$filter": f"assignedGroup eq '{support_group_name}' and (priority eq 'High' or priority eq 'Critical' or severity eq 'Severity A' or severity eq 'Severity B')",
        "$select": "id,summary,status,priority,severity,assignedGroup,created"
    }
    
    url = f"{settings.CANVAS_API_BASE_URL}/incidents"
    return await _make_canvas_request(url, query_params)


@router.get("/incidents/{incident_id}", response_model=Incident)
async def get_specific_incident_by_id(incident_id: str):
    """
    8. Get Specific Incident by ID
    
    Retrieves a specific incident by its ID.
    
    - **incident_id**: The unique identifier of the incident (e.g., 'INC123456')
    """
    url = f"{settings.CANVAS_API_BASE_URL}/incidents('{incident_id}')"
    
    try:
        return await _make_canvas_request(url)
    except HTTPException as e:
        if e.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")
        raise


@router.get("/support-groups/all", response_model=SupportGroupListResponse)
async def get_all_available_support_groups():
    """
    9. Get All Available Support Groups
    
    Retrieves all available support groups to help you find the correct group name 
    to use in incident filters.
    """
    url = f"{settings.CANVAS_API_BASE_URL}/supportGroups"
    return await _make_canvas_request(url)


@router.get("/support-groups/unique-from-incidents")
async def get_unique_support_groups_from_incidents(
    top: int = Query(1000, description="Number of incidents to check", ge=1, le=10000)
):
    """
    10. Get Unique Support Groups from Incidents
    
    Gets a list of all support groups that currently have incidents assigned.
    This extracts unique support group names from the incident data.
    Use this to find valid support group names.
    
    - **top**: Number of incidents to retrieve for analysis (default: 1000)
    """
    query_params = {
        "$select": "assignedGroup",
        "$top": top
    }
    
    url = f"{settings.CANVAS_API_BASE_URL}/incidents"
    data = await _make_canvas_request(url, query_params)
    
    # Extract unique support groups
    unique_groups = list(set([incident.get("assignedGroup") for incident in data.get("value", []) if incident.get("assignedGroup")]))
    
    return {
        "unique_support_groups": sorted(unique_groups),
        "count": len(unique_groups),
        "total_incidents_checked": len(data.get("value", []))
    }


# Additional flexible endpoint for custom queries
@router.get("/incidents/custom", response_model=IncidentListResponse)
async def get_incidents_custom(
    support_group: Optional[str] = Query(None, description="Filter by support group name"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    priority: Optional[str] = Query(None, description="Filter by priority (High, Critical, etc.)"),
    severity: Optional[str] = Query(None, description="Filter by severity (Severity A, Severity B, etc.)"),
    status: Optional[str] = Query(None, description="Filter by status"),
    top: Optional[int] = Query(None, description="Limit number of results", ge=1, le=1000),
    skip: Optional[int] = Query(None, description="Skip number of results", ge=0),
    orderby: Optional[str] = Query(None, description="Order by field (e.g., 'created desc')"),
    count: Optional[bool] = Query(None, description="Include count in response"),
    select: Optional[str] = Query(None, description="Comma-separated list of fields to select")
):
    """
    Custom Flexible Query Endpoint
    
    Get incidents from Canvas Queue API with fully customizable filters.
    This endpoint allows you to combine multiple filters and options.
    
    - **support_group**: Filter incidents by support group name
    - **is_active**: Filter by active/inactive status
    - **priority**: Filter by priority level
    - **severity**: Filter by severity level
    - **status**: Filter by status
    - **top**: Limit number of results (pagination)
    - **skip**: Skip number of results (pagination)
    - **orderby**: Sort results (e.g., 'created desc', 'priority asc')
    - **count**: Include total count in response
    - **select**: Specific fields to return (e.g., 'id,summary,status')
    """
    query_params = {}
    filter_parts = []
    
    # Build filter expression
    if support_group:
        filter_parts.append(f"assignedGroup eq '{support_group}'")
    
    if is_active is not None:
        filter_parts.append(f"isActive eq {str(is_active).lower()}")
    
    if priority:
        filter_parts.append(f"priority eq '{priority}'")
    
    if severity:
        filter_parts.append(f"severity eq '{severity}'")
    
    if status:
        filter_parts.append(f"status eq '{status}'")
    
    if filter_parts:
        query_params["$filter"] = " and ".join(filter_parts)
    
    # Add other OData parameters
    if top is not None:
        query_params["$top"] = top
    
    if skip is not None:
        query_params["$skip"] = skip
    
    if orderby:
        query_params["$orderby"] = orderby
    
    if count:
        query_params["$count"] = "true"
    
    if select:
        query_params["$select"] = select
    
    url = f"{settings.CANVAS_API_BASE_URL}/incidents"
    return await _make_canvas_request(url, query_params)

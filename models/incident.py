"""
Pydantic models for Canvas API responses
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime


class Incident(BaseModel):
    """Model for an individual incident with all Canvas API fields"""
    # Core identifiers
    entityType: Optional[str] = None
    id: str
    requestId: Optional[str] = None
    entryId: Optional[str] = None
    instanceId: Optional[str] = None
    
    # Status and activity
    isActive: Optional[bool] = None
    status: Optional[str] = None
    statusReason: Optional[str] = None
    isEscalated: Optional[bool] = None
    
    # Summary and descriptions
    summary: Optional[str] = None
    notes: Optional[str] = None
    assigneeNotes: Optional[str] = None
    location: Optional[str] = None
    
    # Assignment
    assignedGroup: Optional[str] = None
    assignedRemedyGroupId: Optional[str] = None
    assignee: Optional[str] = None
    assigneeUsername: Optional[str] = None
    supportGroupRole: Optional[str] = None
    
    # Organization
    company: Optional[str] = None
    organization: Optional[str] = None
    site: Optional[str] = None
    
    # Priority and severity
    severity: Optional[str] = None
    severityReason: Optional[str] = None
    priority: Optional[str] = None
    urgency: Optional[str] = None
    slmStatus: Optional[str] = None
    slaResponded: Optional[int] = None
    
    # Dates and timestamps
    created: Optional[str] = None
    createdInSeconds: Optional[int] = None
    lastModified: Optional[str] = None
    lastModifiedInSeconds: Optional[int] = None
    lastModifiedBy: Optional[str] = None
    taskedOut: Optional[Any] = None  # Can be string or boolean
    taskedOutReturned: Optional[Any] = None  # Can be string or boolean
    
    # Submitter information
    submitter: Optional[str] = None
    submitterUsername: Optional[str] = None
    
    # Customer and operator information
    customer: Optional[str] = None
    customerTelephone: Optional[str] = None
    operator: Optional[str] = None
    operatorId: Optional[int] = None
    operatorStatus: Optional[str] = None
    brandName: Optional[str] = None
    
    # Product and service details
    product: Optional[str] = None
    market: Optional[str] = None
    channel: Optional[str] = None
    serviceCategory: Optional[str] = None
    serviceCategoryTier1: Optional[str] = None
    serviceCategoryTier2: Optional[str] = None
    serviceCategoryTier3: Optional[str] = None
    
    # Product categorization
    productCategorizationTier1: Optional[str] = None
    productCategorizationTier2: Optional[str] = None
    productCategorizationTier3: Optional[str] = None
    operationalCategory: Optional[str] = None
    serialNo: Optional[str] = None
    
    # Resolution details
    resolutionMethod: Optional[str] = None
    primaryRootCause: Optional[str] = None
    detailedRootCause: Optional[str] = None
    resolutionNotes: Optional[str] = None
    
    # Tasks
    tasksTotalCount: Optional[int] = None
    tasksActiveCount: Optional[int] = None
    scomTask: Optional[bool] = None
    
    # Contact preferences
    preferredContactDetails: Optional[str] = None
    preferredContactType: Optional[str] = None
    timeZone: Optional[str] = None
    
    # Status flags
    inIcu: Optional[bool] = None
    
    class Config:
        # Allow extra fields that might be added by the API
        extra = "allow"


class IncidentListResponse(BaseModel):
    """Model for the OData incident list response"""
    value: List[Incident]
    odata_count: Optional[int] = Field(None, alias="@odata.count")
    odata_nextLink: Optional[str] = Field(None, alias="@odata.nextLink")
    
    class Config:
        populate_by_name = True


class SupportGroup(BaseModel):
    """Model for a support group"""
    id: Optional[str] = None
    supportGroupName: str
    company: Optional[str] = None
    supportOrganization: Optional[str] = None
    supportGroupRole: Optional[str] = None
    deR_INCResolved: Optional[bool] = None
    
    class Config:
        # Allow extra fields that might be added by the API
        extra = "allow"


class SupportGroupListResponse(BaseModel):
    """Model for the OData support group list response"""
    value: List[SupportGroup]
    odata_count: Optional[int] = Field(None, alias="@odata.count")
    
    class Config:
        populate_by_name = True

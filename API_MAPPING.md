# API Endpoints Mapping - Postman Collection to FastAPI

This document maps each Postman collection request to the corresponding FastAPI endpoint.

## Endpoint Mapping

| # | Postman Collection Name | FastAPI Endpoint | Method |
|---|------------------------|------------------|--------|
| 1 | Get All Incidents by Support Group (Basic) | `/api/incidents/all-by-support-group` | GET |
| 2 | Get Incidents with Key Fields Only | `/api/incidents/key-fields` | GET |
| 3 | Get Incidents - Sorted by Created Date | `/api/incidents/sorted-by-created` | GET |
| 4 | Get Active Incidents Only | `/api/incidents/active-only` | GET |
| 5 | Get Incidents with Pagination (First 10) | `/api/incidents/paginated` | GET |
| 6 | Get Incidents Count Only | `/api/incidents/count-only` | GET |
| 7 | Get High Priority Incidents | `/api/incidents/high-priority` | GET |
| 8 | Get Specific Incident by ID | `/api/incidents/{incident_id}` | GET |
| 9 | Get All Available Support Groups | `/api/support-groups/all` | GET |
| 10 | Get Unique Support Groups from Incidents | `/api/support-groups/unique-from-incidents` | GET |
| 11 | Custom Flexible Query (Bonus) | `/api/incidents/custom` | GET |

---

## Detailed Examples

### 1. Get All Incidents by Support Group (Basic)

**Postman:**
```
{{base_url}}/incidents?$filter=assignedGroup eq '{{support_group_name}}'
```

**FastAPI:**
```
GET http://localhost:8000/api/incidents/all-by-support-group?support_group_name=Gaming%20Services
```

---

### 2. Get Incidents with Key Fields Only

**Postman:**
```
{{base_url}}/incidents?$filter=assignedGroup eq '{{support_group_name}}'&$select=id,summary,status,severity,assignedGroup,assignee,created,lastModified,priority,customer,notes
```

**FastAPI:**
```
GET http://localhost:8000/api/incidents/key-fields?support_group_name=Gaming%20Services
```

---

### 3. Get Incidents - Sorted by Created Date

**Postman:**
```
{{base_url}}/incidents?$filter=assignedGroup eq '{{support_group_name}}'&$orderby=created desc&$select=id,summary,status,severity,assignedGroup,created,lastModified
```

**FastAPI:**
```
GET http://localhost:8000/api/incidents/sorted-by-created?support_group_name=Gaming%20Services
```

---

### 4. Get Active Incidents Only

**Postman:**
```
{{base_url}}/incidents?$filter=assignedGroup eq '{{support_group_name}}' and isActive eq true&$select=id,summary,status,severity,assignedGroup,assignee,isActive,created
```

**FastAPI:**
```
GET http://localhost:8000/api/incidents/active-only?support_group_name=Gaming%20Services
```

---

### 5. Get Incidents with Pagination

**Postman:**
```
{{base_url}}/incidents?$filter=assignedGroup eq '{{support_group_name}}'&$top=10&$skip=0&$select=id,summary,status,assignedGroup,created
```

**FastAPI:**
```
GET http://localhost:8000/api/incidents/paginated?support_group_name=Gaming%20Services&top=10&skip=0
```

**For page 2:**
```
GET http://localhost:8000/api/incidents/paginated?support_group_name=Gaming%20Services&top=10&skip=10
```

---

### 6. Get Incidents Count Only

**Postman:**
```
{{base_url}}/incidents?$filter=assignedGroup eq '{{support_group_name}}'&$count=true&$top=0
```

**FastAPI:**
```
GET http://localhost:8000/api/incidents/count-only?support_group_name=Gaming%20Services
```

---

### 7. Get High Priority Incidents

**Postman:**
```
{{base_url}}/incidents?$filter=assignedGroup eq '{{support_group_name}}' and (priority eq 'High' or priority eq 'Critical' or severity eq 'Severity A' or severity eq 'Severity B')&$select=id,summary,status,priority,severity,assignedGroup,created
```

**FastAPI:**
```
GET http://localhost:8000/api/incidents/high-priority?support_group_name=Gaming%20Services
```

---

### 8. Get Specific Incident by ID

**Postman:**
```
{{base_url}}/incidents('{{incident_id}}')
```

**FastAPI:**
```
GET http://localhost:8000/api/incidents/INC123456
```

---

### 9. Get All Available Support Groups

**Postman:**
```
{{base_url}}/supportGroups
```

**FastAPI:**
```
GET http://localhost:8000/api/support-groups/all
```

---

### 10. Get Unique Support Groups from Incidents

**Postman:**
```
{{base_url}}/incidents?$select=assignedGroup&$top=1000
```

**FastAPI:**
```
GET http://localhost:8000/api/support-groups/unique-from-incidents?top=1000
```

**Response includes:**
```json
{
  "unique_support_groups": ["Gaming Services", "Network Support", "..."],
  "count": 15,
  "total_incidents_checked": 1000
}
```

---

### 11. Custom Flexible Query (Bonus)

This is an additional endpoint that provides maximum flexibility:

**FastAPI:**
```
GET http://localhost:8000/api/incidents/custom?support_group=Gaming%20Services&is_active=true&priority=High&severity=Severity%20A&orderby=created%20desc&top=20&count=true&select=id,summary,status,priority
```

---

## Testing with cURL

### Example 1: Get all incidents for Gaming Services
```bash
curl -X GET "http://localhost:8000/api/incidents/all-by-support-group?support_group_name=Gaming%20Services"
```

### Example 2: Get active incidents only
```bash
curl -X GET "http://localhost:8000/api/incidents/active-only?support_group_name=Gaming%20Services"
```

### Example 3: Get specific incident
```bash
curl -X GET "http://localhost:8000/api/incidents/INC123456"
```

### Example 4: Get high priority incidents
```bash
curl -X GET "http://localhost:8000/api/incidents/high-priority?support_group_name=Gaming%20Services"
```

### Example 5: Get incident count
```bash
curl -X GET "http://localhost:8000/api/incidents/count-only?support_group_name=Gaming%20Services"
```

---

## Key Differences

1. **Cleaner URLs**: FastAPI endpoints use descriptive paths instead of complex OData query strings
2. **Required Parameters**: Some endpoints have required query parameters (like `support_group_name`)
3. **Better Documentation**: Each endpoint is self-documenting via Swagger UI at `/docs`
4. **Type Safety**: Query parameters are validated and typed automatically
5. **Error Handling**: Consistent error responses across all endpoints

---

## Interactive Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These provide interactive API testing directly in your browser!

# Canvas Queue API - FastAPI Server

A simple, modular FastAPI server to interact with the Canvas Queue API.

## Project Structure

```
Ticket Automation/
├── config/
│   └── settings.py          # Configuration and environment variables
├── models/
│   └── incident.py          # Pydantic models for API responses
├── routes/
│   └── incidents.py         # API route handlers for incidents
├── utils/
│   └── auth.py              # Authentication utilities
├── .env                     # Environment variables (not in git)
├── .gitignore              
├── main.py                  # FastAPI application entry point
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Features

- ✅ Modular structure with separate folders for routes, models, config, and utils
- ✅ No `__init__.py` files required in folders
- ✅ Bearer token authentication from environment variables
- ✅ Integration with Canvas Queue API at `https://queues.canvas.mgsops.net:8020`
- ✅ Multiple endpoints for incident management
- ✅ OData query support (filtering, sorting, pagination)

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Edit the `.env` file and update the `CANVAS_BEARER_TOKEN` with your actual JWT token:

**IMPORTANT:** Do NOT include the word "Bearer" in the token value. The application adds it automatically.

```env
CANVAS_API_BASE_URL=https://queues.canvas.mgsops.net:8020
CANVAS_BEARER_TOKEN=eyJraWQiOiI4MVZsTmpXTGp5...  (just the token, no "Bearer" prefix)

HOST=0.0.0.0
PORT=8000
```

### 3. Run the Server

```bash
python main.py
```

Or use uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Root Endpoints

- **GET /** - Server information
- **GET /health** - Health check

### Incident Endpoints

All incident endpoints are prefixed with `/api`:

#### 1. Get All Incidents by Support Group (Basic)
```
GET /api/incidents/all-by-support-group?support_group_name={name}
```

The simplest query - retrieves all incidents for a specific support group.

**Query Parameters:**
- `support_group_name` (required) - Name of the support group

**Example:**
```
GET /api/incidents/all-by-support-group?support_group_name=Gaming%20Services
```

---

#### 2. Get Incidents with Key Fields Only
```
GET /api/incidents/key-fields?support_group_name={name}
```

Returns incidents with only essential fields to reduce response size.

**Query Parameters:**
- `support_group_name` (required) - Name of the support group

**Returned Fields:** id, summary, status, severity, assignedGroup, assignee, created, lastModified, priority, customer, notes

**Example:**
```
GET /api/incidents/key-fields?support_group_name=Gaming%20Services
```

---

#### 3. Get Incidents Sorted by Created Date (Newest First)
```
GET /api/incidents/sorted-by-created?support_group_name={name}
```

Returns incidents sorted by creation date in descending order.

**Query Parameters:**
- `support_group_name` (required) - Name of the support group

**Example:**
```
GET /api/incidents/sorted-by-created?support_group_name=Gaming%20Services
```

---

#### 4. Get Active Incidents Only
```
GET /api/incidents/active-only?support_group_name={name}
```

Returns only active (open) incidents for the support group.

**Query Parameters:**
- `support_group_name` (required) - Name of the support group

**Example:**
```
GET /api/incidents/active-only?support_group_name=Gaming%20Services
```

---

#### 5. Get Incidents with Pagination
```
GET /api/incidents/paginated?support_group_name={name}&top={n}&skip={n}
```

Returns paginated results - useful for large datasets.

**Query Parameters:**
- `support_group_name` (required) - Name of the support group
- `top` (optional, default: 10) - Number of results to return (1-1000)
- `skip` (optional, default: 0) - Number of results to skip

**Example:**
```
GET /api/incidents/paginated?support_group_name=Gaming%20Services&top=10&skip=0
```

---

#### 6. Get Incidents Count Only
```
GET /api/incidents/count-only?support_group_name={name}
```

Returns only the count of incidents without the actual data.

**Query Parameters:**
- `support_group_name` (required) - Name of the support group

**Example:**
```
GET /api/incidents/count-only?support_group_name=Gaming%20Services
```

---

#### 7. Get High Priority Incidents
```
GET /api/incidents/high-priority?support_group_name={name}
```

Returns only high priority or critical severity incidents.
Filters: Priority = High/Critical OR Severity = Severity A/Severity B

**Query Parameters:**
- `support_group_name` (required) - Name of the support group

**Example:**
```
GET /api/incidents/high-priority?support_group_name=Gaming%20Services
```

---

#### 8. Get Specific Incident by ID
```
GET /api/incidents/{incident_id}
```

Retrieves a single incident by its unique identifier.

**Path Parameters:**
- `incident_id` - The unique incident ID (e.g., INC123456)

**Example:**
```
GET /api/incidents/INC123456
```

---

#### 9. Get All Available Support Groups
```
GET /api/support-groups/all
```

Returns all available support groups in the system.

**Example:**
```
GET /api/support-groups/all
```

---

#### 10. Get Unique Support Groups from Incidents
```
GET /api/support-groups/unique-from-incidents?top={n}
```

Extracts unique support group names from incident data.

**Query Parameters:**
- `top` (optional, default: 1000) - Number of incidents to analyze (1-10000)

**Example:**
```
GET /api/support-groups/unique-from-incidents?top=1000
```

---

#### 11. Custom Flexible Query (Advanced)
```
GET /api/incidents/custom
```

Fully customizable endpoint with all available filters and options.

**Query Parameters:**
- `support_group` - Filter by support group name
- `is_active` - Filter by active status (true/false)
- `priority` - Filter by priority level (e.g., High, Critical)
- `severity` - Filter by severity (e.g., Severity A, Severity B)
- `status` - Filter by status
- `top` - Limit results (1-1000)
- `skip` - Skip results (pagination)
- `orderby` - Sort results (e.g., "created desc", "priority asc")
- `count` - Include total count (true/false)
- `select` - Comma-separated fields to return

**Example:**
```
GET /api/incidents/custom?support_group=Gaming%20Services&is_active=true&priority=High&orderby=created%20desc&top=20
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Authentication

The server uses Bearer token authentication. The `get_auth_headers()` function in `utils/auth.py` automatically includes the token from environment variables in all Canvas API requests.

### Future Enhancement

The `get_auth_token()` function in `utils/auth.py` is designed to be extended. You can modify it to:
- Implement token refresh logic
- Fetch tokens from external auth services
- Add token caching mechanisms

## Canvas API Integration

The server calls the Canvas Queue API with:
- **Base URL**: `https://queues.canvas.mgsops.net:8020`
- **Authentication**: Bearer token in header
- **SSL Verification**: Disabled (for self-signed certificates)

All Canvas API requests include:
```
Authorization: Bearer {token}
Accept: application/json
Content-Type: application/json
```

## Development Notes

- The server uses `httpx.AsyncClient` for async HTTP requests
- SSL verification is disabled (`verify=False`) to handle self-signed certificates
- Error handling includes specific messages for connection failures and API errors
- OData query parameters are fully supported for filtering and sorting

## Example Usage

### Using curl

```bash
# Get all incidents for a support group
curl -X GET "http://localhost:8000/api/incidents?support_group=Gaming%20Services"

# Get a specific incident
curl -X GET "http://localhost:8000/api/incidents/INC123456"

# Get support groups
curl -X GET "http://localhost:8000/api/support-groups"
```

### Using Python requests

```python
import requests

# Get incidents
response = requests.get(
    "http://localhost:8000/api/incidents",
    params={"support_group": "Gaming Services", "is_active": True}
)
print(response.json())
```

## Troubleshooting

1. **Connection Error**: Ensure the Canvas API base URL is correct and accessible
2. **Authentication Error**: Verify the Bearer token in `.env` is valid
3. **SSL Error**: The server handles self-signed certificates, but if issues persist, check network/firewall settings

## License

MIT

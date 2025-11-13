# Canvas Queue API Integration & Ticket Automation

A comprehensive FastAPI-based service that integrates with Canvas Queue API to manage incidents and provides AI-powered ticket data extraction capabilities using Azure OpenAI.

## 🚀 Features

### Canvas API Integration
- **Incident Management**: Comprehensive incident retrieval with multiple filtering options
- **Support Group Management**: Query and manage support groups
- **Flexible Querying**: Custom filters for priority, status, severity, and pagination
- **Automated Authentication**: Okta OAuth2 integration with token caching

### AI-Powered Data Extraction
- **LLM Processing**: Extract structured data from unstructured incident notes
- **Azure OpenAI Integration**: Uses GPT-4o for intelligent text parsing
- **Structured Output**: Converts free-text incident notes into structured JSON data
- **Validation**: Pydantic schemas ensure data integrity

## 📋 Prerequisites

- Python 3.8+
- Canvas Queue API access
- Okta authentication credentials
- Azure OpenAI API key (for LLM features)

## 🏗️ Project Structure

```
Ticket Automation/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Project dependencies
├── README.md              # Project documentation
├── config/
│   └── settings.py        # Configuration management
├── routes/
│   ├── incidents.py       # Canvas API incident endpoints
│   └── extraction.py      # LLM extraction endpoints
├── services/
│   └── llm_service.py     # Azure OpenAI integration
├── utils/
│   └── auth.py           # Authentication utilities
├── models/
│   └── incident.py       # Incident data models
├── schemas/
│   └── extraction.py     # Data extraction schemas
└── __pycache__/          # Python cache files
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Canvas API Configuration
CANVAS_API_BASE_URL=https://queues.canvas.mgsops.net:8020
CANVAS_BEARER_TOKEN=  # Optional: Use this OR Okta auth below

# Okta Authentication (required if CANVAS_BEARER_TOKEN not set)
OKTA_TOKEN_URL=https://derivco.okta-emea.com/oauth2/default/v1/token
OKTA_BASIC_AUTH=<Auth_Token>
OKTA_USERNAME=<Your_Username>
OKTA_PASSWORD=<Your_Okta_Password>
OKTA_SCOPE=

# Azure OpenAI Configuration (for LLM features)
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2024-05-01-preview

# OpenAI Configuration (fallback/alternative)
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini

# Server Configuration
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

## 🚀 Running the Application

1. **Start the server**
   ```bash
   python main.py
   ```
   or
   ```bash
   uvicorn main:app --reload
   ```

2. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc
   - Health check: http://localhost:8000/health

## 📚 API Endpoints

### Incident Management (`/api/incidents/`)

| Endpoint | Description |
|----------|-------------|
| `GET /incidents/all-by-support-group` | Get all incidents by support group |
| `GET /incidents/key-fields` | Get incidents with essential fields only |
| `GET /incidents/sorted-by-created` | Get incidents sorted by creation date |
| `GET /incidents/active-only` | Get only active incidents |
| `GET /incidents/paginated` | Get incidents with pagination |
| `GET /incidents/count-only` | Get incident count only |
| `GET /incidents/high-priority` | Get high priority/severity incidents |
| `GET /incidents/{incident_id}` | Get specific incident by ID |
| `GET /incidents/custom` | Flexible custom query endpoint |

### Support Groups

| Endpoint | Description |
|----------|-------------|
| `GET /support-groups/all` | Get all available support groups |
| `GET /support-groups/unique-from-incidents` | Get unique support groups from incidents |

### LLM Data Extraction (`/api/extract/`)

| Endpoint | Description |
|----------|-------------|
| `GET /extract/health` | Check LLM service availability |
| `POST /extract/from-json` | Extract structured data from incident JSON |

## 🔧 Usage Examples

### Get Incidents by Support Group
```bash
curl "http://localhost:8000/api/incidents/all-by-support-group?support_group_name=Gaming Services"
```

### Get High Priority Incidents
```bash
curl "http://localhost:8000/api/incidents/high-priority?support_group_name=Gaming Services"
```

### Extract Data from Incident
```bash
curl -X POST "http://localhost:8000/api/extract/from-json" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "INC123456",
    "notes": "Customer Reference: CUST001\nUrgency: High\nPlayer Login: player123..."
  }'
```

### Detailed Endpoint Documentation

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

## 🔐 Authentication

The application supports two authentication methods:

### 1. Direct Bearer Token
Set `CANVAS_BEARER_TOKEN` in your environment variables.

### 2. Okta OAuth2 (Recommended)
Configure Okta credentials in environment variables. The system will:
- Automatically fetch access tokens from Okta
- Cache tokens until expiry
- Handle token refresh transparently

## 🤖 LLM Data Extraction

The system uses Azure OpenAI to extract structured data from unstructured incident notes:

### Extracted Fields
- Customer Reference
- Urgency Level
- Affected Market
- Related To
- Assistance Needed
- Player Login
- Round ID
- Round Date (UTC)
- Game Name + Variant
- Casino ID
- Error Description
- Full User Identifier

### Configuration
- Uses GPT-4o model via Azure OpenAI
- Implements function calling for structured output
- Includes validation and error handling

## 🧪 Testing

### Test Authentication
```bash
python -c "from utils.auth import get_auth_token; print(get_auth_token())"
```

### Test LLM Service
```bash
curl "http://localhost:8000/api/extract/health"
```

## 📝 Development

### Adding New Endpoints
1. Add route functions to appropriate files in `routes/`
2. Update models in `models/` if needed
3. Add validation schemas in `schemas/`

### Environment Setup
- Use `.env` file for local development
- Set environment variables in production
- Never commit sensitive credentials to version control

## 🔍 Troubleshooting

### Common Issues

1. **"OpenAI Connection Error"**
   - Check Azure OpenAI credentials
   - Verify network connectivity
   - Ensure API endpoint is correct

2. **"Canvas API error"**
   - Verify Canvas API base URL
   - Check authentication credentials
   - Ensure proper network access

3. **"Token fetch failed"**
   - Verify Okta credentials
   - Check network connectivity to Okta
   - Ensure proper base64 encoding of client credentials

### Debugging
- Enable debug logging by setting log level to DEBUG
- Check `/health` and `/api/extract/health` endpoints
- Review error messages in console output

## 📄 License

This project is for internal use by Derivco/Zensar teams.

## 🤝 Contributing

1. Create feature branches from `main`
2. Follow existing code style and patterns
3. Add appropriate error handling and logging
4. Update documentation as needed

## 📞 Support

For support and questions, contact the development team or refer to the API documentation at `/docs` when the server is running.

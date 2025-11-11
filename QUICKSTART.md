# Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Your Token
Edit the `.env` file and add your Canvas API Bearer token:

**IMPORTANT:** Only paste the token itself, NOT the word "Bearer"

```env
CANVAS_BEARER_TOKEN=eyJraWQiOiI4MVZsTmpXTGp5...
```

❌ Wrong:
```env
CANVAS_BEARER_TOKEN=Bearer eyJraWQiOiI4MVZsTmpXTGp5...
```

✅ Correct:
```env
CANVAS_BEARER_TOKEN=eyJraWQiOiI4MVZsTmpXTGp5...
```

### Step 3: Run the Server
```bash
python main.py
```

The server will start at: **http://localhost:8000**

---

## 📚 Quick API Reference

All endpoints are prefixed with `/api`

### Most Common Endpoints

| Purpose | Endpoint | Example |
|---------|----------|---------|
| Get all incidents for a support group | `GET /api/incidents/all-by-support-group` | `?support_group_name=Gaming Services` |
| Get active incidents only | `GET /api/incidents/active-only` | `?support_group_name=Gaming Services` |
| Get high priority incidents | `GET /api/incidents/high-priority` | `?support_group_name=Gaming Services` |
| Get specific incident | `GET /api/incidents/{id}` | `/api/incidents/INC123456` |
| Get paginated results | `GET /api/incidents/paginated` | `?support_group_name=Gaming Services&top=10&skip=0` |
| Get all support groups | `GET /api/support-groups/all` | - |

---

## 🧪 Testing Your API

### Option 1: Interactive Swagger UI
Open in browser: **http://localhost:8000/docs**

- Click on any endpoint
- Click "Try it out"
- Fill in parameters
- Click "Execute"

### Option 2: Using cURL
```bash
# Get all incidents for Gaming Services
curl "http://localhost:8000/api/incidents/all-by-support-group?support_group_name=Gaming%20Services"

# Get a specific incident
curl "http://localhost:8000/api/incidents/INC123456"

# Get high priority incidents
curl "http://localhost:8000/api/incidents/high-priority?support_group_name=Gaming%20Services"
```

### Option 3: Using Python
```python
import requests

# Get active incidents
response = requests.get(
    "http://localhost:8000/api/incidents/active-only",
    params={"support_group_name": "Gaming Services"}
)

data = response.json()
print(f"Found {len(data['value'])} active incidents")
```

---

## 📋 All Available Endpoints

1. **GET /api/incidents/all-by-support-group** - Basic query for all incidents
2. **GET /api/incidents/key-fields** - Get incidents with essential fields only
3. **GET /api/incidents/sorted-by-created** - Get incidents sorted by creation date
4. **GET /api/incidents/active-only** - Get only active incidents
5. **GET /api/incidents/paginated** - Get paginated results
6. **GET /api/incidents/count-only** - Get just the count
7. **GET /api/incidents/high-priority** - Get high priority/severity incidents
8. **GET /api/incidents/{id}** - Get specific incident by ID
9. **GET /api/support-groups/all** - Get all support groups
10. **GET /api/support-groups/unique-from-incidents** - Get unique groups from incidents
11. **GET /api/incidents/custom** - Flexible custom query with all filters

---

## 🔍 Finding Your Support Group Name

Don't know your support group name? Use these endpoints:

```bash
# Get all available support groups
curl "http://localhost:8000/api/support-groups/all"

# Or get unique groups from incidents
curl "http://localhost:8000/api/support-groups/unique-from-incidents"
```

---

## 📖 Documentation

- **Full Documentation**: See [README.md](README.md)
- **API Mapping**: See [API_MAPPING.md](API_MAPPING.md) for Postman → FastAPI mapping
- **Interactive Docs**: http://localhost:8000/docs (when server is running)

---

## 🐛 Troubleshooting

### Server won't start?
- Check if port 8000 is available
- Verify all dependencies are installed: `pip install -r requirements.txt`

### Getting authentication errors?
- Verify your Bearer token in `.env` is correct
- Token should not have quotes around it in the `.env` file

### Can't connect to Canvas API?
- Check the base URL in `.env`: `https://queues.canvas.mgsops.net:8020`
- Verify you have network access to the Canvas API
- Check if firewall is blocking the connection

---

## 💡 Tips

1. **Use Swagger UI** (http://localhost:8000/docs) for testing - it's interactive!
2. **URL encode spaces** in support group names: `Gaming Services` → `Gaming%20Services`
3. **Use pagination** for large result sets to avoid timeouts
4. **Check the count first** before fetching all records using `/count-only` endpoint

---

## 📝 Example Workflow

```bash
# 1. Start the server
python main.py

# 2. In another terminal, find available support groups
curl "http://localhost:8000/api/support-groups/unique-from-incidents"

# 3. Get active incidents for your group
curl "http://localhost:8000/api/incidents/active-only?support_group_name=Gaming%20Services"

# 4. Get high priority incidents
curl "http://localhost:8000/api/incidents/high-priority?support_group_name=Gaming%20Services"
```

---

## 🎉 You're Ready!

The server is now ready to use. Visit http://localhost:8000/docs to explore all endpoints interactively!

# Common Issues and Solutions

## 🔴 401 Unauthorized Error

### Problem
```json
{
  "detail": "Canvas API error: Authorization has been denied for this request."
}
```

### ✅ Solution
This happens when the Bearer token is incorrectly formatted. The most common mistake is including "Bearer" in the `.env` file.

**Check your `.env` file:**

❌ **WRONG:**
```env
CANVAS_BEARER_TOKEN=Bearer eyJraWQiOiI4MVZsTmpXTGp5...
```

✅ **CORRECT:**
```env
CANVAS_BEARER_TOKEN=eyJraWQiOiI4MVZsTmpXTGp5...
```

**Why?** The `get_auth_headers()` function already adds "Bearer" prefix:
```python
return {
    "Authorization": f"Bearer {token}",  # <-- "Bearer" is added here
    ...
}
```

If you include "Bearer" in the `.env` file, it becomes: `Authorization: Bearer Bearer eyJ...` which is invalid.

---

## 🔴 Token Expired Error

### Problem
Getting 401 errors even with correct token format.

### ✅ Solution
JWT tokens expire. Check the `exp` field in your token:
- Your token expires at: `1762771287` (Unix timestamp)
- That's approximately: **November 10, 2025**

**Get a new token from:**
1. Postman (if it's generating tokens automatically)
2. Your authentication service
3. Okta (based on your token issuer: `derivco.okta-emea.com`)

---

## 🔴 Server Won't Start

### Problem
```
Address already in use
```

### ✅ Solution
Port 8000 is already in use. Either:

**Option 1:** Change the port in `.env`:
```env
PORT=8001
```

**Option 2:** Kill the process using port 8000:
```powershell
# PowerShell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process

# Or
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## 🔴 Module Not Found Error

### Problem
```
ModuleNotFoundError: No module named 'fastapi'
```

### ✅ Solution
Dependencies not installed. Run:
```bash
pip install -r requirements.txt
```

If you're using a virtual environment:
```bash
# Create venv
python -m venv venv

# Activate venv (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

---

## 🔴 SSL Certificate Error

### Problem
```
SSL: CERTIFICATE_VERIFY_FAILED
```

### ✅ Solution
The code already handles this with `verify=False` in the httpx client:
```python
async with httpx.AsyncClient(verify=False) as client:
```

This is needed for self-signed certificates. If you still get SSL errors, check:
1. Network/firewall settings
2. Proxy settings
3. VPN connection

---

## 🔴 Connection Timeout

### Problem
```
Failed to connect to Canvas API: timeout
```

### ✅ Solution
1. **Check the base URL** in `.env`:
   ```env
   CANVAS_API_BASE_URL=https://queues.canvas.mgsops.net:8020
   ```

2. **Verify network access:**
   ```powershell
   # Test connection
   Test-NetConnection queues.canvas.mgsops.net -Port 8020
   ```

3. **Check if behind a firewall/proxy**
   - Add proxy settings if needed
   - Contact IT to whitelist the Canvas API

4. **Increase timeout** in `routes/incidents.py`:
   ```python
   response = await client.get(url, headers=headers, params=params, timeout=60.0)
   ```

---

## 🔴 Postman Works But FastAPI Doesn't

### Common Causes

1. **Token Format Issue** (most common)
   - Remove "Bearer" from `.env` file

2. **Different Base URL**
   - Postman: `http://localhost:8022`
   - `.env`: `https://queues.canvas.mgsops.net:8020`
   - Make sure they match!

3. **Headers Difference**
   - Check if Postman has additional headers
   - Compare Postman headers with `utils/auth.py`

4. **Environment Variables**
   - Postman uses `{{bearer_token}}`
   - FastAPI reads from `.env` file
   - Ensure token is the same in both

---

## 🔴 Empty Response / No Data

### Problem
```json
{
  "value": [],
  "@odata.count": 0
}
```

### ✅ Solution
1. **Check support group name:**
   - Use exact name (case-sensitive)
   - Get valid names: `GET /api/support-groups/unique-from-incidents`

2. **URL encode special characters:**
   - Space: `%20`
   - `-`: No encoding needed
   - Example: `PGP - GPSO - Vortex` → `PGP%20-%20GPSO%20-%20Vortex`

3. **Verify data exists:**
   - Try without filters first
   - Check in Postman if data exists

---

## 🔴 Swagger UI Not Loading

### Problem
http://localhost:8000/docs returns 404 or doesn't load.

### ✅ Solution
1. **Verify server is running:**
   ```bash
   python main.py
   ```
   
2. **Check correct URL:**
   - Root: http://localhost:8000/
   - Docs: http://localhost:8000/docs
   - Redoc: http://localhost:8000/redoc

3. **Clear browser cache**

4. **Try different browser**

---

## 🔴 CORS Error (If Using From Browser)

### Problem
```
Access to fetch at 'http://localhost:8000' from origin '...' has been blocked by CORS policy
```

### ✅ Solution
CORS is already enabled in `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    ...
)
```

If still getting errors:
1. Restart the server
2. Clear browser cache
3. Check browser console for actual error

---

## 🛠️ Debug Tips

### Enable Debug Logging

Add to `main.py`:
```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

### Print Token in Auth Function

Temporarily add to `utils/auth.py`:
```python
def get_auth_token() -> str:
    token = settings.CANVAS_BEARER_TOKEN
    print(f"Token (first 20 chars): {token[:20]}...")
    print(f"Token starts with 'Bearer': {token.startswith('Bearer')}")
    return token
```

### Test Headers

Create a test endpoint in `routes/incidents.py`:
```python
@router.get("/test-headers")
async def test_headers():
    headers = get_auth_headers()
    return {
        "headers": headers,
        "auth_header_preview": headers["Authorization"][:30] + "..."
    }
```

---

## 📞 Still Having Issues?

1. **Check server logs** for detailed error messages
2. **Compare with Postman**:
   - Export actual request from Postman
   - Compare headers, URL, and parameters
3. **Verify token is valid**:
   - Decode JWT at https://jwt.io
   - Check expiration date
4. **Test Canvas API directly**:
   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" https://queues.canvas.mgsops.net:8020/incidents
   ```

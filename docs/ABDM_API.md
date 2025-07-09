# Gateway APIs

## Sessions

### Method
- `POST`

### URL
```python
url = f"${GATEWAY_BASE_URL}${SESSIONS_ENDPOINT}"    # from settings.py
```

### Headers
```python
{
    "REQUEST-ID": str(uuid.uuid4()),
    "TIMESTAMP": datetime.now().isoformat(),
    "X-CM-ID": "${X_CM_ID}"    # from settings.py
}
```

### Body
```python
{
  "clientId": "${CLIENT_ID}",    # from settings.py
  "clientSecret": "${CLIENT_SECRET}",    # from settings.py
  "grantType": "client_credentials"
}
```
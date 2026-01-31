# API Testing Guide

## Quick Test Script

Save this as `test_api.py` in the backend directory:

```python
import requests
from requests.auth import HTTPBasicAuth
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000"
USERNAME = "admin"  # Replace with your username
PASSWORD = "admin"  # Replace with your password

auth = HTTPBasicAuth(USERNAME, PASSWORD)

def print_response(title, response):
    """Helper function to print responses nicely."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
    except:
        print(f"Response: {response.text}")

# Test 1: Login
print("\n🔐 TEST 1: Login")
response = requests.post(
    f"{BASE_URL}/api/auth/login/",
    json={"username": USERNAME, "password": PASSWORD}
)
print_response("Login", response)

# Test 2: Upload CSV
print("\n📤 TEST 2: Upload CSV")
with open('sample_equipment_data.csv', 'rb') as f:
    response = requests.post(
        f"{BASE_URL}/api/analytics/csv/upload/",
        files={'file': f},
        auth=auth
    )
print_response("CSV Upload", response)

# Save dataset_id for later tests
dataset_id = None
if response.status_code == 201:
    dataset_id = response.json().get('dataset_id')

# Test 3: List All Datasets
print("\n📋 TEST 3: List All Datasets")
response = requests.get(
    f"{BASE_URL}/api/analytics/csv/datasets/",
    auth=auth
)
print_response("List Datasets", response)

# Test 4: Get Single Dataset
if dataset_id:
    print(f"\n🔍 TEST 4: Get Dataset {dataset_id}")
    response = requests.get(
        f"{BASE_URL}/api/analytics/csv/datasets/{dataset_id}/",
        auth=auth
    )
    print_response(f"Get Dataset {dataset_id}", response)

# Test 5: Get Statistics
print("\n📊 TEST 5: Get Aggregated Statistics")
response = requests.get(
    f"{BASE_URL}/api/analytics/statistics/",
    auth=auth
)
print_response("Statistics", response)

# Test 6: Delete Dataset (optional - uncomment to test)
# if dataset_id:
#     print(f"\n🗑️ TEST 6: Delete Dataset {dataset_id}")
#     response = requests.delete(
#         f"{BASE_URL}/api/analytics/csv/datasets/{dataset_id}/",
#         auth=auth
#     )
#     print_response(f"Delete Dataset {dataset_id}", response)

# Test 7: Logout
print("\n🚪 TEST 7: Logout")
response = requests.post(
    f"{BASE_URL}/api/auth/logout/",
    auth=auth
)
print_response("Logout", response)

print("\n✅ All tests completed!")
```

## Running the Tests

1. Make sure the server is running:
   ```bash
   python manage.py runserver
   ```

2. In a new terminal, run the test script:
   ```bash
   python test_api.py
   ```

## cURL Examples

### Authentication
```bash
# Login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin"}'

# Logout
curl -X POST http://127.0.0.1:8000/api/auth/logout/ \
  -u admin:admin
```

### CSV Operations
```bash
# Upload CSV
curl -X POST http://127.0.0.1:8000/api/analytics/csv/upload/ \
  -u admin:admin \
  -F "file=@sample_equipment_data.csv"

# List all datasets
curl -X GET http://127.0.0.1:8000/api/analytics/csv/datasets/ \
  -u admin:admin

# Get specific dataset (replace 1 with actual ID)
curl -X GET http://127.0.0.1:8000/api/analytics/csv/datasets/1/ \
  -u admin:admin

# Delete dataset (replace 1 with actual ID)
curl -X DELETE http://127.0.0.1:8000/api/analytics/csv/datasets/1/ \
  -u admin:admin

# Get statistics
curl -X GET http://127.0.0.1:8000/api/analytics/statistics/ \
  -u admin:admin
```

## Postman Collection

Import this JSON into Postman:

```json
{
  "info": {
    "name": "Chemical Equipment API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Login",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\"username\": \"admin\", \"password\": \"admin\"}"
        },
        "url": "http://127.0.0.1:8000/api/auth/login/"
      }
    },
    {
      "name": "Upload CSV",
      "request": {
        "auth": {
          "type": "basic",
          "basic": [
            {"key": "username", "value": "admin"},
            {"key": "password", "value": "admin"}
          ]
        },
        "method": "POST",
        "body": {
          "mode": "formdata",
          "formdata": [
            {"key": "file", "type": "file", "src": "sample_equipment_data.csv"}
          ]
        },
        "url": "http://127.0.0.1:8000/api/analytics/csv/upload/"
      }
    },
    {
      "name": "List Datasets",
      "request": {
        "auth": {
          "type": "basic",
          "basic": [
            {"key": "username", "value": "admin"},
            {"key": "password", "value": "admin"}
          ]
        },
        "method": "GET",
        "url": "http://127.0.0.1:8000/api/analytics/csv/datasets/"
      }
    },
    {
      "name": "Get Statistics",
      "request": {
        "auth": {
          "type": "basic",
          "basic": [
            {"key": "username", "value": "admin"},
            {"key": "password", "value": "admin"}
          ]
        },
        "method": "GET",
        "url": "http://127.0.0.1:8000/api/analytics/statistics/"
      }
    }
  ]
}
```

## Testing Invalid CSV

Create `invalid_equipment.csv` to test error handling:

```csv
Equipment Name,Type,Flowrate,Pressure
Pump-A1,Pump,150.5,5.2
```

Upload it to see validation error:
```bash
curl -X POST http://127.0.0.1:8000/api/analytics/csv/upload/ \
  -u admin:admin \
  -F "file=@invalid_equipment.csv"
```

Expected response:
```json
{
  "error": "CSV processing failed.",
  "details": "Missing required columns: Temperature"
}
```

## Testing Negative Values

Create `negative_values.csv`:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-A1,Pump,-150.5,5.2,45.3
```

Expected response:
```json
{
  "error": "CSV processing failed.",
  "details": "Column 'Flowrate' contains negative values."
}
```

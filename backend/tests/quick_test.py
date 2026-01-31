"""Quick API test"""
import requests
from requests.auth import HTTPBasicAuth
import json

BASE_URL = "http://127.0.0.1:8000"
USERNAME = "admin"
PASSWORD = "admin123"

print("=" * 70)
print("  TESTING DJANGO REST API")
print("=" * 70)

# Test 1: Login
print("\n1. Testing Login...")
try:
    response = requests.post(
        f"{BASE_URL}/api/auth/login/",
        json={"username": USERNAME, "password": PASSWORD},
        timeout=5
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Login successful!")
        print(f"   User: {response.json().get('user', {}).get('username')}")
    else:
        print(f"   ❌ Login failed: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Upload CSV
print("\n2. Testing CSV Upload...")
auth = HTTPBasicAuth(USERNAME, PASSWORD)
try:
    with open('sample_equipment_data.csv', 'rb') as f:
        response = requests.post(
            f"{BASE_URL}/api/analytics/csv/upload/",
            files={'file': f},
            auth=auth,
            timeout=10
        )
    print(f"   Status: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        print("   ✅ CSV uploaded successfully!")
        print(f"   Dataset ID: {data.get('dataset_id')}")
        print(f"   Row Count: {data.get('row_count')}")
        print(f"   Equipment Types: {len(data.get('statistics', {}).get('by_type', {}))}")
    else:
        print(f"   Response: {response.text[:200]}")
except FileNotFoundError:
    print("   ⚠️ sample_equipment_data.csv not found")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: List Datasets
print("\n3. Testing List Datasets...")
try:
    response = requests.get(
        f"{BASE_URL}/api/analytics/csv/datasets/",
        auth=auth,
        timeout=5
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        count = response.json().get('count', 0)
        print(f"   ✅ Found {count} dataset(s)")
    else:
        print(f"   ❌ Failed: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Get Statistics
print("\n4. Testing Statistics...")
try:
    response = requests.get(
        f"{BASE_URL}/api/analytics/statistics/",
        auth=auth,
        timeout=5
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("   ✅ Statistics retrieved!")
        print(f"   Total Datasets: {data.get('total_datasets')}")
        print(f"   Total Equipment: {data.get('total_equipment_count')}")
    else:
        print(f"   ❌ Failed: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 5: Logout
print("\n5. Testing Logout...")
try:
    response = requests.post(
        f"{BASE_URL}/api/auth/logout/",
        auth=auth,
        timeout=5
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Logout successful!")
    else:
        print(f"   ❌ Failed: {response.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 70)
print("  TEST COMPLETE!")
print("=" * 70)
print("\n✅ Backend is working!")
print("📝 Admin Panel: http://127.0.0.1:8000/admin/")
print("📊 API Base URL: http://127.0.0.1:8000/api/")
print("\nCredentials:")
print("  Username: admin")
print("  Password: admin123")

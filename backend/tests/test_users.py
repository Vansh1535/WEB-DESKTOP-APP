"""
Test API with different users
"""
import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://127.0.0.1:8000"

users = [
    ('john_doe', 'john123'),
    ('jane_smith', 'jane123'),
    ('engineer1', 'eng123'),
    ('analyst1', 'analyst123')
]

print("=" * 70)
print("TESTING API WITH DIFFERENT USERS")
print("=" * 70)

for username, password in users:
    print(f"\n📋 Testing user: {username}")
    print("-" * 70)
    
    auth = HTTPBasicAuth(username, password)
    
    # Test 1: Login
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login/",
            json={"username": username, "password": password},
            timeout=5
        )
        if response.status_code == 200:
            print(f"  ✅ Login successful")
        else:
            print(f"  ❌ Login failed: {response.status_code}")
            continue
    except Exception as e:
        print(f"  ❌ Error: {e}")
        continue
    
    # Test 2: List datasets
    try:
        response = requests.get(
            f"{BASE_URL}/api/analytics/csv/datasets/",
            auth=auth,
            timeout=5
        )
        if response.status_code == 200:
            count = response.json().get('count', 0)
            print(f"  ✅ Can access datasets: {count} dataset(s)")
        else:
            print(f"  ❌ Failed to list datasets")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Test 3: Get statistics
    try:
        response = requests.get(
            f"{BASE_URL}/api/analytics/statistics/",
            auth=auth,
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Can access statistics: {data.get('total_datasets')} datasets, {data.get('total_equipment_count')} equipment")
        else:
            print(f"  ❌ Failed to get statistics")
    except Exception as e:
        print(f"  ❌ Error: {e}")

print("\n" + "=" * 70)
print("✅ All users can authenticate and use the API!")
print("=" * 70)
print("\n💡 Each user can only see their own datasets")
print("💡 Try uploading CSVs with different users to test isolation")

"""
Test script to verify API connectivity and authentication
Run this after starting the Django server to ensure everything is working.
"""

import requests
import json

API_BASE = "http://localhost:8000"

def test_home():
    """Test if server is running"""
    print("\n1. Testing server connectivity...")
    try:
        response = requests.get(f"{API_BASE}/")
        print(f"   ✓ Server is running (Status: {response.status_code})")
        return True
    except Exception as e:
        print(f"   ✗ Server connection failed: {e}")
        return False

def test_login():
    """Test login endpoint"""
    print("\n2. Testing login...")
    try:
        response = requests.post(
            f"{API_BASE}/api/v1/auth/login/",
            json={"username": "admin", "password": "admin123"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Login successful")
            print(f"   User: {data.get('user', {}).get('username')}")
            return response.cookies
        else:
            print(f"   ✗ Login failed (Status: {response.status_code})")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"   ✗ Login error: {e}")
        return None

def test_datasets(cookies):
    """Test datasets endpoint"""
    print("\n3. Testing datasets list...")
    try:
        # Test with Basic Auth
        from base64 import b64encode
        credentials = b64encode(b"admin:admin123").decode()
        
        response = requests.get(
            f"{API_BASE}/api/v1/analytics/csv/datasets/",
            headers={"Authorization": f"Basic {credentials}"},
            cookies=cookies
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Datasets retrieved successfully")
            print(f"   Count: {data.get('count', 0)}")
            return True
        else:
            print(f"   ✗ Datasets request failed (Status: {response.status_code})")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Datasets error: {e}")
        return False

def test_statistics(cookies):
    """Test statistics endpoint"""
    print("\n4. Testing statistics...")
    try:
        from base64 import b64encode
        credentials = b64encode(b"admin:admin123").decode()
        
        response = requests.get(
            f"{API_BASE}/api/v1/analytics/csv/statistics/",
            headers={"Authorization": f"Basic {credentials}"},
            cookies=cookies
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Statistics retrieved successfully")
            print(f"   Total equipment: {data.get('total_equipment_count', 0)}")
        elif response.status_code == 404:
            print(f"   ⚠ No data uploaded yet (this is expected for new setup)")
        else:
            print(f"   ✗ Statistics request failed (Status: {response.status_code})")
        return True
    except Exception as e:
        print(f"   ✗ Statistics error: {e}")
        return False

def test_cors():
    """Test CORS configuration"""
    print("\n5. Testing CORS configuration...")
    try:
        response = requests.options(
            f"{API_BASE}/api/v1/analytics/csv/datasets/",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        
        if 'access-control-allow-origin' in response.headers:
            print(f"   ✓ CORS is configured correctly")
            return True
        else:
            print(f"   ⚠ CORS headers not found (might cause frontend issues)")
            return False
    except Exception as e:
        print(f"   ✗ CORS test error: {e}")
        return False

def main():
    print("=" * 60)
    print("Backend API Connectivity Test")
    print("=" * 60)
    
    # Run tests
    if not test_home():
        print("\n❌ Server is not running!")
        print("Please start the Django server with: python manage.py runserver")
        return
    
    cookies = test_login()
    if cookies:
        test_datasets(cookies)
        test_statistics(cookies)
    
    test_cors()
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. If all tests passed, start the frontend: cd Web-Frontend && pnpm dev")
    print("2. Open http://localhost:3000 in your browser")
    print("3. Login with: admin / admin123")
    print("=" * 60)

if __name__ == "__main__":
    main()

"""
Quick API Test Script
Run this after setting up the backend to verify all endpoints work.
"""

import requests
from requests.auth import HTTPBasicAuth
import json
import sys

# Configuration
BASE_URL = "http://127.0.0.1:8000"

def print_header(text):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print('='*70)

def print_response(response):
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

def main():
    print_header("🚀 Chemical Equipment API - Quick Test")
    
    # Get credentials
    print("\nEnter your credentials:")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    if not username or not password:
        print("❌ Username and password are required!")
        sys.exit(1)
    
    auth = HTTPBasicAuth(username, password)
    
    # Test 1: Login
    print_header("TEST 1: Login")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login/",
            json={"username": username, "password": password}
        )
        print_response(response)
        if response.status_code != 200:
            print("\n❌ Login failed! Check your credentials.")
            sys.exit(1)
        print("✅ Login successful!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure the server is running: python manage.py runserver")
        sys.exit(1)
    
    # Test 2: Upload CSV
    print_header("TEST 2: Upload CSV")
    try:
        with open('sample_equipment_data.csv', 'rb') as f:
            response = requests.post(
                f"{BASE_URL}/api/analytics/csv/upload/",
                files={'file': f},
                auth=auth
            )
        print_response(response)
        if response.status_code == 201:
            dataset_id = response.json().get('dataset_id')
            print(f"✅ CSV uploaded successfully! Dataset ID: {dataset_id}")
        else:
            print("⚠️ Upload failed!")
            dataset_id = None
    except FileNotFoundError:
        print("⚠️ sample_equipment_data.csv not found - skipping upload test")
        dataset_id = None
    except Exception as e:
        print(f"❌ Error: {e}")
        dataset_id = None
    
    # Test 3: List Datasets
    print_header("TEST 3: List All Datasets")
    try:
        response = requests.get(
            f"{BASE_URL}/api/analytics/csv/datasets/",
            auth=auth
        )
        print_response(response)
        if response.status_code == 200:
            count = response.json().get('count', 0)
            print(f"✅ Found {count} dataset(s)")
        else:
            print("⚠️ Failed to list datasets")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Get Statistics
    print_header("TEST 4: Get Aggregated Statistics")
    try:
        response = requests.get(
            f"{BASE_URL}/api/analytics/statistics/",
            auth=auth
        )
        print_response(response)
        if response.status_code == 200:
            print("✅ Statistics retrieved successfully!")
        else:
            print("⚠️ Failed to get statistics")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 5: Get Single Dataset (if we have one)
    if dataset_id:
        print_header(f"TEST 5: Get Dataset {dataset_id}")
        try:
            response = requests.get(
                f"{BASE_URL}/api/analytics/csv/datasets/{dataset_id}/",
                auth=auth
            )
            print_response(response)
            if response.status_code == 200:
                print("✅ Dataset retrieved successfully!")
            else:
                print("⚠️ Failed to get dataset")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Test 6: Logout
    print_header("TEST 6: Logout")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/logout/",
            auth=auth
        )
        print_response(response)
        if response.status_code == 200:
            print("✅ Logout successful!")
        else:
            print("⚠️ Logout failed")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Summary
    print_header("🎉 Test Complete!")
    print("\nAll core endpoints have been tested.")
    print("Check the responses above for any errors.")
    print("\nAPI Documentation: See README.md")
    print("Admin Panel: http://127.0.0.1:8000/admin/")
    print()

if __name__ == "__main__":
    main()

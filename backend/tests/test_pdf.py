"""
Test PDF report generation
"""
import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://127.0.0.1:8000"
USERNAME = "admin"
PASSWORD = "admin123"

print("=" * 70)
print("TESTING PDF REPORT GENERATION")
print("=" * 70)

auth = HTTPBasicAuth(USERNAME, PASSWORD)

# Step 1: Get list of datasets
print("\n1. Getting datasets...")
response = requests.get(
    f"{BASE_URL}/api/analytics/csv/datasets/",
    auth=auth,
    timeout=5
)

if response.status_code == 200:
    datasets = response.json().get('datasets', [])
    print(f"   Found {len(datasets)} dataset(s)")
    
    if datasets:
        dataset_id = datasets[0]['id']
        file_name = datasets[0]['file_name']
        print(f"   Will generate PDF for: {file_name} (ID: {dataset_id})")
        
        # Step 2: Generate PDF
        print(f"\n2. Generating PDF report for dataset {dataset_id}...")
        response = requests.get(
            f"{BASE_URL}/api/analytics/csv/datasets/{dataset_id}/pdf/",
            auth=auth,
            timeout=10
        )
        
        if response.status_code == 200:
            # Save PDF file
            pdf_filename = f"equipment_report_{dataset_id}.pdf"
            with open(pdf_filename, 'wb') as f:
                f.write(response.content)
            
            print(f"   ✅ PDF generated successfully!")
            print(f"   📄 Saved as: {pdf_filename}")
            print(f"   📊 Size: {len(response.content)} bytes")
            print(f"\n   Open the file to view the report!")
        else:
            print(f"   ❌ Failed to generate PDF: {response.status_code}")
            print(f"   Error: {response.text}")
    else:
        print("\n   ⚠️ No datasets found. Upload a CSV first!")
else:
    print(f"   ❌ Failed to get datasets: {response.status_code}")

print("\n" + "=" * 70)
print("PDF GENERATION TEST COMPLETE")
print("=" * 70)

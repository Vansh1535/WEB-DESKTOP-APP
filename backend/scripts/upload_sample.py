import requests
from requests.auth import HTTPBasicAuth
import json

print("Uploading sample CSV...")

auth = HTTPBasicAuth('admin', 'admin123')
files = {'file': open('sample_equipment_data.csv', 'rb')}

try:
    response = requests.post(
        'http://127.0.0.1:8000/api/analytics/csv/upload/',
        files=files,
        auth=auth,
        timeout=10
    )
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        print("\n✅ SUCCESS! CSV Uploaded and Processed")
        print(f"\nDataset ID: {data['dataset_id']}")
        print(f"File Name: {data['file_name']}")
        print(f"Row Count: {data['row_count']}")
        print(f"Status: {data['status']}")
        
        stats = data.get('statistics', {})
        print(f"\nTotal Equipment: {stats.get('total_equipment_count')}")
        print(f"Equipment Types: {len(stats.get('by_type', {}))}")
        
        print("\n📊 Statistics by Type:")
        for eq_type, type_stats in stats.get('by_type', {}).items():
            print(f"\n  {eq_type}:")
            print(f"    Count: {type_stats['count']}")
            print(f"    Avg Flowrate: {type_stats['flowrate']['avg']}")
            print(f"    Avg Pressure: {type_stats['pressure']['avg']}")
            print(f"    Avg Temperature: {type_stats['temperature']['avg']}")
        
        print("\n\n🎉 Now refresh the admin panel to see the dataset!")
    else:
        print(f"\n❌ Error: {response.text}")
        
except Exception as e:
    print(f"\n❌ Error: {e}")

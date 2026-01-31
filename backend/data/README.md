# Sample Data

This directory contains sample data files for testing the Chemical Equipment Parameter Visualizer backend.

## Files

### `sample_equipment_data.csv`
**Purpose:** Sample CSV file for testing upload and statistics computation

**Format:**
```
Type,Flow Rate (L/min),Pressure (bar),Temperature (°C),Efficiency (%)
Pump,150,5,75,85
Valve,200,10,50,90
...
```

**Specifications:**
- **Rows:** 30 data entries
- **Equipment Types:** 10 unique types
- **Columns:** 5 (Type, Flow Rate, Pressure, Temperature, Efficiency)

**Equipment Types Included:**
1. Pump
2. Valve
3. Heat Exchanger
4. Reactor
5. Compressor
6. Tank
7. Turbine
8. Mixer
9. Separator
10. Boiler

**Statistics Generated:**
- Average Flow Rate: 181.69 L/min
- Average Pressure: 6.84 bar
- Average Temperature: 49.61 °C
- Average Efficiency: 84.83%

### Equipment Type Breakdown

| Type | Count | Avg Flow Rate | Avg Pressure | Avg Temperature | Avg Efficiency |
|------|-------|---------------|--------------|-----------------|----------------|
| Pump | 3 | 163.33 | 6.67 | 70.00 | 86.67 |
| Valve | 3 | 183.33 | 8.33 | 53.33 | 88.33 |
| Heat Exchanger | 3 | 210.00 | 6.67 | 40.00 | 81.67 |
| Reactor | 3 | 193.33 | 7.33 | 46.67 | 82.67 |
| Compressor | 3 | 170.00 | 7.67 | 56.67 | 84.00 |
| Tank | 3 | 163.33 | 5.33 | 46.67 | 85.33 |
| Turbine | 3 | 193.33 | 6.33 | 56.67 | 86.67 |
| Mixer | 3 | 170.00 | 7.00 | 43.33 | 83.67 |
| Separator | 3 | 183.33 | 6.33 | 43.33 | 82.33 |
| Boiler | 3 | 187.33 | 6.67 | 40.00 | 87.00 |

## Usage

### Upload via Admin Panel
1. Navigate to http://127.0.0.1:8000/admin/
2. Login with admin credentials
3. Go to "CSV datasets"
4. Click "Add CSV dataset"
5. Upload `sample_equipment_data.csv`
6. Click "Save"

### Upload via API
```bash
# Using curl
curl -X POST http://127.0.0.1:8000/api/analytics/upload/ \
  -u username:password \
  -F "file=@data/sample_equipment_data.csv"

# Using Python
python scripts/upload_sample.py
```

### Upload via Test Script
```bash
python tests/test_api.py
```

## CSV Format Requirements

For successful upload and processing, CSV files must:

1. **Have Required Columns:**
   - Type (text)
   - Flow Rate (L/min) (numeric)
   - Pressure (bar) (numeric)
   - Temperature (°C) (numeric)
   - Efficiency (%) (numeric)

2. **Format Rules:**
   - First row must be headers
   - No empty rows
   - Numeric values must be valid numbers
   - At least 1 data row required

3. **Size Limits:**
   - Maximum file size: 5 MB
   - Recommended rows: 1-10,000

## Creating Custom Test Data

### Example CSV Structure
```csv
Type,Flow Rate (L/min),Pressure (bar),Temperature (°C),Efficiency (%)
Pump,150,5,75,85
Valve,200,10,50,90
Heat Exchanger,180,8,30,75
```

### Python Script to Generate Data
```python
import pandas as pd
import random

equipment_types = ["Pump", "Valve", "Heat Exchanger", "Reactor", "Compressor"]
data = []

for _ in range(30):
    data.append({
        'Type': random.choice(equipment_types),
        'Flow Rate (L/min)': random.randint(100, 250),
        'Pressure (bar)': random.randint(5, 15),
        'Temperature (°C)': random.randint(20, 80),
        'Efficiency (%)': random.randint(70, 95)
    })

df = pd.DataFrame(data)
df.to_csv('data/custom_data.csv', index=False)
```

## Validation Rules

The backend validates uploaded CSV files:

1. ✅ File must be CSV format
2. ✅ Required columns must exist
3. ✅ At least one data row
4. ✅ Numeric columns contain valid numbers
5. ✅ No completely empty rows

If validation fails, the dataset status is set to "error" and error details are logged.

## Sample Data Usage in Tests

All test scripts use `sample_equipment_data.csv`:
- `tests/test_api.py` - Uploads and validates processing
- `scripts/upload_sample.py` - Direct upload script
- Admin panel - Manual testing

## Generated Files

After upload, the backend stores files in:
```
backend/media/csv_uploads/
└── sample_equipment_data_<timestamp>.csv
```

PDF reports are generated in:
```
backend/
└── equipment_report_<dataset_id>.pdf
```

## Data Privacy

- Each user can only see their own uploaded datasets
- Datasets are automatically deleted when limit is reached (5 per user)
- Media files are cleaned up when datasets are deleted

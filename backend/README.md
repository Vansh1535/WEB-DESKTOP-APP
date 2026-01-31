# Chemical Equipment Parameter Visualizer - Backend

A Django REST API for managing and analyzing chemical equipment parameter data with CSV upload, statistics computation, and PDF report generation.

## 📁 Project Structure

```
backend/
├── analytics/          # Main analytics app
├── config/             # Django configuration
├── users/              # User management
├── data/              # Sample data files
├── docs/              # All documentation
├── scripts/           # Utility scripts
├── tests/             # Test files
├── media/             # Uploaded files
└── venv/              # Virtual environment
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for complete details.

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)

### Installation Steps

1. **Navigate to the backend directory**
   ```bash
   cd backend
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin user.

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

---

## � Documentation

- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Complete folder structure
- **[docs/](docs/)** - All project documentation
  - [API_TESTING.md](docs/API_TESTING.md) - API reference
  - [ARCHITECTURE_BACKEND.md](docs/ARCHITECTURE_BACKEND.md) - System architecture
  - [QUICKSTART.md](docs/QUICKSTART.md) - Quick setup guide
  - [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Deployment guide
- **[tests/](tests/)** - Test documentation and scripts
- **[scripts/](scripts/)** - Utility scripts
- **[data/](data/)** - Sample data files

---

## 🔐 Authentication

All endpoints (except login) require **Basic Authentication**.

### Login
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'
```

**Response:**
```json
{
  "message": "Login successful.",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "",
    "last_name": ""
  }
}
```

### Logout
```bash
curl -X POST http://127.0.0.1:8000/api/auth/logout/ \
  -u admin:your_password
```

---

## 📊 API Endpoints

### 1. Upload CSV File

**Endpoint:** `POST /api/analytics/csv/upload/`

**Authentication:** Required (Basic Auth)

**Content-Type:** `multipart/form-data`

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/analytics/csv/upload/ \
  -u admin:your_password \
  -F "file=@sample_equipment_data.csv"
```

**Response:**
```json
{
  "message": "CSV uploaded and processed successfully.",
  "dataset_id": 1,
  "file_name": "sample_equipment_data.csv",
  "status": "completed",
  "row_count": 50,
  "statistics": {
    "total_equipment_count": 50,
    "by_type": {
      "Pump": {
        "count": 20,
        "flowrate": {"avg": 150.5, "min": 100.0, "max": 200.0},
        "pressure": {"avg": 5.2, "min": 3.0, "max": 7.5},
        "temperature": {"avg": 45.3, "min": 40.0, "max": 50.0}
      }
    },
    "overall_averages": {
      "flowrate": 140.5,
      "pressure": 4.8,
      "temperature": 44.2
    }
  }
}
```

### 2. List All Datasets

**Endpoint:** `GET /api/analytics/csv/datasets/`

**Authentication:** Required (Basic Auth)

**Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/analytics/csv/datasets/ \
  -u admin:your_password
```

**Response:**
```json
{
  "count": 3,
  "datasets": [
    {
      "id": 1,
      "file_name": "equipment1.csv",
      "uploaded_by_username": "admin",
      "uploaded_at": "2026-01-29T10:30:00Z",
      "row_count": 50,
      "status": "completed",
      "statistics": {...}
    }
  ]
}
```

### 3. Retrieve Single Dataset

**Endpoint:** `GET /api/analytics/csv/datasets/{id}/`

**Authentication:** Required (Basic Auth)

**Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/analytics/csv/datasets/1/ \
  -u admin:your_password
```

### 4. Delete Dataset

**Endpoint:** `DELETE /api/analytics/csv/datasets/{id}/`

**Authentication:** Required (Basic Auth)

**Example:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/analytics/csv/datasets/1/ \
  -u admin:your_password
```

**Response:**
```json
{
  "message": "Dataset deleted successfully."
}
```

### 5. Get Aggregated Statistics

**Endpoint:** `GET /api/analytics/statistics/`

**Authentication:** Required (Basic Auth)

**Example:**
```bash
curl -X GET http://127.0.0.1:8000/api/analytics/statistics/ \
  -u admin:your_password
```

**Response:**
```json
{
  "total_datasets": 3,
  "total_equipment_count": 150,
  "datasets": [...]
}
```

---

## 📋 CSV File Format

Your CSV file must contain the following columns:

| Column Name      | Type    | Description                    |
|-----------------|---------|--------------------------------|
| Equipment Name  | String  | Name of the equipment          |
| Type           | String  | Equipment type/category        |
| Flowrate       | Number  | Flowrate (non-negative)        |
| Pressure       | Number  | Pressure (non-negative)        |
| Temperature    | Number  | Temperature (non-negative)     |

**Example CSV:**
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-A1,Pump,150.5,5.2,45.3
Valve-B2,Valve,200.0,7.5,50.0
Heat-Exchanger-C3,Heat Exchanger,180.0,6.0,48.5
```

---

## 🎯 Features

✅ **Automatic Dataset Management:** System keeps only the last 5 datasets per user
✅ **Synchronous Processing:** CSV files are processed immediately upon upload
✅ **Comprehensive Statistics:** Automatic calculation of averages, min, max by equipment type
✅ **Data Validation:** Ensures all required columns exist and numeric values are non-negative
✅ **Error Handling:** Clear error messages for invalid data
✅ **Basic Authentication:** Simple username/password authentication
✅ **SQLite Database:** No external database setup required

---

## 🔧 Database Models

### CSVDataset Model

| Field         | Type         | Description                           |
|--------------|--------------|---------------------------------------|
| id           | Integer      | Primary key (auto-generated)          |
| file_name    | String       | Original filename                     |
| file         | FileField    | Uploaded CSV file                     |
| uploaded_by  | ForeignKey   | User who uploaded the file            |
| uploaded_at  | DateTime     | Upload timestamp                      |
| row_count    | Integer      | Number of rows in CSV                 |
| status       | String       | processing/completed/failed           |
| statistics   | JSONField    | Computed statistics                   |
| error_log    | Text         | Error messages if processing failed   |
| processed_at | DateTime     | Processing completion timestamp       |

---

## 🛠️ Admin Panel

Access the Django admin panel at `http://127.0.0.1:8000/admin/`

Log in with your superuser credentials to:
- View all uploaded datasets
- Monitor processing status
- View statistics
- Manage users

---

## 📝 Testing the API

### Using Python Requests
```python
import requests
from requests.auth import HTTPBasicAuth

# Base URL
base_url = "http://127.0.0.1:8000"

# Authentication
auth = HTTPBasicAuth('admin', 'your_password')

# Upload CSV
with open('sample_equipment_data.csv', 'rb') as f:
    response = requests.post(
        f"{base_url}/api/analytics/csv/upload/",
        files={'file': f},
        auth=auth
    )
    print(response.json())

# List datasets
response = requests.get(
    f"{base_url}/api/analytics/csv/datasets/",
    auth=auth
)
print(response.json())

# Get statistics
response = requests.get(
    f"{base_url}/api/analytics/statistics/",
    auth=auth
)
print(response.json())
```

---

## 🚨 Error Handling

The API returns appropriate HTTP status codes:

- `200 OK` - Successful GET/DELETE requests
- `201 Created` - Successful POST requests
- `400 Bad Request` - Invalid data or CSV format errors
- `401 Unauthorized` - Authentication required or failed
- `404 Not Found` - Resource not found

**Example Error Response:**
```json
{
  "error": "CSV processing failed.",
  "details": "Missing required columns: Type, Flowrate"
}
```

---

## 🎓 Statistics Computation

The system automatically computes:

1. **Total Equipment Count** - Total number of rows in CSV
2. **By Type Statistics:**
   - Count of equipment per type
   - Average, Min, Max for Flowrate, Pressure, Temperature
3. **Overall Averages** - Across all equipment

---

## 📦 Deployment on Render.com

1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python manage.py migrate && gunicorn config.wsgi:application`
6. Add environment variable: `PYTHON_VERSION=3.10.0`
7. Deploy!

---

## 💡 Tips

- The system automatically deletes the oldest datasets when a user exceeds 5 datasets
- All CSV files are stored in `media/csv_uploads/`
- Statistics are computed synchronously during upload
- Use the admin panel for quick data inspection
- Basic Auth credentials are sent with each request (username:password in base64)

---

## 🐛 Troubleshooting

**Issue:** `ModuleNotFoundError: No module named 'rest_framework'`
**Solution:** Run `pip install -r requirements.txt`

**Issue:** `OperationalError: no such table`
**Solution:** Run `python manage.py migrate`

**Issue:** `Authentication credentials were not provided`
**Solution:** Ensure you're sending Basic Auth header with username:password

**Issue:** `CSV processing failed`
**Solution:** Check that your CSV has all required columns and numeric values are valid

---

## 📞 Support

For issues or questions, check:
- Django logs in the console
- Admin panel for dataset status and errors
- CSV validation requirements above

---

**Built with Django 4.2.7 and Django REST Framework 3.14.0**

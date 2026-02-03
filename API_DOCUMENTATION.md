# API Documentation

Complete API reference for the Chemical Equipment Parameter Visualizer backend.

## Base URL

```
Development: http://localhost:8000
Production: https://your-domain.com
```

## Authentication

All API endpoints (except registration and login) require **Basic Authentication**.

### Headers
```http
Authorization: Basic <base64(username:password)>
Content-Type: application/json
```

### Example (JavaScript)
```javascript
const credentials = btoa(`${username}:${password}`);
fetch('/api/v1/analytics/datasets/', {
  headers: {
    'Authorization': `Basic ${credentials}`
  }
});
```

---

## 🔐 Authentication Endpoints

### Register User

Create a new user account.

**Endpoint:** `POST /api/v1/auth/register/`

**Request Body:**
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "username": "newuser",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "message": "User registered successfully"
}
```

**Error Responses:**
- `400 Bad Request` - Validation errors (username exists, invalid email, etc.)

---

### Login

Authenticate user and verify credentials.

**Endpoint:** `POST /api/v1/auth/login/`

**Request Body:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "first_name": "Admin",
    "last_name": "User"
  }
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid credentials
- `400 Bad Request` - Missing fields

---

### Get User Profile

Retrieve authenticated user's profile and preferences.

**Endpoint:** `GET /api/v1/auth/profile/`

**Headers:** Requires authentication

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "first_name": "Admin",
  "last_name": "User",
  "date_joined": "2026-02-01T10:30:00Z",
  "last_login": "2026-02-03T14:15:00Z",
  "preferences": {
    "theme": "dark",
    "default_view": "dashboard",
    "items_per_page": 50,
    "default_sort_column": "uploaded_at",
    "default_sort_order": "desc",
    "last_active_dataset_id": 4,
    "updated_at": "2026-02-03T14:00:00Z"
  },
  "upload_count": 5
}
```

---

### Update User Preferences

Update user preferences.

**Endpoint:** `PUT /api/v1/auth/preferences/`

**Headers:** Requires authentication

**Request Body:**
```json
{
  "theme": "light",
  "default_view": "charts",
  "items_per_page": 100
}
```

**Response (200 OK):**
```json
{
  "message": "Preferences updated successfully",
  "preferences": {
    "theme": "light",
    "default_view": "charts",
    "items_per_page": 100,
    "updated_at": "2026-02-03T14:30:00Z"
  }
}
```

---

## 📊 Analytics Endpoints

### Upload CSV File

Upload and process a CSV file containing equipment data.

**Endpoint:** `POST /api/v1/analytics/csv/upload/`

**Headers:** 
- Requires authentication
- `Content-Type: multipart/form-data`

**Request (Form Data):**
```
file: <CSV File>
```

**CSV Format Required:**
```csv
Equipment_ID,Equipment_Name,Type,Flowrate,Pressure,Temperature
EQ001,Reactor A,Reactor,150.5,10.2,350.0
EQ002,Pump B,Pump,200.3,15.8,25.0
```

**Response (201 Created):**
```json
{
  "message": "CSV uploaded and processed successfully",
  "dataset_id": 5,
  "file_name": "sample_equipment_data.csv",
  "row_count": 30,
  "uploaded_at": "2026-02-03T14:45:00Z"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid file format, missing columns, validation errors
- `413 Payload Too Large` - File exceeds 50MB limit
- `401 Unauthorized` - Not authenticated

**Validation Rules:**
- File must be `.csv` format
- Required columns: Equipment_ID, Equipment_Name, Type, Flowrate, Pressure, Temperature
- Numeric fields must be valid numbers
- Maximum file size: 50 MB

---

### List All Datasets

Retrieve list of all uploaded datasets for authenticated user.

**Endpoint:** `GET /api/v1/analytics/datasets/`

**Headers:** Requires authentication

**Query Parameters:**
- `page` (optional) - Page number (default: 1)
- `page_size` (optional) - Items per page (default: 50)
- `sort` (optional) - Sort field (default: uploaded_at)
- `order` (optional) - Sort order: 'asc' or 'desc' (default: desc)

**Response (200 OK):**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "datasets": [
    {
      "id": 5,
      "file_name": "sample_equipment_data.csv",
      "uploaded_at": "2026-02-03T14:45:00Z",
      "row_count": 30,
      "file_size": 2048,
      "user": "admin"
    },
    {
      "id": 4,
      "file_name": "equipment_jan.csv",
      "uploaded_at": "2026-02-02T10:30:00Z",
      "row_count": 25,
      "file_size": 1800,
      "user": "admin"
    }
  ]
}
```

---

### Get Dataset Details with Statistics

Retrieve specific dataset with complete statistics.

**Endpoint:** `GET /api/v1/analytics/datasets/{id}/`

**Headers:** Requires authentication

**Path Parameters:**
- `id` - Dataset ID (integer)

**Response (200 OK):**
```json
{
  "id": 5,
  "file_name": "sample_equipment_data.csv",
  "uploaded_at": "2026-02-03T14:45:00Z",
  "row_count": 30,
  "file_size": 2048,
  "user": "admin",
  "statistics": {
    "total_equipment_count": 30,
    "overall_averages": {
      "flowrate": 185.5,
      "pressure": 12.8,
      "temperature": 245.3
    },
    "by_type": {
      "Reactor": {
        "count": 8,
        "flowrate": {"mean": 175.2, "min": 150.0, "max": 200.0},
        "pressure": {"mean": 11.5, "min": 10.0, "max": 13.0},
        "temperature": {"mean": 350.0, "min": 320.0, "max": 380.0}
      },
      "Pump": {
        "count": 7,
        "flowrate": {"mean": 210.5, "min": 180.0, "max": 240.0},
        "pressure": {"mean": 15.2, "min": 12.0, "max": 18.0},
        "temperature": {"mean": 28.5, "min": 20.0, "max": 35.0}
      },
      "Heat Exchanger": {
        "count": 6,
        "flowrate": {"mean": 165.8, "min": 140.0, "max": 190.0},
        "pressure": {"mean": 10.8, "min": 8.0, "max": 13.0},
        "temperature": {"mean": 180.0, "min": 150.0, "max": 210.0}
      },
      "Compressor": {
        "count": 5,
        "flowrate": {"mean": 195.0, "min": 170.0, "max": 220.0},
        "pressure": {"mean": 16.5, "min": 14.0, "max": 19.0},
        "temperature": {"mean": 85.0, "min": 70.0, "max": 100.0}
      },
      "Distillation Column": {
        "count": 4,
        "flowrate": {"mean": 155.0, "min": 130.0, "max": 180.0},
        "pressure": {"mean": 9.2, "min": 7.5, "max": 11.0},
        "temperature": {"mean": 280.0, "min": 250.0, "max": 310.0}
      }
    }
  }
}
```

**Error Responses:**
- `404 Not Found` - Dataset does not exist
- `403 Forbidden` - Not authorized to access this dataset

---

### Get Dataset Statistics Only

Retrieve only statistics for a dataset (lighter response).

**Endpoint:** `GET /api/v1/analytics/datasets/{id}/statistics/`

**Headers:** Requires authentication

**Response (200 OK):**
```json
{
  "dataset_id": 5,
  "statistics": {
    "total_equipment_count": 30,
    "overall_averages": {
      "flowrate": 185.5,
      "pressure": 12.8,
      "temperature": 245.3
    },
    "by_type": { /* Same structure as above */ }
  }
}
```

---

### Get Dataset Raw Data

Retrieve raw data rows from a dataset.

**Endpoint:** `GET /api/v1/analytics/datasets/{id}/data/`

**Headers:** Requires authentication

**Query Parameters:**
- `page` (optional) - Page number
- `page_size` (optional) - Rows per page (max 500)

**Response (200 OK):**
```json
{
  "dataset_id": 5,
  "count": 30,
  "data": [
    {
      "Equipment_ID": "EQ001",
      "Equipment_Name": "Reactor A",
      "Type": "Reactor",
      "Flowrate": 150.5,
      "Pressure": 10.2,
      "Temperature": 350.0
    },
    {
      "Equipment_ID": "EQ002",
      "Equipment_Name": "Pump B",
      "Type": "Pump",
      "Flowrate": 200.3,
      "Pressure": 15.8,
      "Temperature": 25.0
    }
    // ... more rows
  ]
}
```

---

### Generate PDF Report

Generate and download a PDF report for a dataset.

**Endpoint:** `GET /api/v1/analytics/datasets/{id}/pdf-report/`

**Headers:** Requires authentication

**Response (200 OK):**
- Content-Type: `application/pdf`
- Binary PDF file

**Report Contents:**
- Dataset metadata
- Summary statistics
- 4 embedded charts (bar, box, line, pie)
- Equipment type breakdown
- Generation timestamp

**Error Responses:**
- `404 Not Found` - Dataset does not exist
- `500 Internal Server Error` - PDF generation failed

**Example (JavaScript):**
```javascript
const response = await fetch(`/api/v1/analytics/datasets/5/pdf-report/`, {
  headers: { 'Authorization': `Basic ${credentials}` }
});
const blob = await response.blob();
const url = window.URL.createObjectURL(blob);
window.open(url);
```

---

### Delete Dataset

Delete a dataset and its associated file.

**Endpoint:** `DELETE /api/v1/analytics/datasets/{id}/`

**Headers:** Requires authentication

**Response (204 No Content):**
- Empty response body

**Error Responses:**
- `404 Not Found` - Dataset does not exist
- `403 Forbidden` - Not authorized to delete this dataset

---

## 📋 Response Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request succeeded |
| 201 | Created - Resource created successfully |
| 204 | No Content - Request succeeded, no response body |
| 400 | Bad Request - Invalid input or validation error |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Not authorized |
| 404 | Not Found - Resource doesn't exist |
| 413 | Payload Too Large - File exceeds size limit |
| 500 | Internal Server Error - Server error occurred |

---

## 🔒 Security

### Authentication
- Basic Authentication required for all protected endpoints
- Credentials base64 encoded: `username:password`
- Session cookies for web frontend

### CORS
- Configured for `http://localhost:3000` (web frontend)
- Credentials allowed
- Headers: Authorization, Content-Type

### File Upload
- Maximum file size: 50 MB
- Allowed extensions: `.csv` only
- File validation before processing
- Unique filename generation

### Data Privacy
- Users can only access their own datasets
- Credentials never logged
- Secure password hashing (Django default)

---

## 📝 Rate Limiting

Currently no rate limiting implemented. For production, consider:
- 100 requests per minute per user
- 10 CSV uploads per hour per user
- 20 PDF generations per hour per user

---

## 🧪 Testing with cURL

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### Upload CSV
```bash
curl -X POST http://localhost:8000/api/v1/analytics/csv/upload/ \
  -u admin:admin123 \
  -F "file=@sample_equipment_data.csv"
```

### List Datasets
```bash
curl -X GET http://localhost:8000/api/v1/analytics/datasets/ \
  -u admin:admin123
```

### Get Dataset
```bash
curl -X GET http://localhost:8000/api/v1/analytics/datasets/5/ \
  -u admin:admin123
```

### Download PDF
```bash
curl -X GET http://localhost:8000/api/v1/analytics/datasets/5/pdf-report/ \
  -u admin:admin123 \
  --output report.pdf
```

---

## 🐛 Error Format

All errors return JSON with descriptive messages:

```json
{
  "error": "Dataset not found",
  "detail": "No dataset with ID 999 exists for this user",
  "code": "NOT_FOUND"
}
```

---

## 📞 Support

For API issues or questions:
- Check backend logs: `python manage.py runserver`
- Review Django debug toolbar (if enabled)
- Open GitHub issue

---

**API Version:** 1.0  
**Last Updated:** February 3, 2026

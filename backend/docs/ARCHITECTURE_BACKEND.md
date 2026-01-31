# 🏗️ System Architecture

## Overview

The Chemical Equipment Parameter Visualizer backend is a Django REST API that processes CSV files containing equipment data and provides statistical analysis.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                            │
│  (cURL, Postman, Browser, Frontend App, Mobile App)            │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/HTTPS + Basic Auth
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      DJANGO REST API                            │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API ENDPOINTS                         │  │
│  │                                                          │  │
│  │  Authentication Endpoints                                │  │
│  │  ├─ POST /api/auth/login/                               │  │
│  │  └─ POST /api/auth/logout/                              │  │
│  │                                                          │  │
│  │  Analytics Endpoints                                     │  │
│  │  ├─ POST   /api/analytics/csv/upload/                   │  │
│  │  ├─ GET    /api/analytics/csv/datasets/                 │  │
│  │  ├─ GET    /api/analytics/csv/datasets/{id}/            │  │
│  │  ├─ DELETE /api/analytics/csv/datasets/{id}/            │  │
│  │  └─ GET    /api/analytics/statistics/                   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                   │
│  ┌──────────────────────────▼────────────────────────────────┐ │
│  │                  MIDDLEWARE LAYER                         │ │
│  │  ├─ Authentication (BasicAuth)                           │ │
│  │  ├─ CSRF Protection                                      │ │
│  │  ├─ Security Headers                                     │ │
│  │  └─ Session Management                                   │ │
│  └──────────────────────────────────────────────────────────┘  │
│                             │                                   │
│  ┌──────────────────────────▼────────────────────────────────┐ │
│  │                    VIEW LAYER                             │ │
│  │  ├─ users/views.py (Authentication)                      │ │
│  │  └─ analytics/views.py (CSV & Statistics)                │ │
│  └───────────────┬──────────────────────────────────────────┘  │
│                  │                                              │
│  ┌───────────────▼────────────────────────────────────────┐    │
│  │               SERIALIZER LAYER                         │    │
│  │  ├─ Request Validation                                 │    │
│  │  ├─ Data Transformation                                │    │
│  │  └─ Response Formatting                                │    │
│  └───────────────┬────────────────────────────────────────┘    │
│                  │                                              │
│  ┌───────────────▼────────────────────────────────────────┐    │
│  │                SERVICE LAYER                           │    │
│  │  analytics/services.py                                 │    │
│  │  ├─ CSV Validation                                     │    │
│  │  ├─ Pandas Processing                                  │    │
│  │  └─ Statistics Computation                             │    │
│  └───────────────┬────────────────────────────────────────┘    │
│                  │                                              │
│  ┌───────────────▼────────────────────────────────────────┐    │
│  │                   MODEL LAYER                          │    │
│  │  ├─ User (Django built-in)                             │    │
│  │  └─ CSVDataset (custom)                                │    │
│  │      ├─ Signal: manage_user_dataset_limit              │    │
│  │      └─ Auto-cleanup (keep last 5)                     │    │
│  └───────────────┬────────────────────────────────────────┘    │
└──────────────────┼─────────────────────────────────────────────┘
                   │
┌──────────────────▼─────────────────────────────────────────────┐
│                    DATA LAYER                                  │
│  ┌────────────────────────┐  ┌──────────────────────────────┐ │
│  │   SQLite Database      │  │   File Storage               │ │
│  │   ├─ Users             │  │   media/csv_uploads/         │ │
│  │   └─ CSVDatasets       │  │   └─ uploaded CSV files      │ │
│  └────────────────────────┘  └──────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### 1. API Endpoints Layer
- **Purpose:** Entry points for client requests
- **Technology:** Django REST Framework views
- **Authentication:** HTTP Basic Auth (username:password)

### 2. Middleware Layer
- **Authentication:** Validates user credentials
- **CSRF Protection:** Protects against cross-site request forgery
- **Security:** Adds security headers, manages sessions

### 3. View Layer
- **users/views.py:** Handles login/logout
- **analytics/views.py:** Handles CSV upload, dataset CRUD, statistics
- **Responsibility:** Request handling, response building

### 4. Serializer Layer
- **Validation:** Ensures data meets requirements
- **Transformation:** Converts between JSON and Python objects
- **Response Formatting:** Structures API responses

### 5. Service Layer
- **CSV Processing:** Reads and validates CSV files
- **Pandas Integration:** Performs data analysis
- **Statistics Computation:** Calculates averages, min, max by type

### 6. Model Layer
- **User:** Django's built-in user model
- **CSVDataset:** Custom model for CSV metadata and statistics
- **Signals:** Auto-cleanup mechanism

### 7. Data Layer
- **SQLite:** Stores user and dataset metadata
- **File Storage:** Stores uploaded CSV files

## Data Flow: CSV Upload

```
1. Client sends CSV file with Basic Auth
          ↓
2. Authentication middleware validates user
          ↓
3. View receives request
          ↓
4. Serializer validates file (type, size)
          ↓
5. Create CSVDataset instance (status: processing)
          ↓
6. Save file to media/csv_uploads/
          ↓
7. Service layer processes CSV:
   ├─ Read file with Pandas
   ├─ Validate columns and data
   ├─ Compute statistics by type
   └─ Store in JSONField
          ↓
8. Update dataset status to 'completed'
          ↓
9. Signal checks if user has > 5 datasets
          ↓
10. If yes, delete oldest datasets
          ↓
11. Return response with statistics
```

## Request/Response Flow

### Example: Upload CSV

**Request:**
```http
POST /api/analytics/csv/upload/ HTTP/1.1
Host: 127.0.0.1:8000
Authorization: Basic YWRtaW46cGFzc3dvcmQ=
Content-Type: multipart/form-data

file=<binary CSV data>
```

**Processing:**
1. BasicAuthentication validates credentials
2. MultiPartParser parses file upload
3. CSVUploadSerializer validates file
4. View creates CSVDataset instance
5. CSVProcessingService processes file
6. Statistics computed with Pandas
7. Signal auto-deletes old datasets if needed

**Response:**
```json
{
  "message": "CSV uploaded and processed successfully.",
  "dataset_id": 1,
  "file_name": "equipment.csv",
  "status": "completed",
  "row_count": 30,
  "statistics": {
    "total_equipment_count": 30,
    "by_type": { ... },
    "overall_averages": { ... }
  }
}
```

## Database Schema

### User (Django built-in)
```sql
- id (PK)
- username (unique)
- password (hashed)
- email
- first_name
- last_name
- is_staff
- is_active
- date_joined
```

### CSVDataset
```sql
- id (PK)
- file_name (varchar 255)
- file (varchar 100) → file path
- uploaded_by_id (FK → User.id)
- uploaded_at (datetime)
- row_count (int, nullable)
- status (varchar 20) → processing/completed/failed
- statistics (json, nullable)
- error_log (text, nullable)
- processed_at (datetime, nullable)

INDEX: uploaded_by_id
INDEX: uploaded_at
```

## File Structure

```
backend/
├── config/              # Django project settings
│   ├── settings.py      # Configuration
│   ├── urls.py          # Root URL routing
│   └── wsgi.py          # WSGI entry point
│
├── analytics/           # Analytics app
│   ├── models.py        # CSVDataset model
│   ├── serializers.py   # DRF serializers
│   ├── views.py         # API views (5 endpoints)
│   ├── services.py      # Business logic
│   ├── urls.py          # URL routing
│   ├── admin.py         # Admin configuration
│   └── apps.py          # App configuration
│
├── users/               # User authentication app
│   ├── serializers.py   # User serializers
│   ├── views.py         # Auth views (2 endpoints)
│   ├── urls.py          # URL routing
│   └── apps.py          # App configuration
│
└── media/               # Uploaded files
    └── csv_uploads/     # CSV storage
```

## Security Architecture

### Authentication
- **Method:** HTTP Basic Authentication
- **Transmission:** Base64 encoded username:password
- **Storage:** Hashed passwords (Django PBKDF2)

### Authorization
- **Per-user isolation:** Users see only their own datasets
- **Query filtering:** All queries filtered by `uploaded_by=request.user`

### Data Validation
- **File type:** Only .csv files allowed
- **File size:** Maximum 10MB
- **CSV structure:** Required columns enforced
- **Numeric values:** Non-negative validation

### CSRF Protection
- Django middleware enabled
- CSRF token required for state-changing operations

## Performance Considerations

### Optimization Techniques
1. **Database Indexing:** Foreign keys and date fields indexed
2. **Query Optimization:** Select related/prefetch used where needed
3. **File Streaming:** Large files processed in chunks
4. **Signal Efficiency:** Auto-cleanup runs asynchronously with save

### Scalability
- **SQLite limitations:** Good for development, use PostgreSQL for production
- **File storage:** Use S3/Cloudinary for production
- **Async processing:** Can add Celery later if needed
- **Caching:** Redis can be added for frequently accessed data

## Error Handling

### Validation Errors (400)
- Missing CSV columns
- Invalid numeric values
- Negative values
- Wrong file type

### Authentication Errors (401)
- Invalid credentials
- Missing authentication

### Not Found Errors (404)
- Dataset doesn't exist
- User doesn't own dataset

### Server Errors (500)
- File processing failures
- Database errors

## Monitoring Points

### Application Logs
- CSV processing success/failure
- User authentication attempts
- Dataset creation/deletion
- Error stack traces

### Metrics to Track
- API response times
- CSV processing duration
- Database query performance
- File storage usage
- Active users
- Datasets per user

## Deployment Architecture

```
┌─────────────────────┐
│   Render.com        │
│   ┌─────────────┐   │
│   │ Web Service │   │
│   │  (Gunicorn) │   │
│   └──────┬──────┘   │
│          │          │
│   ┌──────▼──────┐   │
│   │   Django    │   │
│   │     App     │   │
│   └──────┬──────┘   │
│          │          │
│   ┌──────▼──────┐   │
│   │   SQLite    │   │
│   │ (ephemeral) │   │
│   └─────────────┘   │
└─────────────────────┘
         │
         │ (For production use:)
         ▼
┌─────────────────────┐
│   AWS S3 / Cloud    │
│   File Storage      │
└─────────────────────┘
```

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Web Framework | Django 4.2.7 | Core framework |
| API Framework | DRF 3.14.0 | REST API |
| Database | SQLite | Data storage |
| Data Processing | Pandas 2.1.3 | CSV analysis |
| Web Server | Gunicorn | Production WSGI |
| File Storage | Local/S3 | Media files |
| Authentication | Basic Auth | User auth |

## Design Patterns Used

1. **MVT (Model-View-Template):** Django's architecture
2. **Service Layer:** Business logic separation
3. **Serializer Pattern:** Data validation and transformation
4. **Signal Pattern:** Event-driven auto-cleanup
5. **Repository Pattern:** Django ORM abstraction
6. **RESTful API:** Resource-based endpoints

## Future Extensibility

The architecture supports future enhancements:
- ✅ JWT authentication (replace BasicAuth)
- ✅ Celery for async processing
- ✅ Redis for caching
- ✅ PostgreSQL for production
- ✅ WebSocket for real-time updates
- ✅ Additional equipment CRUD endpoints
- ✅ Advanced analytics features
- ✅ Export to Excel/PDF
- ✅ Scheduled reports

---

**This architecture is production-ready for the screening scope and designed for future growth.**

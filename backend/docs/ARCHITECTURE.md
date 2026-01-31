# System Architecture Design
## Chemical Equipment Parameter Visualizer

**Version:** 1.0  
**Date:** January 29, 2026  
**Author:** Senior Backend Architect

---

## Table of Contents
1. [Folder Structure](#1-folder-structure)
2. [Database Model Schema](#2-database-model-schema)
3. [REST API Endpoints](#3-rest-api-endpoints)
   - [3.0 API Scope Analysis](#30-api-scope-analysis-for-intern-screening)
4. [Authentication Approach](#4-authentication-approach)
5. [Data Flow Diagrams](#5-data-flow-diagram-textual)
6. [Assumptions](#6-clear-assumptions)

---

## 1. FOLDER STRUCTURE

```
chemical-equipment-visualizer/
│
├── backend/                          # Django REST API Backend
│   ├── config/                       # Django project configuration
│   │   ├── __init__.py
│   │   ├── settings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # Base settings
│   │   │   ├── development.py       # Dev-specific settings
│   │   │   └── production.py        # Prod-specific settings
│   │   ├── urls.py                  # Root URL configuration
│   │   ├── wsgi.py
│   │   └── asgi.py
│   │
│   ├── apps/
│   │   ├── equipment/               # Equipment management app
│   │   │   ├── __init__.py
│   │   │   ├── models.py           # Database models
│   │   │   ├── serializers.py      # DRF serializers
│   │   │   ├── views.py            # API views
│   │   │   ├── urls.py             # App-specific URLs
│   │   │   ├── permissions.py      # Custom permissions
│   │   │   └── admin.py
│   │   │
│   │   ├── analytics/               # Analytics & CSV processing
│   │   │   ├── __init__.py
│   │   │   ├── services.py         # Pandas analytics logic
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   └── urls.py
│   │   │
│   │   └── users/                   # User management
│   │       ├── __init__.py
│   │       ├── models.py           # Custom user model
│   │       ├── serializers.py
│   │       ├── views.py
│   │       └── urls.py
│   │
│   ├── utils/                       # Shared utilities
│   │   ├── __init__.py
│   │   ├── csv_processor.py        # CSV import/export utilities
│   │   ├── validators.py           # Custom validators
│   │   └── exceptions.py           # Custom exceptions
│   │
│   ├── media/                       # User-uploaded files
│   │   └── csv_uploads/
│   │
│   ├── static/                      # Static files
│   ├── db.sqlite3                   # SQLite database
│   ├── manage.py
│   ├── requirements.txt
│   └── .env                         # Environment variables
│
├── web-frontend/                    # React Web Application
│   ├── public/
│   │   ├── index.html
│   │   └── favicon.ico
│   │
│   ├── src/
│   │   ├── api/                    # API service layer
│   │   │   ├── axios.js           # Axios configuration
│   │   │   ├── authService.js     # Authentication APIs
│   │   │   ├── equipmentService.js # Equipment APIs
│   │   │   └── analyticsService.js # Analytics APIs
│   │   │
│   │   ├── components/             # Reusable components
│   │   │   ├── common/
│   │   │   │   ├── Navbar.jsx
│   │   │   │   ├── Sidebar.jsx
│   │   │   │   └── Loading.jsx
│   │   │   │
│   │   │   ├── equipment/
│   │   │   │   ├── EquipmentList.jsx
│   │   │   │   ├── EquipmentDetail.jsx
│   │   │   │   ├── EquipmentForm.jsx
│   │   │   │   └── EquipmentCard.jsx
│   │   │   │
│   │   │   └── analytics/
│   │   │       ├── ChartViewer.jsx
│   │   │       ├── StatisticsPanel.jsx
│   │   │       └── CSVUploader.jsx
│   │   │
│   │   ├── pages/                  # Page components
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── EquipmentPage.jsx
│   │   │   └── AnalyticsPage.jsx
│   │   │
│   │   ├── hooks/                  # Custom React hooks
│   │   │   ├── useAuth.js
│   │   │   ├── useEquipment.js
│   │   │   └── useAnalytics.js
│   │   │
│   │   ├── context/                # Context providers
│   │   │   └── AuthContext.jsx
│   │   │
│   │   ├── utils/                  # Utility functions
│   │   │   ├── constants.js
│   │   │   ├── validators.js
│   │   │   └── formatters.js
│   │   │
│   │   ├── App.jsx
│   │   ├── index.js
│   │   └── routes.js
│   │
│   ├── package.json
│   ├── .env
│   └── .gitignore
│
└── desktop-frontend/                # PyQt5 Desktop Application (SIMPLIFIED)
    ├── src/
    │   ├── ui/                     # UI components
    │   │   ├── __init__.py
    │   │   ├── main_window.py     # Main application window
    │   │   ├── login_dialog.py    # Login dialog
    │   │   ├── upload_tab.py      # CSV upload tab
    │   │   └── analytics_tab.py   # Analytics/visualization tab
    │   │
    │   ├── api/                    # API client layer (same as web)
    │   │   ├── __init__.py
    │   │   ├── client.py          # Base API client with Basic Auth
    │   │   ├── auth_api.py        # Authentication APIs
    │   │   └── analytics_api.py   # Analytics/CSV APIs
    │   │
    │   ├── utils/                  # Utilities
    │   │   ├── __init__.py
    │   │   ├── config.py          # Server URL configuration
    │   │   └── validators.py      # Input validation
    │   │
    │   ├── widgets/                # Custom widgets
    │   │   ├── __init__.py
    │   │   ├── chart_widget.py    # Matplotlib charts
    │   │   └── table_widget.py    # CSV data table widget
    │   │
    │   ├── resources/              # UI resources
    │   │   ├── icons/
    │   │   └── styles/
    │   │       └── stylesheet.qss
    │   │
    │   └── main.py                 # Application entry point
    │
    ├── requirements.txt
    └── config.ini                  # Server URL configuration
```

---

## 2. DATABASE MODEL SCHEMA

> **SIMPLIFIED FOR INTERN SCREENING**: This implementation focuses on CSV upload and analytics without persistent equipment storage. Equipment CRUD and history tracking are marked as future enhancements.

---

## 2.0 MODEL SIMPLIFICATION RATIONALE

### Current Implementation: CSV-Focused Analytics Tool

The intern screening implementation is simplified to focus on:
1. **CSV Upload & Processing** - Core Pandas integration
2. **Summary Statistics** - Aggregated analytics (no per-equipment storage)
3. **Upload History** - Track last 5 datasets for comparison
4. **User Authentication** - Basic auth with roles

### Why This Simplification?

#### ✅ **Reduces Complexity (60% fewer models)**
- **2 models** instead of 5 (User + CSV Upload tracking)
- No relational complexity (no FK dependencies between Equipment/History)
- Single app focus (analytics) instead of multi-app architecture
- Faster migrations and development

#### ✅ **Focuses on Core Skills**
- **Pandas mastery**: CSV parsing, data validation, aggregation
- **File handling**: Upload, storage, validation
- **Django basics**: Models, views, serializers
- **Statistics**: Group-by operations, min/max/avg calculations

#### ✅ **Complete User Experience**
- Upload CSV → View statistics → Compare datasets → Download results
- No need for per-record CRUD operations
- Demonstrates analytical capabilities without inventory management overhead

#### ✅ **Production-Grade Thinking**
- Retains upload history (last 5 datasets with auto-cleanup)
- Stores calculated statistics for quick retrieval
- Error logging for debugging
- Clear migration path to full Equipment CRUD

---

## 2.0.1 DESKTOP APP SIMPLIFICATION RATIONALE

### Current Implementation: Thin Client, Online-Only

The PyQt5 desktop app is simplified to be an **online-only thin client** that consumes the same REST APIs as the web frontend.

### Why No Offline Features?

#### ✅ **Reduces Complexity (~50% less desktop code)**
- **No local database**: No SQLite caching, no ORM models
- **No sync logic**: No conflict resolution, data merging, or queue management
- **No state management**: No offline/online detection, pending operations
- **Simpler architecture**: Desktop and web share identical API interaction patterns

#### ✅ **Focuses on Core PyQt5 Skills**
- **UI development**: QMainWindow, QTableWidget, QDialog layouts
- **HTTP requests**: REST API consumption with Basic Auth
- **Data visualization**: Matplotlib charts embedded in PyQt widgets
- **File handling**: CSV file picker and upload with multipart/form-data
- **Error handling**: Network errors, API validation responses

#### ✅ **Realistic Constraints**
- **Time-boxed implementation**: Offline sync adds ~8-10 hours to development
- **Demo environment**: Screening tasks assume stable internet connection
- **Core competency test**: Desktop app demonstrates GUI programming, not distributed systems
- **Clear scope boundary**: Separates "nice-to-have" from "must-have" features

#### ✅ **Production Migration Path**
When ready to add offline features:
1. Add local SQLite database with same models as backend
2. Implement sync queue (POST/PATCH/DELETE operations stored when offline)
3. Add conflict resolution logic (last-write-wins or merge strategies)
4. Implement background sync thread with retry logic
5. Add network connectivity detection

**Estimated effort**: 10-12 hours for basic offline sync + 5-8 hours for conflict resolution

### Desktop App Feature Comparison

| Feature | Current (Screening) | Future (Production) |
|---------|---------------------|---------------------|
| **CSV Upload** | ✅ Online via API | ✅ Same + offline queue |
| **View Statistics** | ✅ Fetch from server | ✅ Same + local cache |
| **Data Visualization** | ✅ Matplotlib charts | ✅ Same + cached data |
| **Authentication** | ✅ Basic Auth (memory) | ✅ Token auth + secure storage |
| **Local Storage** | ❌ None | ✅ SQLite cache |
| **Offline Mode** | ❌ Not implemented | ✅ View cached data |
| **Sync Logic** | ❌ Not implemented | ✅ Bi-directional sync |
| **Conflict Resolution** | ❌ Not needed | ✅ Merge strategies |

---

## 2.0.2 IMPLEMENTED FEATURES VS DESIGNED ARCHITECTURE

### Overview

This architecture document presents a **production-grade design** with a **controlled implementation scope** for intern screening. The full design demonstrates systems thinking and scalability planning, while the implemented subset validates core technical competencies within realistic time constraints.

---

### Implemented Features (Current Demo - 12-16 Hours)

#### Backend (Django + DRF)
- ✅ **User Authentication**: Django's built-in user model with role-based profiles
- ✅ **Basic Auth**: HTTP Basic Authentication for simplicity
- ✅ **CSV Upload API**: Multipart file upload with validation
- ✅ **Pandas Processing**: CSV parsing, validation, statistical aggregation
- ✅ **Statistics Storage**: JSONField for calculated statistics (min/max/avg/count)
- ✅ **Dataset Management**: List, retrieve, delete uploaded datasets
- ✅ **Auto-Cleanup**: Keep last 5 datasets per user
- ✅ **6 REST Endpoints**: 2 auth + 4 analytics/CSV operations

#### Web Frontend (React)
- ✅ **Login Page**: Basic Auth credential submission
- ✅ **CSV Upload Form**: File picker with validation feedback
- ✅ **Statistics Dashboard**: Display aggregated statistics from uploaded CSVs
- ✅ **Data Visualization**: Charts for equipment parameters (Recharts/Chart.js)
- ✅ **Dataset History**: View/compare last 5 uploaded datasets
- ✅ **Responsive Design**: Desktop/tablet layout

#### Desktop Frontend (PyQt5)
- ✅ **Login Dialog**: Username/password authentication
- ✅ **CSV Upload Tab**: File picker and upload via REST API
- ✅ **Analytics Tab**: Display statistics and charts (Matplotlib)
- ✅ **Online-Only Mode**: All data fetched from server (no local caching)
- ✅ **REST API Consumer**: Reuses same endpoints as web frontend

---

### Designed but Not Implemented Features (Future Enhancements)

#### Database Models (4 Future Models)
- ⏳ **Equipment Model**: Per-equipment CRUD operations with full parameter storage
- ⏳ **Parameter History Model**: Time-series tracking of parameter changes
- ⏳ **Alert Rules Model**: Configurable thresholds for parameter monitoring
- ⏳ **Alert History Model**: Log of triggered alerts with acknowledgment workflow

#### API Endpoints (16 Future Endpoints)
- ⏳ **Equipment CRUD**: Create, update, delete individual equipment (4 endpoints)
- ⏳ **Parameter History**: Retrieve time-series data for equipment (2 endpoints)
- ⏳ **Advanced Analytics**: Anomaly detection, trend analysis, forecasting (4 endpoints)
- ⏳ **Alert Management**: CRUD for alert rules and history (4 endpoints)
- ⏳ **Async CSV Processing**: Background job tracking with Celery (2 endpoints)

#### Authentication & Security
- ⏳ **Token-Based Auth**: JWT with refresh tokens for production
- ⏳ **Session Management**: Token expiration, refresh, and blacklisting
- ⏳ **Secure Storage**: OS keychain integration for desktop app credentials
- ⏳ **Rate Limiting**: Django REST throttling to prevent abuse

#### Desktop App Enhancements
- ⏳ **Offline Mode**: Local SQLite cache for viewing data without connectivity
- ⏳ **Sync Logic**: Bi-directional sync with conflict resolution
- ⏳ **Background Workers**: Async data sync and upload queue
- ⏳ **Network Detection**: Automatic online/offline state management

#### Operational Features
- ⏳ **Real-Time Updates**: WebSocket integration for live data streaming
- ⏳ **Export Functionality**: PDF reports, Excel exports, data download
- ⏳ **Audit Logging**: Track all CRUD operations with user attribution
- ⏳ **Advanced Permissions**: Granular role-based access control (RBAC)

---

### Reasoning for Scope Control

#### Time-Boxing for Intern Screening
- **Implemented Scope**: Demonstrates core skills in **12-16 hours** of focused development
- **Skills Validated**: Django, DRF, Pandas, React, PyQt5, REST APIs, data processing
- **Avoids Over-Engineering**: Eliminates features requiring distributed systems knowledge (Celery, WebSockets, caching strategies)

#### Risk Mitigation
- **Prevents Scope Creep**: Clear boundary between "must-have" and "nice-to-have"
- **Reduces Complexity**: No async processing, no conflict resolution, no caching layers
- **Simplifies Testing**: Synchronous flows easier to validate and debug

#### Production-Ready Thinking
- **Comprehensive Design**: Demonstrates ability to architect scalable systems
- **Migration Paths**: Documents how each future feature integrates into existing architecture
- **Technical Debt Awareness**: Explicitly notes trade-offs (e.g., "Synchronous CSV processing acceptable for demo, async with Celery for production")

#### Learning-Oriented
- **Focuses on Fundamentals**: Master core frameworks before tackling distributed systems
- **Incremental Complexity**: Each future feature adds one new concept (async, caching, real-time)
- **Clear Documentation**: Architecture serves as learning roadmap for system evolution

---

### How the System Can Scale in Future

#### Phase 1: Current Implementation (Weeks 1-2)
- **Capacity**: 50-100 concurrent users, <10k CSV rows per upload
- **Architecture**: Monolithic Django backend, SQLite database, synchronous processing
- **Deployment**: Single VPS server with Nginx reverse proxy
- **Limitations**: No horizontal scaling, synchronous processing blocks on large CSVs

#### Phase 2: Token Auth + Equipment CRUD (Weeks 3-4)
- **Add**: 4 database models (Equipment, History, Alerts)
- **Add**: 16 REST endpoints for full CRUD operations
- **Migration**: Zero downtime (additive models, backward-compatible APIs)
- **Benefit**: Transition from "CSV analytics tool" to "Equipment management system"

#### Phase 3: Async Processing (Weeks 5-6)
- **Add**: Celery + Redis for background job processing
- **Add**: 2 endpoints for async CSV import tracking
- **Migration**: Replace synchronous `POST /analytics/csv/upload/` with async variant
- **Benefit**: Handle large CSVs (>50k rows) without blocking API server

#### Phase 4: Desktop Offline Mode (Weeks 7-8)
- **Add**: Local SQLite cache in desktop app
- **Add**: Sync queue with conflict resolution (last-write-wins or 3-way merge)
- **Migration**: Transparent to backend (same REST APIs, client-side caching)
- **Benefit**: Desktop users work offline, sync changes on reconnect

#### Phase 5: Production Hardening (Weeks 9-12)
- **Database**: Migrate SQLite → PostgreSQL for multi-user concurrency
- **Caching**: Add Redis for API response caching and session storage
- **Real-Time**: Implement WebSockets with Django Channels for live updates
- **Monitoring**: Add Sentry (error tracking), Prometheus (metrics), ELK (logs)
- **Deployment**: Dockerize services, Kubernetes orchestration, CI/CD pipelines

#### Horizontal Scaling Path
- **API Layer**: Stateless Django containers behind load balancer (Nginx/HAProxy)
- **Database**: PostgreSQL with read replicas for analytics queries
- **Background Jobs**: Multiple Celery workers with auto-scaling
- **File Storage**: Migrate local file storage → S3/MinIO for distributed access
- **CDN**: Serve React frontend via CloudFront/Cloudflare

---

### Architecture Decision Records (ADRs)

#### ADR-001: SQLite for Screening, PostgreSQL for Production
- **Context**: Intern screening requires fast setup with minimal infrastructure
- **Decision**: Use SQLite for demo; design schema compatible with PostgreSQL
- **Consequences**: No distributed transactions; migrate to PostgreSQL when >100 concurrent users

#### ADR-002: Synchronous CSV Processing for Demo
- **Context**: Celery adds 4-6 hours setup time (Redis, workers, monitoring)
- **Decision**: Process CSVs synchronously; limit file size to 10 MB / 5k rows
- **Consequences**: API blocks during processing; acceptable for demo data size

#### ADR-003: Basic Auth Before Token Auth
- **Context**: Token auth requires token model, refresh logic, expiration handling
- **Decision**: Implement Basic Auth first, document token migration path
- **Consequences**: Credentials sent with every request; requires HTTPS in production

#### ADR-004: Desktop Online-Only Mode
- **Context**: Offline sync adds ~15-20 hours (SQLite, queue, conflict resolution)
- **Decision**: Desktop app fetches data from server in real-time
- **Consequences**: No offline viewing; demonstrates PyQt5 + REST APIs integration

---

## 2.1 User Model (Django's built-in User + custom fields)

**Table: `auth_user` (Django default)** ✅ IMPLEMENTED
```
├── id (PK, AutoField)
├── username (CharField, unique)
├── email (EmailField, unique)
├── password (CharField, hashed)
├── first_name (CharField)
├── last_name (CharField)
├── is_active (BooleanField)
├── is_staff (BooleanField)
├── date_joined (DateTimeField)
└── last_login (DateTimeField)
```

**Table: `users_userprofile` (Custom extension)** ✅ IMPLEMENTED
```
├── id (PK, AutoField)
├── user (OneToOneField → auth_user)
├── role (CharField: 'admin', 'engineer', 'viewer')
├── department (CharField, nullable)
└── created_at (DateTimeField)
```

---

## 2.2 CSV Dataset Model (Core Analytics Model)

**Table: `analytics_csvdataset`** ✅ IMPLEMENTED

Stores uploaded CSV files and their computed statistics.

```
├── id (PK, AutoField)
├── file_name (CharField, max_length=255)
│   Original filename (e.g., "equipment_data_jan2026.csv")
│
├── file_path (FileField, upload_to='csv_uploads/')
│   Stored file location on server
│
├── uploaded_by (ForeignKey → auth_user, on_delete=SET_NULL, nullable)
│   User who uploaded the dataset
│
├── uploaded_at (DateTimeField, auto_now_add)
│   Timestamp of upload
│
├── row_count (IntegerField, default=0)
│   Total number of equipment records in CSV
│
├── status (CharField, choices, default='processing')
│   Choices: 'processing', 'completed', 'failed'
│   Processing status of the upload
│
├── error_log (TextField, blank=True)
│   Validation errors or processing issues
│
├── statistics (JSONField, default=dict)
│   Computed summary statistics stored as JSON:
│   {
│     "total_equipment": 15,
│     "by_type": {
│       "Pump": {
│         "count": 4,
│         "avg_flowrate": 126.75,
│         "avg_pressure": 5.50,
│         "avg_temperature": 115.50,
│         "min_flowrate": 120.00,
│         "max_flowrate": 132.00
│       },
│       "Compressor": { ... }
│     },
│     "overall": {
│       "avg_flowrate": 118.33,
│       "avg_pressure": 6.15,
│       "avg_temperature": 115.40
│     }
│   }
│
└── processed_at (DateTimeField, nullable)
    Timestamp when processing completed

Indexes:
- uploaded_at (DESC) for recent uploads query
- uploaded_by + uploaded_at for user history

Model Methods:
- calculate_statistics(): Compute stats using Pandas
- cleanup_old_datasets(): Keep only last 5, delete older ones
```

**Design Decisions:**
1. **JSONField for Statistics**: Avoids separate tables for stats, flexible schema
2. **File Retention**: Actual CSV files stored for re-processing or export
3. **Auto-Cleanup**: Database trigger or periodic task keeps last 5 datasets
4. **No Equipment Storage**: CSV is processed on-the-fly, stats are cached

---

## 2.3 REMOVED MODELS (Marked as Future Enhancements)

### 2.3.1 Equipment Model ⏳ FUTURE ENHANCEMENT

> **Not implemented in current scope**. Statistics are computed from uploaded CSV files without persisting individual equipment records.

**Table: `equipment_equipment` (Future Implementation)**
```
├── id (PK, AutoField)
├── equipment_name (CharField, max_length=100, unique)
├── equipment_type (CharField, choices, max_length=50)
│   Choices: 'Pump', 'Compressor', 'Valve', 'HeatExchanger', 
│            'Reactor', 'Condenser', 'Other'
├── flowrate (DecimalField, max_digits=10, decimal_places=2)
├── pressure (DecimalField, max_digits=10, decimal_places=2)
├── temperature (DecimalField, max_digits=10, decimal_places=2)
├── status (CharField, choices, default='active')
│   Choices: 'active', 'maintenance', 'inactive'
├── installation_date (DateField, nullable)
├── last_maintenance_date (DateField, nullable)
├── notes (TextField, blank=True)
├── created_by (ForeignKey → auth_user, nullable)
├── created_at (DateTimeField, auto_now_add)
└── updated_at (DateTimeField, auto_now)
```

**Why Future:**
- Adds relational complexity (FK to users, potential M2M relationships)
- Requires full CRUD API endpoints (5 endpoints)
- Manual data entry vs bulk CSV import focus
- Inventory management overhead for analytics tool

**Migration Path:**
1. Add Equipment model with all fields
2. Update CSV upload to parse and create Equipment records
3. Link statistics to Equipment table instead of JSON storage
4. Add CRUD endpoints (GET, POST, PATCH, DELETE)

---

### 2.3.2 Equipment Parameter History Model ⏳ FUTURE ENHANCEMENT

> **Not implemented in current scope**. Time-series tracking is an advanced feature requiring complex queries and visualization.

**Table: `equipment_parameterhistory` (Future Implementation)**
```
├── id (PK, AutoField)
├── equipment (ForeignKey → equipment_equipment, on_delete=CASCADE)
├── flowrate (DecimalField, max_digits=10, decimal_places=2)
├── pressure (DecimalField, max_digits=10, decimal_places=2)
├── temperature (DecimalField, max_digits=10, decimal_places=2)
├── recorded_by (ForeignKey → auth_user, nullable)
└── timestamp (DateTimeField, auto_now_add)

Indexes:
- equipment_id + timestamp (for time-series queries)
```

**Why Future:**
- Requires Equipment model as prerequisite
- Complex time-series queries and charting libraries
- High data volume (potentially millions of history records)
- Advanced analytics (trends, predictions, anomaly detection)

**Migration Path:**
1. Implement Equipment model first
2. Add ParameterHistory model with FK to Equipment
3. Create background job to record parameters periodically
4. Add trend analysis endpoints with date filtering
5. Implement charting in frontend (line graphs, time-series)

---

### 2.3.3 CSV Import History Model (Replaced by CSVDataset)

> **Merged into CSVDataset model**. The original `analytics_csvimport` model was designed for async job tracking (Celery). Current implementation uses synchronous processing with simplified tracking.

**Original Table: `analytics_csvimport` (Not Implemented)**
```
├── id (PK, AutoField)
├── file_name (CharField, max_length=255)
├── file_path (FileField)
├── records_imported (IntegerField)
├── records_failed (IntegerField)
├── status (CharField, choices)
│   Choices: 'pending', 'processing', 'completed', 'failed'
├── error_log (TextField, blank=True)
├── imported_by (ForeignKey → auth_user)
├── created_at (DateTimeField, auto_now_add)
└── completed_at (DateTimeField, nullable)
```

**Changes in CSVDataset:**
- Removed `records_imported` / `records_failed` → Replaced with `row_count` (simpler)
- Removed `pending` status → Only `processing`, `completed`, `failed` (synchronous)
- Added `statistics` JSONField → Store computed analytics
- Renamed `created_at` → `uploaded_at` (clearer naming)
- Added `processed_at` → Track processing completion time

---

### 2.3.4 API Access Token Model ⏳ FUTURE ENHANCEMENT

> **Not implemented in current scope**. Token-based authentication is planned for production but current implementation uses Basic Authentication.

**Table: `users_apitoken` (Future Implementation)**
```
├── id (PK, AutoField)
├── user (ForeignKey → auth_user)
├── token (CharField, unique, max_length=64)
├── client_type (CharField, choices)
│   Choices: 'web', 'desktop'
├── created_at (DateTimeField, auto_now_add)
├── last_used (DateTimeField, nullable)
└── expires_at (DateTimeField, nullable)
```

**Why Future:**
- Basic Auth sufficient for demo/screening
- Token management adds complexity (generation, expiration, refresh)
- Requires additional endpoints (token creation, validation)
- Production feature for scalability and security

**Migration Path:**
1. Add `users_apitoken` model
2. Create token generation endpoint (`POST /auth/token/`)
3. Switch DRF authentication from `BasicAuthentication` to `TokenAuthentication`
4. Update frontend to store and use tokens
5. Implement token refresh mechanism

---

## 2.4 MODEL COMPARISON: Current vs Future

| Model | Current Status | Purpose | Records Estimated |
|-------|----------------|---------|-------------------|
| **auth_user** | ✅ Implemented | User authentication | <50 users |
| **users_userprofile** | ✅ Implemented | Role-based access | <50 profiles |
| **analytics_csvdataset** | ✅ Implemented | CSV tracking + stats | 5 (auto-cleanup) |
| **equipment_equipment** | ⏳ Future | Equipment inventory | 1000-10,000 |
| **equipment_parameterhistory** | ⏳ Future | Time-series data | 100,000-1,000,000 |
| **users_apitoken** | ⏳ Future | Token auth | <200 tokens |

**Storage Impact:**
- **Current**: <1 MB database size (5 CSV metadata + stats)
- **Future**: 100 MB - 1 GB (with equipment inventory + history)

---

## 2.5 README DOCUMENTATION: DATA MODEL SIMPLIFICATION

### Overview

This Chemical Equipment Parameter Visualizer uses a **simplified data model** focused on CSV analytics rather than persistent equipment storage. This design choice is intentional for the intern screening scope.

### Current Implementation (2 Models)

#### **1. User Management**
- `auth_user` (Django built-in): User authentication
- `users_userprofile`: Role-based access control (Admin, Engineer, Viewer)

#### **2. CSV Analytics**
- `analytics_csvdataset`: Stores uploaded CSV files and computed statistics

### How It Works

```
1. User uploads CSV file
   ↓
2. Backend validates CSV structure (Pandas)
   ↓
3. Compute summary statistics (group by equipment type)
   ↓
4. Store statistics in JSONField (CSVDataset.statistics)
   ↓
5. Keep last 5 uploads, auto-delete older ones
   ↓
6. Return statistics to frontend for visualization
```

### What's NOT Stored

❌ **Individual Equipment Records**: CSV rows are processed but not saved to database  
❌ **Parameter History**: No time-series tracking of flowrate/pressure/temperature  
❌ **Equipment CRUD**: Cannot edit individual equipment via API

### Why This Approach?

✅ **Simpler for Screening**: Focuses on Pandas + Django integration  
✅ **Faster Development**: 2 models vs 5 models (60% reduction)  
✅ **Analytics Focus**: Demonstrates data analysis skills over CRUD operations  
✅ **No Data Bloat**: Only stores aggregated stats, not raw records  
✅ **Clear Upgrade Path**: Easy to add Equipment model later

### Example: CSVDataset Record

```json
{
  "id": 3,
  "file_name": "equipment_data_jan2026.csv",
  "uploaded_by": "john_doe",
  "uploaded_at": "2026-01-29T10:30:00Z",
  "row_count": 15,
  "status": "completed",
  "statistics": {
    "total_equipment": 15,
    "by_type": {
      "Pump": {
        "count": 4,
        "avg_flowrate": 126.75,
        "avg_pressure": 5.50,
        "avg_temperature": 115.50
      },
      "Compressor": {
        "count": 2,
        "avg_flowrate": 97.50,
        "avg_pressure": 8.20,
        "avg_temperature": 96.50
      }
    },
    "overall": {
      "avg_flowrate": 118.33,
      "avg_pressure": 6.15,
      "avg_temperature": 115.40
    }
  }
}
```

### Auto-Cleanup Logic

```python
# Pseudo-code for maintaining last 5 datasets
def cleanup_old_datasets():
    # Get all datasets ordered by upload date (newest first)
    all_datasets = CSVDataset.objects.order_by('-uploaded_at')
    
    # Keep first 5, delete the rest
    if all_datasets.count() > 5:
        to_delete = all_datasets[5:]
        for dataset in to_delete:
            dataset.file_path.delete()  # Delete file from disk
            dataset.delete()  # Delete database record
```

### Future Enhancement Path

When ready to add full Equipment CRUD:

1. **Add Equipment Model** (Section 2.3.1)
   - Create migration: `python manage.py makemigrations`
   - Run migration: `python manage.py migrate`

2. **Update CSV Upload Logic**
   - Parse CSV and create Equipment records
   - Link statistics to Equipment table

3. **Add CRUD Endpoints**
   - GET `/equipment/` - List all equipment
   - POST `/equipment/` - Create new equipment
   - PATCH `/equipment/{id}/` - Update equipment
   - DELETE `/equipment/{id}/` - Remove equipment

4. **Add Parameter History** (Section 2.3.2)
   - Create ParameterHistory model
   - Add background job for periodic recording
   - Implement trend analysis endpoints

---

## 3. REST API ENDPOINTS

**Base URL**: `http://localhost:8000/api/v1/`

---

## 3.0 API SCOPE ANALYSIS (FOR INTERN SCREENING)

### Overview
The full API design contains **18 endpoints**. For an intern screening project, this scope should be reduced to focus on core functionality while demonstrating essential skills.

---

### API Classification Table

| # | Endpoint | Method | Category | Status | Justification |
|---|----------|--------|----------|--------|---------------|
| 1 | `/auth/login/` | POST | Authentication | **✅ REQUIRED** | Essential for user authentication |
| 2 | `/auth/logout/` | POST | Authentication | **✅ REQUIRED** | Complete auth flow |
| 3 | `/auth/register/` | POST | Authentication | **⏳ FUTURE** | Admin can pre-create users; registration adds complexity |
| 4 | `/auth/user/me/` | GET | Authentication | **⏳ FUTURE** | User info can be returned in login response |
| 5 | `/equipment/` | GET | Equipment CRUD | **⏳ FUTURE** | **No Equipment model in simplified scope** |
| 6 | `/equipment/{id}/` | GET | Equipment CRUD | **⏳ FUTURE** | **No Equipment model in simplified scope** |
| 7 | `/equipment/` | POST | Equipment CRUD | **⏳ FUTURE** | **No Equipment model in simplified scope** |
| 8 | `/equipment/{id}/` | PUT | Equipment CRUD | **⏳ FUTURE** | **No Equipment model in simplified scope** |
| 9 | `/equipment/{id}/` | PATCH | Equipment CRUD | **⏳ FUTURE** | **No Equipment model in simplified scope** |
| 10 | `/equipment/{id}/` | DELETE | Equipment CRUD | **⏳ FUTURE** | **No Equipment model in simplified scope** |
| 11 | `/equipment/{id}/history/` | GET | Parameter History | **⏳ FUTURE** | Time-series tracking is advanced |
| 12 | `/equipment/{id}/history/` | POST | Parameter History | **⏳ FUTURE** | Time-series tracking is advanced |
| 13 | `/analytics/statistics/` | GET | Analytics | **✅ REQUIRED** | Core feature: Display aggregated data from CSV |
| 14 | `/analytics/trends/` | GET | Analytics | **⏳ FUTURE** | Time-series trends require history feature |
| 15 | `/analytics/csv/upload/` | POST | CSV Import | **✅ REQUIRED** | Core feature: Bulk import from sample CSV |
| 16 | `/analytics/csv/datasets/` | GET | CSV History | **✅ REQUIRED** | List last 5 uploaded datasets |
| 17 | `/analytics/csv/datasets/{id}/` | GET | CSV History | **✅ REQUIRED** | Get specific dataset statistics |
| 18 | `/analytics/csv/import/{id}/` | GET | CSV Import | **⏳ FUTURE** | Async status tracking adds complexity |
| 19 | `/analytics/csv/export/` | GET | CSV Export | **⏳ FUTURE** | Not in requirements; import is priority |
| 20 | `/analytics/comparison/` | GET | Analytics | **⏳ FUTURE** | Advanced feature; not core to task |
| 21 | `/metadata/equipment-types/` | GET | Metadata | **⏳ FUTURE** | Can hardcode in frontend choices |
| 22 | `/metadata/status-choices/` | GET | Metadata | **⏳ FUTURE** | Can hardcode in frontend choices |

---

### Minimal API Set for Intern Screening (6 Endpoints)

> **SIMPLIFIED MODEL**: Equipment CRUD removed. Focus on CSV upload and analytics.

#### **Authentication (2 endpoints)**
1. **POST `/api/v1/auth/login/`** - Authenticate user and establish session
2. **POST `/api/v1/auth/logout/`** - Terminate user session

#### **CSV Analytics (4 endpoints)**
3. **POST `/api/v1/analytics/csv/upload/`** - Bulk import equipment from CSV file (Pandas)
4. **GET `/api/v1/analytics/statistics/`** - Aggregate statistics by equipment type (Pandas)
5. **GET `/api/v1/analytics/csv/datasets/`** - List last 5 uploaded CSV datasets
6. **GET `/api/v1/analytics/csv/datasets/{id}/`** - Get specific dataset and its statistics

---

### Justification for Minimal Scope

#### **Why This Scope is Appropriate for Intern Screening:**

##### ✅ **Demonstrates Core Skills**
- **Django Models**: CSVDataset model with JSONField for statistics
- **Django REST Framework**: ViewSets, Serializers, Permissions
- **File Upload**: Multipart form-data handling and file storage
- **Pandas Integration**: CSV parsing, validation, and aggregation
- **Authentication**: DRF BasicAuthentication
- **Data Analysis**: Group-by operations, statistical calculations

##### ✅ **Manageable Complexity**
- **6 endpoints** can be implemented in **12-15 hours** (appropriate for screening)
- **2 database models** (User + CSVDataset) reduces migration complexity
- No async processing (Celery) or background jobs required
- No relational FK complexity (Equipment → History)
- Synchronous CSV processing (acceptable for demo data size)
- JSONField eliminates need for separate statistics tables

##### ✅ **Complete User Experience**
- Login → Upload CSV → View Statistics → Compare Datasets → Logout
- Demonstrates full workflow from authentication to data visualization
- Historical comparison (last 5 uploads) shows state management
- Both frontends (web/desktop) can consume all APIs

##### ✅ **Addresses Project Requirements**
- **"Visualizer"**: Statistics endpoint provides aggregated data for charts
- **"Parameter"**: Flowrate, Pressure, Temperature analysis from CSV
- **"CSV Analytics"**: Upload, processing, and Pandas demonstrated
- **"Hybrid App"**: Same APIs work for React and PyQt5

##### ✅ **Simplified Data Model (60% reduction)**
- No Equipment CRUD → Eliminates 5 endpoints
- No Parameter History → Eliminates 2 endpoints and complex queries
- Focus on analytics over inventory management
- CSV-centric approach: process on-the-fly, store statistics

##### ⏳ **Future Scope is Well-Documented**
- Equipment CRUD (5 endpoints) can be added when model is implemented
- Parameter history (2 endpoints) for time-series tracking
- User registration for multi-user scenarios
- Trends/comparison for advanced analytics

##### 📊 **Intern Learning Value**
Focusing on 6 endpoints allows intern to:
- Write **clean, well-tested code** instead of rushing through features
- Master **Pandas** for data processing and aggregation
- Implement **proper error handling** for file uploads
- Focus on **code quality** over quantity
- Demonstrate **analytical thinking** (statistics, data modeling)

---

### Implementation Priority Order

**Phase 1: Foundation (Required for screening - SIMPLIFIED MODEL)**
1. Setup Django project + DRF + Basic Auth
2. CSVDataset model + migrations (no Equipment model)
3. Authentication endpoints (login/logout)
4. CSV upload endpoint with Pandas processing
5. Statistics endpoint (Pandas aggregation from CSV)
6. Dataset history endpoints (list last 5, get details)
7. Auto-cleanup logic (keep last 5 datasets)

**Phase 2: Enhancement (Post-screening if adding Equipment model)**
8. Add Equipment model + migrations
9. Equipment CRUD endpoints (GET, POST, PATCH, DELETE)
10. Update CSV upload to create Equipment records
11. User registration endpoint

**Phase 3: Production Features (Beyond screening scope)**
12. Parameter history model + endpoints
13. Trends endpoint (time-series analysis)
14. Token-based authentication
15. Equipment comparison
16. Async CSV processing (Celery)
17. Real-time updates (WebSockets)

---

### Comparison: Full vs Minimal API

| Metric | Original Design | Simplified (Intern) | Reduction |
|--------|-----------------|---------------------|-----------|
| **Total Endpoints** | 20 | 6 | 70% fewer |
| **Database Models** | 5 | 2 (User + CSVDataset) | 60% fewer |
| **Estimated Hours** | 40-50 | 12-15 | 70% faster |
| **Lines of Code** | ~3000 | ~800 | 73% less |
| **CRUD Complexity** | Equipment + History | None (CSV-only) | 100% simpler |
| **External Dependencies** | Celery, Redis | None (Django + DRF + Pandas) | Minimal |
| **Learning Curve** | Steep | Gentle | More accessible |
| **MVP Completeness** | Over-specified | Lean & Focused | Analytics-first |

---

### What Gets Removed (Future Scope)

#### **1. Parameter History Tracking** (2 endpoints)
- **Why Future**: Requires time-series data model, complex queries, and charting
- **Alternative**: Current equipment state is sufficient for initial demo
- **Migration Path**: Add ParameterHistory model later, minimal API changes

#### **2. User Registration** (1 endpoint)
- **Why Future**: Admin can create users via Django Admin panel
- **Alternative**: Pre-seed users in fixtures or manually create
- **Migration Path**: Add registration serializer + view when multi-tenancy needed

#### **3. User Profile Endpoint** (1 endpoint)
- **Why Future**: User data can be included in login response
- **Alternative**: Return full user object on login
- **Migration Path**: Add dedicated endpoint when profile updates are needed

#### **4. CSV Import Status Tracking** (1 endpoint)
- **Why Future**: Requires async processing (Celery) and job queue
- **Alternative**: Synchronous upload with immediate response
- **Migration Path**: Add Celery + Redis when handling large files (>5000 rows)

#### **5. CSV Export** (1 endpoint)
- **Why Future**: Import is higher priority; export is nice-to-have
- **Alternative**: Users can view data in UI or use Django Admin
- **Migration Path**: Simple endpoint addition when needed

#### **6. Equipment Comparison** (1 endpoint)
- **Why Future**: Advanced analytical feature, not core CRUD
- **Alternative**: Statistics endpoint shows all equipment data
- **Migration Path**: Add comparison logic when UX demands it

#### **7. Trends Analysis** (1 endpoint)
- **Why Future**: Depends on parameter history feature
- **Alternative**: Current state is sufficient for screening
- **Migration Path**: Implement after history tracking is added

#### **8. Metadata Endpoints** (2 endpoints)
- **Why Future**: Equipment types and statuses can be hardcoded in frontend
- **Alternative**: Define choices in frontend constants
- **Migration Path**: Add when dynamic configuration is needed

#### **9. Full Replace (PUT)** (1 endpoint)
- **Why Future**: PATCH (partial update) covers all update scenarios
- **Alternative**: PATCH is more flexible and user-friendly
- **Migration Path**: Add PUT if strict REST compliance is required

---

### 3.1 Authentication Endpoints (✅ IMPLEMENTED - 2 endpoints)

#### **POST /api/v1/auth/login/**
Validate user credentials and return user profile. (Session-based authentication)

**Request:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "engineer",
    "department": "Operations"
  },
  "message": "Login successful"
}
```

**Errors:**
- 400: Invalid credentials
- 401: Account inactive

**Note**: For current implementation, use Basic Authentication header in subsequent requests.

---

#### **POST /api/v1/auth/logout/**
Logout and clear session.

**Request Headers:**
```
Authorization: Basic base64(username:password)
```

**Response (200 OK):**
```json
{
  "message": "Logout successful"
}
```

---

#### **POST /api/v1/auth/register/** ⏳ FUTURE SCOPE
Register a new user (admin only or open signup).

> **Note**: Not implemented in current screening scope. Admin creates users via Django Admin panel.

**Request:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "first_name": "string",
  "last_name": "string",
  "role": "engineer" | "viewer",
  "department": "string"
}
```

**Response (201 Created):**
```json
{
  "id": 2,
  "username": "new_user",
  "email": "user@example.com",
  "role": "engineer"
}
```

---

#### **GET /api/v1/auth/user/me/** ⏳ FUTURE SCOPE
Get current authenticated user's profile.

> **Note**: Not implemented in current screening scope. User data returned in login response.

**Request Headers:**
```
Authorization: Basic base64(username:password)
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "engineer",
  "department": "Operations",
  "date_joined": "2025-01-15T08:00:00Z"
}
```

---

### 3.2 Equipment Endpoints ⏳ FUTURE SCOPE (5 endpoints)

> **Note**: Equipment CRUD endpoints are NOT implemented in current screening scope. The simplified model focuses on CSV upload and statistics without persistent equipment storage. See Section 2.3.1 for Equipment model details.

**Why Not Implemented:**
- No Equipment model in current database schema
- CSV data processed on-the-fly without persisting records
- Focuses on analytical capabilities (Pandas) over CRUD operations
- Reduces implementation time by 60%

**Future Endpoints (when Equipment model is added):**
- `GET /api/v1/equipment/` - List all equipment
- `GET /api/v1/equipment/{id}/` - Equipment details
- `POST /api/v1/equipment/` - Create equipment
- `PATCH /api/v1/equipment/{id}/` - Update equipment
- `DELETE /api/v1/equipment/{id}/` - Remove equipment

---

#### **GET /api/v1/equipment/** ⏳ FUTURE SCOPE
List all equipment with optional filtering and pagination.

**Query Parameters:**
- `equipment_type` (optional): Filter by type
- `status` (optional): Filter by status
- `search` (optional): Search in equipment_name
- `page` (optional, default=1): Page number
- `page_size` (optional, default=20): Items per page

**Request Headers:**
```
Authorization: Basic base64(username:password)
```

**Response (200 OK):**
```json
{
  "count": 15,
  "next": "http://localhost:8000/api/v1/equipment/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "equipment_name": "Pump-1",
      "equipment_type": "Pump",
      "flowrate": 120.00,
      "pressure": 5.20,
      "temperature": 110.00,
      "status": "active",
      "installation_date": "2024-06-15",
      "last_maintenance_date": "2025-12-10",
      "notes": "",
      "created_at": "2025-01-10T10:00:00Z",
      "updated_at": "2025-01-20T14:30:00Z"
    },
    {
      "id": 2,
      "equipment_name": "Compressor-1",
      "equipment_type": "Compressor",
      "flowrate": 95.00,
      "pressure": 8.40,
      "temperature": 95.00,
      "status": "active",
      "installation_date": "2024-08-20",
      "last_maintenance_date": "2026-01-05",
      "notes": "Recently serviced",
      "created_at": "2025-01-11T11:00:00Z",
      "updated_at": "2025-01-22T09:15:00Z"
    }
  ]
}
```

---

#### **GET /api/v1/equipment/{id}/**
Retrieve a single equipment by ID.

**Request Headers:**
```
Authorization: Basic base64(username:password)
```

**Response (200 OK):**
```json
{
  "id": 1,
  "equipment_name": "Pump-1",
  "equipment_type": "Pump",
  "flowrate": 120.00,
  "pressure": 5.20,
  "temperature": 110.00,
  "status": "active",
  "installation_date": "2024-06-15",
  "last_maintenance_date": "2025-12-10",
  "notes": "",
  "created_by": {
    "id": 1,
    "username": "john_doe"
  },
  "created_at": "2025-01-10T10:00:00Z",
  "updated_at": "2025-01-20T14:30:00Z"
}
```

**Errors:**
- 404: Equipment not found

---

#### **POST /api/v1/equipment/**
Create a new equipment entry.

**Request Headers:**
```
Authorization: Basic base64(username:password)
Content-Type: application/json
```

**Request:**
```json
{
  "equipment_name": "Pump-5",
  "equipment_type": "Pump",
  "flowrate": 128.50,
  "pressure": 5.50,
  "temperature": 112.00,
  "status": "active",
  "installation_date": "2026-01-20",
  "notes": "New installation"
}
```

**Response (201 Created):**
```json
{
  "id": 16,
  "equipment_name": "Pump-5",
  "equipment_type": "Pump",
  "flowrate": 128.50,
  "pressure": 5.50,
  "temperature": 112.00,
  "status": "active",
  "installation_date": "2026-01-20",
  "last_maintenance_date": null,
  "notes": "New installation",
  "created_by": {
    "id": 1,
    "username": "john_doe"
  },
  "created_at": "2026-01-29T15:00:00Z",
  "updated_at": "2026-01-29T15:00:00Z"
}
```

**Errors:**
- 400: Validation error (duplicate name, invalid values)
- 403: Permission denied

---

#### **PUT /api/v1/equipment/{id}/** ⏳ FUTURE SCOPE
Update an existing equipment (full update).

> **Note**: Not implemented in current screening scope. Use PATCH for partial updates.

**Request Headers:**
```
Authorization: Basic base64(username:password)
Content-Type: application/json
```

**Request:**
```json
{
  "equipment_name": "Pump-1",
  "equipment_type": "Pump",
  "flowrate": 125.00,
  "pressure": 5.30,
  "temperature": 115.00,
  "status": "maintenance",
  "installation_date": "2024-06-15",
  "last_maintenance_date": "2026-01-28",
  "notes": "Under scheduled maintenance"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "equipment_name": "Pump-1",
  "equipment_type": "Pump",
  "flowrate": 125.00,
  "pressure": 5.30,
  "temperature": 115.00,
  "status": "maintenance",
  "installation_date": "2024-06-15",
  "last_maintenance_date": "2026-01-28",
  "notes": "Under scheduled maintenance",
  "created_by": {
    "id": 1,
    "username": "john_doe"
  },
  "created_at": "2025-01-10T10:00:00Z",
  "updated_at": "2026-01-29T16:00:00Z"
}
```

---

#### **PATCH /api/v1/equipment/{id}/**
Partially update an equipment.

**Request Headers:**
```
Authorization: Basic base64(username:password)
Content-Type: application/json
```

**Request:**
```json
{
  "temperature": 117.00,
  "notes": "Temperature adjusted"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "equipment_name": "Pump-1",
  "equipment_type": "Pump",
  "flowrate": 125.00,
  "pressure": 5.30,
  "temperature": 117.00,
  "status": "maintenance",
  "installation_date": "2024-06-15",
  "last_maintenance_date": "2026-01-28",
  "notes": "Temperature adjusted",
  "created_at": "2025-01-10T10:00:00Z",
  "updated_at": "2026-01-29T16:30:00Z"
}
```

---

#### **DELETE /api/v1/equipment/{id}/**
Delete an equipment (soft delete recommended).

**Request Headers:**
```
Authorization: Basic base64(username:password)
```

**Response (204 No Content)**

**Errors:**
- 403: Permission denied (only admin)
- 404: Equipment not found

---

### 3.3 Equipment Parameter History Endpoints ⏳ FUTURE SCOPE

> **Note**: Not implemented in current screening scope. Time-series tracking is an advanced feature for post-screening enhancement.

#### **GET /api/v1/equipment/{id}/history/**
Get parameter history for a specific equipment.

**Query Parameters:**
- `start_date` (optional): ISO 8601 date
- `end_date` (optional): ISO 8601 date
- `page` (optional): Page number
- `page_size` (optional): Items per page

**Request Headers:**
```
Authorization: Basic base64(username:password)
```

**Response (200 OK):**
```json
{
  "count": 50,
  "next": "http://localhost:8000/api/v1/equipment/1/history/?page=2",
  "previous": null,
  "results": [
    {
      "id": 101,
      "equipment": 1,
      "flowrate": 120.00,
      "pressure": 5.20,
      "temperature": 110.00,
      "timestamp": "2026-01-29T08:00:00Z",
      "recorded_by": {
        "id": 1,
        "username": "john_doe"
      }
    },
    {
      "id": 102,
      "equipment": 1,
      "flowrate": 122.50,
      "pressure": 5.25,
      "temperature": 112.00,
      "timestamp": "2026-01-29T12:00:00Z",
      "recorded_by": {
        "id": 1,
        "username": "john_doe"
      }
    }
  ]
}
```

---

#### **POST /api/v1/equipment/{id}/history/**
Record new parameter reading for equipment.

**Request Headers:**
```
Authorization: Basic base64(username:password)
Content-Type: application/json
```

**Request:**
```json
{
  "flowrate": 123.50,
  "pressure": 5.28,
  "temperature": 113.00
}
```

**Response (201 Created):**
```json
{
  "id": 103,
  "equipment": 1,
  "flowrate": 123.50,
  "pressure": 5.28,
  "temperature": 113.00,
  "timestamp": "2026-01-29T16:00:00Z",
  "recorded_by": {
    "id": 1,
    "username": "john_doe"
  }
}
```

---

### 3.4 Analytics Endpoints (✅ IMPLEMENTED - 2 endpoints)

#### **GET /api/v1/analytics/statistics/**
Get aggregate statistics for all equipment or filtered by type.

**Query Parameters:**
- `equipment_type` (optional): Filter by type
- `status` (optional): Filter by status

**Request Headers:**
```
Authorization: Basic base64(username:password)
```

**Response (200 OK):**
```json
{
  "total_equipment": 15,
  "by_type": {
    "Pump": {
      "count": 4,
      "avg_flowrate": 126.75,
      "avg_pressure": 5.50,
      "avg_temperature": 115.50,
      "min_flowrate": 120.00,
      "max_flowrate": 132.00,
      "min_pressure": 5.20,
      "max_pressure": 5.90,
      "min_temperature": 110.00,
      "max_temperature": 119.00
    },
    "Compressor": {
      "count": 2,
      "avg_flowrate": 97.50,
      "avg_pressure": 8.20,
      "avg_temperature": 96.50,
      "min_flowrate": 95.00,
      "max_flowrate": 100.00,
      "min_pressure": 8.00,
      "max_pressure": 8.40,
      "min_temperature": 95.00,
      "max_temperature": 98.00
    }
  },
  "overall": {
    "avg_flowrate": 118.33,
    "avg_pressure": 6.15,
    "avg_temperature": 115.40
  }
}
```

---

#### **GET /api/v1/analytics/trends/** ⏳ FUTURE SCOPE
Get time-series trends for equipment parameters.

> **Note**: Not implemented in current screening scope. Requires parameter history feature.

**Query Parameters:**
- `equipment_id` (required): Equipment ID
- `parameter` (required): 'flowrate', 'pressure', or 'temperature'
- `start_date` (optional): ISO 8601 date
- `end_date` (optional): ISO 8601 date
- `interval` (optional): 'hourly', 'daily', 'weekly' (default: 'daily')

**Request Headers:**
```
Authorization: Basic base64(username:password)
```

**Response (200 OK):**
```json
{
  "equipment_id": 1,
  "equipment_name": "Pump-1",
  "parameter": "temperature",
  "interval": "daily",
  "data_points": [
    {
      "timestamp": "2026-01-20T00:00:00Z",
      "value": 110.00,
      "count": 24
    },
    {
      "timestamp": "2026-01-21T00:00:00Z",
      "value": 112.50,
      "count": 24
    },
    {
      "timestamp": "2026-01-22T00:00:00Z",
      "value": 111.80,
      "count": 24
    }
  ]
}
```

---

#### **POST /api/v1/analytics/csv/upload/**
Upload CSV file to bulk import equipment data.

**Request Headers:**
```
Authorization: Basic base64(username:password)
Content-Type: multipart/form-data
```

**Request (multipart/form-data):**
```
file: <binary_file_data>
```

**Response (200 OK - Synchronous Processing):**
```json
{
  "dataset_id": 5,
  "file_name": "equipment_data_jan2026.csv",
  "status": "completed",
  "message": "CSV processed successfully.",
  "row_count": 487,
  "statistics": {
    "flowrate_avg": 245.6,
    "pressure_avg": 8.2,
    "temperature_avg": 112.4
  },
  "created_at": "2026-01-29T17:00:00Z"
}
```

> **Note**: Asynchronous processing with background jobs (Celery) is documented as a **future enhancement** (Phase 3).

**Errors:**
- 400: Invalid file format, column mismatch, or validation errors
- 413: File too large (>10 MB)

---

#### **GET /api/v1/analytics/csv/datasets/**  ✅ IMPLEMENTED
List last 5 uploaded CSV datasets.

**Request Headers:**
```
Authorization: Basic base64(username:password)
```

**Response (200 OK):**
```json
{
  "count": 5,
  "results": [
    {
      "id": 5,
      "file_name": "equipment_data_jan2026.csv",
      "uploaded_by": {
        "id": 1,
        "username": "john_doe"
      },
      "uploaded_at": "2026-01-29T17:00:00Z",
      "row_count": 15,
      "status": "completed",
      "processed_at": "2026-01-29T17:00:05Z"
    },
    {
      "id": 4,
      "file_name": "equipment_data_dec2025.csv",
      "uploaded_by": {
        "id": 2,
        "username": "jane_smith"
      },
      "uploaded_at": "2026-01-20T14:30:00Z",
      "row_count": 12,
      "status": "completed",
      "processed_at": "2026-01-20T14:30:03Z"
    }
  ]
}
```

---

#### **GET /api/v1/analytics/csv/datasets/{id}/**  ✅ IMPLEMENTED
Get specific dataset and its computed statistics.

**Request Headers:**
```
Authorization: Basic base64(username:password)
```

**Response (200 OK):**
```json
{
  "id": 5,
  "file_name": "equipment_data_jan2026.csv",
  "file_path": "/media/csv_uploads/equipment_data_jan2026_2026-01-29.csv",
  "uploaded_by": {
    "id": 1,
    "username": "john_doe"
  },
  "uploaded_at": "2026-01-29T17:00:00Z",
  "row_count": 15,
  "status": "completed",
  "error_log": "",
  "statistics": {
    "total_equipment": 15,
    "by_type": {
      "Pump": {
        "count": 4,
        "avg_flowrate": 126.75,
        "avg_pressure": 5.50,
        "avg_temperature": 115.50,
        "min_flowrate": 120.00,
        "max_flowrate": 132.00,
        "min_pressure": 5.20,
        "max_pressure": 5.90,
        "min_temperature": 110.00,
        "max_temperature": 119.00
      },
      "Compressor": {
        "count": 2,
        "avg_flowrate": 97.50,
        "avg_pressure": 8.20,
        "avg_temperature": 96.50
      }
    },
    "overall": {
      "avg_flowrate": 118.33,
      "avg_pressure": 6.15,
      "avg_temperature": 115.40
    }
  },
  "processed_at": "2026-01-29T17:00:05Z"
}
```

**Errors:**
- 404: Dataset not found

---

#### **GET /api/v1/analytics/csv/import/{id}/** ⏳ FUTURE SCOPE
Check status of CSV import.

> **Note**: Not implemented in current screening scope. CSV upload is synchronous; async tracking requires Celery.

**Request Headers:**
```
Authorization: Basic base64(username:password)
```

**Response (200 OK):**
```json
{
  "id": 5,
  "file_name": "equipment_data_jan2026.csv",
  "status": "completed",
  "records_imported": 45,
  "records_failed": 2,
  "error_log": "Row 12: Duplicate equipment name 'Pump-1'\nRow 23: Invalid pressure value",
  "imported_by": {
    "id": 1,
    "username": "john_doe"
  },
  "created_at": "2026-01-29T17:00:00Z",
  "completed_at": "2026-01-29T17:02:30Z"
}
```

---

#### **GET /api/v1/analytics/csv/export/** ⏳ FUTURE SCOPE
Export equipment data as CSV.

> **Note**: Not implemented in current screening scope. Import is higher priority than export.

**Query Parameters:**
- `equipment_type` (optional): Filter by type
- `status` (optional): Filter by status
- `include_history` (optional): true | false (default: false)

**Request Headers:**
```
Authorization: Basic base64(username:password)
```

**Response (200 OK):**
```
Content-Type: text/csv
Content-Disposition: attachment; filename="equipment_export_2026-01-29.csv"

<CSV_FILE_CONTENT>
```

---

#### **GET /api/v1/analytics/comparison/** ⏳ FUTURE SCOPE
Compare multiple equipment side-by-side.

> **Note**: Not implemented in current screening scope. Statistics endpoint provides aggregated data.

**Query Parameters:**
- `equipment_ids` (required): Comma-separated IDs (e.g., "1,2,3")

**Request Headers:**
```
Authorization: Basic base64(username:password)
```

**Response (200 OK):**
```json
{
  "equipment": [
    {
      "id": 1,
      "equipment_name": "Pump-1",
      "equipment_type": "Pump",
      "flowrate": 120.00,
      "pressure": 5.20,
      "temperature": 110.00,
      "status": "active"
    },
    {
      "id": 2,
      "equipment_name": "Compressor-1",
      "equipment_type": "Compressor",
      "flowrate": 95.00,
      "pressure": 8.40,
      "temperature": 95.00,
      "status": "active"
    }
  ],
  "comparison": {
    "flowrate": {
      "highest": {"equipment_id": 1, "value": 120.00},
      "lowest": {"equipment_id": 2, "value": 95.00}
    },
    "pressure": {
      "highest": {"equipment_id": 2, "value": 8.40},
      "lowest": {"equipment_id": 1, "value": 5.20}
    },
    "temperature": {
      "highest": {"equipment_id": 1, "value": 110.00},
      "lowest": {"equipment_id": 2, "value": 95.00}
    }
  }
}
```

---

### 3.5 Metadata Endpoints ⏳ FUTURE SCOPE

> **Note**: Not implemented in current screening scope. Equipment types and statuses can be hardcoded in frontend.

#### **GET /api/v1/metadata/equipment-types/**
Get list of available equipment types.

**Request Headers:**
```
Authorization: Basic base64(username:password)
```

**Response (200 OK):**
```json
{
  "types": [
    "Pump",
    "Compressor",
    "Valve",
    "HeatExchanger",
    "Reactor",
    "Condenser",
    "Other"
  ]
}
```

---

#### **GET /api/v1/metadata/status-choices/**
Get list of valid equipment status values.

**Response (200 OK):**
```json
{
  "statuses": [
    {"value": "active", "label": "Active"},
    {"value": "maintenance", "label": "Under Maintenance"},
    {"value": "inactive", "label": "Inactive"}
  ]
}
```

---

## 4. AUTHENTICATION APPROACH

### 4.1 Current Implementation: Basic Authentication

#### **Justification for Basic Auth (Intern Screening Scope)**

For this screening project, **Basic Authentication** is implemented for the following reasons:

1. **Simplicity**: Built-in Django REST Framework support with `BasicAuthentication` class
2. **Rapid Development**: No need to manage token generation, storage, or expiration logic
3. **Standard Compliance**: Uses HTTP standard (RFC 7617) - widely understood and testable
4. **Educational Value**: Demonstrates understanding of authentication fundamentals
5. **Sufficient for Demo**: Appropriate for single-user development and demo scenarios
6. **Easy Testing**: Simple to test with tools like Postman, cURL, or browser DevTools
7. **No Additional Models**: Leverages Django's built-in User model without custom token tables

#### **Current Flow:**
1. **Web/Desktop Client** sends credentials in Authorization header: `Basic base64(username:password)`
2. **Backend** validates credentials using Django's authentication system
3. **Backend** returns user details (no token generation)
4. **Client** includes credentials in every subsequent request header
5. **Backend** validates credentials on each request via DRF's `BasicAuthentication`

#### **Credential Encoding Example:**
```python
# Username: john_doe, Password: SecurePass123
import base64
credentials = base64.b64encode(b"john_doe:SecurePass123").decode('utf-8')
# Result: am9obl9kb2U6U2VjdXJlUGFzczEyMw==

# HTTP Header:
# Authorization: Basic am9obl9kb2U6U2VjdXJlUGFzczEyMw==
```

#### **Security Considerations (Current):**
- **HTTPS Required**: Credentials sent with every request must be over HTTPS in production
- **CORS Configuration**: Restrict origins to prevent unauthorized access
- **Password Hashing**: Django's PBKDF2 with SHA-256 for secure password storage
- **Rate Limiting**: Consider adding throttling in production (DRF throttle classes)
- **No Credential Storage**: Web frontend does NOT store credentials in localStorage (security risk)
- **Session Alternative**: Can use session-based auth for web frontend; Basic Auth for desktop

#### **Role-Based Access Control (RBAC):**
- **Admin**: Full CRUD on all resources, user management
- **Engineer**: Upload CSV datasets, view analytics, delete own datasets
- **Viewer**: Read-only access to datasets and analytics

#### **Implementation:**
- DRF's `BasicAuthentication` class in `settings.py`
- Custom DRF permission classes: `IsAdminUser`, `IsEngineerOrAdmin`, `IsAuthenticated`
- Permissions checked at view level
- Object-level permissions for equipment updates (creator or admin)

---

### 4.2 Future Enhancement: Token-Based Authentication

> **Note**: Token authentication is planned for production deployment but NOT in current screening scope.

#### **Future Flow (Post-Screening):**
1. **Client** sends credentials to `/api/v1/auth/token/` (new endpoint)
2. **Backend** validates and generates unique token (JWT or DRF Token)
3. **Backend** returns token + expiration time
4. **Client** stores token securely (web: memory/httpOnly cookie, desktop: OS keychain)
5. **Subsequent requests** include `Authorization: Token <token>` or `Authorization: Bearer <jwt>`
6. **Backend** validates token without database lookup (JWT) or with lookup (DRF Token)

#### **Future Token Storage:**
- **Web Frontend**: httpOnly cookies or in-memory storage (not localStorage due to XSS risk)
- **Desktop Frontend**: OS-specific secure storage (Windows Credential Manager, macOS Keychain)

#### **Future Token Security:**
- Tokens hashed in database (if using DRF Token Auth)
- Short expiration times (15 min access token, 7 day refresh token)
- Token refresh mechanism for seamless UX
- Logout invalidates token
- Rate limiting on token generation

#### **Why Token Auth is Better for Production:**
- **Stateless**: No need to query database on every request (JWT)
- **Scalability**: Works better with load balancers and multiple servers
- **Expiration**: Built-in token expiration reduces credential exposure
- **Granular Control**: Can revoke specific tokens without changing password
- **Mobile/Desktop Friendly**: Better UX for long-lived sessions

#### **Migration Path:**
Transitioning from Basic to Token Auth requires:
1. Add `users_apitoken` model (see Section 2.5)
2. Create token generation endpoint
3. Update frontend to store and manage tokens
4. Switch DRF authentication class from `BasicAuthentication` to `TokenAuthentication`
5. Add token refresh logic for desktop clients

---

## 5. DATA FLOW DIAGRAM (Textual)

### 5.1 User Login Flow (Basic Auth)
```
[Web/Desktop Client]
    |
    | POST /api/v1/auth/login/ (username, password)
    v
[Django Backend]
    |
    | Validate credentials via Django Auth
    v
[Database (SQLite)]
    |
    | Retrieve User record and verify password hash
    v
[Django Backend]
    |
    | Return {user_data, success}
    |
    | NO token generation
    v
[Web/Desktop Client]
    |
    | Store credentials securely (desktop) or session (web)
    |
    | Navigate to Dashboard
    |
    | Include Authorization: Basic header in subsequent requests
```

---

### 5.2 Equipment Listing Flow
```
[Web/Desktop Client]
    |
    | GET /api/v1/equipment/ (Authorization: Basic <base64_credentials>)
    v
[Django Backend - Equipment ViewSet]
    |
    | Verify credentials via BasicAuthentication
    |
    | Check user permissions
    v
[Database (SQLite)]
    |
    | Query equipment_equipment table
    |
    | Apply filters (type, status, search)
    |
    | Paginate results
    v
[Django Backend]
    |
    | Serialize data (DRF Serializer)
    |
    | Return JSON response
    v
[Web/Desktop Client]
    |
    | Render equipment list/table
```

---

### 5.3 CSV Upload and Analytics Flow
```
[Web/Desktop Client]
    |
    | POST /api/v1/analytics/csv/upload/ (file, Authorization: Basic)
    v
[Django Backend - Analytics View]
    |
    | Verify credentials and permissions
    |
    | Validate CSV file
    v
[File System - media/csv_uploads/]
    |
    | Save uploaded file
    v
[Django Backend - CSV Processor (Pandas)]
    |
    | Read CSV using pandas.read_csv()
    |
    | Validate column structure (Equipment Name, Type, Flowrate, Pressure, Temperature)
    |
    | Compute statistics using Pandas (min/max/avg/count per equipment type)
    |
    | No persistence of individual equipment records (CSV-only analytics)
    v
[Database (SQLite)]
    |
    | Create analytics_csvdataset record with statistics JSONField
    |
    | Store aggregated statistics only (not individual rows)
    v
[Django Backend]
    |
    | Return import status {import_id, status}
    v
[Web/Desktop Client]
    |
    | Display import progress/results
    |
    | Poll GET /api/v1/analytics/csv/import/{id}/ for status
```

---

### 5.4 Parameter History Recording Flow
```
[Web/Desktop Client]
    |
    | POST /api/v1/equipment/{id}/history/ (flowrate, pressure, temp)
    v
[Django Backend - Equipment History View]
    |
    | Verify credentials via Basic Auth
    |
    | Validate parameter values
    v
[Database (SQLite)]
    |
    | Insert into equipment_parameterhistory table
    |
    | Link to equipment via FK
    |
    | Record timestamp and user
    v
[Django Backend]
    |
    | Return created history record
    v
[Web/Desktop Client]
    |
    | Update UI with new reading
    |
    | Refresh charts/graphs
```

---

### 5.5 Analytics Statistics Flow
```
[Web/Desktop Client]
    |
    | GET /api/v1/analytics/statistics/ (Authorization: Basic)
    v
[Django Backend - Analytics Service (Pandas)]
    |
    | Query equipment_equipment table
    |
    | Load into pandas DataFrame
    v
[Pandas Processing Layer]
    |
    | df.groupby('equipment_type').agg({'flowrate': ['mean', 'min', 'max'], ...})
    |
    | Calculate overall averages
    |
    | Format results as JSON
    v
[Django Backend]
    |
    | Return aggregated statistics
    v
[Web/Desktop Client]
    |
    | Render charts (bar, pie, line graphs)
    |
    | Display KPIs
```

---

### 5.6 Desktop App Simplified Workflow (Online-Only)

> **SIMPLIFIED**: Desktop app is a thin client consuming the same REST APIs as the web frontend. No offline caching, sync, or local storage.

```
[Desktop Client (PyQt5)]
    |
    | User Login: Prompt for username/password
    |
    | POST /api/v1/auth/login/ (Authorization: Basic)
    v
[Django Backend]
    |
    | Validate credentials → Return success
    v
[Desktop Client]
    |
    | Store credentials in memory (session only)
    |
    | Navigate to CSV Upload Tab
    |
    | User selects CSV file → Upload
    |
    | POST /api/v1/analytics/csv/upload/ (multipart/form-data)
    v
[Django Backend]
    |
    | Validate CSV → Process with Pandas → Store statistics in DB
    |
    | Return dataset_id, statistics, validation errors
    v
[Desktop Client]
    |
    | Display upload status
    |
    | Navigate to Analytics Tab
    |
    | GET /api/v1/analytics/csv/datasets/ (fetch list)
    |
    | User selects dataset → GET /api/v1/analytics/csv/datasets/{id}/
    v
[Django Backend]
    |
    | Return dataset details + statistics JSON
    v
[Desktop Client]
    |
    | Render charts (Matplotlib) in QWidget
    |
    | Display data in QTableWidget
```

**Key Simplifications**:
- **No Offline Mode**: Desktop requires internet connection to function
- **No Local Cache**: All data fetched from server in real-time
- **No Sync Logic**: No conflict resolution or data merging
- **Same APIs**: Reuses identical REST endpoints as web frontend
- **Session-Only Auth**: Credentials stored in memory, cleared on exit

---

## 6. CLEAR ASSUMPTIONS

### 6.1 Technical Assumptions
1. **Single Server Deployment**: Backend runs on a single server (not distributed)
2. **SQLite Database**: Suitable for small-to-medium datasets (<100k equipment records)
3. **Basic Authentication (Current)**: Uses HTTP Basic Auth for simplicity in demo/screening
4. **Token Auth (Future)**: Token-based authentication planned for production deployment
5. **Synchronous CSV Processing**: CSV imports processed synchronously; async with Celery recommended for production
6. **No Real-Time Updates**: Clients poll APIs; WebSockets not implemented initially
7. **Parameter Units**: Fixed units (Flowrate: L/min, Pressure: bar, Temperature: °C)
8. **Desktop Online-Only Mode**: Desktop app requires internet connection; no offline caching or sync implemented
9. **File Upload Size Limit**: CSV files limited to 10 MB
10. **Credential Storage (Current)**: Desktop stores credentials in memory (session-only); web uses session or prompts per-request

### 6.2 Business Logic Assumptions
1. **Equipment Naming**: Equipment names must be unique across the system
2. **User Roles**: Three roles (Admin, Engineer, Viewer) with predefined permissions
3. **CSV Format**: CSV must match exact column structure: `Equipment Name, Type, Flowrate, Pressure, Temperature`
4. **Duplicate Handling**: CSV uploads skip duplicates unless `update_existing=true`
5. **Parameter History**: Unlimited history retention (consider archival strategy for production)
6. **Maintenance Tracking**: Manual maintenance date updates; no automated scheduling
7. **Data Validation**: Negative values for flowrate/pressure/temperature are rejected

### 6.3 Security Assumptions
1. **HTTPS in Production**: Backend served over HTTPS; Basic Auth credentials encrypted in transit
2. **CORS Configuration**: Web frontend served from same domain or whitelisted origin
3. **Password Hashing**: Django's PBKDF2 with SHA-256 for password storage
4. **Credential Storage (Current)**: Desktop stores credentials in memory (session-only); web uses session or prompts per-request
5. **Token Storage (Future)**: Desktop will use OS-specific secure storage (Windows Credential Manager, macOS Keychain) when token auth is implemented
6. **Input Sanitization**: Django ORM provides SQL injection protection; CSV inputs validated
7. **Rate Limiting**: Not implemented initially; add Django REST throttling for production
8. **Basic Auth Limitation**: Credentials sent with every request; acceptable for demo, migrate to token for production

### 6.4 Scalability Assumptions
1. **User Concurrency**: System designed for <100 concurrent users
2. **Data Volume**: <10,000 equipment records; <1M parameter history records
3. **CSV Batch Size**: <5,000 rows per CSV file
4. **API Response Time**: Target <500ms for equipment list, <2s for analytics

### 6.5 Deployment Assumptions
1. **Backend Hosting**: Deployed on VPS or PaaS (e.g., DigitalOcean, Heroku)
2. **Web Frontend**: Served via Nginx or deployed on Vercel/Netlify
3. **Desktop Distribution**: Packaged as standalone executables (PyInstaller)
4. **Database Backups**: Manual SQLite file backups; no automated backup system initially
5. **Environment Separation**: Separate dev/staging/prod configurations

### 6.6 Frontend Assumptions
1. **Chart Library (Web)**: Recharts or Chart.js for React
2. **Chart Library (Desktop)**: Matplotlib or PyQtGraph for PyQt5
3. **Responsive Design**: Web frontend supports desktop/tablet (not mobile-optimized initially)
4. **Browser Support**: Modern browsers (Chrome, Firefox, Edge, Safari - last 2 versions)
5. **Desktop OS**: Windows 10+, macOS 11+, Ubuntu 20.04+

---

## SUMMARY

This architecture provides:
- **Clear separation of concerns**: Backend (Django), Web (React), Desktop (PyQt5)
- **Unified API interface**: Both frontends consume identical REST endpoints
- **Scalable data model**: Supports equipment CRUD, parameter history, analytics
- **Secure authentication**: Token-based auth with RBAC
- **Extensible design**: Easy to add new equipment types, parameters, or analytics

**Next Steps** (when ready to code):
1. Set up Django project with virtual environment
2. Configure Django REST Framework + Basic Authentication
3. Implement database models and migrations (User + CSVDataset only)
4. Build API views and serializers with DRF BasicAuthentication (6 endpoints)
5. Create React web app structure (session or Basic Auth)
6. Develop PyQt5 desktop app with online-only mode (no offline caching)
7. Implement Pandas analytics services for CSV processing
8. Testing and deployment
9. **Future**: Add offline features to desktop app (SQLite cache + sync logic)
10. **Future**: Migrate to Token-based authentication for production

---

**Document Version**: 1.0  
**Last Updated**: January 29, 2026  
**Status**: Ready for Implementation

---

## APPENDIX: QUICK REFERENCE - API SCOPE

### Implemented APIs (Intern Screening - SIMPLIFIED MODEL - 6 Endpoints)

| Category | Method | Endpoint | Purpose |
|----------|--------|----------|---------|
| **Auth** | POST | `/api/v1/auth/login/` | User authentication |
| **Auth** | POST | `/api/v1/auth/logout/` | Session termination |
| **Analytics** | POST | `/api/v1/analytics/csv/upload/` | Bulk CSV import + statistics |
| **Analytics** | GET | `/api/v1/analytics/statistics/` | Aggregated stats from last upload |
| **Analytics** | GET | `/api/v1/analytics/csv/datasets/` | List last 5 datasets |
| **Analytics** | GET | `/api/v1/analytics/csv/datasets/{id}/` | Get dataset statistics |

### Future Scope APIs (Post-Screening - 16 Endpoints)

| Category | Method | Endpoint | Reason for Deferral |
|----------|--------|----------|---------------------|
| **Auth** | POST | `/api/v1/auth/register/` | Admin creates users |
| **Auth** | GET | `/api/v1/auth/user/me/` | Data in login response |
| **Equipment** | GET | `/api/v1/equipment/` | **No Equipment model** |
| **Equipment** | GET | `/api/v1/equipment/{id}/` | **No Equipment model** |
| **Equipment** | POST | `/api/v1/equipment/` | **No Equipment model** |
| **Equipment** | PATCH | `/api/v1/equipment/{id}/` | **No Equipment model** |
| **Equipment** | PUT | `/api/v1/equipment/{id}/` | **No Equipment model** |
| **Equipment** | DELETE | `/api/v1/equipment/{id}/` | **No Equipment model** |
| **History** | GET | `/api/v1/equipment/{id}/history/` | Time-series is advanced |
| **History** | POST | `/api/v1/equipment/{id}/history/` | Time-series is advanced |
| **Analytics** | GET | `/api/v1/analytics/trends/` | Requires history feature |
| **Analytics** | GET | `/api/v1/analytics/csv/import/{id}/` | Async tracking complex |
| **Analytics** | GET | `/api/v1/analytics/csv/export/` | Import higher priority |
| **Analytics** | GET | `/api/v1/analytics/comparison/` | Advanced feature |
| **Metadata** | GET | `/api/v1/metadata/equipment-types/` | Hardcode in frontend |
| **Metadata** | GET | `/api/v1/metadata/status-choices/` | Hardcode in frontend |

### Database Models: Implemented vs Future

| Model | Status | Justification |
|-------|--------|---------------|
| `auth_user` (Django) | ✅ Implemented | Built-in, required for auth |
| `users_userprofile` | ✅ Implemented | Role-based access control |
| `analytics_csvdataset` | ✅ Implemented | **CSV tracking + statistics (JSONField)** |
| `equipment_equipment` | ⏳ Future | **Not needed for CSV-only analytics** |
| `equipment_parameterhistory` | ⏳ Future | Time-series tracking |
| `analytics_csvimport` | ⏳ Future | Merged into CSVDataset |
| `users_apitoken` | ⏳ Future | Token auth migration |

### Technology Stack: Current vs Future

| Component | Current (Screening) | Future (Production) |
|-----------|---------------------|---------------------|
| **Authentication** | Basic Auth | Token/JWT |
| **Data Storage** | JSONField statistics | Relational Equipment model |
| **CSV Processing** | Synchronous (Pandas) | Async (Celery + Pandas) |
| **Database** | SQLite | PostgreSQL/MySQL |
| **API Docs** | Manual (in code) | Swagger/OpenAPI |
| **Frontend State** | Local | Redux/Context API |
| **Real-time** | Polling | WebSockets |
| **Deployment** | Dev server | Gunicorn + Nginx |

---

### Estimated Implementation Time (Intern Screening - SIMPLIFIED)

| Task | Hours | Notes |
|------|-------|-------|
| Django + DRF Setup | 2 | Project structure, settings |
| CSVDataset Model + Migrations | 2 | Model with JSONField, admin |
| Authentication APIs | 2 | Login/logout views |
| CSV Upload (Pandas) | 4 | File handling, validation, stats calculation |
| Statistics Endpoint | 1 | Return statistics from CSVDataset |
| Dataset History Endpoints | 2 | List & detail views |
| Auto-cleanup Logic | 1 | Keep last 5 datasets |
| Testing + Documentation | 2 | Unit tests, API docs |
| **Total** | **12-16 hours** | Simplified scope |

**Comparison:**
- **Original Design**: 30-40 hours (with Equipment CRUD, Parameter History, offline sync, token auth)
- **Simplified Implementation**: 12-16 hours (CSV-only analytics, Basic Auth, online-only)
- **Reduction**: 60-65% time savings + 70% fewer endpoints + 60% fewer models

---

**End of Architecture Document**

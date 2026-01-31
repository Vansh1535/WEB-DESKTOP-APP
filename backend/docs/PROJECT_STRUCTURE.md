# Project Structure

This document outlines the organized folder structure of the backend project.

## Directory Layout

```
backend/
│
├── analytics/                  # Main analytics Django app
│   ├── migrations/            # Database migrations
│   ├── __init__.py
│   ├── admin.py               # Admin panel configuration
│   ├── models.py              # CSVDataset model
│   ├── serializers.py         # DRF serializers
│   ├── services.py            # CSV processing logic
│   ├── pdf_service.py         # PDF generation service
│   ├── urls.py                # Analytics URL routing
│   └── views.py               # API endpoints
│
├── config/                     # Django project configuration
│   ├── __init__.py
│   ├── asgi.py                # ASGI configuration
│   ├── settings.py            # Project settings
│   ├── urls.py                # Root URL configuration
│   ├── views.py               # Root endpoint views
│   └── wsgi.py                # WSGI configuration
│
├── users/                      # User management app
│   ├── __init__.py
│   ├── serializers.py         # User serializers
│   ├── urls.py                # User URL routing
│   └── views.py               # Auth endpoints
│
├── data/                       # Sample and test data files
│   ├── README.md              # Data documentation
│   └── sample_equipment_data.csv  # Sample CSV file
│
├── docs/                       # All project documentation
│   ├── README.md              # Documentation index
│   ├── API_TESTING.md         # API endpoint reference
│   ├── ARCHITECTURE_BACKEND.md # System architecture
│   ├── CHECKLIST.md           # Development checklist
│   ├── DEPLOYMENT.md          # Deployment guide
│   ├── INDEX.md               # Master index
│   ├── PROJECT_SUMMARY.md     # Project overview
│   ├── QUICKSTART.md          # Quick start guide
│   └── SETUP_COMPLETE.md      # Post-setup guide
│
├── media/                      # User uploaded files
│   └── csv_uploads/           # CSV files storage
│
├── scripts/                    # Utility scripts
│   ├── README.md              # Scripts documentation
│   ├── create_users.py        # Create test users
│   ├── upload_sample.py       # Upload sample data
│   ├── setup.bat              # Windows setup script
│   └── setup.sh               # Unix setup script
│
├── tests/                      # All test files
│   ├── README.md              # Test documentation
│   ├── test_api.py            # API endpoint tests
│   ├── test_users.py          # User isolation tests
│   ├── test_pdf.py            # PDF generation tests
│   └── quick_test.py          # Quick smoke tests
│
├── venv/                       # Virtual environment (ignored)
│
├── .gitignore                 # Git ignore rules
├── db.sqlite3                 # SQLite database
├── manage.py                  # Django management script
├── README.md                  # Main project README
└── requirements.txt           # Python dependencies
```

## Key Directories

### `/analytics`
Core application containing CSV processing, statistics computation, and PDF generation.

**Key Files:**
- `models.py` - CSVDataset model with auto-deletion logic
- `services.py` - CSV validation and processing
- `pdf_service.py` - PDF report generation
- `views.py` - All analytics API endpoints

### `/config`
Django project configuration and root URL routing.

**Key Files:**
- `settings.py` - Database, DRF, authentication settings
- `urls.py` - Root URL patterns
- `views.py` - Welcome page endpoint

### `/users`
User authentication and registration endpoints.

**Key Files:**
- `views.py` - Register and login endpoints
- `serializers.py` - User data serialization

### `/data`
Sample data files for testing and development.

**Files:**
- `sample_equipment_data.csv` - 30 rows, 10 equipment types

### `/docs`
Complete project documentation.

**Categories:**
- Setup guides (QUICKSTART.md, SETUP_COMPLETE.md)
- API reference (API_TESTING.md)
- Architecture (ARCHITECTURE_BACKEND.md)
- Deployment (DEPLOYMENT.md)

### `/scripts`
Utility scripts for setup, testing, and data management.

**Scripts:**
- `create_users.py` - Create test users
- `upload_sample.py` - Upload sample CSV
- `setup.bat/sh` - Automated setup

### `/tests`
All test scripts with comprehensive test coverage.

**Test Files:**
- `test_api.py` - Full API testing
- `test_users.py` - User isolation testing
- `test_pdf.py` - PDF generation testing
- `quick_test.py` - Smoke tests

## File Organization Principles

### Documentation
- All `.md` files in `/docs`
- Each folder has its own README.md
- Clear separation of concerns

### Tests
- All test scripts in `/tests`
- Organized by feature area
- Test documentation included

### Data
- Sample files in `/data`
- User uploads in `/media/csv_uploads`
- Generated PDFs in root (temporary)

### Scripts
- Utility scripts in `/scripts`
- Setup scripts included
- Clear documentation per script

## Navigation Guide

### For New Developers
1. Start with [README.md](README.md)
2. Read [docs/QUICKSTART.md](docs/QUICKSTART.md)
3. Review [docs/ARCHITECTURE_BACKEND.md](docs/ARCHITECTURE_BACKEND.md)

### For Testing
1. Check [tests/README.md](tests/README.md)
2. Run tests from `/tests` directory
3. Use sample data from `/data`

### For API Integration
1. Read [docs/API_TESTING.md](docs/API_TESTING.md)
2. Use examples from `/tests`
3. Reference [docs/ARCHITECTURE_BACKEND.md](docs/ARCHITECTURE_BACKEND.md)

### For Deployment
1. Follow [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
2. Check [docs/CHECKLIST.md](docs/CHECKLIST.md)
3. Use setup scripts from `/scripts`

## Best Practices

### Adding New Features
1. Update models in `/analytics/models.py`
2. Add views in `/analytics/views.py`
3. Create tests in `/tests`
4. Update documentation in `/docs`

### Running Tests
```bash
# From project root
python tests/test_api.py
python tests/test_users.py
python tests/test_pdf.py
```

### Using Scripts
```bash
# Create test users
python scripts/create_users.py

# Upload sample data
python scripts/upload_sample.py
```

### Accessing Documentation
All documentation is in `/docs` with clear filenames indicating purpose.

## Maintenance

### Keeping Structure Clean
- Tests → `/tests`
- Docs → `/docs`
- Data → `/data`
- Scripts → `/scripts`
- Code → App directories

### Version Control
See `.gitignore` for excluded files:
- `/venv` - Virtual environment
- `/media` - User uploads
- `db.sqlite3` - Database
- `*.pyc` - Compiled Python
- `__pycache__` - Python cache

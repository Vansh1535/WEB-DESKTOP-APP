# Backend Scripts

This directory contains utility scripts for the Chemical Equipment Parameter Visualizer backend.

## Scripts

### 1. `create_users.py`
**Purpose:** Create multiple test users for development and testing

**Features:**
- Creates users with predefined credentials
- Handles duplicate user prevention
- Provides clear success/error messages

**Usage:**
```bash
python scripts/create_users.py
```

**Users Created:**
| Username | Password | Purpose |
|----------|----------|---------|
| john_doe | john123 | Test user 1 |
| jane_smith | jane123 | Test user 2 |
| engineer1 | engineer123 | Engineering role test |
| analyst1 | analyst123 | Analyst role test |

**When to Use:**
- Initial development setup
- Testing user isolation
- Demonstrating multi-user features
- After database reset

---

### 2. `upload_sample.py`
**Purpose:** Upload sample CSV data via API

**Features:**
- Authenticates with admin credentials
- Uploads sample_equipment_data.csv
- Displays upload response and statistics

**Usage:**
```bash
python scripts/upload_sample.py
```

**Prerequisites:**
- Django server running
- Admin user exists (username: admin, password: admin123)
- Sample data file exists at `data/sample_equipment_data.csv`

**Output:**
```
Uploading sample CSV file...
✅ File uploaded successfully!
Dataset ID: 2
Status: processing/completed
```

---

## Setup Scripts

### `setup.bat` (Windows)
**Purpose:** Automated setup for Windows environments

**Features:**
- Creates virtual environment
- Installs dependencies
- Runs migrations
- Creates superuser
- Starts development server

**Usage:**
```cmd
setup.bat
```

---

### `setup.sh` (Linux/Mac)
**Purpose:** Automated setup for Unix-based systems

**Features:**
- Creates virtual environment
- Installs dependencies
- Runs migrations
- Creates superuser
- Starts development server

**Usage:**
```bash
chmod +x setup.sh
./setup.sh
```

---

## Creating New Scripts

### Template Structure
```python
#!/usr/bin/env python
"""
Script Name: script_name.py
Purpose: Brief description
Author: Your Name
Date: YYYY-MM-DD
"""

import os
import sys
import django

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Your script logic here
def main():
    pass

if __name__ == '__main__':
    main()
```

### Best Practices
1. Add docstring explaining purpose
2. Handle errors gracefully
3. Provide clear user feedback
4. Accept command-line arguments where appropriate
5. Document prerequisites and usage

---

## Common Use Cases

### Reset Database and Create Fresh Users
```bash
# Delete database
rm db.sqlite3

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create test users
python scripts/create_users.py
```

### Populate Database with Sample Data
```bash
# Start server
python manage.py runserver

# In new terminal, upload data
python scripts/upload_sample.py
```

### Test Multi-User Scenarios
```bash
# Create test users
python scripts/create_users.py

# Run user isolation tests
python tests/test_users.py
```

---

## Environment Variables

Scripts may use these environment variables:

- `DJANGO_SETTINGS_MODULE` - Django settings (default: config.settings)
- `DEBUG` - Enable debug mode (True/False)
- `SECRET_KEY` - Django secret key
- `DATABASE_URL` - Database connection string

Set in `.env` file or export directly:
```bash
export DJANGO_SETTINGS_MODULE=config.settings
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'django'"
**Solution:** Activate virtual environment
```bash
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### Issue: "django.core.exceptions.ImproperlyConfigured"
**Solution:** Set DJANGO_SETTINGS_MODULE
```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
```

### Issue: Script can't find project files
**Solution:** Ensure script is in `scripts/` directory and add project root to path
```python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

---

## Future Scripts

Potential scripts to add:

- `backup_database.py` - Backup SQLite database
- `generate_test_data.py` - Generate random test CSV files
- `cleanup_media.py` - Clean up orphaned media files
- `export_statistics.py` - Export all statistics to Excel
- `reset_user_data.py` - Reset specific user's datasets
- `migrate_users.py` - Migrate users from one system to another

---

## Contributing

When adding new scripts:
1. Place in `scripts/` directory
2. Follow template structure above
3. Add documentation to this README
4. Include error handling
5. Test in clean environment
6. Commit with descriptive message

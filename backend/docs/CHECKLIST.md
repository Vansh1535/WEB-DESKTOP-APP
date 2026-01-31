# ✅ Backend Verification Checklist

Use this checklist to verify that your Django REST API backend is working correctly.

## 🔧 Installation Checklist

- [ ] Python 3.10+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed from requirements.txt
- [ ] No installation errors

**Verify:**
```bash
python --version  # Should show 3.10+
pip list | grep Django  # Should show Django 4.2.7
pip list | grep pandas  # Should show pandas 2.1.3
```

---

## 🗄️ Database Checklist

- [ ] Migrations created successfully
- [ ] Migrations applied successfully
- [ ] db.sqlite3 file exists
- [ ] Superuser created

**Verify:**
```bash
python manage.py showmigrations  # All should show [X]
ls -la db.sqlite3  # File should exist
python manage.py shell -c "from django.contrib.auth.models import User; print(User.objects.count())"
```

---

## 🚀 Server Checklist

- [ ] Server starts without errors
- [ ] No port conflicts
- [ ] Server accessible at http://127.0.0.1:8000
- [ ] Admin panel loads

**Verify:**
```bash
python manage.py runserver
# Open browser: http://127.0.0.1:8000/admin/
# Should see Django admin login page
```

---

## 🔐 Authentication Checklist

### Login Endpoint
- [ ] POST /api/auth/login/ accepts credentials
- [ ] Valid credentials return 200 OK
- [ ] Invalid credentials return 401 Unauthorized
- [ ] Response includes user data

**Test:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'
```

**Expected:** Status 200, JSON with "message" and "user"

### Logout Endpoint
- [ ] POST /api/auth/logout/ requires authentication
- [ ] Returns 200 OK with valid auth
- [ ] Returns 401 without auth

**Test:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/logout/ \
  -u admin:your_password
```

**Expected:** Status 200, JSON with "message": "Logout successful."

---

## 📊 Analytics Endpoints Checklist

### CSV Upload
- [ ] POST /api/analytics/csv/upload/ accepts CSV files
- [ ] Valid CSV returns 201 Created
- [ ] Invalid CSV returns 400 Bad Request
- [ ] Response includes dataset_id and statistics
- [ ] File saved to media/csv_uploads/

**Test:**
```bash
curl -X POST http://127.0.0.1:8000/api/analytics/csv/upload/ \
  -u admin:your_password \
  -F "file=@sample_equipment_data.csv"
```

**Expected:** Status 201, JSON with dataset_id, statistics

**Verify file saved:**
```bash
ls -la media/csv_uploads/
```

### List Datasets
- [ ] GET /api/analytics/csv/datasets/ requires auth
- [ ] Returns list of user's datasets
- [ ] Shows count and datasets array
- [ ] Only shows current user's datasets

**Test:**
```bash
curl -X GET http://127.0.0.1:8000/api/analytics/csv/datasets/ \
  -u admin:your_password
```

**Expected:** Status 200, JSON with "count" and "datasets"

### Retrieve Dataset
- [ ] GET /api/analytics/csv/datasets/{id}/ returns single dataset
- [ ] Returns 404 for non-existent dataset
- [ ] Returns 404 for other user's dataset
- [ ] Includes full statistics

**Test:**
```bash
curl -X GET http://127.0.0.1:8000/api/analytics/csv/datasets/1/ \
  -u admin:your_password
```

**Expected:** Status 200, JSON with dataset details

### Delete Dataset
- [ ] DELETE /api/analytics/csv/datasets/{id}/ deletes dataset
- [ ] Returns 200 OK on success
- [ ] Returns 404 for non-existent dataset
- [ ] Deletes file from storage
- [ ] Deletes database record

**Test:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/analytics/csv/datasets/1/ \
  -u admin:your_password
```

**Expected:** Status 200, JSON with "message": "Dataset deleted successfully."

### Get Statistics
- [ ] GET /api/analytics/statistics/ returns aggregated stats
- [ ] Shows total datasets count
- [ ] Shows total equipment count
- [ ] Includes all completed datasets
- [ ] Only shows current user's data

**Test:**
```bash
curl -X GET http://127.0.0.1:8000/api/analytics/statistics/ \
  -u admin:your_password
```

**Expected:** Status 200, JSON with total_datasets, total_equipment_count, datasets

---

## 📋 CSV Processing Checklist

### Valid CSV
- [ ] Accepts CSV with all required columns
- [ ] Processes numeric columns correctly
- [ ] Computes statistics accurately
- [ ] Stores row_count correctly
- [ ] Sets status to 'completed'

**Required Columns:**
- Equipment Name
- Type
- Flowrate
- Pressure
- Temperature

### Invalid CSV Handling
- [ ] Rejects CSV missing columns
- [ ] Rejects CSV with negative values
- [ ] Rejects CSV with non-numeric values
- [ ] Returns clear error messages
- [ ] Sets status to 'failed'
- [ ] Stores error in error_log

**Test with invalid CSV:**
```csv
Equipment Name,Type,Flowrate,Pressure
Pump-A1,Pump,150.5,5.2
```

**Expected:** Status 400, error message about missing "Temperature"

---

## 📈 Statistics Computation Checklist

Upload sample_equipment_data.csv and verify:

- [ ] total_equipment_count matches row count (should be 30)
- [ ] by_type contains all equipment types (10 types)
- [ ] Each type shows count, flowrate, pressure, temperature stats
- [ ] avg, min, max calculated correctly
- [ ] overall_averages calculated correctly
- [ ] Statistics stored in JSONField

**Verify in Admin Panel:**
1. Go to http://127.0.0.1:8000/admin/
2. Click "CSV Datasets"
3. Open a completed dataset
4. Check statistics field

---

## 🔄 Auto-Cleanup Checklist

- [ ] System keeps last 5 datasets per user
- [ ] Uploading 6th dataset deletes oldest
- [ ] File deleted from storage
- [ ] Database record deleted
- [ ] No orphaned files remain

**Test:**
Upload 6 CSV files, then verify:
```bash
curl -X GET http://127.0.0.1:8000/api/analytics/csv/datasets/ \
  -u admin:your_password
```

**Expected:** Count should be 5 (not 6)

---

## 👨‍💼 Admin Panel Checklist

- [ ] Admin accessible at /admin/
- [ ] Can login with superuser credentials
- [ ] Users model visible
- [ ] CSV Datasets model visible
- [ ] Can view dataset list
- [ ] Can view dataset details
- [ ] Can filter by status, date, user
- [ ] Can search by file_name, username
- [ ] Cannot manually add datasets
- [ ] Statistics field displays correctly

---

## 🔒 Security Checklist

- [ ] All endpoints (except login) require auth
- [ ] Unauthorized requests return 401
- [ ] Users can only access their own datasets
- [ ] CSRF protection enabled
- [ ] Passwords hashed in database
- [ ] File type validation working
- [ ] File size limit enforced (10MB)
- [ ] SQL injection protected (Django ORM)

---

## 📁 File Structure Checklist

Verify all files exist:

```
backend/
├── config/
│   ├── __init__.py               [ ]
│   ├── settings.py               [ ]
│   ├── urls.py                   [ ]
│   ├── wsgi.py                   [ ]
│   └── asgi.py                   [ ]
├── analytics/
│   ├── __init__.py               [ ]
│   ├── models.py                 [ ]
│   ├── serializers.py            [ ]
│   ├── views.py                  [ ]
│   ├── services.py               [ ]
│   ├── urls.py                   [ ]
│   ├── admin.py                  [ ]
│   └── apps.py                   [ ]
├── users/
│   ├── __init__.py               [ ]
│   ├── serializers.py            [ ]
│   ├── views.py                  [ ]
│   ├── urls.py                   [ ]
│   └── apps.py                   [ ]
├── media/
│   └── csv_uploads/              [ ]
├── manage.py                     [ ]
├── requirements.txt              [ ]
├── README.md                     [ ]
├── API_TESTING.md                [ ]
├── DEPLOYMENT.md                 [ ]
├── QUICKSTART.md                 [ ]
├── PROJECT_SUMMARY.md            [ ]
├── ARCHITECTURE_BACKEND.md       [ ]
├── CHECKLIST.md                  [ ]
├── .gitignore                    [ ]
├── setup.bat                     [ ]
├── setup.sh                      [ ]
├── test_api.py                   [ ]
├── sample_equipment_data.csv     [ ]
└── db.sqlite3 (after migration)  [ ]
```

---

## 🧪 Automated Test Checklist

Run the automated test:

```bash
python test_api.py
```

Verify:
- [ ] Login test passes
- [ ] CSV upload test passes
- [ ] List datasets test passes
- [ ] Statistics test passes
- [ ] Get dataset test passes
- [ ] Logout test passes
- [ ] No errors in output

---

## 📊 Sample Data Checklist

Verify sample_equipment_data.csv:
- [ ] File exists and is readable
- [ ] Contains 30 rows (plus header)
- [ ] Has all 5 required columns
- [ ] Contains 10 different equipment types
- [ ] All numeric values are valid
- [ ] No negative values

**Quick check:**
```bash
head -5 sample_equipment_data.csv
wc -l sample_equipment_data.csv  # Should show 31 (30 + header)
```

---

## 🚀 Deployment Readiness Checklist

- [ ] All tests pass
- [ ] No errors in logs
- [ ] Admin panel working
- [ ] Sample data uploads successfully
- [ ] Statistics compute correctly
- [ ] Documentation complete
- [ ] .gitignore configured
- [ ] requirements.txt complete
- [ ] Secret key can be configured via env var
- [ ] Debug mode can be toggled
- [ ] ALLOWED_HOSTS configurable

---

## 📚 Documentation Checklist

- [ ] README.md complete with setup instructions
- [ ] API_TESTING.md has test examples
- [ ] DEPLOYMENT.md has Render.com guide
- [ ] QUICKSTART.md for fast setup
- [ ] PROJECT_SUMMARY.md for overview
- [ ] ARCHITECTURE_BACKEND.md for system design
- [ ] All endpoints documented
- [ ] Error responses documented
- [ ] CSV format documented

---

## ✅ Final Verification

Run this complete test sequence:

```bash
# 1. Start server
python manage.py runserver

# 2. In new terminal, run tests
python test_api.py

# 3. Upload sample data
curl -X POST http://127.0.0.1:8000/api/analytics/csv/upload/ \
  -u admin:your_password \
  -F "file=@sample_equipment_data.csv"

# 4. Verify in admin
# Open browser: http://127.0.0.1:8000/admin/
# Check CSV Datasets section

# 5. Get statistics
curl -X GET http://127.0.0.1:8000/api/analytics/statistics/ \
  -u admin:your_password
```

---

## 🎯 Success Criteria

All of the following should be true:

✅ Server starts without errors
✅ All 7 endpoints respond correctly
✅ CSV upload processes successfully
✅ Statistics computed accurately
✅ Auto-cleanup works (keeps last 5)
✅ Authentication enforces access control
✅ Admin panel accessible and functional
✅ Documentation complete
✅ No TODO or placeholder code
✅ Ready for production deployment

---

## 🐛 Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| Import errors | `pip install -r requirements.txt` |
| Database errors | `python manage.py migrate` |
| Port in use | `python manage.py runserver 8001` |
| 401 errors | Check credentials, ensure auth header |
| 400 on upload | Check CSV format, required columns |
| File not found | Check media/csv_uploads/ exists |
| Admin 404 | Run migrations, check INSTALLED_APPS |

---

**If all checkboxes are ticked, your backend is production-ready! 🎉**

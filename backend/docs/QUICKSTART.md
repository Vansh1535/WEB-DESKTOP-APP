# ⚡ QUICKSTART GUIDE

**Get the API running in 5 minutes!**

## 🎯 Prerequisites

- Python 3.10 or higher
- pip installed
- Terminal/Command Prompt

## 🚀 Method 1: Automatic Setup (Recommended)

### Windows
```bash
cd backend
setup.bat
```

### macOS/Linux
```bash
cd backend
chmod +x setup.sh
./setup.sh
```

The script will:
1. ✅ Create virtual environment
2. ✅ Install dependencies
3. ✅ Run database migrations
4. ✅ Prompt you to create admin user

Then start the server:
```bash
# Windows
venv\Scripts\activate
python manage.py runserver

# macOS/Linux
source venv/bin/activate
python manage.py runserver
```

## 🔧 Method 2: Manual Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run migrations
python manage.py makemigrations
python manage.py migrate

# 6. Create admin user
python manage.py createsuperuser
# Enter: username, email (optional), password

# 7. Start server
python manage.py runserver
```

## ✅ Verify Installation

Server should be running at: **http://127.0.0.1:8000**

### Option A: Quick Test Script
```bash
python test_api.py
```
Follow the prompts to test all endpoints.

### Option B: Admin Panel
Visit: **http://127.0.0.1:8000/admin/**
Login with your superuser credentials.

### Option C: Manual API Test
```bash
# Login (replace credentials)
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'

# Upload sample CSV
curl -X POST http://127.0.0.1:8000/api/analytics/csv/upload/ \
  -u admin:your_password \
  -F "file=@sample_equipment_data.csv"

# List datasets
curl -X GET http://127.0.0.1:8000/api/analytics/csv/datasets/ \
  -u admin:your_password

# Get statistics
curl -X GET http://127.0.0.1:8000/api/analytics/statistics/ \
  -u admin:your_password
```

## 📊 Test with Sample Data

A sample CSV file is included: `sample_equipment_data.csv`

It contains 30 rows of equipment data across 10 different types:
- Pumps
- Valves
- Heat Exchangers
- Reactors
- Compressors
- Tanks
- Turbines
- Mixers
- Separators
- Boilers

## 🎯 Next Steps

1. **Read the docs:** `README.md` for full API documentation
2. **Test the API:** Use `test_api.py` or examples in `API_TESTING.md`
3. **Explore admin:** Visit `/admin/` to manage data
4. **Deploy:** Follow `DEPLOYMENT.md` to deploy on Render.com

## 📱 API Endpoints Summary

### Authentication
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout

### Analytics
- `POST /api/analytics/csv/upload/` - Upload CSV
- `GET /api/analytics/csv/datasets/` - List datasets
- `GET /api/analytics/csv/datasets/{id}/` - Get dataset
- `DELETE /api/analytics/csv/datasets/{id}/` - Delete dataset
- `GET /api/analytics/statistics/` - Get statistics

All endpoints (except login) require Basic Authentication.

## 🐛 Troubleshooting

### "Python not found"
Install Python 3.10+ from python.org

### "pip not found"
```bash
python -m ensurepip --upgrade
```

### "Port already in use"
```bash
# Use different port
python manage.py runserver 8001
```

### "ModuleNotFoundError"
```bash
# Make sure virtual environment is activated
pip install -r requirements.txt
```

### "No such table"
```bash
python manage.py migrate
```

## 📚 Documentation Files

- `README.md` - Complete documentation
- `API_TESTING.md` - Testing guide
- `DEPLOYMENT.md` - Deployment guide
- `PROJECT_SUMMARY.md` - Project overview
- `QUICKSTART.md` - This file

## 💡 Tips

- Keep the virtual environment activated while working
- Use the admin panel for quick data inspection
- Check server logs in terminal for errors
- Sample CSV file is included for testing
- System keeps only last 5 datasets per user

## 🎉 Success!

If you can:
- ✅ Access http://127.0.0.1:8000/admin/
- ✅ Login with your credentials
- ✅ Upload the sample CSV
- ✅ See statistics

**Your backend is working perfectly!**

---

**Need help?** Check `README.md` for detailed documentation.

**Ready to deploy?** See `DEPLOYMENT.md` for production setup.

**Want to test?** Run `python test_api.py` or see `API_TESTING.md`.

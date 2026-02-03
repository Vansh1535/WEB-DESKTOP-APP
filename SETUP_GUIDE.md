# 🚀 Complete Setup & Installation Guide

This guide provides detailed step-by-step instructions for setting up the Chemical Equipment Parameter Visualizer on your system.

## 📋 Table of Contents

- [System Requirements](#system-requirements)
- [Quick Start](#quick-start)
- [Detailed Setup Instructions](#detailed-setup-instructions)
- [Configuration](#configuration)
- [Testing the Setup](#testing-the-setup)
- [Common Issues & Troubleshooting](#common-issues--troubleshooting)
- [Production Deployment](#production-deployment)

---

## 🖥️ System Requirements

### Minimum Requirements
- **Operating System:** Windows 10/11, macOS 10.14+, or Linux (Ubuntu 20.04+)
- **RAM:** 4GB minimum (8GB recommended)
- **Storage:** 1GB free space
- **Internet:** Required for downloading dependencies

### Software Prerequisites

#### Required
- **Python 3.11 or higher** → [Download Python](https://www.python.org/downloads/)
- **Node.js 18 or higher** → [Download Node.js](https://nodejs.org/)
- **Git** → [Download Git](https://git-scm.com/)

#### Optional but Recommended
- **pnpm** (faster than npm) → Install: `npm install -g pnpm`
- **VS Code** or your preferred IDE
- **Postman** for API testing

### Verify Installation

```bash
# Check Python version
python --version
# Should output: Python 3.11.x or higher

# Check Node.js version
node --version
# Should output: v18.x.x or higher

# Check Git version
git --version
# Should output: git version 2.x.x
```

---

## ⚡ Quick Start

For experienced developers who want to get started immediately:

```bash
# 1. Clone repository
git clone https://github.com/Vansh1535/WEB-DESKTOP-APP.git
cd WEB_DESKTOP_APP

# 2. Backend setup
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python manage.py migrate
python create_desktop_users.py
python manage.py runserver

# 3. Frontend setup (new terminal)
cd Web-Frontend
pnpm install
pnpm dev

# 4. Desktop app (new terminal)
cd Desktop-App
pip install -r requirements.txt
python main.py
```

**Access:**
- Web: http://localhost:3000
- Backend API: http://localhost:8000
- Login: `admin` / `admin123`

---

## 📖 Detailed Setup Instructions

### Step 1: Clone the Repository

```bash
# Clone via HTTPS
git clone https://github.com/Vansh1535/WEB-DESKTOP-APP.git

# OR Clone via SSH (if configured)
git clone git@github.com:Vansh1535/WEB-DESKTOP-APP.git

# Navigate to project directory
cd WEB_DESKTOP_APP
```

**Verify clone:**
```bash
# List project structure
dir        # Windows
ls -la     # Mac/Linux
```

You should see: `backend/`, `Web-Frontend/`, `Desktop-App/`, `README.md`

---

### Step 2: Backend (Django) Setup

#### 2.1 Navigate to Backend Directory

```bash
cd backend
```

#### 2.2 Create Virtual Environment

**Windows:**
```bash
python -m venv venv
```

**Mac/Linux:**
```bash
python3 -m venv venv
```

#### 2.3 Activate Virtual Environment

**Windows (CMD):**
```bash
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

Your prompt should now show `(venv)` prefix.

#### 2.4 Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected packages:**
- Django 4.2+
- djangorestframework
- django-cors-headers
- pandas
- reportlab
- matplotlib
- Pillow

#### 2.5 Database Setup

```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

You should see output like:
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying users.0001_initial... OK
  Applying analytics.0001_initial... OK
  ...
```

#### 2.6 Create Test Users

```bash
# Option 1: Use automated script (creates admin, test, demo users)
python create_desktop_users.py

# Option 2: Create superuser manually
python manage.py createsuperuser
```

**Test User Credentials:**
- Username: `admin` | Password: `admin123`
- Username: `test` | Password: `test123`
- Username: `demo` | Password: `demo123`

#### 2.7 Start Backend Server

```bash
python manage.py runserver
```

**Success message:**
```
Django version 4.2.x, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

**Test the backend:**
Open browser → http://localhost:8000/api/v1/auth/login/

You should see the Django REST framework browsable API.

---

### Step 3: Web Frontend (Next.js) Setup

**Open a NEW terminal** (keep backend running)

#### 3.1 Navigate to Frontend Directory

```bash
cd Web-Frontend
```

#### 3.2 Install Node Dependencies

**Using pnpm (recommended):**
```bash
# Install pnpm globally if not installed
npm install -g pnpm

# Install project dependencies
pnpm install
```

**Using npm:**
```bash
npm install
```

**Using yarn:**
```bash
yarn install
```

#### 3.3 Configure Environment Variables

Create `.env.local` file:

**Windows:**
```bash
echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
```

**Mac/Linux:**
```bash
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

**Or manually create** `Web-Frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### 3.4 Start Development Server

```bash
pnpm dev
# or
npm run dev
```

**Success message:**
```
▲ Next.js 16.0.10
- Local:        http://localhost:3000
- Network:      http://192.168.x.x:3000

✓ Ready in 2.5s
```

**Test the frontend:**
Open browser → http://localhost:3000

You should see the login page with chemistry theme.

---

### Step 4: Desktop App (PyQt5) Setup

**Open a NEW terminal** (keep backend & frontend running)

#### 4.1 Navigate to Desktop App Directory

```bash
cd Desktop-App
```

#### 4.2 Install Desktop Dependencies

**Option A: Use existing backend venv**
```bash
# If you're using the same venv as backend
# Activate backend's venv
cd ..\backend
venv\Scripts\activate    # Windows
cd ..\Desktop-App
pip install -r requirements.txt
```

**Option B: Create separate venv**
```bash
python -m venv venv_desktop
venv_desktop\Scripts\activate    # Windows
pip install -r requirements.txt
```

**Expected packages:**
- PyQt5
- matplotlib
- numpy
- requests

#### 4.3 Configure Backend URL (Optional)

If backend is not running on default port, edit `utils/config.py`:

```python
API_BASE_URL = "http://localhost:8000"  # Change if needed
```

#### 4.4 Launch Desktop Application

```bash
python main.py
```

A PyQt5 window should open with the login screen.

**Login using:**
- Username: `admin`
- Password: `admin123`

---

## ⚙️ Configuration

### Backend Configuration

Edit `backend/config/settings.py` for:

```python
# Debug mode (disable in production)
DEBUG = True

# Allowed hosts
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# CORS settings
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

# Database (default: SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Media files (CSV uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Frontend Configuration

Edit `Web-Frontend/.env.local`:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Optional: Analytics, etc.
# NEXT_PUBLIC_GA_ID=your-ga-id
```

### Desktop App Configuration

Edit `Desktop-App/utils/config.py`:

```python
# Backend API URL
API_BASE_URL = "http://localhost:8000"

# Window settings
WINDOW_TITLE = "Chemical Equipment Visualizer"
DEFAULT_WIDTH = 1000
DEFAULT_HEIGHT = 850
```

---

## 🧪 Testing the Setup

### 1. Test Backend API

**Using curl:**
```bash
# Test login endpoint
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

**Using Python script:**
```bash
cd backend/tests
python test_connection.py
```

**Expected output:**
```
✓ Backend connection successful
✓ Authentication working
✓ API endpoints available
```

### 2. Test Web Frontend

1. Open http://localhost:3000
2. Login with `admin` / `admin123`
3. Upload sample CSV: `backend/data/sample_equipment_data.csv`
4. Check dashboard displays charts
5. Generate PDF report
6. Verify history shows uploaded file

### 3. Test Desktop App

1. Launch desktop app: `python main.py`
2. Login with `admin` / `admin123`
3. Dashboard should load with statistics
4. Click "Upload CSV" and select sample file
5. Verify charts display correctly
6. Try "Generate Report" feature

### 4. Upload Sample Data

**Sample CSV location:** `backend/data/sample_equipment_data.csv`

**Via Web:**
1. Dashboard → Upload CSV button
2. Select `sample_equipment_data.csv`
3. Click Upload

**Via Desktop:**
1. Main window → 📤 Upload CSV
2. Browse and select CSV
3. Confirm upload

---

## 🔧 Common Issues & Troubleshooting

### Issue 1: Virtual Environment Not Activating (Windows)

**Error:** `Activate.ps1 cannot be loaded because running scripts is disabled`

**Solution:**
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 2: Port Already in Use

**Error:** `Error: That port is already in use.`

**Solution:**

**Backend (change port):**
```bash
python manage.py runserver 8001
# Update frontend .env.local accordingly
```

**Frontend (change port):**
```bash
# Edit package.json
"dev": "next dev -p 3001"
```

**Find and kill process:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

### Issue 3: CORS Errors in Browser

**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Solution:**

1. Verify backend CORS settings in `backend/config/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
CORS_ALLOW_CREDENTIALS = True
```

2. Restart backend server

### Issue 4: Module Not Found Errors

**Error:** `ModuleNotFoundError: No module named 'django'`

**Solution:**
```bash
# Ensure virtual environment is activated
# Windows
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 5: Database Migration Errors

**Error:** `django.db.utils.OperationalError`

**Solution:**
```bash
# Delete database and migrations
rm db.sqlite3
rm */migrations/0*.py

# Recreate migrations
python manage.py makemigrations
python manage.py migrate
python create_desktop_users.py
```

### Issue 6: PyQt5 Not Displaying

**Error:** `ImportError: No module named 'PyQt5'`

**Solution:**
```bash
pip install PyQt5 PyQt5-tools
# On Linux, you may need:
sudo apt-get install python3-pyqt5
```

### Issue 7: CSV Upload Fails

**Error:** `Invalid CSV format`

**Solution:**
1. Ensure CSV has correct columns:
   - Equipment_ID, Equipment_Name, Type, Flowrate, Pressure, Temperature
2. Use provided sample: `backend/data/sample_equipment_data.csv`
3. Check for proper encoding (UTF-8)

### Issue 8: Frontend Not Connecting to Backend

**Checklist:**
- [ ] Backend is running on http://localhost:8000
- [ ] `.env.local` has correct `NEXT_PUBLIC_API_URL`
- [ ] CORS is configured correctly
- [ ] No firewall blocking requests
- [ ] Browser console shows no errors

**Debug:**
```bash
# Check backend status
curl http://localhost:8000/api/v1/auth/login/

# Verify frontend env
cd Web-Frontend
cat .env.local
```

---

## 🌐 Production Deployment

### Backend Deployment (Django)

#### Using Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Collect static files
python manage.py collectstatic --no-input

# Run with gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

#### Environment Variables

Create `.env` file:
```env
DEBUG=False
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

#### Database (PostgreSQL)

```bash
# Install psycopg2
pip install psycopg2-binary

# Update settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'chemequip_db',
        'USER': 'dbuser',
        'PASSWORD': 'dbpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Frontend Deployment (Next.js)

#### Build for Production

```bash
cd Web-Frontend

# Build
pnpm build

# Start production server
pnpm start
```

#### Using Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

#### Using Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

### Desktop App Distribution

#### Windows Executable (PyInstaller)

```bash
pip install pyinstaller

pyinstaller --onefile --windowed \
  --name="ChemicalEquipmentVisualizer" \
  --icon=icon.ico \
  main.py
```

Output: `dist/ChemicalEquipmentVisualizer.exe`

---

## 📝 Additional Resources

### Project Documentation
- [API Documentation](API_DOCUMENTATION.md)
- [Features Overview](FEATURES.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Backend README](backend/README.md)
- [Frontend README](Web-Frontend/README.md)
- [Desktop App README](Desktop-App/README.md)

### External Resources
- [Django Documentation](https://docs.djangoproject.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

### Video Tutorials
- Django REST Framework Basics
- Next.js App Router Guide
- PyQt5 GUI Development

---

## 🆘 Getting Help

If you encounter issues not covered in this guide:

1. **Check existing documentation** in the `docs/` folders
2. **Search closed issues** on GitHub
3. **Open a new issue** with:
   - Detailed problem description
   - Steps to reproduce
   - Error messages/screenshots
   - Environment details (OS, Python version, etc.)

---

## ✅ Setup Verification Checklist

Before submitting or deploying, verify:

- [ ] Backend runs without errors
- [ ] Frontend loads and displays correctly
- [ ] Desktop app launches successfully
- [ ] Login/authentication works
- [ ] CSV upload functions properly
- [ ] Charts display data correctly
- [ ] PDF generation works
- [ ] All test users can login
- [ ] Sample data uploads successfully
- [ ] No console errors in browser
- [ ] All API endpoints respond
- [ ] Documentation is complete

---

**Setup complete! 🎉 You're ready to use the Chemical Equipment Parameter Visualizer.**

For questions, refer to [CONTRIBUTING.md](CONTRIBUTING.md) or open an issue on GitHub.

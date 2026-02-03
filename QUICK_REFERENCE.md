# 🚀 Quick Reference Guide

One-page reference for common tasks and commands.

---

## ⚡ Quick Start Commands

### Automated Setup
```bash
# Windows
setup.bat

# Mac/Linux
chmod +x setup.sh && ./setup.sh
```

### Start All Services
```bash
# Windows
start-all.bat

# Mac/Linux
chmod +x start-all.sh && ./start-all.sh
```

---

## 🔑 Default Credentials

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Superuser |
| test | test123 | Regular User |
| demo | demo123 | Regular User |

---

## 🌐 Access URLs

| Service | URL |
|---------|-----|
| Web Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| Django Admin | http://localhost:8000/admin |
| API Documentation | http://localhost:8000/api/v1/ |

---

## 📂 Project Structure

```
WEB_DESKTOP_APP/
├── backend/           # Django REST API
├── Web-Frontend/      # Next.js Web App
├── Desktop-App/       # PyQt5 Desktop App
├── README.md          # Main documentation
├── SETUP_GUIDE.md     # Detailed setup
├── CONTRIBUTING.md    # Contribution guide
└── PROJECT_STATUS.md  # Project status
```

---

## 🛠️ Common Commands

### Backend (Django)

```bash
cd backend
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Run server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Create test users
python create_desktop_users.py

# Run tests
python manage.py test
python tests/test_api.py
```

### Web Frontend (Next.js)

```bash
cd Web-Frontend

# Install dependencies
npm install  # or pnpm install

# Development mode
npm run dev  # or pnpm dev

# Production build
npm run build
npm start

# Lint
npm run lint
```

### Desktop App (PyQt5)

```bash
cd Desktop-App

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py

# Run tests
python test_app.py
```

---

## 📤 CSV Upload

### Required CSV Format

```csv
Equipment_ID,Equipment_Name,Type,Flowrate,Pressure,Temperature
EQ001,Reactor A,Reactor,150.5,10.2,350.0
EQ002,Pump B,Pump,200.3,15.8,25.0
```

### Sample Data Location
`backend/data/sample_equipment_data.csv`

---

## 🔌 API Endpoints Quick Reference

### Authentication
```bash
POST /api/v1/auth/register/    # Register new user
POST /api/v1/auth/login/       # Login
POST /api/v1/auth/logout/      # Logout
```

### Analytics
```bash
POST   /api/v1/analytics/csv/upload/          # Upload CSV
GET    /api/v1/analytics/csv/datasets/        # List datasets
GET    /api/v1/analytics/csv/datasets/{id}/   # Get dataset
DELETE /api/v1/analytics/csv/datasets/{id}/   # Delete dataset
GET    /api/v1/analytics/csv/statistics/      # Get stats
GET    /api/v1/analytics/csv/datasets/{id}/pdf/  # Download PDF
```

### Example API Call
```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# List datasets (Basic Auth)
curl -X GET http://localhost:8000/api/v1/analytics/csv/datasets/ \
  -u admin:admin123
```

---

## 🐛 Troubleshooting Quick Fixes

### Port Already in Use
```bash
# Backend (change port)
python manage.py runserver 8001

# Frontend (package.json)
"dev": "next dev -p 3001"
```

### Virtual Environment Issues
```bash
# Windows
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Recreate venv
rm -rf venv
python -m venv venv
```

### Database Reset
```bash
cd backend
rm db.sqlite3
rm */migrations/0*.py
python manage.py makemigrations
python manage.py migrate
python create_desktop_users.py
```

### Clear Node Modules
```bash
cd Web-Frontend
rm -rf node_modules package-lock.json
npm install
```

### CORS Errors
Check `backend/config/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
```

---

## 📊 Feature Checklist

### Web Application
- [x] User login/registration
- [x] CSV file upload
- [x] Data visualization (4 chart types)
- [x] Statistics dashboard
- [x] History management
- [x] PDF report generation
- [x] Responsive design

### Desktop Application
- [x] Login window
- [x] Fullscreen dashboard
- [x] CSV upload dialog
- [x] Chart visualizations
- [x] Report generation
- [x] Data export

### Backend API
- [x] User authentication
- [x] CSV parsing
- [x] Statistical analysis
- [x] Dataset management
- [x] PDF generation
- [x] RESTful API design

---

## 🧪 Testing Commands

```bash
# Backend API tests
cd backend
python tests/test_api.py
python tests/test_users.py
python tests/test_complete_flow.py
python tests/test_pdf.py
python tests/test_connection.py

# Desktop app test
cd Desktop-App
python test_app.py
```

---

## 📦 Dependencies Summary

### Backend (Python)
- Django 4.2+
- djangorestframework
- django-cors-headers
- pandas
- reportlab
- matplotlib
- Pillow

### Frontend (Node.js)
- next 16+
- react 19+
- recharts
- typescript
- tailwindcss
- shadcn/ui components

### Desktop (Python)
- PyQt5
- matplotlib
- numpy
- requests

---

## 🎥 Demo Video Checklist

### Recording (2-3 minutes)
- [ ] Introduction & overview
- [ ] Web app demo (login, upload, charts, PDF)
- [ ] Desktop app demo (dashboard, visualizations)
- [ ] Backend API demo (Postman/curl)
- [ ] Key features highlight
- [ ] GitHub repository mention

### Tools
- OBS Studio (free)
- Loom (easy)
- Camtasia (professional)

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| [README.md](README.md) | Main project overview |
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | Detailed setup instructions |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |
| [PROJECT_STATUS.md](PROJECT_STATUS.md) | Project status & checklist |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | API reference |
| [FEATURES.md](FEATURES.md) | Feature descriptions |
| [LICENSE](LICENSE) | MIT License |

---

## 🚀 Deployment Quick Guide

### Frontend (Vercel)
```bash
npm i -g vercel
cd Web-Frontend
vercel
```

### Backend (Railway)
```bash
npm i -g @railway/cli
cd backend
railway login
railway init
railway up
```

---

## 📞 Getting Help

1. Check [SETUP_GUIDE.md](SETUP_GUIDE.md) troubleshooting section
2. Review [CONTRIBUTING.md](CONTRIBUTING.md)
3. Search GitHub issues
4. Open new issue with details

---

## ✅ Pre-Submission Checklist

- [ ] All features working
- [ ] Tests passing
- [ ] Documentation complete
- [ ] No sensitive data in repo
- [ ] .gitignore configured
- [ ] Demo video recorded
- [ ] README updated with links

---

**Quick Reference v1.0** | Chemical Equipment Parameter Visualizer | FOSSEE Internship

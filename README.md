# Chemical Equipment Parameter Visualizer
## Hybrid Web + Desktop Application

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Django](https://img.shields.io/badge/django-4.2-green.svg)
![Next.js](https://img.shields.io/badge/next.js-16.0-black.svg)
![React](https://img.shields.io/badge/react-19.2-blue.svg)

A full-stack application for uploading, analyzing, and visualizing chemical equipment parameters with CSV data processing, real-time statistics, and PDF report generation.

## 🚀 Features

- ✅ **CSV Upload & Processing** - Upload equipment data with automatic validation
- ✅ **Real-time Analytics** - Compute statistics, averages, min/max values
- ✅ **Data Visualization** - Interactive charts and graphs
- ✅ **History Management** - Keep last 5 datasets per user
- ✅ **PDF Reports** - Generate professional reports with one click
- ✅ **Authentication** - Secure login with Basic Authentication
- ✅ **Responsive UI** - Dark/Light theme support
- ✅ **RESTful API** - Well-documented API endpoints

## 📋 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend (Web)** | Next.js 16 + React 19 + TypeScript | Modern web interface |
| **Frontend (Desktop)** | PyQt5 + Matplotlib | Desktop application |
| **Backend** | Django 4.2 + Django REST Framework | API server |
| **Data Processing** | Pandas + NumPy | CSV analysis |
| **Database** | SQLite | Data storage |
| **Charts** | Recharts (Web) + Matplotlib (Desktop) | Data visualization |
| **Reports** | ReportLab | PDF generation |

## 📁 Project Structure

```
WEB_DESKTOP_APP/
├── backend/                 # Django Backend
│   ├── analytics/          # Main analytics app
│   ├── users/             # Authentication
│   ├── config/            # Django settings
│   ├── data/              # Sample CSV data
│   ├── media/             # Uploaded files
│   └── tests/             # Test scripts
│
├── Web-Frontend/           # Next.js Frontend
│   ├── app/               # Pages (Login, Dashboard)
│   ├── components/        # React components
│   ├── lib/               # API utilities
│   └── public/            # Static assets
│
├── Desktop-App/           # PyQt5 Desktop Application
│   ├── main.py           # Application entry point
│   ├── ui/               # UI components
│   ├── services/         # API client
│   └── utils/            # Utilities
│
├── START.bat              # Windows quick start
├── START.sh               # Linux/Mac quick start
└── SETUP_AND_RUN.md       # Detailed setup guide
```

## 🏃 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- pnpm (or npm)

### 1. Backend Setup

```bash
cd backend

# Windows
setup.bat

# Linux/Mac
chmod +x setup.sh
./setup.sh
```

### 2. Frontend Setup

```bash
cd Web-Frontend
pnpm install
```

### 3. Start Applications

**Backend (Required for all frontends):**
```bash
# Terminal 1
cd backend
python manage.py runserver
```

**Web Frontend:**
```bash
# Terminal 2
cd Web-Frontend
pnpm dev
```

**Desktop Application:**
```bash
# Windows
cd Desktop-App
run.bat

# Linux/Mac
cd Desktop-App
chmod +x run.sh
./run.sh
```

Or manually:
```bash
cd Desktop-App
pip install -r requirements.txt
python main.py
```

### 4. Access the Application

- **Web Frontend**: http://localhost:3000
- **Desktop App**: Launch via PyQt5 window
- **Backend API**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin

**Default Login:**
- Username: `admin`
- Password: `admin123`

## 📊 CSV File Format

Your CSV must have these columns:

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump A1,Pump,250.5,8.2,85.0
Reactor B2,Reactor,180.3,12.5,120.5
Heat Exchanger C3,Heat Exchanger,300.0,6.8,95.2
```

**Sample data:** `backend/data/sample_equipment_data.csv`

## 🔌 API Endpoints

### Authentication
```
POST   /api/v1/auth/login/     - Login
POST   /api/v1/auth/logout/    - Logout
```

### Analytics
```
POST   /api/v1/analytics/csv/upload/          - Upload CSV
GET    /api/v1/analytics/csv/datasets/        - List datasets
GET    /api/v1/analytics/csv/datasets/{id}/   - Get dataset
DELETE /api/v1/analytics/csv/datasets/{id}/   - Delete dataset
GET    /api/v1/analytics/csv/statistics/      - Get statistics
GET    /api/v1/analytics/csv/datasets/{id}/pdf/ - Download PDF
```

## 🧪 Testing

### Test Backend Connection
```bash
cd backend
python tests/test_connection.py
```

### Test API Manually
```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# List datasets (with Basic Auth)
curl -X GET http://localhost:8000/api/v1/analytics/csv/datasets/ \
  -u admin:admin123
```

## 🎨 Screenshots

### Login Page
Clean, modern authentication interface with vibrant chemistry-themed design.

### Dashboard
- Real-time statistics cards
- Interactive charts (Bar, Line, Pie)
- Data table with sorting/filtering
- Recent uploads history

### Features
- Drag & drop CSV upload
- PDF report generation
- Dark/Light theme toggle
- Responsive design

## 🔧 Configuration

### Backend Environment Variables
Create `backend/.env` (optional):
```bash
SECRET_KEY=your-secret-key
DEBUG=True
MAX_DATASETS_PER_USER=5
```

### Frontend Environment Variables
Edit `Web-Frontend/.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📚 Documentation

- **[Complete Setup Guide](SETUP_AND_RUN.md)** - Detailed installation instructions
- **[Backend Architecture](backend/docs/ARCHITECTURE_BACKEND.md)** - Backend design
- **[API Testing Guide](backend/docs/API_TESTING.md)** - API documentation
- **[Frontend Guide](Web-Frontend/README.md)** - Frontend details

## 🐛 Troubleshooting

### CORS Errors
Ensure `django-cors-headers` is installed and configured in `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
```

### Connection Refused
1. Check backend is running: `http://localhost:8000`
2. Verify `.env.local` has correct API URL
3. Check firewall settings

### Port Already in Use
```bash
# Backend - use different port
python manage.py runserver 8001

# Update frontend .env.local
NEXT_PUBLIC_API_URL=http://localhost:8001
```

## 🚀 Deployment

### Backend
```bash
cd backend
python manage.py collectstatic
python manage.py migrate
# Use gunicorn or similar for production
gunicorn config.wsgi:application
```

### Frontend
```bash
cd Web-Frontend
pnpm build
pnpm start
```

## 📦 Dependencies

### Backend
- Django 4.2.7
- djangorestframework 3.14.0
- django-cors-headers 4.3.1
- pandas 2.2.0+
- reportlab 4.0.7

### Frontend
- next 16.0.10
- react 19.2.0
- recharts 2.15.4
- typescript 5+

## 🎯 Roadmap

- [ ] PyQt5 Desktop Application
- [ ] Advanced filtering and search
- [ ] Excel export functionality
- [ ] User management interface
- [ ] Data comparison between uploads
- [ ] Scheduled reports
- [ ] Email notifications
- [ ] Docker containerization

## 👥 Contributing

This is an intern screening project. Contributions and suggestions are welcome!

## 📄 License

This project is created for educational purposes.

## 🙏 Acknowledgments

- FOSSEE (Free and Open Source Software for Education)
- Django REST Framework
- Next.js Team
- All open-source contributors

---

**Made with ❤️ for chemical equipment analysis**

For questions or issues, please check the [detailed setup guide](SETUP_AND_RUN.md) or review the troubleshooting section.

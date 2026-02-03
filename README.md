# Chemical Equipment Parameter Visualizer

A comprehensive hybrid application for visualizing and analyzing chemical equipment data, built with Django backend, Next.js web frontend, and PyQt5 desktop application.

![Project Banner](https://img.shields.io/badge/Status-Complete-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-4.2+-green?style=for-the-badge&logo=django)
![Next.js](https://img.shields.io/badge/Next.js-16-black?style=for-the-badge&logo=next.js)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-blue?style=for-the-badge&logo=qt)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project is a **FOSSEE Internship Screening Task** that demonstrates the ability to build a full-stack hybrid application. It provides both web and desktop interfaces for uploading, analyzing, and visualizing chemical equipment data with features like:

- **CSV Data Upload** - Import equipment data with parameters like flowrate, pressure, and temperature
- **Data Analytics** - Automatic statistical analysis and summary generation
- **Interactive Visualizations** - Multiple chart types showing equipment metrics
- **PDF Report Generation** - Export professional reports with charts and statistics
- **User Authentication** - Secure login and registration system
- **History Management** - Track all uploaded datasets with metadata
- **Responsive UI** - Modern, professional interface with vibrant orange/coral gradient theme

## ✨ Features

### Core Features (Task Requirements)
- ✅ CSV file upload (Web + Desktop)
- ✅ Data summary API with statistics
- ✅ Interactive charts and visualizations
- ✅ History of uploaded datasets
- ✅ PDF report generation
- ✅ Basic authentication system
- ✅ Sample CSV data provided

### Bonus Features (Enhancements)
- 🎨 Modern vibrant UI with gradient theme
- 📊 4 visualization types (Bar, Box Plot, Line Chart, Pie Chart)
- 👥 Multi-user support with user preferences
- 🔒 Secure Basic Authentication
- 📱 Responsive web design
- 🖥️ Fullscreen desktop application
- 💾 Export data to CSV
- 🔄 Real-time data refresh
- 📈 Statistics cards with key metrics

## 🛠️ Tech Stack

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework** - API development
- **Pandas** - Data processing and analysis
- **ReportLab** - PDF generation
- **Matplotlib** - Chart generation for PDFs
- **SQLite** - Database

### Web Frontend
- **Next.js 16** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Shadcn/ui** - UI components
- **React Hook Form** - Form handling

### Desktop Frontend
- **PyQt5** - GUI framework
- **Matplotlib** - Data visualization
- **NumPy** - Numerical operations

## 📁 Project Structure

```
WEB_DESKTOP_APP/
├── backend/                    # Django Backend
│   ├── analytics/             # Analytics app (CSV processing, statistics)
│   ├── users/                 # User authentication app
│   ├── config/                # Django settings
│   ├── media/                 # Uploaded CSV files
│   ├── db.sqlite3            # SQLite database
│   ├── manage.py             # Django management script
│   └── requirements.txt      # Python dependencies
│
├── Web-Frontend/              # Next.js Web Application
│   ├── app/                   # Next.js 13+ app directory
│   │   ├── dashboard/        # Dashboard pages
│   │   ├── login/            # Login page
│   │   └── page.tsx          # Home page
│   ├── components/            # React components
│   ├── lib/                   # Utilities and API client
│   ├── hooks/                 # Custom React hooks
│   ├── styles/                # CSS styles
│   └── package.json          # Node.js dependencies
│
├── Desktop-App/               # PyQt5 Desktop Application
│   ├── ui/                    # UI components
│   │   ├── login_window.py   # Login/Register window
│   │   ├── main_window.py    # Main dashboard
│   │   ├── chart_widgets.py  # Chart components
│   │   ├── upload_dialog.py  # Upload dialog
│   │   └── report_dialog.py  # Report generation dialog
│   ├── utils/                 # Utilities
│   │   ├── api_client.py     # Backend API client
│   │   └── config.py         # Configuration
│   ├── main.py               # Application entry point
│   ├── requirements.txt      # Python dependencies
│   └── setup.bat             # Windows setup script
│
└── data/                      # Sample data
    └── sample_equipment_data.csv
```

## 🚀 Installation & Setup

### Prerequisites
- **Python 3.11+** installed
- **Node.js 18+** and npm/pnpm installed
- **Git** installed
- **Virtual environment** (recommended)

### Step 1: Clone Repository

```bash
git clone https://github.com/Vansh1535/WEB-DESKTOP-APP.git
cd WEB_DESKTOP_APP
```

### Step 2: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create test users
python create_desktop_users.py

# Start backend server
python manage.py runserver
```

Backend will run at **http://localhost:8000**

### Step 3: Web Frontend Setup

```bash
# Open new terminal
cd Web-Frontend

# Install dependencies
npm install
# or
pnpm install

# Start development server
npm run dev
# or
pnpm dev
```

Web frontend will run at **http://localhost:3000**

### Step 4: Desktop App Setup

```bash
# Open new terminal
cd Desktop-App

# Activate virtual environment
# (Use same venv as backend or create new one)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run desktop application
python main.py
```

Desktop app will open in a new window

## 📖 Usage Guide

### Test Credentials
```
Username: admin  | Password: admin123
Username: test   | Password: test123
Username: demo   | Password: demo123
```

### Web Application

1. **Login**: Navigate to http://localhost:3000 and login
2. **Upload CSV**: Click "Upload CSV" button in dashboard
3. **View Data**: Browse uploaded data in Data View tab
4. **Generate Report**: Click "Generate Report" to create PDF
5. **View History**: Check History tab for all uploads

### Desktop Application

1. **Launch**: Run `python main.py` in Desktop-App directory
2. **Login**: Enter credentials in login window
3. **Dashboard**: View statistics and charts in fullscreen
4. **Upload**: Click "📤 Upload CSV" to add data
5. **Export**: Generate PDF reports or export to CSV

### CSV File Format

Your CSV file should have these columns:
```csv
Equipment_ID,Equipment_Name,Type,Flowrate,Pressure,Temperature
EQ001,Reactor A,Reactor,150.5,10.2,350.0
EQ002,Pump B,Pump,200.3,15.8,25.0
```

**Required Columns:**
- Equipment_ID
- Equipment_Name  
- Type
- Flowrate (numeric)
- Pressure (numeric)
- Temperature (numeric)

## 🔌 API Documentation

### Authentication

**Register User**
```http
POST /api/v1/auth/register/
Content-Type: application/json

{
  "username": "newuser",
  "email": "user@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Login**
```http
POST /api/v1/auth/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

### Analytics Endpoints

**Upload CSV**
```http
POST /api/v1/analytics/csv/upload/
Authorization: Basic <credentials>
Content-Type: multipart/form-data

file: <CSV file>
```

**List Datasets**
```http
GET /api/v1/analytics/datasets/
Authorization: Basic <credentials>
```

**Get Dataset Statistics**
```http
GET /api/v1/analytics/datasets/{id}/
Authorization: Basic <credentials>
```

**Generate PDF Report**
```http
GET /api/v1/analytics/datasets/{id}/pdf-report/
Authorization: Basic <credentials>
```

**Delete Dataset**
```http
DELETE /api/v1/analytics/datasets/{id}/
Authorization: Basic <credentials>
```

For complete API documentation, see [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

## 📸 Screenshots

### Web Application
- **Dashboard**: Statistics cards, interactive charts
- **Data View**: Sortable table with all equipment data
- **History**: Track all uploaded datasets

### Desktop Application
- **Login Window**: Clean authentication interface (1000×850px)
- **Dashboard**: Fullscreen with 4 chart visualizations (16×10 figsize)
- **History Table**: 75px rows with prominent action buttons

## 🎥 Demo Video

📹 [Watch Demo Video](./demo-video-link) - 2-3 minute walkthrough of key features

## 🧪 Testing

### Backend Tests
```bash
cd backend
python manage.py test
```

### Sample Data
Use `data/sample_equipment_data.csv` for testing:
- 30 rows of sample equipment data
- Various equipment types (Reactor, Pump, Heat Exchanger, Compressor, Distillation Column)
- Realistic parameter ranges

## 🚧 Development Notes

### Backend
- Uses SQLite for development (easily switchable to PostgreSQL)
- Basic Authentication implemented
- CORS enabled for local development
- Media files stored in `backend/media/csv_uploads/`

### Web Frontend
- Built with Next.js 16 App Router
- Environment variable: `NEXT_PUBLIC_API_URL`
- TypeScript for type safety
- Responsive design for mobile/tablet

### Desktop Application
- Vibrant orange/coral gradient theme (#eb915f, #f97c66, #a966d9)
- Charts: 700px minimum height, 14pt/11pt/10pt fonts
- Fullscreen on startup with scrollable dashboard
- 75px row height in history table

## 🤝 Contributing

This is a screening task project, but contributions are welcome:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is created as part of FOSSEE Internship screening task.

## 👨‍💻 Author

**Vansh** - [GitHub Profile](https://github.com/Vansh1535)

## 🙏 Acknowledgments

- **FOSSEE** for the internship opportunity
- Django, Next.js, and PyQt5 communities
- Sample CSV data structure provided in task requirements

## 📞 Support

For questions or issues:
- Open an issue on [GitHub Repository](https://github.com/Vansh1535/WEB-DESKTOP-APP)
- Review [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed troubleshooting
- Check [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines

---

**Built with ❤️ for FOSSEE Internship Screening Task**

## 🎯 Quick Start Summary

### Automated Setup (Recommended)

**Windows:**
```bash
setup.bat
```

**Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### Quick Start All Services

**Windows:**
```bash
start-all.bat
```

**Mac/Linux:**
```bash
chmod +x start-all.sh
./start-all.sh
```

### Manual Start

**Backend:**
```bash
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
python manage.py runserver
```

**Web Frontend:**
```bash
cd Web-Frontend
npm run dev  # or pnpm dev
```

**Desktop Application:**
```bash
cd Desktop-App
pip install -r requirements.txt
python main.py
```

### Access Points

- **Web Frontend**: http://localhost:3000
- **Desktop App**: PyQt5 Window (launches automatically)
- **Backend API**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin

**Default Login Credentials:**
- Username: `admin` | Password: `admin123`
- Username: `test` | Password: `test123`
- Username: `demo` | Password: `demo123`

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

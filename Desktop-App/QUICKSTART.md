# Quick Start Guide - Desktop Application

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies

Open a terminal in the `Desktop-App` folder and run:

```bash
# Windows (using setup script)
setup.bat

# OR manually
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Start Backend Server

**IMPORTANT:** The backend must be running first!

Open a **separate terminal** in the backend folder:

```bash
# Navigate to backend
cd ..\backend

# Activate backend virtual environment
..\venv\Scripts\activate

# Run Django server
python manage.py runserver
```

The backend should start at: `http://localhost:8000`

### Step 3: Launch Desktop App

Return to the Desktop-App folder and run:

```bash
# Windows (using start script)
start_app.bat

# OR manually
venv\Scripts\activate
python main.py
```

## 🎯 First Time Usage

### 1. Login or Register
- **New User**: Click "Sign Up" and create an account
- **Existing User**: Enter credentials and click "Sign In"

### 2. Upload Data
- Click "📤 Upload CSV" button in top navbar
- Drag & drop your CSV file or click browse
- Wait for processing (you'll see a progress bar)
- File is automatically analyzed and charts are generated

### 3. Explore Dashboard
- **📊 Dashboard Tab**: View beautiful charts and statistics
- **📋 Data View Tab**: Browse your data in a table
- **📜 History Tab**: Manage all your uploaded files

### 4. Generate Reports
- Click "📄 Generate Report" button
- Choose report options
- Select save location
- Get a professional PDF with charts and analysis

## 📊 Features Overview

### Dashboard Tab
- **4 Interactive Charts:**
  - Bar Chart: Average values comparison
  - Box Plot: Data distribution analysis
  - Line Chart: Trend visualization
  - Pie Chart: Value distribution breakdown

- **Statistics Cards:**
  - Total Records count
  - Average Flowrate
  - Average Pressure
  - Average Temperature

### Data View Tab
- Full dataset table view
- Sortable columns
- Export to CSV functionality
- Real-time data display

### History Tab
- List of all uploaded datasets
- View any previous dataset
- Delete old datasets
- Track upload dates and sizes

## 🎨 UI Features

### Dark Theme (Default)
- Professional dark interface
- Reduced eye strain
- Modern color scheme
- High contrast for clarity

### Large Text & Elements
- 11-13pt font sizes throughout
- Enlarged buttons (45-50px height)
- Generous padding (12-16px)
- Spacious input fields

### Seamless Navigation
- Tab-based interface for easy switching
- Quick access buttons in top navbar
- Responsive design
- Smooth interactions

## 🔧 Configuration

### Change Backend URL
If your backend runs on a different address, edit `utils/config.py`:

```python
API_BASE_URL = "http://your-server:port"
```

### Customize Theme Colors
Modify colors in `utils/config.py`:

```python
PRIMARY_COLOR = "#6366f1"  # Change to your preferred color
```

### Adjust Window Size
Update in `utils/config.py`:

```python
WINDOW_MIN_WIDTH = 1400
WINDOW_MIN_HEIGHT = 900
```

## ❓ Common Issues

### "Cannot connect to backend"
**Solution:** Ensure backend server is running
```bash
cd backend
python manage.py runserver
```

### "Module not found" error
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Charts not displaying
**Solution:** Reinstall matplotlib
```bash
pip install --upgrade matplotlib
```

### Upload fails
**Check:**
- File is CSV format
- File size < 50 MB
- File has proper headers
- Backend is reachable

## 💡 Tips & Tricks

### Multiple Datasets
- Upload multiple CSV files
- Switch between them using the dropdown in navbar
- Each dataset maintains its own statistics

### Keyboard Shortcuts
- Enter key: Submit forms (login/register)
- Tab: Navigate between fields
- Esc: Close dialogs

### Data Export
- Export current dataset from Data View tab
- Choose location and filename
- Opens in Excel or any CSV viewer

### Report Customization
- Select what to include in reports
- Charts, statistics, and raw data
- Saved as professional PDF

## 🔐 Security Notes

- Credentials are securely transmitted using Basic Auth
- Passwords stored securely in backend
- No local storage of sensitive data
- HTTPS recommended for production

## 📚 Data Format

### CSV Requirements
- Must have header row
- Expected columns: flowrate, pressure, temperature
- Numeric values for analysis
- UTF-8 encoding recommended

### Sample CSV:
```csv
equipment_id,flowrate,pressure,temperature,timestamp
EQ001,45.2,120.5,78.3,2024-01-01 10:00
EQ002,48.1,118.2,79.1,2024-01-01 10:05
```

## 🛠️ Advanced Usage

### Custom API Endpoints
Modify `utils/api_client.py` to add new endpoints:

```python
def custom_endpoint(self):
    url = f"{self.base_url}/api/custom/"
    return self._handle_response(requests.get(url))
```

### Add New Charts
Edit `ui/chart_widgets.py` to add visualization:

```python
def plot_custom_chart(self, ax, statistics):
    # Your matplotlib code here
    ax.plot(data)
```

### Extend Main Window
Add new tabs or features in `ui/main_window.py`

## 📞 Support

For issues:
1. Check this guide first
2. Verify backend is running
3. Check console for errors
4. Review API documentation

## 🎓 Learning Resources

- **PyQt5:** https://www.riverbankcomputing.com/software/pyqt/
- **Matplotlib:** https://matplotlib.org/
- **Django REST:** https://www.django-rest-framework.org/

---

**Happy Analyzing! 🎉**

Enjoy the professional desktop experience for your equipment analytics!

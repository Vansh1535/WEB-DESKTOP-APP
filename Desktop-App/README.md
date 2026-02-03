# Equipment Analytics Desktop Application

A professional desktop application built with PyQt5 and Matplotlib, providing a complete analytics platform for equipment data management and visualization.

## Features

✨ **Complete Feature Parity with Web Frontend**
- 🔐 User Authentication (Login/Register)
- 📤 CSV Upload with Drag & Drop
- 📊 Interactive Dashboard with Real-time Charts
- 📈 Statistical Analysis & Visualization
- 📋 Data Table View with Export
- 📄 PDF Report Generation
- 📜 Upload History Management
- 🎨 Professional Dark Theme (Default)
- 💾 Dataset Management

## Technologies

- **PyQt5** - Modern GUI framework
- **Matplotlib** - Professional data visualization
- **NumPy & Pandas** - Data processing
- **Requests** - API communication
- **ReportLab** - PDF generation

## Installation

### Prerequisites
- Python 3.8 or higher
- Backend server running on `http://localhost:8000`

### Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Backend URL** (if different)
   Edit `utils/config.py` and update `API_BASE_URL`

3. **Run the Application**
   ```bash
   python main.py
   ```

## Usage

### First Time Setup

1. **Launch the Application**
   ```bash
   python main.py
   ```

2. **Create an Account or Login**
   - New users: Click "Sign Up" to create an account
   - Existing users: Enter credentials and click "Sign In"

3. **Upload Your Data**
   - Click "Upload CSV" button
   - Drag & drop or browse for your CSV file
   - Wait for processing to complete

4. **Explore Your Data**
   - **Dashboard Tab**: View interactive charts and statistics
   - **Data View Tab**: Browse raw data in table format
   - **History Tab**: Manage all uploaded datasets

5. **Generate Reports**
   - Click "Generate Report" button
   - Select report options
   - Download professional PDF report

## Features in Detail

### Dashboard
- **Statistics Cards**: Total records, average values
- **4 Chart Types**:
  - Bar Chart: Value comparisons
  - Box Plot: Data distribution
  - Line Chart: Trend analysis
  - Pie Chart: Value distribution

### Data Management
- Upload multiple CSV files
- Switch between datasets
- View detailed statistics
- Export data to CSV
- Delete old datasets

### Report Generation
- Comprehensive PDF reports
- Include charts and graphs
- Statistical summaries
- Raw data tables
- Professional formatting

## UI Features

### Dark Theme
- Modern, professional dark theme by default
- Reduced eye strain for extended use
- High contrast for better readability
- Consistent color scheme throughout

### Large Text & UI Elements
- Increased font sizes (11-13pt)
- Larger buttons and input fields
- Enhanced padding and spacing
- Better accessibility

### Seamless Navigation
- Intuitive tab-based interface
- Quick action buttons in navbar
- Responsive layout
- Smooth transitions

## Configuration

Edit `utils/config.py` to customize:

```python
# API Settings
API_BASE_URL = "http://localhost:8000"

# Window Settings
WINDOW_MIN_WIDTH = 1400
WINDOW_MIN_HEIGHT = 900

# File Settings
MAX_FILE_SIZE_MB = 50

# Theme Colors (customize as needed)
```

## Architecture

```
Desktop-App/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── utils/
│   ├── config.py          # Configuration settings
│   └── api_client.py      # Backend API communication
└── ui/
    ├── login_window.py    # Authentication interface
    ├── main_window.py     # Main dashboard window
    ├── chart_widgets.py   # Matplotlib chart components
    ├── upload_dialog.py   # CSV upload interface
    └── report_dialog.py   # Report generation interface
```

## API Integration

The application communicates with the Django backend using:
- **Basic Authentication** for secure access
- **RESTful API endpoints** for all operations
- **File upload** with multipart/form-data
- **JSON responses** for data exchange

### Key Endpoints Used
- `/api/v1/auth/login/` - User authentication
- `/api/v1/auth/register/` - User registration
- `/api/v1/analytics/csv/upload/` - CSV upload
- `/api/v1/analytics/datasets/` - Dataset management
- `/api/v1/analytics/datasets/{id}/` - Dataset details
- `/api/v1/analytics/datasets/{id}/pdf-report/` - PDF generation

## Troubleshooting

### Cannot Connect to Backend
- Ensure backend server is running
- Check `API_BASE_URL` in `utils/config.py`
- Verify firewall settings

### Charts Not Displaying
- Ensure matplotlib is properly installed
- Check data format in statistics

### Upload Fails
- Verify CSV file format
- Check file size (max 50 MB)
- Ensure proper permissions

## Development

### Adding New Features
1. Create new UI component in `ui/` directory
2. Add API methods to `utils/api_client.py`
3. Update main window to integrate new feature
4. Follow existing code style and patterns

### Customizing Theme
- Modify stylesheet in `main.py` `setup_dark_theme()`
- Update colors in `utils/config.py`
- Adjust widget styles in individual components

## License

This project is part of the FOSSEE initiative.

## Support

For issues and questions:
- Check backend API documentation
- Review configuration settings
- Ensure all dependencies are installed

## Credits

**Developed with:**
- PyQt5 - GUI Framework
- Matplotlib - Data Visualization
- Django REST Framework - Backend API
- FOSSEE Project

---

**Enjoy analyzing your equipment data with a professional desktop experience!** 🚀

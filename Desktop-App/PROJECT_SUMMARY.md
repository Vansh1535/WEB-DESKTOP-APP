# Equipment Analytics Desktop Application
## Complete Project Documentation

### 📋 Project Overview

A professional desktop application built with PyQt5 and Matplotlib that provides complete feature parity with the web frontend. The application offers equipment data management, visualization, and analytics with a modern dark theme interface.

---

## 🎯 Core Features

### 1. **Authentication System**
- User registration with validation
- Secure login with Basic Authentication
- Remember me functionality
- Automatic session management
- Profile management

### 2. **Data Management**
- CSV file upload with drag & drop
- Multiple dataset support
- Dataset switching via dropdown
- Delete datasets
- Export data to CSV
- Upload history tracking

### 3. **Visualization Dashboard**
- **4 Professional Charts:**
  - Bar Chart: Average values comparison
  - Box Plot: Statistical distribution
  - Line Chart: Trend analysis with noise
  - Pie Chart: Value distribution
  
- **Statistics Cards:**
  - Total records count with color coding
  - Average flowrate (Indigo)
  - Average pressure (Purple)
  - Average temperature (Green)

### 4. **Data View**
- Full dataset table display
- Alternating row colors
- Sortable columns
- Column resizing
- Row selection
- Export functionality
- Record count display

### 5. **Report Generation**
- PDF report creation
- Customizable options:
  - Include/exclude charts
  - Include/exclude statistics
  - Include/exclude raw data
- Professional formatting
- Automatic opening of generated PDF
- Progress tracking

### 6. **User Interface**
- **Dark Theme (Default):**
  - Background: #121214
  - Cards: #18181b
  - Accents: #6366f1 (Indigo)
  - Text: #f0f0f5
  
- **Large Text & Elements:**
  - Base font: 11pt
  - Headings: 16-24pt
  - Buttons: 45-50px height
  - Input padding: 12-16px
  
- **Seamless Navigation:**
  - Tab-based interface
  - Navbar with quick actions
  - Modal dialogs
  - Progress indicators
  - Status bar updates

---

## 🏗️ Architecture

### Directory Structure
```
Desktop-App/
├── main.py                    # Application entry point, dark theme setup
├── requirements.txt           # Python dependencies
├── README.md                  # Main documentation
├── QUICKSTART.md             # Quick start guide
├── setup.bat                 # Windows setup script
├── start_app.bat             # Windows launcher
│
├── utils/
│   ├── __init__.py
│   ├── config.py             # Configuration constants
│   └── api_client.py         # Backend API communication
│
└── ui/
    ├── __init__.py
    ├── login_window.py       # Authentication interface
    ├── main_window.py        # Main dashboard window
    ├── chart_widgets.py      # Matplotlib chart components
    ├── upload_dialog.py      # CSV upload interface
    └── report_dialog.py      # Report generation interface
```

### Component Breakdown

#### **main.py** (350+ lines)
- Application initialization
- Dark theme setup
- Global stylesheet application
- Font configuration
- Entry point

#### **utils/config.py** (80+ lines)
- API settings (URL, timeout)
- Window dimensions
- Color scheme constants
- File upload limits
- Chart colors array

#### **utils/api_client.py** (300+ lines)
- APIClient class
- Authentication methods
- Dataset CRUD operations
- File upload handling
- PDF download
- Error handling
- Response parsing

#### **ui/login_window.py** (450+ lines)
- LoginWindow class
- Login form
- Registration form
- Form validation
- Stacked widget switching
- Success/error handling
- Transition to main window

#### **ui/main_window.py** (700+ lines)
- MainWindow class
- Top navigation bar
- Dataset selector dropdown
- Tab widget (3 tabs)
- Statistics cards (4 cards)
- Dashboard creation
- Data table management
- History table
- Action buttons
- Data loading/refresh
- Export functionality
- Delete confirmation

#### **ui/chart_widgets.py** (250+ lines)
- ChartWidget base class
- MultiChartWidget class
- 4 chart plotting methods:
  - Bar chart with value labels
  - Box plot with styling
  - Line chart with legend
  - Pie chart with percentages
- Dark theme matplotlib config
- Figure and canvas management

#### **ui/upload_dialog.py** (250+ lines)
- UploadDialog class
- UploadWorker thread
- Drag & drop support
- File browser
- File validation
- Size checking
- Progress tracking
- Success/error messages

#### **ui/report_dialog.py** (280+ lines)
- ReportDialog class
- ReportWorker thread
- Report options checkboxes
- File save dialog
- Progress tracking
- PDF generation
- Automatic opening
- Success confirmation

---

## 🎨 Design System

### Color Palette
```python
PRIMARY:      #6366f1  # Indigo - Main actions
SECONDARY:    #8b5cf6  # Purple - Secondary actions
ACCENT:       #ec4899  # Pink - Accents
SUCCESS:      #10b981  # Green - Success states
WARNING:      #f59e0b  # Amber - Warnings
DANGER:       #ef4444  # Red - Dangerous actions

BG_PRIMARY:   #121214  # Main background
BG_SECONDARY: #18181b  # Card background
BG_TERTIARY:  #27272a  # Elevated elements

TEXT_PRIMARY:   #f0f0f5  # Main text
TEXT_SECONDARY: #a1a1aa  # Secondary text
TEXT_MUTED:     #71717a  # Muted text

BORDER:       #3f3f46  # Default borders
BORDER_FOCUS: #6366f1  # Focused elements
```

### Typography
```
Base Font:     Segoe UI, 11pt
Headings:      Segoe UI, 16-24pt, Bold
Buttons:       Segoe UI, 11-13pt, Bold
Labels:        Segoe UI, 11-12pt, Bold
Input:         Segoe UI, 12pt
```

### Spacing
```
Card Padding:     20-50px
Button Padding:   14px vertical, 24px horizontal
Input Padding:    12px vertical, 16px horizontal
Section Spacing:  20-30px
Element Spacing:  10-15px
```

### Component Sizes
```
Buttons:        45-50px height
Input Fields:   40-50px height
Cards:          120px minimum height
Windows:        1400x900 minimum
Navbar:         80px height
```

---

## 🔌 API Integration

### Endpoints Used

#### Authentication
- `POST /api/v1/auth/login/`
  - Body: {username, password}
  - Returns: user object with token
  
- `POST /api/v1/auth/register/`
  - Body: {username, email, password, first_name, last_name}
  - Returns: user object

- `GET /api/v1/auth/profile/`
  - Headers: Basic Auth
  - Returns: user profile with preferences

#### Dataset Management
- `POST /api/v1/analytics/csv/upload/`
  - Content-Type: multipart/form-data
  - Body: {file}
  - Returns: {dataset_id, statistics}

- `GET /api/v1/analytics/datasets/`
  - Headers: Basic Auth
  - Returns: {count, datasets[]}

- `GET /api/v1/analytics/datasets/{id}/`
  - Headers: Basic Auth
  - Returns: dataset details with statistics

- `GET /api/v1/analytics/datasets/{id}/data/`
  - Headers: Basic Auth
  - Returns: {data: [...]}

- `GET /api/v1/analytics/datasets/{id}/statistics/`
  - Headers: Basic Auth
  - Returns: statistics object

- `DELETE /api/v1/analytics/datasets/{id}/`
  - Headers: Basic Auth
  - Returns: 204 No Content

- `GET /api/v1/analytics/datasets/{id}/pdf-report/`
  - Headers: Basic Auth
  - Returns: PDF file (binary)

- `GET /api/v1/analytics/csv/statistics/`
  - Headers: Basic Auth
  - Returns: latest statistics

### Authentication Flow
1. User enters credentials
2. Client encodes credentials to Base64
3. Sends POST to /login/
4. Stores encoded credentials
5. Adds "Authorization: Basic {encoded}" header to all requests

---

## 📊 Data Flow

### Upload Flow
```
1. User selects CSV file
   ↓
2. File validation (size, format)
   ↓
3. UploadWorker thread starts
   ↓
4. File sent to backend via multipart/form-data
   ↓
5. Backend processes CSV
   ↓
6. Statistics calculated
   ↓
7. Response with dataset_id and stats
   ↓
8. UI refreshes with new data
   ↓
9. Charts updated automatically
```

### Dataset Loading Flow
```
1. User selects dataset from dropdown
   ↓
2. API call to get dataset details
   ↓
3. Statistics loaded and displayed in cards
   ↓
4. API call to get raw data
   ↓
5. Table populated with data
   ↓
6. Charts updated with new statistics
   ↓
7. Status bar updated
```

### Report Generation Flow
```
1. User clicks Generate Report
   ↓
2. Report options dialog shown
   ↓
3. User selects options and save location
   ↓
4. ReportWorker thread starts
   ↓
5. API call to download PDF
   ↓
6. File saved to disk
   ↓
7. Confirmation dialog shown
   ↓
8. Optional: Open PDF automatically
```

---

## 🛠️ Technical Details

### Threading
- **UploadWorker**: Handles CSV upload without blocking UI
- **ReportWorker**: Handles PDF generation without blocking UI
- Both emit signals for progress and completion

### Error Handling
- Network errors caught and displayed
- File validation before upload
- API error messages shown to user
- Graceful fallbacks for missing data

### Data Validation
- CSV format checking
- File size limits (50 MB default)
- Required fields validation
- Password strength requirements
- Email format validation

### State Management
- Current dataset ID tracked
- User data stored in memory
- API credentials managed centrally
- UI state updates on data changes

---

## 🚀 Performance Optimizations

- Threaded file operations
- Lazy loading of data
- Efficient chart rendering
- Minimal API calls
- Caching of current dataset
- Progress indicators for long operations

---

## 🔒 Security Features

- Basic Authentication over HTTPS (recommended)
- No local credential storage
- Secure password transmission
- Session management
- Input validation
- File type restrictions

---

## 📦 Dependencies

```
PyQt5>=5.15.9           # GUI framework
matplotlib>=3.7.1       # Charting library
numpy>=1.24.3          # Numerical operations
pandas>=2.0.2          # Data manipulation
requests>=2.31.0       # HTTP requests
reportlab>=4.0.4       # PDF generation
Pillow>=10.0.0         # Image processing
```

---

## 🎓 Development Guidelines

### Code Style
- PEP 8 compliance
- Descriptive variable names
- Comprehensive docstrings
- Type hints where applicable
- Comments for complex logic

### UI Principles
- Consistent spacing
- Clear visual hierarchy
- Immediate feedback
- Error prevention
- Helpful error messages

### Best Practices
- Separation of concerns
- Reusable components
- Centralized configuration
- Comprehensive error handling
- User-friendly messages

---

## 🔄 Future Enhancements

### Potential Features
- [ ] Real-time data updates
- [ ] Multiple chart types
- [ ] Custom color themes
- [ ] Data filtering
- [ ] Advanced analytics
- [ ] Export to multiple formats
- [ ] Batch operations
- [ ] User preferences
- [ ] Offline mode
- [ ] Auto-update checking

---

## 📝 Version History

### Version 1.0.0 (Current)
- ✅ Complete feature parity with web frontend
- ✅ Dark theme implementation
- ✅ All CRUD operations
- ✅ Professional charts
- ✅ PDF report generation
- ✅ Upload history
- ✅ Data export
- ✅ Comprehensive documentation

---

## 🎉 Summary

This desktop application provides a complete, professional alternative to the web frontend with:
- **Exact feature parity**
- **Enhanced dark theme**
- **Larger, more readable UI**
- **Seamless navigation**
- **Professional visualizations**
- **Comprehensive documentation**

Built with modern technologies and best practices, it offers a superior desktop experience for equipment analytics.

---

**Project Status:** ✅ Complete and Ready for Use

**Total Lines of Code:** ~2,800+

**Components:** 8 main files + configuration

**Features Implemented:** 15+

**UI Screens:** 5 (Login, Dashboard, Data View, History, Upload, Report)

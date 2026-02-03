"""
Configuration settings for the desktop application
"""

class Config:
    """Application configuration matching web frontend theme"""
    
    # API Settings
    API_BASE_URL = "http://localhost:8000"
    API_TIMEOUT = 30
    
    # UI Settings
    WINDOW_TITLE = "Equipment Analytics Desktop"
    WINDOW_MIN_WIDTH = 1400
    WINDOW_MIN_HEIGHT = 900
    
    # Theme Colors (matching web frontend vibrant orange/coral gradient)
    PRIMARY_COLOR = "#eb915f"  # Vibrant orange
    SECONDARY_COLOR = "#a966d9"  # Light purple
    ACCENT_COLOR = "#f97c66"  # Coral/pink
    SUCCESS_COLOR = "#10b981"  # Green
    WARNING_COLOR = "#f59e0b"  # Amber
    DANGER_COLOR = "#ef4444"  # Red
    
    # Background Colors (matching web dark theme)
    BG_PRIMARY = "#1e1e22"  # oklch(0.12 0.02 270)
    BG_SECONDARY = "#28282e"  # oklch(0.16 0.02 270)
    BG_TERTIARY = "#38383e"  # oklch(0.22 0.02 270)
    
    # Text Colors
    TEXT_PRIMARY = "#fafafa"  # oklch(0.98 0.005 0)
    TEXT_SECONDARY = "#b3b3bb"  # oklch(0.70 0.02 265)
    TEXT_MUTED = "#8a8a92"  # oklch(0.55 0.02 265)
    
    # Border Colors
    BORDER_COLOR = "#3a3a44"  # oklch(0.24 0.02 270)
    BORDER_FOCUS = "#eb915f"  # Primary orange
    
    # Chart Colors (vibrant matching web frontend)
    CHART_COLORS = [
        '#eb915f',  # Vibrant orange (primary)
        '#f97c66',  # Coral (accent)
        '#a966d9',  # Light purple (secondary)
        '#e5a24c',  # Golden yellow
        '#d67f9b',  # Rose pink
        '#10b981',  # Green
        '#06b6d4',  # Cyan
        '#f59e0b',  # Amber
    ]
    
    # File Settings
    MAX_FILE_SIZE_MB = 50
    ALLOWED_EXTENSIONS = ['.csv']
    
    # Table Settings
    DEFAULT_ROWS_PER_PAGE = 50
    
    # Authentication
    AUTH_TOKEN_KEY = "auth_token"
    USERNAME_KEY = "username"

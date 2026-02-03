#!/usr/bin/env python
"""
Desktop Application Test Script
Validates that all components are working correctly
"""

import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    errors = []
    
    try:
        from PyQt5.QtWidgets import QApplication
        print("✓ PyQt5 installed")
    except ImportError as e:
        errors.append(f"✗ PyQt5 not installed: {e}")
    
    try:
        import matplotlib
        print("✓ Matplotlib installed")
    except ImportError as e:
        errors.append(f"✗ Matplotlib not installed: {e}")
    
    try:
        import numpy
        print("✓ NumPy installed")
    except ImportError as e:
        errors.append(f"✗ NumPy not installed: {e}")
    
    try:
        import pandas
        print("✓ Pandas installed")
    except ImportError as e:
        errors.append(f"✗ Pandas not installed: {e}")
    
    try:
        import requests
        print("✓ Requests installed")
    except ImportError as e:
        errors.append(f"✗ Requests not installed: {e}")
    
    try:
        import reportlab
        print("✓ ReportLab installed")
    except ImportError as e:
        errors.append(f"✗ ReportLab not installed: {e}")
    
    try:
        from PIL import Image
        print("✓ Pillow installed")
    except ImportError as e:
        errors.append(f"✗ Pillow not installed: {e}")
    
    return errors

def test_modules():
    """Test if custom modules can be imported"""
    print("\nTesting custom modules...")
    errors = []
    
    try:
        from utils.config import Config
        print("✓ utils.config imported")
    except ImportError as e:
        errors.append(f"✗ utils.config import failed: {e}")
    
    try:
        from utils.api_client import api_client
        print("✓ utils.api_client imported")
    except ImportError as e:
        errors.append(f"✗ utils.api_client import failed: {e}")
    
    try:
        from ui.login_window import LoginWindow
        print("✓ ui.login_window imported")
    except ImportError as e:
        errors.append(f"✗ ui.login_window import failed: {e}")
    
    try:
        from ui.main_window import MainWindow
        print("✓ ui.main_window imported")
    except ImportError as e:
        errors.append(f"✗ ui.main_window import failed: {e}")
    
    try:
        from ui.chart_widgets import ChartWidget, MultiChartWidget
        print("✓ ui.chart_widgets imported")
    except ImportError as e:
        errors.append(f"✗ ui.chart_widgets import failed: {e}")
    
    try:
        from ui.upload_dialog import UploadDialog
        print("✓ ui.upload_dialog imported")
    except ImportError as e:
        errors.append(f"✗ ui.upload_dialog import failed: {e}")
    
    try:
        from ui.report_dialog import ReportDialog
        print("✓ ui.report_dialog imported")
    except ImportError as e:
        errors.append(f"✗ ui.report_dialog import failed: {e}")
    
    return errors

def test_backend():
    """Test backend connection"""
    print("\nTesting backend connection...")
    errors = []
    
    try:
        import requests
        response = requests.get('http://localhost:8000', timeout=3)
        if response.status_code == 200:
            print(f"✓ Backend is running (Status: {response.status_code})")
        else:
            print(f"⚠ Backend responded with status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        errors.append("✗ Cannot connect to backend at http://localhost:8000")
        print("✗ Backend is NOT running!")
    except Exception as e:
        errors.append(f"✗ Backend test failed: {e}")
    
    return errors

def test_config():
    """Test configuration"""
    print("\nTesting configuration...")
    errors = []
    
    try:
        from utils.config import Config
        
        # Check required attributes
        required_attrs = [
            'API_BASE_URL', 'WINDOW_TITLE', 'WINDOW_MIN_WIDTH', 
            'WINDOW_MIN_HEIGHT', 'PRIMARY_COLOR', 'CHART_COLORS'
        ]
        
        for attr in required_attrs:
            if hasattr(Config, attr):
                print(f"✓ Config.{attr} exists")
            else:
                errors.append(f"✗ Config.{attr} missing")
        
        # Display some config values
        print(f"  - API URL: {Config.API_BASE_URL}")
        print(f"  - Window Size: {Config.WINDOW_MIN_WIDTH}x{Config.WINDOW_MIN_HEIGHT}")
        print(f"  - Primary Color: {Config.PRIMARY_COLOR}")
        
    except Exception as e:
        errors.append(f"✗ Config test failed: {e}")
    
    return errors

def main():
    """Run all tests"""
    print("=" * 60)
    print("Equipment Analytics Desktop - System Test")
    print("=" * 60)
    print()
    
    all_errors = []
    
    # Run tests
    all_errors.extend(test_imports())
    all_errors.extend(test_modules())
    all_errors.extend(test_config())
    all_errors.extend(test_backend())
    
    # Summary
    print("\n" + "=" * 60)
    if not all_errors:
        print("✓ ALL TESTS PASSED!")
        print("\nYour desktop application is ready to run!")
        print("\nTo start the application, run:")
        print("  python main.py")
        print("\nOr use the start script:")
        print("  start_app.bat")
    else:
        print("✗ TESTS FAILED!")
        print(f"\nFound {len(all_errors)} error(s):")
        for error in all_errors:
            print(f"  {error}")
        print("\nPlease fix the errors above before running the application.")
    print("=" * 60)
    
    return 0 if not all_errors else 1

if __name__ == '__main__':
    sys.exit(main())

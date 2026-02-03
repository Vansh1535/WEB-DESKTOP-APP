"""
Desktop Analytics Application - Main Entry Point
A professional PyQt5 desktop application with dark theme
Replicates all functionality from the web frontend
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QColor
from ui.login_window import LoginWindow
from utils.config import Config

def setup_dark_theme(app):
    """Apply dark theme matching web frontend - vibrant orange/coral gradient"""
    app.setStyle("Fusion")
    
    # Dark palette matching web frontend
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(30, 30, 34))  # oklch(0.12 0.02 270)
    dark_palette.setColor(QPalette.WindowText, QColor(250, 250, 250))
    dark_palette.setColor(QPalette.Base, QColor(40, 40, 46))  # oklch(0.16 0.02 270)
    dark_palette.setColor(QPalette.AlternateBase, QColor(35, 35, 40))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(250, 250, 250))
    dark_palette.setColor(QPalette.ToolTipText, QColor(250, 250, 250))
    dark_palette.setColor(QPalette.Text, QColor(250, 250, 250))
    dark_palette.setColor(QPalette.Button, QColor(56, 56, 64))
    dark_palette.setColor(QPalette.ButtonText, QColor(250, 250, 250))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 120, 100))
    dark_palette.setColor(QPalette.Link, QColor(235, 145, 95))  # Vibrant orange
    dark_palette.setColor(QPalette.Highlight, QColor(235, 145, 95))
    dark_palette.setColor(QPalette.HighlightedText, QColor(30, 30, 34))
    
    app.setPalette(dark_palette)
    
    # Set default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Apply comprehensive stylesheet matching web frontend
    app.setStyleSheet("""
        QMainWindow {
            background-color: #1e1e22;
        }
        
        QWidget {
            background-color: #1e1e22;
            color: #fafafa;
            font-size: 10pt;
        }
        
        QLabel {
            color: #fafafa;
            font-size: 10pt;
        }
        
        QLineEdit {
            background-color: #28282e;
            border: 2px solid #3a3a44;
            border-radius: 6px;
            padding: 10px 14px;
            color: #fafafa;
            font-size: 10pt;
            min-height: 18px;
        }
        
        QLineEdit:focus {
            border: 2px solid #eb915f;
            background-color: #2e2e36;
        }
        
        QLineEdit:disabled {
            background-color: #38383e;
            color: #a0a0a8;
        }
        
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #eb915f, stop:1 #f97c66);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 20px;
            font-size: 10pt;
            font-weight: bold;
            min-height: 18px;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #f59e6d, stop:1 #fa8a74);
        }
        
        QPushButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #d97f4f, stop:1 #e76d58);
        }
        
        QPushButton:disabled {
            background-color: #3a3a44;
            color: #6a6a72;
        }
        
        QPushButton#secondary {
            background-color: #38383e;
            color: #fafafa;
            border: 2px solid #3a3a44;
        }
        
        QPushButton#secondary:hover {
            background-color: #48484e;
            border-color: #eb915f;
        }
        
        QPushButton#danger {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #dc2626, stop:1 #b91c1c);
        }
        
        QPushButton#danger:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #ef4444, stop:1 #dc2626);
        }
        
        QTableWidget {
            background-color: #28282e;
            alternate-background-color: #2e2e36;
            gridline-color: #3a3a44;
            border: 2px solid #3a3a44;
            border-radius: 8px;
            color: #fafafa;
            font-size: 10pt;
        }
        
        QTableWidget::item {
            padding: 8px;
        }
        
        QTableWidget::item:selected {
            background-color: #eb915f;
            color: white;
        }
        
        QHeaderView::section {
            background-color: #38383e;
            color: #fafafa;
            padding: 10px;
            border: none;
            border-bottom: 3px solid #eb915f;
            font-weight: bold;
            font-size: 10pt;
        }
        
        QTabWidget::pane {
            border: 2px solid #3a3a44;
            border-radius: 8px;
            background-color: #28282e;
        }
        
        QTabBar::tab {
            background-color: #38383e;
            color: #b3b3bb;
            border: none;
            padding: 12px 24px;
            margin-right: 4px;
            font-size: 10pt;
            font-weight: bold;
            border-radius: 6px;
        }
        
        QTabBar::tab:selected {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #eb915f, stop:1 #f97c66);
            color: white;
        }
        
        QTabBar::tab:hover:!selected {
            background-color: #48484e;
            color: #fafafa;
        }
        
        QComboBox {
            background-color: #28282e;
            border: 2px solid #3a3a44;
            border-radius: 6px;
            padding: 8px 14px;
            color: #fafafa;
            font-size: 10pt;
            min-height: 18px;
        }
        
        QComboBox:hover {
            border-color: #eb915f;
        }
        
        QComboBox::drop-down {
            border: none;
            width: 30px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #f0f0f5;
            margin-right: 10px;
        }
        
        QComboBox QAbstractItemView {
            background-color: #18181b;
            border: 2px solid #6366f1;
            selection-background-color: #6366f1;
            selection-color: white;
            color: #f0f0f5;
            font-size: 11pt;
        }
        
        QScrollBar:vertical {
            background-color: #18181b;
            width: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #3f3f46;
            border-radius: 6px;
            min-height: 30px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #52525b;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        QScrollBar:horizontal {
            background-color: #18181b;
            height: 12px;
            border-radius: 6px;
        }
        
        QScrollBar::handle:horizontal {
            background-color: #3f3f46;
            border-radius: 6px;
            min-width: 30px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background-color: #52525b;
        }
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
        }
        
        QTextEdit, QPlainTextEdit {
            background-color: #18181b;
            border: 2px solid #3f3f46;
            border-radius: 8px;
            padding: 12px;
            color: #f0f0f5;
            font-size: 11pt;
        }
        
        QProgressBar {
            border: 2px solid #3f3f46;
            border-radius: 8px;
            text-align: center;
            background-color: #18181b;
            color: #f0f0f5;
            font-size: 11pt;
            font-weight: bold;
        }
        
        QProgressBar::chunk {
            background-color: #6366f1;
            border-radius: 6px;
        }
        
        QMessageBox {
            background-color: #18181b;
            color: #f0f0f5;
        }
        
        QMessageBox QLabel {
            color: #f0f0f5;
            font-size: 12pt;
        }
        
        QMenu {
            background-color: #18181b;
            border: 2px solid #3f3f46;
            color: #f0f0f5;
            font-size: 11pt;
        }
        
        QMenu::item:selected {
            background-color: #6366f1;
            color: white;
        }
        
        QToolTip {
            background-color: #27272a;
            color: #f0f0f5;
            border: 2px solid #3f3f46;
            padding: 8px;
            font-size: 11pt;
        }
    """)

def main():
    """Main application entry point"""
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("Equipment Analytics Desktop")
    app.setOrganizationName("FOSSEE")
    
    # Apply dark theme
    setup_dark_theme(app)
    
    # Show login window
    login_window = LoginWindow()
    login_window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

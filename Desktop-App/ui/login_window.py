"""
Login Window - Authentication UI
Professional login/register interface with dark theme
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame,
                             QStackedWidget, QCheckBox, QProgressDialog)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor
from utils.api_client import api_client
from utils.config import Config

class LoginWindow(QWidget):
    """Login window with login and registration forms"""
    
    login_successful = pyqtSignal(dict)  # Emits user data on successful login
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(Config.WINDOW_TITLE)
        self.setFixedSize(1000, 850)
        self.setStyleSheet("background-color: #121214;")
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Content container
        content = QWidget()
        content.setStyleSheet("""
            background-color: #121214;
        """)
        content_layout = QVBoxLayout(content)
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setSpacing(30)
        content_layout.setContentsMargins(80, 50, 80, 50)
        
        # Header section
        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        header_layout.setSpacing(15)
        
        # App title
        title_label = QLabel("⚗️ Equipment Analytics")
        title_label.setFont(QFont("Segoe UI", 32, QFont.Bold))
        title_label.setStyleSheet("""
            color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #eb915f, stop:1 #f97c66);
            background: transparent;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Professional Desktop Application")
        subtitle_label.setFont(QFont("Segoe UI", 14))
        subtitle_label.setStyleSheet("""
            color: #a1a1aa;
            background: transparent;
        """)
        subtitle_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle_label)
        
        content_layout.addLayout(header_layout)
        content_layout.addSpacing(20)
        
        # Card container for forms
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #28282e;
                border: 3px solid #eb915f;
                border-radius: 16px;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(50, 40, 50, 40)
        card_layout.setSpacing(25)
        
        # Stacked widget for login/register forms
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background: transparent; border: none;")
        
        # Create login and register forms
        self.login_form = self.create_login_form()
        self.register_form = self.create_register_form()
        
        self.stacked_widget.addWidget(self.login_form)
        self.stacked_widget.addWidget(self.register_form)
        
        card_layout.addWidget(self.stacked_widget)
        
        content_layout.addWidget(card)
        content_layout.addStretch()
        
        # Footer
        footer_label = QLabel("Powered by FOSSEE • PyQt5 & Matplotlib")
        footer_label.setFont(QFont("Segoe UI", 10))
        footer_label.setStyleSheet("""
            color: #71717a;
            background: transparent;
        """)
        footer_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(footer_label)
        
        main_layout.addWidget(content)
        self.setLayout(main_layout)
    
    def create_login_form(self):
        """Create login form widget"""
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        
        # Username field
        username_label = QLabel("Username")
        username_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        username_label.setStyleSheet("color: #fafafa; background: transparent;")
        layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setFont(QFont("Segoe UI", 12))
        layout.addWidget(self.username_input)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        password_label.setStyleSheet("color: #fafafa; background: transparent;")
        layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Segoe UI", 12))
        self.password_input.returnPressed.connect(self.handle_login)
        layout.addWidget(self.password_input)
        
        # Remember me checkbox
        self.remember_checkbox = QCheckBox("Remember me")
        self.remember_checkbox.setStyleSheet("""
            QCheckBox {
                color: #b3b3bb;
                background: transparent;
                font-size: 11pt;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #3a3a44;
                border-radius: 4px;
                background-color: #28282e;
            }
            QCheckBox::indicator:checked {
                background-color: #eb915f;
                border-color: #eb915f;
            }
        """)
        layout.addWidget(self.remember_checkbox)
        
        layout.addSpacing(10)
        
        # Login button
        login_btn = QPushButton("🔐 Sign In")
        login_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setMinimumHeight(50)
        login_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #eb915f, stop:1 #f97c66);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-size: 14pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f59e6d, stop:1 #fa8a74);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #d97f4f, stop:1 #e76d58);
            }
        """)
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)
        
        # Switch to register
        switch_layout = QHBoxLayout()
        switch_layout.setAlignment(Qt.AlignCenter)
        switch_layout.setSpacing(10)
        
        switch_label = QLabel("Don't have an account?")
        switch_label.setStyleSheet("color: #b3b3bb; background: transparent; font-size: 11pt;")
        switch_layout.addWidget(switch_label)
        
        switch_btn = QPushButton("Create Account")
        switch_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        switch_btn.setCursor(Qt.PointingHandCursor)
        switch_btn.setFixedHeight(36)
        switch_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #eb915f;
                border: 2px solid #eb915f;
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #eb915f;
                color: white;
            }
        """)
        switch_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        switch_layout.addWidget(switch_btn)
        
        layout.addSpacing(10)
        layout.addLayout(switch_layout)
        
        return widget
    
    def create_register_form(self):
        """Create registration form widget"""
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(widget)
        layout.setSpacing(18)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Username field
        reg_username_label = QLabel("Username *")
        reg_username_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        reg_username_label.setStyleSheet("color: #fafafa; background: transparent;")
        layout.addWidget(reg_username_label)
        
        self.reg_username_input = QLineEdit()
        self.reg_username_input.setPlaceholderText("Choose a username")
        layout.addWidget(self.reg_username_input)
        
        # Email field
        email_label = QLabel("Email *")
        email_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        email_label.setStyleSheet("color: #fafafa; background: transparent;")
        layout.addWidget(email_label)
        
        self.reg_email_input = QLineEdit()
        self.reg_email_input.setPlaceholderText("your.email@example.com")
        layout.addWidget(self.reg_email_input)
        
        layout.addSpacing(5)
        
        # Name fields in a row
        name_layout = QHBoxLayout()
        name_layout.setSpacing(15)
        
        # First name
        first_name_container = QVBoxLayout()
        first_name_container.setSpacing(8)
        first_name_label = QLabel("First Name")
        first_name_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        first_name_label.setStyleSheet("color: #fafafa; background: transparent;")
        first_name_container.addWidget(first_name_label)
        
        self.reg_firstname_input = QLineEdit()
        self.reg_firstname_input.setPlaceholderText("First name")
        first_name_container.addWidget(self.reg_firstname_input)
        name_layout.addLayout(first_name_container)
        
        # Last name
        last_name_container = QVBoxLayout()
        last_name_container.setSpacing(8)
        last_name_label = QLabel("Last Name")
        last_name_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        last_name_label.setStyleSheet("color: #fafafa; background: transparent;")
        last_name_container.addWidget(last_name_label)
        
        self.reg_lastname_input = QLineEdit()
        self.reg_lastname_input.setPlaceholderText("Last name")
        last_name_container.addWidget(self.reg_lastname_input)
        name_layout.addLayout(last_name_container)
        
        layout.addLayout(name_layout)
        
        layout.addSpacing(5)
        
        # Password field
        reg_password_label = QLabel("Password *")
        reg_password_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        reg_password_label.setStyleSheet("color: #fafafa; background: transparent;")
        layout.addWidget(reg_password_label)
        
        self.reg_password_input = QLineEdit()
        self.reg_password_input.setPlaceholderText("At least 6 characters")
        self.reg_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.reg_password_input)
        
        # Confirm password field
        confirm_password_label = QLabel("Confirm Password *")
        confirm_password_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        confirm_password_label.setStyleSheet("color: #fafafa; background: transparent;")
        layout.addWidget(confirm_password_label)
        
        self.reg_confirm_password_input = QLineEdit()
        self.reg_confirm_password_input.setPlaceholderText("Re-enter password")
        self.reg_confirm_password_input.setEchoMode(QLineEdit.Password)
        self.reg_confirm_password_input.returnPressed.connect(self.handle_register)
        layout.addWidget(self.reg_confirm_password_input)
        
        layout.addSpacing(10)
        
        # Register button
        register_btn = QPushButton("✨ Create Account")
        register_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        register_btn.setCursor(Qt.PointingHandCursor)
        register_btn.setMinimumHeight(50)
        register_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #eb915f, stop:1 #f97c66);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-size: 14pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f59e6d, stop:1 #fa8a74);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #d97f4f, stop:1 #e76d58);
            }
        """)
        register_btn.clicked.connect(self.handle_register)
        layout.addWidget(register_btn)
        
        # Switch to login
        switch_layout = QHBoxLayout()
        switch_layout.setAlignment(Qt.AlignCenter)
        switch_layout.setSpacing(10)
        
        switch_label = QLabel("Already have an account?")
        switch_label.setStyleSheet("color: #b3b3bb; background: transparent; font-size: 11pt;")
        switch_layout.addWidget(switch_label)
        
        switch_btn = QPushButton("Sign In")
        switch_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        switch_btn.setCursor(Qt.PointingHandCursor)
        switch_btn.setFixedHeight(36)
        switch_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #eb915f;
                border: 2px solid #eb915f;
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #eb915f;
                color: white;
            }
        """)
        switch_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        switch_layout.addWidget(switch_btn)
        
        layout.addSpacing(5)
        layout.addLayout(switch_layout)
        
        return widget
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Input Error", 
                              "Please enter both username and password.")
            return
        
        # Disable inputs during login
        self.username_input.setEnabled(False)
        self.password_input.setEnabled(False)
        self.setEnabled(False)
        
        # Show loading message
        progress = QProgressDialog("Logging in...", None, 0, 0, self)
        progress.setWindowTitle("Please Wait")
        progress.setWindowModality(Qt.WindowModal)
        progress.setCancelButton(None)
        progress.setMinimumDuration(0)
        progress.setValue(0)
        progress.show()
        
        QTimer.singleShot(100, lambda: self.do_login(username, password, progress))
    
    def do_login(self, username, password, progress):
        """Perform the actual login"""
        try:
            # Attempt login
            success, result = api_client.login(username, password)
            
            progress.close()
            
            if success:
                # Store credentials if remember me is checked
                if self.remember_checkbox.isChecked():
                    # In a real app, use secure storage
                    pass
                
                # Show main window
                try:
                    from ui.main_window import MainWindow
                    self.main_window = MainWindow(result)
                    self.main_window.show()
                    self.close()
                except Exception as e:
                    QMessageBox.critical(self, "Error", 
                                       f"Failed to open main window:\n{str(e)}")
                    self.username_input.setEnabled(True)
                    self.password_input.setEnabled(True)
                    self.setEnabled(True)
            else:
                QMessageBox.critical(self, "Login Failed", 
                                   f"Unable to login:\n{result}\n\n"
                                   f"Please check your credentials and try again.")
                # Re-enable inputs
                self.username_input.setEnabled(True)
                self.password_input.setEnabled(True)
                self.setEnabled(True)
                self.password_input.clear()
                self.password_input.setFocus()
        except Exception as e:
            progress.close()
            QMessageBox.critical(self, "Error", 
                               f"An error occurred:\n{str(e)}")
            self.username_input.setEnabled(True)
            self.password_input.setEnabled(True)
            self.setEnabled(True)
    
    def handle_register(self):
        """Handle registration button click"""
        username = self.reg_username_input.text().strip()
        email = self.reg_email_input.text().strip()
        password = self.reg_password_input.text()
        confirm_password = self.reg_confirm_password_input.text()
        first_name = self.reg_firstname_input.text().strip()
        last_name = self.reg_lastname_input.text().strip()
        
        # Validation
        if not username or not email or not password:
            QMessageBox.warning(self, "Input Error", 
                              "Please fill in all required fields (marked with *).")
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, "Password Mismatch", 
                              "Passwords do not match.")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "Invalid Password", 
                              "Password must be at least 6 characters long.")
            return
        
        # Attempt registration
        success, result = api_client.register(username, email, password, 
                                             first_name, last_name)
        
        if success:
            QMessageBox.information(self, "Registration Successful", 
                                  "Your account has been created successfully!\n"
                                  "You can now sign in.")
            # Switch to login form
            self.stacked_widget.setCurrentIndex(0)
            self.username_input.setText(username)
        else:
            QMessageBox.critical(self, "Registration Failed", 
                               f"Unable to create account:\n{result}")

"""
Upload Dialog - CSV file upload interface
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFileDialog, QMessageBox, QFrame,
                             QProgressBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QDragEnterEvent, QDropEvent
from utils.api_client import api_client
from utils.config import Config
import os

class UploadWorker(QThread):
    """Worker thread for uploading files"""
    
    upload_complete = pyqtSignal(bool, object)  # success, result
    progress_update = pyqtSignal(int)  # progress percentage
    
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
    
    def run(self):
        """Run the upload"""
        try:
            self.progress_update.emit(30)
            success, result = api_client.upload_csv(self.file_path)
            self.progress_update.emit(100)
            self.upload_complete.emit(success, result)
        except Exception as e:
            self.upload_complete.emit(False, str(e))


class UploadDialog(QDialog):
    """Dialog for uploading CSV files"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_file = None
        self.upload_worker = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("Upload CSV File")
        self.setFixedSize(700, 500)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel("📤 Upload Equipment Data")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setStyleSheet("color: #f0f0f5; background: transparent;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel("Select a CSV file containing equipment data to upload and analyze")
        desc_label.setFont(QFont("Segoe UI", 11))
        desc_label.setStyleSheet("color: #a1a1aa; background: transparent;")
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        layout.addSpacing(10)
        
        # Drop zone
        self.drop_zone = QFrame()
        self.drop_zone.setStyleSheet("""
            QFrame {
                background-color: #18181b;
                border: 3px dashed #6366f1;
                border-radius: 12px;
            }
        """)
        self.drop_zone.setMinimumHeight(200)
        self.drop_zone.setAcceptDrops(True)
        
        drop_layout = QVBoxLayout(self.drop_zone)
        drop_layout.setAlignment(Qt.AlignCenter)
        drop_layout.setSpacing(15)
        
        drop_icon = QLabel("📁")
        drop_icon.setFont(QFont("Segoe UI", 48))
        drop_icon.setAlignment(Qt.AlignCenter)
        drop_icon.setStyleSheet("background: transparent;")
        drop_layout.addWidget(drop_icon)
        
        drop_text = QLabel("Drag & Drop CSV file here\nor click browse button")
        drop_text.setFont(QFont("Segoe UI", 13))
        drop_text.setStyleSheet("color: #a1a1aa; background: transparent;")
        drop_text.setAlignment(Qt.AlignCenter)
        drop_layout.addWidget(drop_text)
        
        self.file_label = QLabel("No file selected")
        self.file_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.file_label.setStyleSheet("color: #6366f1; background: transparent;")
        self.file_label.setAlignment(Qt.AlignCenter)
        self.file_label.setWordWrap(True)
        drop_layout.addWidget(self.file_label)
        
        layout.addWidget(self.drop_zone)
        
        # Browse button
        browse_btn = QPushButton("📂 Browse Files")
        browse_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        browse_btn.setCursor(Qt.PointingHandCursor)
        browse_btn.setFixedHeight(50)
        browse_btn.clicked.connect(self.browse_file)
        layout.addWidget(browse_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Uploading... %p%")
        layout.addWidget(self.progress_bar)
        
        # Info label
        info_label = QLabel(f"Maximum file size: {Config.MAX_FILE_SIZE_MB} MB • Supported format: CSV")
        info_label.setFont(QFont("Segoe UI", 9))
        info_label.setStyleSheet("color: #71717a; background: transparent;")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("secondary")
        cancel_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setFixedHeight(45)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        self.upload_btn = QPushButton("Upload & Process")
        self.upload_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.upload_btn.setCursor(Qt.PointingHandCursor)
        self.upload_btn.setFixedHeight(45)
        self.upload_btn.setEnabled(False)
        self.upload_btn.clicked.connect(self.start_upload)
        button_layout.addWidget(self.upload_btn)
        
        layout.addLayout(button_layout)
        
        # Enable drag and drop
        self.setAcceptDrops(True)
    
    def browse_file(self):
        """Open file browser"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            self.set_selected_file(file_path)
    
    def set_selected_file(self, file_path):
        """Set the selected file"""
        # Validate file
        if not os.path.exists(file_path):
            QMessageBox.warning(self, "Invalid File", "The selected file does not exist.")
            return
        
        file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
        if file_size_mb > Config.MAX_FILE_SIZE_MB:
            QMessageBox.warning(self, "File Too Large", 
                              f"The file is {file_size_mb:.1f} MB. "
                              f"Maximum allowed size is {Config.MAX_FILE_SIZE_MB} MB.")
            return
        
        if not file_path.lower().endswith('.csv'):
            QMessageBox.warning(self, "Invalid Format", 
                              "Please select a CSV file.")
            return
        
        self.selected_file = file_path
        file_name = os.path.basename(file_path)
        self.file_label.setText(f"✓ {file_name} ({file_size_mb:.2f} MB)")
        self.upload_btn.setEnabled(True)
    
    def start_upload(self):
        """Start the upload process"""
        if not self.selected_file:
            return
        
        # Disable upload button
        self.upload_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Start upload in worker thread
        self.upload_worker = UploadWorker(self.selected_file)
        self.upload_worker.progress_update.connect(self.update_progress)
        self.upload_worker.upload_complete.connect(self.upload_finished)
        self.upload_worker.start()
    
    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.setValue(value)
    
    def upload_finished(self, success, result):
        """Handle upload completion"""
        self.progress_bar.setVisible(False)
        self.upload_btn.setEnabled(True)
        
        if success:
            dataset_id = result.get('dataset_id', 'N/A')
            row_count = result.get('row_count', 0)
            
            QMessageBox.information(
                self, "Upload Successful",
                f"CSV file uploaded and processed successfully!\n\n"
                f"Dataset ID: {dataset_id}\n"
                f"Rows processed: {row_count}"
            )
            self.accept()
        else:
            QMessageBox.critical(
                self, "Upload Failed",
                f"Failed to upload file:\n{result}"
            )
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """Handle file drop"""
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.lower().endswith('.csv'):
                self.set_selected_file(file_path)
            else:
                QMessageBox.warning(self, "Invalid File", "Please drop a CSV file.")

"""
Report Dialog - PDF report generation interface
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFileDialog, QMessageBox, QFrame,
                             QProgressBar, QCheckBox, QGroupBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from utils.api_client import api_client
from utils.config import Config
import os

class ReportWorker(QThread):
    """Worker thread for generating reports"""
    
    report_complete = pyqtSignal(bool, object)  # success, result
    progress_update = pyqtSignal(int)  # progress percentage
    
    def __init__(self, dataset_id, output_path):
        super().__init__()
        self.dataset_id = dataset_id
        self.output_path = output_path
    
    def run(self):
        """Generate the report"""
        try:
            self.progress_update.emit(30)
            success, result = api_client.download_pdf_report(self.dataset_id, self.output_path)
            self.progress_update.emit(100)
            self.report_complete.emit(success, result)
        except Exception as e:
            self.report_complete.emit(False, str(e))


class ReportDialog(QDialog):
    """Dialog for generating PDF reports"""
    
    def __init__(self, dataset_id, dataset_name, parent=None):
        super().__init__(parent)
        self.dataset_id = dataset_id
        self.dataset_name = dataset_name
        self.report_worker = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("Generate PDF Report")
        self.setFixedSize(650, 550)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel("📄 Generate PDF Report")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setStyleSheet("color: #f0f0f5; background: transparent;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Dataset info
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #18181b;
                border: 2px solid #3f3f46;
                border-left: 4px solid #6366f1;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(8)
        
        dataset_label = QLabel(f"Dataset: {self.dataset_name}")
        dataset_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        dataset_label.setStyleSheet("color: #f0f0f5; background: transparent;")
        info_layout.addWidget(dataset_label)
        
        id_label = QLabel(f"Dataset ID: {self.dataset_id}")
        id_label.setFont(QFont("Segoe UI", 10))
        id_label.setStyleSheet("color: #a1a1aa; background: transparent;")
        info_layout.addWidget(id_label)
        
        layout.addWidget(info_frame)
        
        # Report options
        options_group = QGroupBox("Report Options")
        options_group.setFont(QFont("Segoe UI", 12, QFont.Bold))
        options_group.setStyleSheet("""
            QGroupBox {
                color: #f0f0f5;
                border: 2px solid #3f3f46;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
            }
        """)
        
        options_layout = QVBoxLayout(options_group)
        options_layout.setSpacing(12)
        
        self.include_charts_cb = QCheckBox("Include Charts and Graphs")
        self.include_charts_cb.setChecked(True)
        self.include_charts_cb.setStyleSheet("""
            QCheckBox {
                color: #f0f0f5;
                font-size: 11pt;
            }
            QCheckBox::indicator {
                width: 22px;
                height: 22px;
                border: 2px solid #3f3f46;
                border-radius: 4px;
                background-color: #18181b;
            }
            QCheckBox::indicator:checked {
                background-color: #6366f1;
                border-color: #6366f1;
            }
        """)
        options_layout.addWidget(self.include_charts_cb)
        
        self.include_statistics_cb = QCheckBox("Include Statistical Summary")
        self.include_statistics_cb.setChecked(True)
        self.include_statistics_cb.setStyleSheet(self.include_charts_cb.styleSheet())
        options_layout.addWidget(self.include_statistics_cb)
        
        self.include_data_cb = QCheckBox("Include Raw Data Table")
        self.include_data_cb.setChecked(True)
        self.include_data_cb.setStyleSheet(self.include_charts_cb.styleSheet())
        options_layout.addWidget(self.include_data_cb)
        
        layout.addWidget(options_group)
        
        # Description
        desc_label = QLabel(
            "A comprehensive PDF report will be generated with visualizations, "
            "statistics, and insights from your dataset."
        )
        desc_label.setFont(QFont("Segoe UI", 10))
        desc_label.setStyleSheet("color: #a1a1aa; background: transparent;")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Generating report... %p%")
        layout.addWidget(self.progress_bar)
        
        layout.addStretch()
        
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
        
        self.generate_btn = QPushButton("Generate & Download")
        self.generate_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.generate_btn.setCursor(Qt.PointingHandCursor)
        self.generate_btn.setFixedHeight(45)
        self.generate_btn.clicked.connect(self.start_generation)
        button_layout.addWidget(self.generate_btn)
        
        layout.addLayout(button_layout)
    
    def start_generation(self):
        """Start report generation"""
        # Get save location
        default_filename = f"report_{self.dataset_name.replace('.csv', '')}.pdf"
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Report", default_filename, "PDF Files (*.pdf)"
        )
        
        if not file_path:
            return
        
        # Ensure .pdf extension
        if not file_path.lower().endswith('.pdf'):
            file_path += '.pdf'
        
        # Disable button and show progress
        self.generate_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Start generation in worker thread
        self.report_worker = ReportWorker(self.dataset_id, file_path)
        self.report_worker.progress_update.connect(self.update_progress)
        self.report_worker.report_complete.connect(self.generation_finished)
        self.report_worker.start()
    
    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.setValue(value)
    
    def generation_finished(self, success, result):
        """Handle generation completion"""
        self.progress_bar.setVisible(False)
        self.generate_btn.setEnabled(True)
        
        if success:
            reply = QMessageBox.question(
                self, "Report Generated",
                f"PDF report generated successfully!\n\n"
                f"File: {os.path.basename(result)}\n\n"
                f"Would you like to open the report now?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
            )
            
            if reply == QMessageBox.Yes:
                # Open PDF with default application
                import subprocess
                import platform
                
                try:
                    if platform.system() == 'Windows':
                        os.startfile(result)
                    elif platform.system() == 'Darwin':  # macOS
                        subprocess.call(['open', result])
                    else:  # Linux
                        subprocess.call(['xdg-open', result])
                except Exception as e:
                    QMessageBox.warning(self, "Cannot Open File", 
                                      f"Report saved but couldn't open automatically:\n{str(e)}")
            
            self.accept()
        else:
            QMessageBox.critical(
                self, "Generation Failed",
                f"Failed to generate report:\n{result}"
            )

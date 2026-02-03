"""
Main Window - Dashboard with all features
Includes charts, data tables, upload, and reports
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QTabWidget, QTableWidget, 
                             QTableWidgetItem, QFileDialog, QMessageBox, 
                             QComboBox, QFrame, QScrollArea, QSplitter,
                             QHeaderView, QProgressDialog)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor
import os
from datetime import datetime
from utils.api_client import api_client
from utils.config import Config
from ui.chart_widgets import ChartWidget, MultiChartWidget
from ui.upload_dialog import UploadDialog
from ui.report_dialog import ReportDialog

class MainWindow(QMainWindow):
    """Main application window with dashboard"""
    
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.current_dataset_id = None
        self.current_dataset_name = ""
        self.datasets = []
        self.statistics = None
        self.data_rows = []
        
        self.init_ui()
        self.load_initial_data()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(f"{Config.WINDOW_TITLE} - {self.user_data.get('user', {}).get('username', 'User')}")
        self.setMinimumSize(Config.WINDOW_MIN_WIDTH, Config.WINDOW_MIN_HEIGHT)
        
        # Start in fullscreen mode
        self.showMaximized()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top navigation bar
        navbar = self.create_navbar()
        main_layout.addWidget(navbar)
        
        # Content area with tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #121214;
            }
            QTabBar::tab {
                background-color: #27272a;
                color: #a1a1aa;
                border: none;
                padding: 15px 40px;
                margin-right: 2px;
                font-size: 12pt;
                font-weight: bold;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                min-width: 140px;
            }
            QTabBar::tab:selected {
                background-color: #6366f1;
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background-color: #3f3f46;
                color: #f0f0f5;
            }
        """)
        
        # Create tab pages
        self.dashboard_tab = self.create_dashboard_tab()
        self.data_tab = self.create_data_tab()
        self.history_tab = self.create_history_tab()
        
        self.tabs.addTab(self.dashboard_tab, "📊 Dashboard")
        self.tabs.addTab(self.data_tab, "📋 Data View")
        self.tabs.addTab(self.history_tab, "📜 History")
        
        main_layout.addWidget(self.tabs)
        
        # Status bar
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: #18181b;
                color: #a1a1aa;
                border-top: 2px solid #3f3f46;
                font-size: 10pt;
                padding: 5px;
            }
        """)
        self.statusBar().showMessage("Ready")
    
    def create_navbar(self):
        """Create top navigation bar"""
        navbar = QFrame()
        navbar.setStyleSheet("""
            QFrame {
                background-color: #18181b;
                border-bottom: 2px solid #6366f1;
            }
        """)
        navbar.setFixedHeight(80)
        
        layout = QHBoxLayout(navbar)
        layout.setContentsMargins(25, 10, 25, 10)
        
        # Left section - Title and dataset selector
        left_layout = QVBoxLayout()
        left_layout.setSpacing(5)
        
        title_label = QLabel("⚗️ Equipment Analytics")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setStyleSheet("color: #f0f0f5; background: transparent;")
        left_layout.addWidget(title_label)
        
        # Dataset selector
        selector_layout = QHBoxLayout()
        selector_label = QLabel("Dataset:")
        selector_label.setStyleSheet("color: #a1a1aa; background: transparent; font-size: 11pt;")
        selector_layout.addWidget(selector_label)
        
        self.dataset_combo = QComboBox()
        self.dataset_combo.setMinimumWidth(300)
        self.dataset_combo.currentIndexChanged.connect(self.on_dataset_changed)
        selector_layout.addWidget(self.dataset_combo)
        selector_layout.addStretch()
        
        left_layout.addLayout(selector_layout)
        layout.addLayout(left_layout)
        
        layout.addStretch()
        
        # Right section - Action buttons
        right_layout = QHBoxLayout()
        right_layout.setSpacing(15)
        
        # Upload button
        upload_btn = QPushButton("📤 Upload CSV")
        upload_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        upload_btn.setCursor(Qt.PointingHandCursor)
        upload_btn.setFixedHeight(45)
        upload_btn.clicked.connect(self.show_upload_dialog)
        right_layout.addWidget(upload_btn)
        
        # Generate Report button
        report_btn = QPushButton("📄 Generate Report")
        report_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        report_btn.setCursor(Qt.PointingHandCursor)
        report_btn.setFixedHeight(45)
        report_btn.clicked.connect(self.show_report_dialog)
        right_layout.addWidget(report_btn)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.setObjectName("secondary")
        refresh_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.setFixedHeight(45)
        refresh_btn.clicked.connect(self.refresh_data)
        right_layout.addWidget(refresh_btn)
        
        # Logout button
        logout_btn = QPushButton("🚪 Logout")
        logout_btn.setObjectName("danger")
        logout_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.setFixedHeight(45)
        logout_btn.clicked.connect(self.handle_logout)
        right_layout.addWidget(logout_btn)
        
        layout.addLayout(right_layout)
        
        return navbar
    
    def create_dashboard_tab(self):
        """Create dashboard tab with charts and statistics"""
        widget = QWidget()
        
        # Make it scrollable
        scroll = QScrollArea()
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # Statistics section header
        stats_header = QLabel("📊 Key Metrics")
        stats_header.setFont(QFont("Segoe UI", 13, QFont.Bold))
        stats_header.setStyleSheet("color: #f0f0f5; background: transparent; margin-bottom: 3px;")
        layout.addWidget(stats_header)
        
        # Statistics cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)
        
        self.total_records_card = self.create_stat_card("Total Records", "0", "#eb915f")
        self.avg_flowrate_card = self.create_stat_card("Avg Flowrate", "0.0", "#f97c66")
        self.avg_pressure_card = self.create_stat_card("Avg Pressure", "0.0", "#a966d9")
        self.avg_temperature_card = self.create_stat_card("Avg Temperature", "0.0", "#10b981")
        
        stats_layout.addWidget(self.total_records_card)
        stats_layout.addWidget(self.avg_flowrate_card)
        stats_layout.addWidget(self.avg_pressure_card)
        stats_layout.addWidget(self.avg_temperature_card)
        
        layout.addLayout(stats_layout)
        
        layout.addSpacing(20)
        
        # Charts section
        charts_label = QLabel("📈 Data Visualization")
        charts_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
        charts_label.setStyleSheet("color: #f0f0f5; background: transparent; margin-top: 5px;")
        layout.addWidget(charts_label)
        
        # Multi-chart widget
        self.multi_chart_widget = MultiChartWidget()
        layout.addWidget(self.multi_chart_widget)
        
        layout.addStretch()
        
        return scroll
    
    def create_data_tab(self):
        """Create data view tab with table"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        data_label = QLabel("📋 Dataset Preview")
        data_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        data_label.setStyleSheet("color: #f0f0f5; background: transparent;")
        header_layout.addWidget(data_label)
        
        header_layout.addStretch()
        
        # Export button
        export_btn = QPushButton("💾 Export to CSV")
        export_btn.setObjectName("secondary")
        export_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        export_btn.setCursor(Qt.PointingHandCursor)
        export_btn.clicked.connect(self.export_to_csv)
        header_layout.addWidget(export_btn)
        
        layout.addLayout(header_layout)
        
        # Table
        self.data_table = QTableWidget()
        self.data_table.setAlternatingRowColors(True)
        self.data_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.data_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.data_table.setMinimumHeight(400)
        self.data_table.setStyleSheet("""
            QTableWidget {
                font-size: 10pt;
            }
            QTableWidget::item {
                padding: 10px;
                color: #fafafa;
            }
        """)
        
        layout.addWidget(self.data_table)
        
        # Info label
        self.table_info_label = QLabel("No data loaded")
        self.table_info_label.setStyleSheet("color: #a1a1aa; background: transparent; font-size: 11pt;")
        layout.addWidget(self.table_info_label)
        
        return widget
    
    def create_history_tab(self):
        """Create history tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        history_label = QLabel("📜 Upload History")
        history_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        history_label.setStyleSheet("color: #f0f0f5; background: transparent;")
        layout.addWidget(history_label)
        
        # History table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["ID", "Filename", "Upload Date", "Rows", "Actions"])
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.history_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.history_table.verticalHeader().setDefaultSectionSize(75)  # Set row height
        self.history_table.setWordWrap(True)  # Enable word wrap for text
        self.history_table.setStyleSheet("""
            QTableWidget {
                font-size: 11pt;
            }
            QTableWidget::item {
                padding: 12px;
                color: #fafafa;
            }
        """)
        
        layout.addWidget(self.history_table)
        
        return widget
    
    def create_stat_card(self, title, value, color):
        """Create a statistics card widget with vibrant gradient"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2e2e36, stop:1 #28282e);
                border: 3px solid {color};
                border-radius: 10px;
            }}
        """)
        card.setFixedHeight(100)
        card.setMinimumWidth(200)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(8)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 9, QFont.Bold))
        title_label.setStyleSheet("color: #fafafa; background: transparent;")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        value_label.setStyleSheet(f"color: {color}; background: transparent;")
        layout.addWidget(value_label)
        
        layout.addStretch()
        
        # Store value label for updates
        card.value_label = value_label
        
        return card
    
    def load_initial_data(self):
        """Load initial data when window opens"""
        self.statusBar().showMessage("Loading datasets...")
        
        # Load datasets list
        success, result = api_client.list_datasets()
        
        if success:
            self.datasets = result.get('datasets', [])
            self.update_dataset_combo()
            
            # Load the most recent dataset if available
            if self.datasets:
                self.current_dataset_id = self.datasets[0]['id']
                self.load_dataset_data(self.current_dataset_id)
            else:
                self.statusBar().showMessage("No datasets found. Upload a CSV to get started.")
        else:
            QMessageBox.warning(self, "Error", f"Failed to load datasets:\n{result}")
            self.statusBar().showMessage("Error loading datasets")
        
        # Load history
        self.load_history()
    
    def update_dataset_combo(self):
        """Update dataset combo box"""
        self.dataset_combo.clear()
        
        if not self.datasets:
            self.dataset_combo.addItem("No datasets available")
            self.dataset_combo.setEnabled(False)
            return
        
        self.dataset_combo.setEnabled(True)
        for dataset in self.datasets:
            display_name = f"{dataset['file_name']} ({dataset['row_count']} rows)"
            self.dataset_combo.addItem(display_name, dataset['id'])
    
    def on_dataset_changed(self, index):
        """Handle dataset selection change"""
        if index < 0 or not self.datasets:
            return
        
        dataset_id = self.dataset_combo.itemData(index)
        if dataset_id and dataset_id != self.current_dataset_id:
            self.load_dataset_data(dataset_id)
    
    def load_dataset_data(self, dataset_id):
        """Load data for a specific dataset"""
        self.statusBar().showMessage(f"Loading dataset {dataset_id}...")
        
        # Get dataset details
        success, result = api_client.get_dataset(dataset_id)
        
        if success:
            self.current_dataset_id = dataset_id
            self.current_dataset_name = result.get('file_name', '')
            self.statistics = result.get('statistics', {})
            
            # Update statistics cards
            self.update_statistics_display()
            
            # Load data for table
            self.load_table_data(dataset_id)
            
            # Update charts
            self.update_charts()
            
            self.statusBar().showMessage(f"Loaded: {self.current_dataset_name}")
        else:
            QMessageBox.warning(self, "Error", f"Failed to load dataset:\n{result}")
            self.statusBar().showMessage("Error loading dataset")
    
    def update_statistics_display(self):
        """Update statistics cards with current data"""
        if not self.statistics:
            return
        
        # Handle both formats: new (overall_averages) and old (direct stats)
        if 'overall_averages' in self.statistics:
            # New format from backend
            overall = self.statistics['overall_averages']
            count = self.statistics.get('total_equipment_count', 0)
            
            self.total_records_card.value_label.setText(str(count))
            self.avg_flowrate_card.value_label.setText(f"{overall.get('flowrate', 0):.2f}")
            self.avg_pressure_card.value_label.setText(f"{overall.get('pressure', 0):.2f}")
            self.avg_temperature_card.value_label.setText(f"{overall.get('temperature', 0):.2f}")
            
            # Convert to expected format for charts
            self.statistics = self._convert_statistics_format(self.statistics)
        else:
            # Old format (direct count, flowrate, pressure, temperature)
            self.total_records_card.value_label.setText(
                str(self.statistics.get('count', 0))
            )
            
            flowrate_mean = self.statistics.get('flowrate', {}).get('mean', 0)
            self.avg_flowrate_card.value_label.setText(f"{flowrate_mean:.2f}")
            
            pressure_mean = self.statistics.get('pressure', {}).get('mean', 0)
            self.avg_pressure_card.value_label.setText(f"{pressure_mean:.2f}")
            
            temperature_mean = self.statistics.get('temperature', {}).get('mean', 0)
            self.avg_temperature_card.value_label.setText(f"{temperature_mean:.2f}")
    
    def _convert_statistics_format(self, stats):
        """Convert backend statistics format to frontend expected format"""
        if 'overall_averages' not in stats:
            return stats
        
        overall = stats['overall_averages']
        by_type = stats.get('by_type', {})
        
        # Calculate overall min/max/std from by_type data
        flowrate_values = []
        pressure_values = []
        temperature_values = []
        
        for equip_type, data in by_type.items():
            if 'flowrate' in data:
                flowrate_values.extend([data['flowrate'].get('min', 0), data['flowrate'].get('max', 0)])
            if 'pressure' in data:
                pressure_values.extend([data['pressure'].get('min', 0), data['pressure'].get('max', 0)])
            if 'temperature' in data:
                temperature_values.extend([data['temperature'].get('min', 0), data['temperature'].get('max', 0)])
        
        # Calculate std as (max - min) / 4 (rough estimate)
        flowrate_std = (max(flowrate_values) - min(flowrate_values)) / 4 if flowrate_values else 1
        pressure_std = (max(pressure_values) - min(pressure_values)) / 4 if pressure_values else 1
        temperature_std = (max(temperature_values) - min(temperature_values)) / 4 if temperature_values else 1
        
        return {
            'count': stats.get('total_equipment_count', 0),
            'flowrate': {
                'mean': overall.get('flowrate', 0),
                'std': flowrate_std,
                'min': min(flowrate_values) if flowrate_values else 0,
                'max': max(flowrate_values) if flowrate_values else 0
            },
            'pressure': {
                'mean': overall.get('pressure', 0),
                'std': pressure_std,
                'min': min(pressure_values) if pressure_values else 0,
                'max': max(pressure_values) if pressure_values else 0
            },
            'temperature': {
                'mean': overall.get('temperature', 0),
                'std': temperature_std,
                'min': min(temperature_values) if temperature_values else 0,
                'max': max(temperature_values) if temperature_values else 0
            }
        }
    
    def load_table_data(self, dataset_id):
        """Load data into table view"""
        success, result = api_client.get_dataset_data(dataset_id)
        
        if success:
            # Handle both list and dict responses
            if isinstance(result, list):
                data = result
            else:
                data = result.get('data', [])
            
            if not data:
                self.data_table.setRowCount(0)
                self.table_info_label.setText("No data available")
                return
            
            # Store data
            self.data_rows = data
            
            # Set up table
            headers = list(data[0].keys()) if data else []
            self.data_table.setColumnCount(len(headers))
            self.data_table.setHorizontalHeaderLabels(headers)
            self.data_table.setRowCount(len(data))
            
            # Populate table
            for row_idx, row_data in enumerate(data):
                for col_idx, header in enumerate(headers):
                    value = row_data.get(header, '')
                    item = QTableWidgetItem(str(value))
                    self.data_table.setItem(row_idx, col_idx, item)
            
            # Resize columns
            self.data_table.resizeColumnsToContents()
            
            self.table_info_label.setText(
                f"Showing {len(data)} records from {self.current_dataset_name}"
            )
        else:
            self.table_info_label.setText(f"Error loading data: {result}")
    
    def update_charts(self):
        """Update chart displays with current data"""
        if not self.statistics:
            return
        
        self.multi_chart_widget.update_charts(self.statistics, self.current_dataset_name)
    
    def load_history(self):
        """Load upload history"""
        if not self.datasets:
            self.history_table.setRowCount(0)
            return
        
        self.history_table.setRowCount(len(self.datasets))
        
        for row_idx, dataset in enumerate(self.datasets):
            # ID
            id_item = QTableWidgetItem(str(dataset['id']))
            self.history_table.setItem(row_idx, 0, id_item)
            
            # Filename
            name_item = QTableWidgetItem(dataset['file_name'])
            self.history_table.setItem(row_idx, 1, name_item)
            
            # Upload date
            date_str = dataset.get('uploaded_at', '')
            if date_str:
                try:
                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    date_formatted = date_obj.strftime('%Y-%m-%d %H:%M')
                except:
                    date_formatted = date_str
            else:
                date_formatted = 'N/A'
            date_item = QTableWidgetItem(date_formatted)
            self.history_table.setItem(row_idx, 2, date_item)
            
            # Row count
            rows_item = QTableWidgetItem(str(dataset.get('row_count', 0)))
            self.history_table.setItem(row_idx, 3, rows_item)
            
            # Actions - Create buttons with tooltips
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(10, 8, 10, 8)
            actions_layout.setSpacing(12)
            
            view_btn = QPushButton("📊 Load")
            view_btn.setFixedSize(100, 44)
            view_btn.setToolTip("Load this dataset and display its data in Dashboard and Data View tabs")
            view_btn.setStyleSheet("""
                QPushButton {
                    font-size: 12pt;
                    font-weight: bold;
                    padding: 8px 12px;
                }
            """)
            view_btn.clicked.connect(lambda checked, did=dataset['id']: self.load_dataset_data(did))
            actions_layout.addWidget(view_btn)
            
            delete_btn = QPushButton("🗑️ Delete")
            delete_btn.setObjectName("danger")
            delete_btn.setFixedSize(100, 44)
            delete_btn.setToolTip("Permanently delete this dataset from the database")
            delete_btn.setStyleSheet("""
                QPushButton {
                    font-size: 12pt;
                    font-weight: bold;
                    padding: 8px 12px;
                }
            """)
            delete_btn.clicked.connect(lambda checked, did=dataset['id']: self.delete_dataset(did))
            actions_layout.addWidget(delete_btn)
            
            self.history_table.setCellWidget(row_idx, 4, actions_widget)
    
    def show_upload_dialog(self):
        """Show upload dialog"""
        dialog = UploadDialog(self)
        if dialog.exec_():
            # Refresh data after upload
            self.refresh_data()
    
    def show_report_dialog(self):
        """Show report generation dialog"""
        if not self.current_dataset_id:
            QMessageBox.warning(self, "No Dataset", 
                              "Please select or upload a dataset first.")
            return
        
        dialog = ReportDialog(self.current_dataset_id, self.current_dataset_name, self)
        dialog.exec_()
    
    def refresh_data(self):
        """Refresh all data"""
        self.load_initial_data()
        self.statusBar().showMessage("Data refreshed", 3000)
    
    def delete_dataset(self, dataset_id):
        """Delete a dataset"""
        reply = QMessageBox.question(
            self, 'Confirm Delete',
            'Are you sure you want to delete this dataset?\nThis action cannot be undone.',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, result = api_client.delete_dataset(dataset_id)
            
            if success:
                QMessageBox.information(self, "Success", "Dataset deleted successfully.")
                self.refresh_data()
            else:
                QMessageBox.critical(self, "Error", f"Failed to delete dataset:\n{result}")
    
    def export_to_csv(self):
        """Export current data to CSV"""
        if not self.data_rows:
            QMessageBox.warning(self, "No Data", "No data to export.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export to CSV", "", "CSV Files (*.csv)"
        )
        
        if file_path:
            try:
                import csv
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    if self.data_rows:
                        writer = csv.DictWriter(f, fieldnames=self.data_rows[0].keys())
                        writer.writeheader()
                        writer.writerows(self.data_rows)
                
                QMessageBox.information(self, "Success", 
                                      f"Data exported successfully to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", 
                                   f"Failed to export data:\n{str(e)}")
    
    def handle_logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            self, 'Confirm Logout',
            'Are you sure you want to logout?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            api_client.clear_credentials()
            from ui.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()

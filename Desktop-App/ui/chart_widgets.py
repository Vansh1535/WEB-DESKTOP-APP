"""
Chart widgets using matplotlib
Professional charts with dark theme
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from utils.config import Config

class ChartWidget(QWidget):
    """Base chart widget with matplotlib"""
    
    def __init__(self, title="Chart"):
        super().__init__()
        self.title = title
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Create matplotlib figure with dark theme
        self.figure = Figure(figsize=(8, 6), facecolor='#18181b')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: #18181b;")
        
        layout.addWidget(self.canvas)
    
    def clear_chart(self):
        """Clear the chart"""
        self.figure.clear()
        self.canvas.draw()


class MultiChartWidget(QWidget):
    """Widget containing multiple charts"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Create matplotlib figure with subplots - BIGGER SIZE
        self.figure = Figure(figsize=(16, 10), facecolor='#1a1a1d')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("""
            background-color: #1a1a1d; 
            border: 2px solid #3f3f46;
            border-radius: 8px;
        """)
        self.canvas.setMinimumHeight(700)
        
        layout.addWidget(self.canvas)
    
    def update_charts(self, statistics, dataset_name="Dataset"):
        """Update all charts with new data"""
        self.figure.clear()
        
        # Create 2x2 subplot grid
        axes = self.figure.subplots(2, 2)
        
        # Apply dark theme to all axes
        for ax_row in axes:
            for ax in ax_row:
                ax.set_facecolor('#0f0f11')
                ax.tick_params(colors='#e5e7eb', labelsize=10)
                ax.spines['bottom'].set_color('#4b5563')
                ax.spines['top'].set_color('#4b5563')
                ax.spines['left'].set_color('#4b5563')
                ax.spines['right'].set_color('#4b5563')
                ax.spines['bottom'].set_linewidth(1.5)
                ax.spines['top'].set_linewidth(1.5)
                ax.spines['left'].set_linewidth(1.5)
                ax.spines['right'].set_linewidth(1.5)
                ax.title.set_color('#f9fafb')
                ax.xaxis.label.set_color('#e5e7eb')
                ax.yaxis.label.set_color('#e5e7eb')
                ax.grid(True, alpha=0.2, color='#4b5563', linestyle='--', linewidth=0.8)
        
        # Chart 1: Statistics Comparison (Bar Chart)
        self.plot_statistics_comparison(axes[0, 0], statistics)
        
        # Chart 2: Distribution (Box Plot)
        self.plot_distribution(axes[0, 1], statistics)
        
        # Chart 3: Time Series / Line Chart
        self.plot_time_series(axes[1, 0], statistics)
        
        # Chart 4: Pie Chart - Value Distribution
        self.plot_value_distribution(axes[1, 1], statistics)
        
        # Adjust layout with more padding
        self.figure.tight_layout(pad=2.5)
        self.canvas.draw()
    
    def plot_statistics_comparison(self, ax, statistics):
        """Plot bar chart comparing mean values"""
        metrics = ['Flowrate', 'Pressure', 'Temperature']
        values = [
            statistics.get('flowrate', {}).get('mean', 0),
            statistics.get('pressure', {}).get('mean', 0),
            statistics.get('temperature', {}).get('mean', 0)
        ]
        
        colors = [Config.CHART_COLORS[0], Config.CHART_COLORS[1], Config.CHART_COLORS[2]]
        
        bars = ax.bar(metrics, values, color=colors, alpha=0.9, edgecolor='#e5e7eb', linewidth=2, width=0.6)
        
        ax.set_title('Average Values Comparison', fontsize=14, fontweight='bold', pad=15, color='#f9fafb')
        ax.set_ylabel('Value', fontsize=11, fontweight='bold')
        ax.tick_params(axis='x', labelsize=11)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value:.2f}',
                   ha='center', va='bottom', color='#f9fafb', fontsize=10, fontweight='bold')
    
    def plot_distribution(self, ax, statistics):
        """Plot box plot showing data distribution"""
        data_to_plot = []
        labels = []
        
        for metric in ['flowrate', 'pressure', 'temperature']:
            if metric in statistics:
                stats = statistics[metric]
                # Create synthetic data points from statistics
                mean = stats.get('mean', 0)
                std = stats.get('std', 0)
                min_val = stats.get('min', mean - std)
                max_val = stats.get('max', mean + std)
                
                # Generate synthetic distribution
                data_points = [
                    min_val,
                    mean - std * 0.5,
                    mean,
                    mean + std * 0.5,
                    max_val
                ]
                data_to_plot.append(data_points)
                labels.append(metric.capitalize())
        
        if data_to_plot:
            bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True,
                           boxprops=dict(facecolor=Config.CHART_COLORS[3], alpha=0.8, edgecolor='#e5e7eb', linewidth=1.5),
                           whiskerprops=dict(color='#e5e7eb', linewidth=1.5),
                           capprops=dict(color='#e5e7eb', linewidth=1.5),
                           medianprops=dict(color='#fbbf24', linewidth=3),
                           flierprops=dict(marker='o', markerfacecolor=Config.CHART_COLORS[4], 
                                          markersize=8, alpha=0.8, markeredgecolor='#e5e7eb'))
        
        ax.set_title('Data Distribution', fontsize=14, fontweight='bold', pad=15, color='#f9fafb')
        ax.set_ylabel('Value', fontsize=11, fontweight='bold')
        ax.tick_params(axis='x', labelsize=11)
    
    def plot_time_series(self, ax, statistics):
        """Plot line chart (simulated time series)"""
        # Generate sample time series data based on statistics
        count = statistics.get('count', 10)
        x = np.linspace(0, count, min(count, 50))
        
        flowrate_mean = statistics.get('flowrate', {}).get('mean', 0)
        pressure_mean = statistics.get('pressure', {}).get('mean', 0)
        temperature_mean = statistics.get('temperature', {}).get('mean', 0)
        
        flowrate_std = statistics.get('flowrate', {}).get('std', 1)
        pressure_std = statistics.get('pressure', {}).get('std', 1)
        temperature_std = statistics.get('temperature', {}).get('std', 1)
        
        # Generate smooth curves with noise
        np.random.seed(42)
        flowrate_y = flowrate_mean + flowrate_std * 0.3 * np.sin(x / 5) + np.random.normal(0, flowrate_std * 0.1, len(x))
        pressure_y = pressure_mean + pressure_std * 0.3 * np.cos(x / 7) + np.random.normal(0, pressure_std * 0.1, len(x))
        temperature_y = temperature_mean + temperature_std * 0.2 * np.sin(x / 10) + np.random.normal(0, temperature_std * 0.1, len(x))
        
        ax.plot(x, flowrate_y, color=Config.CHART_COLORS[0], linewidth=2, label='Flowrate', alpha=0.95)
        ax.plot(x, pressure_y, color=Config.CHART_COLORS[1], linewidth=2, label='Pressure', alpha=0.95)
        ax.plot(x, temperature_y, color=Config.CHART_COLORS[2], linewidth=2, label='Temperature', alpha=0.95)
        
        ax.set_title('Trend Analysis', fontsize=14, fontweight='bold', pad=15, color='#f9fafb')
        ax.set_xlabel('Data Points', fontsize=11, fontweight='bold')
        ax.set_ylabel('Value', fontsize=11, fontweight='bold')
        
        legend = ax.legend(loc='upper right', framealpha=0.95, edgecolor='#4b5563', 
                          facecolor='#1f2937', fontsize=10)
        for text in legend.get_texts():
            text.set_color('#f9fafb')
    
    def plot_value_distribution(self, ax, statistics):
        """Plot pie chart showing value distribution"""
        flowrate_mean = statistics.get('flowrate', {}).get('mean', 0)
        pressure_mean = statistics.get('pressure', {}).get('mean', 0)
        temperature_mean = statistics.get('temperature', {}).get('mean', 0)
        
        # Calculate percentages
        total = flowrate_mean + pressure_mean + temperature_mean
        
        if total > 0:
            sizes = [flowrate_mean, pressure_mean, temperature_mean]
            labels = [
                f'Flowrate\n{flowrate_mean:.1f}',
                f'Pressure\n{pressure_mean:.1f}',
                f'Temperature\n{temperature_mean:.1f}'
            ]
            colors = [Config.CHART_COLORS[0], Config.CHART_COLORS[1], Config.CHART_COLORS[2]]
            
            wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
                                              startangle=90, textprops={'fontsize': 10, 'color': '#f9fafb',
                                                                       'fontweight': 'bold'},
                                              wedgeprops={'edgecolor': '#0f0f11', 'linewidth': 2})
            
            # Make percentage text white and bold
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(10)
                autotext.set_fontweight('bold')
        else:
            ax.text(0.5, 0.5, 'No data available', 
                   horizontalalignment='center', verticalalignment='center',
                   transform=ax.transAxes, color='#9ca3af', fontsize=12, fontweight='bold')
        
        ax.set_title('Value Distribution', fontsize=14, fontweight='bold', pad=15, color='#f9fafb')

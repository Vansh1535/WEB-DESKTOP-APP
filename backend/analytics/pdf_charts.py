"""
Chart generation utilities for PDF reports.
"""
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from reportlab.platypus import Image
from reportlab.lib.units import inch


def create_bar_chart(statistics):
    """Create a stacked bar chart showing parameter composition for each equipment."""
    try:
        by_type = statistics.get('by_type', {})
        
        if not by_type:
            return None
        
        # Prepare data - normalize to percentages for better visualization
        types = list(by_type.keys())
        
        # Calculate normalized values (as percentage of total for each equipment)
        normalized_data = []
        for t in types:
            total = (by_type[t]['flowrate']['avg'] + 
                    by_type[t]['pressure']['avg'] * 20 +  # Scale pressure
                    by_type[t]['temperature']['avg'])
            normalized_data.append([
                (by_type[t]['flowrate']['avg'] / total) * 100,
                (by_type[t]['pressure']['avg'] * 20 / total) * 100,
                (by_type[t]['temperature']['avg'] / total) * 100
            ])
        
        normalized_data = np.array(normalized_data).T
        
        # Create stacked bar chart
        fig, ax = plt.subplots(figsize=(6, 4))
        
        x = np.arange(len(types))
        width = 0.6
        
        colors = ['#0EA5E9', '#FBBF24', '#FF6B6B']
        labels = ['Flowrate', 'Pressure (scaled)', 'Temperature']
        
        bottom = np.zeros(len(types))
        for i, (data, color, label) in enumerate(zip(normalized_data, colors, labels)):
            ax.bar(x, data, width, bottom=bottom, label=label, color=color, alpha=0.8)
            bottom += data
        
        ax.set_xlabel('Equipment Type', fontweight='bold', fontsize=10)
        ax.set_ylabel('Parameter Composition (%)', fontweight='bold', fontsize=10)
        ax.set_title('Parameter Composition by Equipment', fontweight='bold', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(types, rotation=45, ha='right', fontsize=9)
        ax.legend(fontsize=9, loc='upper right')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        # Save to buffer
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        # Create ReportLab Image
        img = Image(img_buffer, width=5*inch, height=3.3*inch)
        return img
        
    except Exception as e:
        print(f"Error creating bar chart: {e}")
        return None


def create_pie_chart(statistics):
    """Create a donut chart with equipment count rankings."""
    try:
        by_type = statistics.get('by_type', {})
        
        if not by_type:
            return None
        
        # Prepare data - sorted by count
        sorted_items = sorted(by_type.items(), key=lambda x: x[1]['count'], reverse=True)
        types = [item[0] for item in sorted_items]
        counts = [item[1]['count'] for item in sorted_items]
        
        # Create figure with donut chart
        fig, ax = plt.subplots(figsize=(6, 4))
        
        colors_list = ['#FF6B1A', '#D94452', '#7B2C9E', '#0EA5E9', '#10B981', 
                      '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4', '#84CC16']
        
        wedges, texts, autotexts = ax.pie(
            counts, 
            labels=types, 
            autopct='%1.1f%%',
            colors=colors_list[:len(types)],
            startangle=90,
            pctdistance=0.85,
            textprops={'fontsize': 9}
        )
        
        # Create donut effect
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        ax.add_artist(centre_circle)
        
        # Add total count in center
        total_count = sum(counts)
        ax.text(0, 0, f'{total_count}\\nTotal\\nEquipment', 
               ha='center', va='center', fontsize=11, fontweight='bold')
        
        # Bold percentage text
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        ax.set_title('Equipment Count Distribution (Ranked)', fontweight='bold', fontsize=12)
        
        plt.tight_layout()
        
        # Save to buffer
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        # Create ReportLab Image
        img = Image(img_buffer, width=5*inch, height=3.3*inch)
        return img
        
    except Exception as e:
        print(f"Error creating pie chart: {e}")
        return None


def create_comparison_chart(statistics):
    """Create a grouped comparison chart showing min/max/avg for each parameter."""
    try:
        by_type = statistics.get('by_type', {})
        
        if not by_type:
            return None
        
        # Prepare data for all equipment types
        types = list(by_type.keys())
        
        # Get min, max, avg for flowrate, pressure, temperature
        flowrate_data = [(by_type[t]['flowrate']['min'], 
                         by_type[t]['flowrate']['avg'], 
                         by_type[t]['flowrate']['max']) for t in types]
        
        pressure_data = [(by_type[t]['pressure']['min'], 
                         by_type[t]['pressure']['avg'], 
                         by_type[t]['pressure']['max']) for t in types]
        
        temp_data = [(by_type[t]['temperature']['min'], 
                     by_type[t]['temperature']['avg'], 
                     by_type[t]['temperature']['max']) for t in types]
        
        # Create figure with 3 subplots
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 3))
        
        x = np.arange(len(types))
        width = 0.6
        
        # Flowrate plot
        ax1.bar(x, [d[1] for d in flowrate_data], width, color='#0EA5E9', alpha=0.8)
        ax1.errorbar(x, [d[1] for d in flowrate_data], 
                    yerr=[[d[1]-d[0] for d in flowrate_data], 
                          [d[2]-d[1] for d in flowrate_data]], 
                    fmt='none', ecolor='black', capsize=3, alpha=0.6)
        ax1.set_title('Flowrate (L/min)', fontweight='bold', fontsize=9)
        ax1.set_xticks(x)
        ax1.set_xticklabels(types, rotation=45, ha='right', fontsize=7)
        ax1.grid(axis='y', alpha=0.3)
        
        # Pressure plot
        ax2.bar(x, [d[1] for d in pressure_data], width, color='#FBBF24', alpha=0.8)
        ax2.errorbar(x, [d[1] for d in pressure_data], 
                    yerr=[[d[1]-d[0] for d in pressure_data], 
                          [d[2]-d[1] for d in pressure_data]], 
                    fmt='none', ecolor='black', capsize=3, alpha=0.6)
        ax2.set_title('Pressure (bar)', fontweight='bold', fontsize=9)
        ax2.set_xticks(x)
        ax2.set_xticklabels(types, rotation=45, ha='right', fontsize=7)
        ax2.grid(axis='y', alpha=0.3)
        
        # Temperature plot
        ax3.bar(x, [d[1] for d in temp_data], width, color='#FF6B6B', alpha=0.8)
        ax3.errorbar(x, [d[1] for d in temp_data], 
                    yerr=[[d[1]-d[0] for d in temp_data], 
                          [d[2]-d[1] for d in temp_data]], 
                    fmt='none', ecolor='black', capsize=3, alpha=0.6)
        ax3.set_title('Temperature (°C)', fontweight='bold', fontsize=9)
        ax3.set_xticks(x)
        ax3.set_xticklabels(types, rotation=45, ha='right', fontsize=7)
        ax3.grid(axis='y', alpha=0.3)
        
        fig.suptitle('Parameter Range Analysis (Min-Avg-Max)', fontweight='bold', fontsize=11)
        plt.tight_layout()
        
        # Save to buffer
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        # Create ReportLab Image
        img = Image(img_buffer, width=6.5*inch, height=2.5*inch)
        return img
        
    except Exception as e:
        print(f"Error creating comparison chart: {e}")
        return None


def create_box_plot(statistics):
    """Create box plots showing parameter distribution across equipment types."""
    try:
        by_type = statistics.get('by_type', {})
        
        if not by_type:
            return None
        
        types = list(by_type.keys())
        
        # Prepare data for box plots
        flowrate_data = [[by_type[t]['flowrate']['min'], 
                         by_type[t]['flowrate']['avg'], 
                         by_type[t]['flowrate']['max']] for t in types]
        
        pressure_data = [[by_type[t]['pressure']['min'], 
                         by_type[t]['pressure']['avg'], 
                         by_type[t]['pressure']['max']] for t in types]
        
        temp_data = [[by_type[t]['temperature']['min'], 
                     by_type[t]['temperature']['avg'], 
                     by_type[t]['temperature']['max']] for t in types]
        
        # Create figure with 3 subplots
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 3.5))
        
        # Flowrate box plot
        bp1 = ax1.boxplot(flowrate_data, labels=types, patch_artist=True)
        for patch in bp1['boxes']:
            patch.set_facecolor('#0EA5E9')
            patch.set_alpha(0.6)
        ax1.set_title('Flowrate Distribution', fontweight='bold', fontsize=10)
        ax1.set_ylabel('L/min', fontweight='bold', fontsize=9)
        ax1.tick_params(axis='x', rotation=45, labelsize=7)
        ax1.grid(axis='y', alpha=0.3)
        
        # Pressure box plot
        bp2 = ax2.boxplot(pressure_data, labels=types, patch_artist=True)
        for patch in bp2['boxes']:
            patch.set_facecolor('#FBBF24')
            patch.set_alpha(0.6)
        ax2.set_title('Pressure Distribution', fontweight='bold', fontsize=10)
        ax2.set_ylabel('bar', fontweight='bold', fontsize=9)
        ax2.tick_params(axis='x', rotation=45, labelsize=7)
        ax2.grid(axis='y', alpha=0.3)
        
        # Temperature box plot
        bp3 = ax3.boxplot(temp_data, labels=types, patch_artist=True)
        for patch in bp3['boxes']:
            patch.set_facecolor('#FF6B6B')
            patch.set_alpha(0.6)
        ax3.set_title('Temperature Distribution', fontweight='bold', fontsize=10)
        ax3.set_ylabel('°C', fontweight='bold', fontsize=9)
        ax3.tick_params(axis='x', rotation=45, labelsize=7)
        ax3.grid(axis='y', alpha=0.3)
        
        fig.suptitle('Parameter Distribution Analysis', fontweight='bold', fontsize=12)
        plt.tight_layout()
        
        # Save to buffer
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        # Create ReportLab Image
        img = Image(img_buffer, width=6.5*inch, height=2.8*inch)
        return img
        
    except Exception as e:
        print(f"Error creating box plot: {e}")
        return None


def create_scatter_plot(statistics):
    """Create scatter plots showing correlations between parameters."""
    try:
        by_type = statistics.get('by_type', {})
        
        if not by_type:
            return None
        
        types = list(by_type.keys())
        
        # Prepare data
        flowrates = [by_type[t]['flowrate']['avg'] for t in types]
        pressures = [by_type[t]['pressure']['avg'] for t in types]
        temps = [by_type[t]['temperature']['avg'] for t in types]
        
        # Create figure with 3 scatter plots
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 3))
        
        colors_list = ['#FF6B1A', '#D94452', '#7B2C9E', '#0EA5E9', '#10B981', 
                      '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4', '#84CC16']
        
        # Flowrate vs Pressure
        for i, (f, p, t_type) in enumerate(zip(flowrates, pressures, types)):
            ax1.scatter(f, p, s=100, color=colors_list[i % len(colors_list)], 
                       alpha=0.7, edgecolors='black', linewidth=1)
        ax1.set_xlabel('Flowrate (L/min)', fontweight='bold', fontsize=9)
        ax1.set_ylabel('Pressure (bar)', fontweight='bold', fontsize=9)
        ax1.set_title('Flowrate vs Pressure', fontweight='bold', fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # Flowrate vs Temperature
        for i, (f, t, t_type) in enumerate(zip(flowrates, temps, types)):
            ax2.scatter(f, t, s=100, color=colors_list[i % len(colors_list)], 
                       alpha=0.7, edgecolors='black', linewidth=1)
        ax2.set_xlabel('Flowrate (L/min)', fontweight='bold', fontsize=9)
        ax2.set_ylabel('Temperature (°C)', fontweight='bold', fontsize=9)
        ax2.set_title('Flowrate vs Temperature', fontweight='bold', fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        # Pressure vs Temperature
        for i, (p, t, t_type) in enumerate(zip(pressures, temps, types)):
            ax3.scatter(p, t, s=100, color=colors_list[i % len(colors_list)], 
                       alpha=0.7, edgecolors='black', linewidth=1, label=t_type)
        ax3.set_xlabel('Pressure (bar)', fontweight='bold', fontsize=9)
        ax3.set_ylabel('Temperature (°C)', fontweight='bold', fontsize=9)
        ax3.set_title('Pressure vs Temperature', fontweight='bold', fontsize=10)
        ax3.grid(True, alpha=0.3)
        ax3.legend(fontsize=6, loc='best', ncol=2)
        
        fig.suptitle('Parameter Correlation Analysis', fontweight='bold', fontsize=12)
        plt.tight_layout()
        
        # Save to buffer
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        # Create ReportLab Image
        img = Image(img_buffer, width=6.5*inch, height=2.5*inch)
        return img
        
    except Exception as e:
        print(f"Error creating scatter plot: {e}")
        return None


def create_heatmap(statistics):
    """Create a heatmap showing average values for each equipment type."""
    try:
        by_type = statistics.get('by_type', {})
        
        if not by_type:
            return None
        
        types = list(by_type.keys())
        
        # Prepare data matrix (equipment types x parameters)
        data_matrix = []
        for t in types:
            data_matrix.append([
                by_type[t]['flowrate']['avg'],
                by_type[t]['pressure']['avg'],
                by_type[t]['temperature']['avg']
            ])
        
        data_matrix = np.array(data_matrix)
        
        # Normalize data for better visualization
        data_normalized = (data_matrix - data_matrix.min(axis=0)) / (data_matrix.max(axis=0) - data_matrix.min(axis=0))
        
        # Create figure
        fig, ax = plt.subplots(figsize=(5, 4))
        
        im = ax.imshow(data_normalized, cmap='YlOrRd', aspect='auto')
        
        # Set ticks and labels
        ax.set_xticks(np.arange(3))
        ax.set_yticks(np.arange(len(types)))
        ax.set_xticklabels(['Flowrate', 'Pressure', 'Temperature'], fontsize=9, fontweight='bold')
        ax.set_yticklabels(types, fontsize=8)
        
        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Normalized Value', rotation=270, labelpad=15, fontweight='bold', fontsize=9)
        
        # Add text annotations with actual values
        for i in range(len(types)):
            for j in range(3):
                text = ax.text(j, i, f'{data_matrix[i, j]:.1f}',
                             ha="center", va="center", color="black", fontsize=7, fontweight='bold')
        
        ax.set_title('Equipment Parameter Heatmap', fontweight='bold', fontsize=12, pad=10)
        plt.tight_layout()
        
        # Save to buffer
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        # Create ReportLab Image
        img = Image(img_buffer, width=4.5*inch, height=3.5*inch)
        return img
        
    except Exception as e:
        print(f"Error creating heatmap: {e}")
        return None


def create_radar_chart(statistics):
    """Create a radar chart comparing equipment types across parameters."""
    try:
        by_type = statistics.get('by_type', {})
        
        if not by_type or len(by_type) > 6:  # Limit to 6 types for clarity
            return None
        
        types = list(by_type.keys())[:6]
        
        # Parameters to compare (normalized)
        categories = ['Flowrate', 'Pressure', 'Temperature']
        
        # Prepare data and normalize
        all_data = []
        for t in types:
            all_data.append([
                by_type[t]['flowrate']['avg'],
                by_type[t]['pressure']['avg'],
                by_type[t]['temperature']['avg']
            ])
        
        all_data = np.array(all_data)
        # Normalize to 0-100 scale
        data_normalized = (all_data - all_data.min(axis=0)) / (all_data.max(axis=0) - all_data.min(axis=0)) * 100
        
        # Create figure
        fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(projection='polar'))
        
        # Angles for each parameter
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        colors_list = ['#0EA5E9', '#FBBF24', '#FF6B6B', '#10B981', '#8B5CF6', '#F59E0B']
        
        # Plot each equipment type
        for i, (t, data) in enumerate(zip(types, data_normalized)):
            values = data.tolist()
            values += values[:1]  # Complete the circle
            ax.plot(angles, values, 'o-', linewidth=2, label=t, color=colors_list[i], alpha=0.7)
            ax.fill(angles, values, alpha=0.15, color=colors_list[i])
        
        # Set labels and title
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=10, fontweight='bold')
        ax.set_ylim(0, 100)
        ax.set_yticks([25, 50, 75, 100])
        ax.set_yticklabels(['25', '50', '75', '100'], fontsize=8)
        ax.grid(True, alpha=0.3)
        
        ax.set_title('Equipment Performance Radar Chart', fontweight='bold', fontsize=12, pad=20)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=8)
        
        plt.tight_layout()
        
        # Save to buffer
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        # Create ReportLab Image
        img = Image(img_buffer, width=4.5*inch, height=4.5*inch)
        return img
        
    except Exception as e:
        print(f"Error creating radar chart: {e}")
        return None


def create_horizontal_ranking_chart(statistics):
    """Create horizontal bar chart showing equipment ranked by average flowrate."""
    try:
        by_type = statistics.get('by_type', {})
        
        if not by_type:
            return None
        
        # Sort by flowrate descending
        sorted_items = sorted(by_type.items(), key=lambda x: x[1]['flowrate']['avg'], reverse=True)
        types = [item[0] for item in sorted_items]
        flowrates = [item[1]['flowrate']['avg'] for item in sorted_items]
        
        # Create horizontal bar chart
        fig, ax = plt.subplots(figsize=(6, 4))
        
        y_pos = np.arange(len(types))
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(types)))
        
        bars = ax.barh(y_pos, flowrates, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars, flowrates)):
            ax.text(val + 2, i, f'{val:.1f}', va='center', fontweight='bold', fontsize=9)
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(types, fontsize=9)
        ax.invert_yaxis()  # Highest on top
        ax.set_xlabel('Average Flowrate (L/min)', fontweight='bold', fontsize=10)
        ax.set_title('Equipment Ranked by Flowrate Performance', fontweight='bold', fontsize=12)
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        
        # Save to buffer
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        img = Image(img_buffer, width=5*inch, height=3.5*inch)
        return img
        
    except Exception as e:
        print(f"Error creating ranking chart: {e}")
        return None


def create_line_chart(statistics):
    """Create line chart showing parameter trends across equipment types."""
    try:
        by_type = statistics.get('by_type', {})
        
        if not by_type:
            return None
        
        # Sort types alphabetically for consistent ordering
        types = sorted(by_type.keys())
        
        flowrates = [by_type[t]['flowrate']['avg'] for t in types]
        pressures = [by_type[t]['pressure']['avg'] for t in types]
        temps = [by_type[t]['temperature']['avg'] for t in types]
        
        # Create line chart
        fig, ax = plt.subplots(figsize=(6, 4))
        
        x = np.arange(len(types))
        
        # Plot lines with markers
        ax.plot(x, flowrates, marker='o', linewidth=2.5, markersize=8, 
               label='Flowrate', color='#0EA5E9', markerfacecolor='white', markeredgewidth=2)
        ax.plot(x, pressures, marker='s', linewidth=2.5, markersize=8, 
               label='Pressure', color='#FBBF24', markerfacecolor='white', markeredgewidth=2)
        ax.plot(x, temps, marker='^', linewidth=2.5, markersize=8, 
               label='Temperature', color='#FF6B6B', markerfacecolor='white', markeredgewidth=2)
        
        ax.set_xlabel('Equipment Type', fontweight='bold', fontsize=10)
        ax.set_ylabel('Parameter Value', fontweight='bold', fontsize=10)
        ax.set_title('Parameter Trends Across Equipment Types', fontweight='bold', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(types, rotation=45, ha='right', fontsize=9)
        ax.legend(fontsize=9, loc='best')
        ax.grid(True, alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        # Save to buffer
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        img = Image(img_buffer, width=5*inch, height=3.3*inch)
        return img
        
    except Exception as e:
        print(f"Error creating line chart: {e}")
        return None


def create_area_chart(statistics):
    """Create stacked area chart showing cumulative parameter values."""
    try:
        by_type = statistics.get('by_type', {})
        
        if not by_type:
            return None
        
        # Sort by total parameter sum
        sorted_items = sorted(by_type.items(), 
                            key=lambda x: x[1]['flowrate']['avg'] + 
                                        x[1]['pressure']['avg'] + 
                                        x[1]['temperature']['avg'])
        
        types = [item[0] for item in sorted_items]
        flowrates = [item[1]['flowrate']['avg'] for item in sorted_items]
        pressures = [item[1]['pressure']['avg'] * 20 for item in sorted_items]  # Scale for visibility
        temps = [item[1]['temperature']['avg'] for item in sorted_items]
        
        # Create stacked area chart
        fig, ax = plt.subplots(figsize=(6, 4))
        
        x = np.arange(len(types))
        
        ax.fill_between(x, 0, flowrates, label='Flowrate', color='#0EA5E9', alpha=0.6)
        ax.fill_between(x, flowrates, np.array(flowrates) + np.array(pressures), 
                       label='Pressure (×20)', color='#FBBF24', alpha=0.6)
        ax.fill_between(x, np.array(flowrates) + np.array(pressures), 
                       np.array(flowrates) + np.array(pressures) + np.array(temps),
                       label='Temperature', color='#FF6B6B', alpha=0.6)
        
        ax.set_xlabel('Equipment Type (sorted by total)', fontweight='bold', fontsize=10)
        ax.set_ylabel('Cumulative Parameter Values', fontweight='bold', fontsize=10)
        ax.set_title('Cumulative Parameter Analysis', fontweight='bold', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(types, rotation=45, ha='right', fontsize=8)
        ax.legend(fontsize=9, loc='upper left')
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        
        # Save to buffer
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        img = Image(img_buffer, width=5*inch, height=3.3*inch)
        return img
        
    except Exception as e:
        print(f"Error creating area chart: {e}")
        return None


def create_violin_plot(statistics):
    """Create violin plot showing parameter distribution shapes."""
    try:
        by_type = statistics.get('by_type', {})
        
        if not by_type:
            return None
        
        types = list(by_type.keys())
        
        # Create synthetic distribution data from min/avg/max
        flowrate_data = []
        pressure_data = []
        temp_data = []
        
        for t in types:
            # Generate distribution approximation
            f_min, f_avg, f_max = (by_type[t]['flowrate']['min'], 
                                   by_type[t]['flowrate']['avg'], 
                                   by_type[t]['flowrate']['max'])
            flowrate_data.append(np.random.normal(f_avg, (f_max - f_min) / 4, 50))
            
            p_min, p_avg, p_max = (by_type[t]['pressure']['min'], 
                                   by_type[t]['pressure']['avg'], 
                                   by_type[t]['pressure']['max'])
            pressure_data.append(np.random.normal(p_avg, (p_max - p_min) / 4, 50))
            
            t_min, t_avg, t_max = (by_type[t]['temperature']['min'], 
                                   by_type[t]['temperature']['avg'], 
                                   by_type[t]['temperature']['max'])
            temp_data.append(np.random.normal(t_avg, (t_max - t_min) / 4, 50))
        
        # Create figure with 3 subplots
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 3.5))
        
        # Flowrate violin
        parts1 = ax1.violinplot(flowrate_data, positions=range(len(types)), 
                               showmeans=True, showmedians=True)
        for pc in parts1['bodies']:
            pc.set_facecolor('#0EA5E9')
            pc.set_alpha(0.6)
        ax1.set_title('Flowrate Distribution', fontweight='bold', fontsize=10)
        ax1.set_ylabel('L/min', fontweight='bold', fontsize=9)
        ax1.set_xticks(range(len(types)))
        ax1.set_xticklabels(types, rotation=45, ha='right', fontsize=7)
        ax1.grid(axis='y', alpha=0.3)
        
        # Pressure violin
        parts2 = ax2.violinplot(pressure_data, positions=range(len(types)), 
                               showmeans=True, showmedians=True)
        for pc in parts2['bodies']:
            pc.set_facecolor('#FBBF24')
            pc.set_alpha(0.6)
        ax2.set_title('Pressure Distribution', fontweight='bold', fontsize=10)
        ax2.set_ylabel('bar', fontweight='bold', fontsize=9)
        ax2.set_xticks(range(len(types)))
        ax2.set_xticklabels(types, rotation=45, ha='right', fontsize=7)
        ax2.grid(axis='y', alpha=0.3)
        
        # Temperature violin
        parts3 = ax3.violinplot(temp_data, positions=range(len(types)), 
                               showmeans=True, showmedians=True)
        for pc in parts3['bodies']:
            pc.set_facecolor('#FF6B6B')
            pc.set_alpha(0.6)
        ax3.set_title('Temperature Distribution', fontweight='bold', fontsize=10)
        ax3.set_ylabel('°C', fontweight='bold', fontsize=9)
        ax3.set_xticks(range(len(types)))
        ax3.set_xticklabels(types, rotation=45, ha='right', fontsize=7)
        ax3.grid(axis='y', alpha=0.3)
        
        fig.suptitle('Distribution Shape Analysis (Violin Plot)', fontweight='bold', fontsize=12)
        plt.tight_layout()
        
        # Save to buffer
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        img = Image(img_buffer, width=6.5*inch, height=2.8*inch)
        return img
        
    except Exception as e:
        print(f"Error creating violin plot: {e}")
        return None

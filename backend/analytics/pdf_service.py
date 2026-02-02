from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime
from .pdf_charts import create_bar_chart, create_pie_chart


class PDFReportService:
    """
    Service to generate PDF reports for CSV dataset statistics.
    """
    
    def __init__(self, dataset):
        """
        Initialize with a CSVDataset instance.
        
        Args:
            dataset: CSVDataset model instance
        """
        self.dataset = dataset
        self.buffer = BytesIO()
        self.styles = getSampleStyleSheet()
        
    def generate(self):
        """
        Generate PDF report and return bytes.
        
        Returns:
            BytesIO: PDF file buffer
        """
        # Create PDF document
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build document elements
        elements = []
        
        # Define section heading style once
        heading_style = ParagraphStyle(
            'SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c5aa0'),
            spaceAfter=12,
            spaceBefore=6,
            fontName='Helvetica-Bold'
        )
        
        # PAGE 1: Title and Dataset Information
        elements.append(self._create_title())
        elements.append(Spacer(1, 20))
        elements.append(self._create_dataset_info())
        elements.append(PageBreak())
        
        # PAGE 2: Summary Statistics
        if self.dataset.statistics:
            elements.append(Paragraph("Summary Statistics", heading_style))
            elements.append(Spacer(1, 12))
            elements.append(self._create_overall_stats())
            elements.append(PageBreak())
            
            # PAGE 3: Distribution & Composition
            elements.append(Paragraph("Distribution & Composition Analysis", heading_style))
            elements.append(Spacer(1, 12))
            
            # Stacked bar chart - composition
            bar_chart = create_bar_chart(self.dataset.statistics)
            if bar_chart:
                elements.append(bar_chart)
                elements.append(Spacer(1, 20))
            
            # Donut chart - ranked distribution
            pie_chart = create_pie_chart(self.dataset.statistics)
            if pie_chart:
                elements.append(pie_chart)
            
            elements.append(PageBreak())
            
            # PAGE 4: Trend & Performance Ranking
            elements.append(Paragraph("Trend & Performance Ranking", heading_style))
            elements.append(Spacer(1, 12))
            
            # Line chart - trends
            from .pdf_charts import create_line_chart, create_horizontal_ranking_chart
            line_chart = create_line_chart(self.dataset.statistics)
            if line_chart:
                elements.append(line_chart)
                elements.append(Spacer(1, 20))
            
            # Horizontal ranking chart
            ranking_chart = create_horizontal_ranking_chart(self.dataset.statistics)
            if ranking_chart:
                elements.append(ranking_chart)
            
            elements.append(PageBreak())
            
            # PAGE 5: Parameter Range Analysis
            elements.append(Paragraph("Parameter Range & Variability", heading_style))
            elements.append(Spacer(1, 12))
            
            # Comparison chart with error bars
            from .pdf_charts import create_comparison_chart, create_violin_plot
            comparison_chart = create_comparison_chart(self.dataset.statistics)
            if comparison_chart:
                elements.append(comparison_chart)
                elements.append(Spacer(1, 20))
            
            # Violin plot - distribution shapes
            violin_plot = create_violin_plot(self.dataset.statistics)
            if violin_plot:
                elements.append(violin_plot)
            
            elements.append(PageBreak())
            
            # PAGE 6: Correlation & Cumulative Analysis
            elements.append(Paragraph("Correlation & Cumulative Analysis", heading_style))
            elements.append(Spacer(1, 12))
            
            # Scatter plot - correlations
            from .pdf_charts import create_scatter_plot, create_area_chart
            scatter_plot = create_scatter_plot(self.dataset.statistics)
            if scatter_plot:
                elements.append(scatter_plot)
                elements.append(Spacer(1, 20))
            
            # Area chart - cumulative
            area_chart = create_area_chart(self.dataset.statistics)
            if area_chart:
                elements.append(area_chart)
            
            elements.append(PageBreak())
            
            # PAGE 7: Multi-Dimensional Comparison
            elements.append(Paragraph("Multi-Dimensional Performance View", heading_style))
            elements.append(Spacer(1, 12))
            
            # Heatmap - intensity matrix
            from .pdf_charts import create_heatmap, create_radar_chart
            heatmap = create_heatmap(self.dataset.statistics)
            if heatmap:
                elements.append(heatmap)
                elements.append(Spacer(1, 20))
            
            # Radar chart - performance comparison
            radar_chart = create_radar_chart(self.dataset.statistics)
            if radar_chart:
                elements.append(radar_chart)
            
            elements.append(PageBreak())
            
            # PAGE 8: Detailed Equipment Breakdown
            elements.append(Paragraph("Detailed Equipment Breakdown", heading_style))
            elements.append(Spacer(1, 12))
            elements.append(self._create_type_breakdown())
            elements.append(PageBreak())
            
            # PAGE 8: Statistical Insights
            elements.append(Paragraph("Statistical Insights & Analysis", heading_style))
            elements.append(Spacer(1, 12))
            elements.append(self._create_insights())
            elements.append(Spacer(1, 20))
            elements.append(self._create_statistical_summary())
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF bytes
        pdf_bytes = self.buffer.getvalue()
        self.buffer.close()
        
        return pdf_bytes
    
    def _create_title(self):
        """Create title section."""
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        return Paragraph("Equipment Parameter Analysis Report", title_style)
    
    def _create_dataset_info(self):
        """Create dataset information section."""
        heading_style = ParagraphStyle(
            'SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2c5aa0'),
            spaceAfter=10
        )
        
        # Calculate equipment types count from statistics
        equipment_types_count = 0
        if self.dataset.statistics and self.dataset.statistics.get('by_type'):
            equipment_types_count = len(self.dataset.statistics.get('by_type', {}))
        
        info_data = [
            ['Dataset Information', ''],
            ['File Name:', self.dataset.file_name],
            ['Uploaded By:', self.dataset.uploaded_by.username],
            ['Upload Date:', self.dataset.uploaded_at.strftime('%B %d, %Y at %I:%M %p')],
            ['Equipment Types:', str(equipment_types_count)],
            ['Status:', self.dataset.status.capitalize()],
        ]
        
        table = Table(info_data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#e8f0f8')),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        return table
    
    def _create_overall_stats(self):
        """Create overall statistics section with calculated metrics."""
        stats = self.dataset.statistics
        overall = stats.get('overall_averages', {})
        by_type = stats.get('by_type', {})
        
        # Calculate additional metrics from backend data
        total_equipment_count = sum(type_data['count'] for type_data in by_type.values())
        equipment_types_count = len(by_type)
        
        # Calculate min and max values across all equipment
        all_flowrates = [type_data['flowrate']['avg'] for type_data in by_type.values()]
        all_pressures = [type_data['pressure']['avg'] for type_data in by_type.values()]
        all_temps = [type_data['temperature']['avg'] for type_data in by_type.values()]
        
        data = [
            ['Overall Dataset Metrics'],
            ['Metric', 'Value'],
            ['Total Equipment Count', str(total_equipment_count)],
            ['Equipment Types', str(equipment_types_count)],
            ['', ''],
            ['Average Parameters'],
            ['Average Flowrate', f"{overall.get('flowrate', 0):.2f} L/min"],
            ['Average Pressure', f"{overall.get('pressure', 0):.2f} bar"],
            ['Average Temperature', f"{overall.get('temperature', 0):.2f} °C"],
            ['', ''],
            ['Parameter Ranges'],
            ['Flowrate Range', f"{min(all_flowrates):.2f} - {max(all_flowrates):.2f} L/min"],
            ['Pressure Range', f"{min(all_pressures):.2f} - {max(all_pressures):.2f} bar"],
            ['Temperature Range', f"{min(all_temps):.2f} - {max(all_temps):.2f} °C"],
        ]
        
        table = Table(data, colWidths=[2.5*inch, 3.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('SPAN', (0, 0), (-1, 0)),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Section headers
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#4a7ba7')),
            ('BACKGROUND', (0, 5), (-1, 5), colors.HexColor('#4a7ba7')),
            ('BACKGROUND', (0, 10), (-1, 10), colors.HexColor('#4a7ba7')),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.whitesmoke),
            ('TEXTCOLOR', (0, 5), (-1, 5), colors.whitesmoke),
            ('TEXTCOLOR', (0, 10), (-1, 10), colors.whitesmoke),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('FONTNAME', (0, 5), (-1, 5), 'Helvetica-Bold'),
            ('FONTNAME', (0, 10), (-1, 10), 'Helvetica-Bold'),
            ('SPAN', (0, 1), (-1, 1)),
            ('SPAN', (0, 5), (-1, 5)),
            ('SPAN', (0, 10), (-1, 10)),
            
            # Metric labels
            ('BACKGROUND', (0, 2), (0, 3), colors.HexColor('#e8f0f8')),
            ('BACKGROUND', (0, 6), (0, 8), colors.HexColor('#e8f0f8')),
            ('BACKGROUND', (0, 11), (0, 13), colors.HexColor('#e8f0f8')),
            ('FONTNAME', (0, 2), (0, 13), 'Helvetica-Bold'),
            
            ('ALIGN', (1, 2), (1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        
        return table
    
    def _create_type_breakdown(self):
        """Create equipment type breakdown section."""
        stats = self.dataset.statistics
        by_type = stats.get('by_type', {})
        
        # Header
        data = [
            ['Equipment Type Breakdown'],
            ['Type', 'Count', 'Avg Flowrate', 'Avg Pressure', 'Avg Temp (°C)']
        ]
        
        # Add each equipment type
        for eq_type, type_stats in sorted(by_type.items()):
            data.append([
                eq_type,
                str(type_stats['count']),
                f"{type_stats['flowrate']['avg']:.2f}",
                f"{type_stats['pressure']['avg']:.2f}",
                f"{type_stats['temperature']['avg']:.2f}"
            ])
        
        table = Table(data, colWidths=[2*inch, 0.8*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('SPAN', (0, 0), (-1, 0)),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#4a7ba7')),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.whitesmoke),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('ALIGN', (0, 1), (-1, 1), 'CENTER'),
            ('FONTSIZE', (0, 1), (-1, 1), 10),
            ('ALIGN', (1, 2), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 2), (0, -1), 'LEFT'),
            ('ROWBACKGROUNDS', (0, 2), (-1, -1), [colors.white, colors.HexColor('#f8f8f8')]),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        
        return table
    
    def _create_insights(self):
        """Create data insights section."""
        stats = self.dataset.statistics
        by_type = stats.get('by_type', {})
        overall = stats.get('overall_averages', {})
        
        # Find highest and lowest values
        if not by_type:
            return Paragraph("No insights available.", self.styles['Normal'])
        
        # Find equipment with highest flowrate
        highest_flowrate = max(by_type.items(), key=lambda x: x[1]['flowrate']['avg'])
        lowest_flowrate = min(by_type.items(), key=lambda x: x[1]['flowrate']['avg'])
        
        # Find equipment with highest pressure
        highest_pressure = max(by_type.items(), key=lambda x: x[1]['pressure']['avg'])
        lowest_pressure = min(by_type.items(), key=lambda x: x[1]['pressure']['avg'])
        
        # Find equipment with highest temperature
        highest_temp = max(by_type.items(), key=lambda x: x[1]['temperature']['avg'])
        lowest_temp = min(by_type.items(), key=lambda x: x[1]['temperature']['avg'])
        
        insight_style = ParagraphStyle(
            'Insight',
            parent=self.styles['Normal'],
            fontSize=10,
            leading=14,
            leftIndent=20,
            bulletIndent=10,
            spaceAfter=8
        )
        
        insights = []
        insights.append(Paragraph(
            f"• <b>Highest Flowrate:</b> {highest_flowrate[0]} ({highest_flowrate[1]['flowrate']['avg']:.2f} L/min)",
            insight_style
        ))
        insights.append(Paragraph(
            f"• <b>Lowest Flowrate:</b> {lowest_flowrate[0]} ({lowest_flowrate[1]['flowrate']['avg']:.2f} L/min)",
            insight_style
        ))
        insights.append(Spacer(1, 6))
        insights.append(Paragraph(
            f"• <b>Highest Pressure:</b> {highest_pressure[0]} ({highest_pressure[1]['pressure']['avg']:.2f} bar)",
            insight_style
        ))
        insights.append(Paragraph(
            f"• <b>Lowest Pressure:</b> {lowest_pressure[0]} ({lowest_pressure[1]['pressure']['avg']:.2f} bar)",
            insight_style
        ))
        insights.append(Spacer(1, 6))
        insights.append(Paragraph(
            f"• <b>Highest Temperature:</b> {highest_temp[0]} ({highest_temp[1]['temperature']['avg']:.2f} °C)",
            insight_style
        ))
        insights.append(Paragraph(
            f"• <b>Lowest Temperature:</b> {lowest_temp[0]} ({lowest_temp[1]['temperature']['avg']:.2f} °C)",
            insight_style
        ))
        insights.append(Spacer(1, 6))
        insights.append(Paragraph(
            f"• <b>Total Equipment Types Analyzed:</b> {len(by_type)}",
            insight_style
        ))
        
        # Create a container for insights
        from reportlab.platypus import KeepTogether
        return KeepTogether(insights)
    
    def _create_statistical_summary(self):
        """Create statistical summary with variance and distribution info."""
        stats = self.dataset.statistics
        by_type = stats.get('by_type', {})
        
        if not by_type:
            return Paragraph("No statistical data available.", self.styles['Normal'])
        
        # Calculate coefficient of variation for each parameter
        flowrate_values = [type_data['flowrate']['avg'] for type_data in by_type.values()]
        pressure_values = [type_data['pressure']['avg'] for type_data in by_type.values()]
        temp_values = [type_data['temperature']['avg'] for type_data in by_type.values()]
        
        import statistics
        
        flowrate_std = statistics.stdev(flowrate_values) if len(flowrate_values) > 1 else 0
        pressure_std = statistics.stdev(pressure_values) if len(pressure_values) > 1 else 0
        temp_std = statistics.stdev(temp_values) if len(temp_values) > 1 else 0
        
        flowrate_mean = statistics.mean(flowrate_values)
        pressure_mean = statistics.mean(pressure_values)
        temp_mean = statistics.mean(temp_values)
        
        data = [
            ['Statistical Distribution Analysis'],
            ['Parameter', 'Mean', 'Std Dev', 'Coefficient of Variation'],
            ['Flowrate', 
             f"{flowrate_mean:.2f} L/min", 
             f"{flowrate_std:.2f}",
             f"{(flowrate_std/flowrate_mean*100):.1f}%" if flowrate_mean > 0 else 'N/A'],
            ['Pressure', 
             f"{pressure_mean:.2f} bar", 
             f"{pressure_std:.2f}",
             f"{(pressure_std/pressure_mean*100):.1f}%" if pressure_mean > 0 else 'N/A'],
            ['Temperature', 
             f"{temp_mean:.2f} °C", 
             f"{temp_std:.2f}",
             f"{(temp_std/temp_mean*100):.1f}%" if temp_mean > 0 else 'N/A'],
        ]
        
        table = Table(data, colWidths=[1.5*inch, 1.5*inch, 1.2*inch, 1.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('SPAN', (0, 0), (-1, 0)),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#4a7ba7')),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.whitesmoke),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('ALIGN', (0, 1), (-1, 1), 'CENTER'),
            ('FONTSIZE', (0, 1), (-1, 1), 9),
            ('ALIGN', (1, 2), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 2), (0, -1), 'LEFT'),
            ('BACKGROUND', (0, 2), (0, -1), colors.HexColor('#e8f0f8')),
            ('FONTNAME', (0, 2), (0, -1), 'Helvetica-Bold'),
            ('ROWBACKGROUNDS', (1, 2), (-1, -1), [colors.white, colors.HexColor('#f8f8f8')]),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        
        return table

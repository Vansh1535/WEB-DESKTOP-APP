from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime


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
        
        # Add title
        elements.append(self._create_title())
        elements.append(Spacer(1, 12))
        
        # Add dataset info
        elements.append(self._create_dataset_info())
        elements.append(Spacer(1, 12))
        
        # Add overall statistics
        if self.dataset.statistics:
            elements.append(self._create_overall_stats())
            elements.append(Spacer(1, 12))
            
            # Add equipment type breakdown
            elements.append(self._create_type_breakdown())
        
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
        
        info_data = [
            ['Dataset Information', ''],
            ['File Name:', self.dataset.file_name],
            ['Uploaded By:', self.dataset.uploaded_by.username],
            ['Upload Date:', self.dataset.uploaded_at.strftime('%B %d, %Y at %I:%M %p')],
            ['Total Records:', str(self.dataset.row_count or 0)],
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
        """Create overall statistics section."""
        stats = self.dataset.statistics
        overall = stats.get('overall_averages', {})
        
        data = [
            ['Overall Statistics', '', '', ''],
            ['Metric', 'Average', 'Unit', ''],
            ['Flowrate', f"{overall.get('flowrate', 0):.2f}", 'Units', ''],
            ['Pressure', f"{overall.get('pressure', 0):.2f}", 'Units', ''],
            ['Temperature', f"{overall.get('temperature', 0):.2f}", '°C', ''],
            ['', '', '', ''],
            ['Total Equipment Count', str(stats.get('total_equipment_count', 0)), '', ''],
            ['Equipment Types', str(len(stats.get('by_type', {}))), '', ''],
        ]
        
        table = Table(data, colWidths=[2*inch, 1.5*inch, 1*inch, 1.5*inch])
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
            ('BACKGROUND', (0, 2), (0, 4), colors.HexColor('#e8f0f8')),
            ('ALIGN', (1, 2), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 6), (0, 7), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 6), (0, 7), colors.HexColor('#f0f0f0')),
            ('SPAN', (0, 6), (1, 6)),
            ('SPAN', (0, 7), (1, 7)),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
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

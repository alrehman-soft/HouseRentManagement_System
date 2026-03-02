# print_utils.py
from tkinter import messagebox
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import tempfile
import os
from datetime import datetime

def send_to_printer(tree, title="Huraira Enterprises \nHouse Rent Report", orientation="portrait"):
    
    try:
        # Create temporary PDF file
        temp_path = tempfile.mktemp(suffix=".pdf")
        # Set page size based on orientation
        if orientation == "landscape":
            page_size = landscape(letter)
        else:
            page_size = letter
        
        doc = SimpleDocTemplate(temp_path, pagesize=page_size)
        styles = getSampleStyleSheet()
        elements = []
        
        # Custom title style
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=16,
            alignment=1,  # Center
            spaceAfter=10,
            textColor=colors.HexColor('#1e3a8a')
        )
        
        # Title
        elements.append(Paragraph(title, title_style))
        
        # Date
        date_style = ParagraphStyle(
            'DateStyle',
            parent=styles['Normal'],
            fontSize=9,
            alignment=1,
            textColor=colors.gray
        )
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}", date_style))
        elements.append(Spacer(1, 15))
        
        # Get headers
        headers = [tree.heading(col)["text"] for col in tree["columns"]]
        
        # Get data
        data = [headers]
        for row_id in tree.get_children():
            row_values = tree.item(row_id)["values"]
            # Convert all values to string
            row_data = [str(val) if val is not None else "" for val in row_values]
            data.append(row_data)
        
        # Create table
        table = Table(data, repeatRows=1)
        
        # Table style
        table_style = TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            
            # Data rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ])
        
        # Add alternating row colors
        for i in range(1, len(data)):
            if i % 2 == 0:
                table_style.add('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f5f5f5'))
        
        table.setStyle(table_style)
        elements.append(table)
        
        # Build PDF
        doc.build(elements)
        
        # Open print dialog
        os.startfile(temp_path, "print")
        
    except Exception as e:
        messagebox.showerror("Print Error", f"Failed to print: {str(e)}")
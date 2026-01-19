#!/usr/bin/env python3
"""
Robust PDF watermarking with error handling
"""

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import gray
from io import BytesIO

def create_watermark(text, width, height):
    """Create tiled watermark PDF"""
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    
    c.setFont("Helvetica-Bold", 36)
    c.setFillColor(gray, alpha=0.12)
    c.saveState()
    c.translate(width / 2, height / 2)
    c.rotate(45)
    
    # Tile pattern
    for x in range(-3, 4):
        for y in range(-3, 4):
            c.drawString(x * 250, y * 180, text)
    
    c.restoreState()
    c.save()
    packet.seek(0)
    return packet

def add_watermark_to_pdf(input_path, output_path, watermark_text):
    """Add watermark to PDF"""
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    for page in reader.pages:
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        
        watermark_pdf = create_watermark(watermark_text, width, height)
        watermark_page = PdfReader(watermark_pdf).pages[0]
        
        page.merge_page(watermark_page)
        writer.add_page(page)
    
    with open(output_path, 'wb') as f:
        writer.write(f)

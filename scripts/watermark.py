#!/usr/bin/env python3
"""
Advanced PDF watermarking with tiled pattern
"""

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import gray
from io import BytesIO

def create_watermark(text, page_width, page_height):
    """Create a watermark PDF with tiled text pattern"""
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))
    
    c.setFont("Helvetica-Bold", 40)
    c.setFillColor(gray, alpha=0.15)
    c.saveState()
    
    # Center and rotate
    c.translate(page_width / 2, page_height / 2)
    c.rotate(45)
    
    # Tile watermark across page
    for x in range(-2, 3):
        for y in range(-2, 3):
            c.drawString(x * 300, y * 200, text)
    
    c.restoreState()
    c.save()
    
    packet.seek(0)
    return packet

def add_watermark_to_pdf(input_path, output_path, watermark_text):
    """Add watermark to every page of a PDF"""
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    for page in reader.pages:
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)
        
        watermark_pdf = create_watermark(watermark_text, page_width, page_height)
        watermark_page = PdfReader(watermark_pdf).pages[0]
        
        page.merge_page(watermark_page)
        writer.add_page(page)
    
    with open(output_path, 'wb') as f:
        writer.write(f)

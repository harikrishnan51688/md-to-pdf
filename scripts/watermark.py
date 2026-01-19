#!/usr/bin/env python3
"""
Advanced PDF watermarking utility
"""

import sys
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import gray
from io import BytesIO

def create_watermark_pdf(text, page_width, page_height):
    """Create watermark PDF with repeated text for coverage"""
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=(page_width, page_height))
    can.setFont('Helvetica-Bold', 40)
    can.setFillColor(gray, alpha=0.15)
    can.saveState()
    
    # Center and rotate
    can.translate(page_width / 2, page_height / 2)
    can.rotate(45)
    
    # Draw watermark pattern (5x5 grid)
    for i in range(-2, 3):
        for j in range(-2, 3):
            x = i * 300
            y = j * 200
            can.drawString(x, y, text)
    
    can.restoreState()
    can.save()
    packet.seek(0)
    return packet

def add_watermark(input_pdf, output_pdf, watermark_text):
    """Apply watermark to PDF"""
    print(f"  Adding watermark: {watermark_text}")
    
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    
    for page in reader.pages:
        # Get page dimensions
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        
        # Create and merge watermark
        watermark_packet = create_watermark_pdf(watermark_text, width, height)
        watermark_pdf = PdfReader(watermark_packet)
        page.merge_page(watermark_pdf.pages[0])
        writer.add_page(page)
    
    # Write output
    with open(output_pdf, 'wb') as f:
        writer.write(f)
    
    print(f"  ✓ Watermarked: {output_pdf}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python watermark.py <input.pdf> <output.pdf> <watermark_text>")
        sys.exit(1)
    
    add_watermark(sys.argv[1], sys.argv[2], sys.argv[3])
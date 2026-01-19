#!/usr/bin/env python3
"""
Optimized PDF generation script for GitHub Actions
"""

import os
import sys
import json
import subprocess
from datetime import datetime

def convert_md_to_pdf(md_file, pdf_file):
    """Convert markdown to PDF using pandoc"""
    cmd = [
        'pandoc', md_file,
        '-o', pdf_file,
        '--pdf-engine=xelatex',
        '-V', 'geometry:margin=1in',
        '-V', 'fontsize=11pt',
        '--toc',
        '--toc-depth=3'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def main():
    # Get files from environment or command line
    if len(sys.argv) > 1:
        files_json = sys.argv[1]
    else:
        files_json = os.environ.get('FILES_TO_PROCESS', '[]')
    
    try:
        files_to_process = json.loads(files_json)
    except:
        files_to_process = []
    
    if not files_to_process:
        print("No files to process")
        return
    
    print(f"Processing {len(files_to_process)} file(s)")
    
    for md_file in files_to_process:
        if os.path.exists(md_file):
            pdf_file = md_file.replace('.md', '.pdf')
            if convert_md_to_pdf(md_file, pdf_file):
                print(f"✓ Generated: {pdf_file}")
            else:
                print(f"✗ Failed: {md_file}")

if __name__ == "__main__":
    main()

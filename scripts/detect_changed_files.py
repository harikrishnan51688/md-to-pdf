#!/usr/bin/env python3
"""
Detect which markdown files need PDF generation
"""

import os
import sys
import json
from pathlib import Path

def get_changed_files():
    """Get list of changed .md files in doc/ directory"""
    try:
        # Get files changed in the last commit
        import subprocess
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD', '--', 'doc/**/*.md'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            files = [f.strip() for f in result.stdout.split('\n') if f.strip()]
            return files
    except:
        pass
    return []

def get_all_files():
    """Get all .md files in doc/ directory"""
    doc_path = Path('doc')
    return [str(p) for p in doc_path.rglob('*.md') if p.is_file()]

def main():
    event_name = os.environ.get('GITHUB_EVENT_NAME', '')
    scope = os.environ.get('INPUT_GENERATION_SCOPE', 'changed')
    specific_files = os.environ.get('INPUT_SPECIFIC_FILES', '')
    
    files_to_process = []
    
    # Manual trigger logic
    if event_name == 'workflow_dispatch':
        if scope == 'all':
            files_to_process = get_all_files()
        elif scope == 'specific' and specific_files:
            files_to_process = [f.strip() for f in specific_files.split(',') if f.strip()]
    else:
        # Automatic push trigger - only changed files
        files_to_process = get_changed_files()
    
    # Filter only existing files
    files_to_process = [f for f in files_to_process if os.path.isfile(f)]
    
    # Set output for GitHub Actions
    json_output = json.dumps(files_to_process)
    print(f"Files to process: {json_output}")
    
    # Write to environment file
    with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
        f.write(f"files={json_output}\n")
    
    return files_to_process

if __name__ == '__main__':
    files = main()
    sys.exit(0 if files else 0)  # Don't fail if no files

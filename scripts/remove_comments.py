#!/usr/bin/env python
"""
Script to remove comments from the TypeScript configuration file.

This script specifically targets JSDoc comments and regular comments,
producing a clean file without comments for easier parsing.
"""

import re
import sys
from pathlib import Path

# File paths
ROOT_DIR = Path(__file__).parent.parent.parent
TS_FILE = ROOT_DIR / "js-source" / "tailwind-merge-v3" / "src" / "lib" / "default-config.ts"
OUTPUT_FILE = ROOT_DIR / "js-source" / "tailwind-merge-v3" / "src" / "lib" / "parsed-config.ts"

def remove_comments(content):
    """
    Remove all comments from TypeScript content.
    
    Args:
        content: The TypeScript file content
        
    Returns:
        The content with all comments removed
    """
    # Remove multi-line JSDoc comments (/**...*/)
    content = re.sub(r'/\*\*[\s\S]*?\*/', '', content)
    
    # Remove multi-line regular comments (/*...*/)
    content = re.sub(r'/\*[\s\S]*?\*/', '', content)
    
    # Remove single-line comments (//....)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    
    # Remove empty lines completely
    content = re.sub(r'\n\s*\n', '\n', content)
    
    # Ensure the file doesn't start with empty lines
    content = content.lstrip()
    
    return content

def main():
    """Main function to remove comments from TypeScript file."""
    if not TS_FILE.exists():
        print(f"Error: TypeScript file not found at {TS_FILE}")
        sys.exit(1)
    
    # Read TypeScript file
    with open(TS_FILE, 'r') as f:
        ts_content = f.read()
    
    # Remove comments
    cleaned_content = remove_comments(ts_content)
    
    # Write cleaned file
    with open(OUTPUT_FILE, 'w') as f:
        f.write(cleaned_content)
    
    print(f"Comments removed. Output written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main() 
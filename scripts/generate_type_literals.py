#!/usr/bin/env python3
"""
Utility script to parse TypeScript types.ts and generate Python literal types.

Usage:
    python generate_type_literals.py path/to/types.ts output_file.py

This script extracts the DefaultThemeGroupIds and DefaultClassGroupIds from the
TypeScript file and generates equivalent Python literal type definitions.
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple


def extract_type_values(content: str, type_name: str) -> List[str]:
    """Extract values from a TypeScript type definition."""
    # Find the type definition block
    pattern = rf"export\s+type\s+{type_name}\s*=\s*(?:\n|.)+?(?=export|$)"
    match = re.search(pattern, content)
    if not match:
        return []
    
    type_block = match.group(0)
    
    # Extract individual values
    values = []
    value_pattern = r"\|\s*'([^']+)'"
    for value_match in re.finditer(value_pattern, type_block):
        values.append(value_match.group(1))
    
    return values


def generate_python_literal(values: List[str], name: str) -> str:
    """Generate a Python literal type definition from a list of values."""
    if not values:
        return f"{name} = Literal[]  # Empty literal - no values found"
    
    # Start with the opening
    lines = [f"{name} = Literal["]
    
    # Format values in groups of 5 per line
    current_line = "    "
    for i, value in enumerate(values):
        value_str = f"'{value}'"
        # Add comma if not the last value
        if i < len(values) - 1:
            value_str += ", "
            
        # If adding this would make the line too long, start a new line
        if len(current_line) + len(value_str) > 100:
            lines.append(current_line)
            current_line = "    " + value_str
        else:
            current_line += value_str
    
    # Add the last line if it has content
    if current_line.strip():
        lines.append(current_line)
    
    # Close the literal
    lines.append("]")
    
    return "\n".join(lines)


def main() -> None:
    """Main function to parse TypeScript and generate Python types."""
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} path/to/types.ts output_file.py")
        sys.exit(1)
        
    ts_file = Path(sys.argv[1])
    py_file = Path(sys.argv[2])
    
    if not ts_file.exists():
        print(f"Error: File {ts_file} not found")
        sys.exit(1)
    
    with open(ts_file, 'r') as f:
        content = f.read()
    
    theme_values = extract_type_values(content, "DefaultThemeGroupIds")
    class_values = extract_type_values(content, "DefaultClassGroupIds")
    
    if not theme_values:
        print("Warning: Could not extract DefaultThemeGroupIds")
    
    if not class_values:
        print("Warning: Could not extract DefaultClassGroupIds")
    
    py_content = f"""\"\"\"
Auto-generated literal type definitions for tailwind-merge.
Generated from {ts_file.name}
\"\"\"

from typing import Literal

# Theme group IDs from the original TypeScript implementation
{generate_python_literal(theme_values, "DefaultThemeGroupIds")}

# Class group IDs from the original TypeScript implementation
{generate_python_literal(class_values, "DefaultClassGroupIds")}
"""
    
    with open(py_file, 'w') as f:
        f.write(py_content)
    
    print(f"Generated {len(theme_values)} theme group IDs and {len(class_values)} class group IDs")
    print(f"Output written to {py_file}")


if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Convenience script to update the generated type literals.

This script runs the generate_type_literals.py script with the correct
file paths to update the generated_types.py file.
"""

import os
import subprocess
from pathlib import Path

def main():
    # Get the project root directory (parent of this script's directory)
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent

    # Source TypeScript file
    ts_file = project_root / "js-source" / "tailwind-merge-v3" / "src" / "lib" / "types.ts"
    
    # Destination Python file
    py_file = project_root / "tw_merge_py" / "lib" / "generated_types.py"
    
    # Generator script
    generator = script_dir / "generate_type_literals.py"
    
    # Check if source file exists
    if not ts_file.exists():
        print(f"Error: Source file not found: {ts_file}")
        print("Please make sure you have the TypeScript code in the correct location.")
        return 1
    
    # Run the generator
    cmd = [str(generator), str(ts_file), str(py_file)]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    
    print("\nDone! Now you can import these types from tw_merge_py.lib.generated_types")
    return 0

if __name__ == "__main__":
    exit(main()) 
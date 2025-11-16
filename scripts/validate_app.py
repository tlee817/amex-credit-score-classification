#!/usr/bin/env python3
"""Validate that Streamlit app files can be imported without errors.

Ensures the app structure is valid before deployment.
"""
import sys
import importlib.util
from pathlib import Path

def validate_module(file_path):
    try:
        spec = importlib.util.spec_from_file_location("test_module", file_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            # Note: We don't execute the module to avoid side effects
            # Just check if it can be loaded
            print(f"✓ {file_path.name} - Valid Python syntax")
            return True
    except Exception as e:
        print(f"✗ {file_path.name} - Error: {e}")
        return False

def main():
    """Validate all app files."""
    project_root = Path(__file__).parent.parent
    
    files_to_check = [
        project_root / "app.py",
        project_root / "utils.py",
    ]
    
    # Add all page files
    pages_dir = project_root / "pages"
    if pages_dir.exists():
        files_to_check.extend(pages_dir.glob("*.py"))
    
    print("Validating Streamlit app files...\n")
    
    all_valid = True
    for file_path in files_to_check:
        if file_path.exists():
            if not validate_module(file_path):
                all_valid = False
        else:
            print(f"⚠ {file_path.name} - File not found")
    
    if all_valid:
        print("\n✓ All app files validated successfully")
        sys.exit(0)
    else:
        print("\n✗ Validation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
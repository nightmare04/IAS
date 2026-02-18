#!/usr/bin/env python3
"""
Application launcher - ensures proper Python path setup.

Usage:
    python run.py    - Run the IAS application
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.main import main

if __name__ == "__main__":
    main()

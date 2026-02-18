"""
Application configuration module.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database configuration
DATABASE_PATH = os.getenv("IAS_DATABASE_PATH", str(BASE_DIR / "data" / "database.db"))
DATABASE_NAME = DATABASE_PATH

# Application settings
APP_NAME = "IAS - Inspection/Failures App"
APP_VERSION = "0.1.0"

# UI settings
DEFAULT_WINDOW_WIDTH = 1024
DEFAULT_WINDOW_HEIGHT = 768
FUSION_STYLE = "Fusion"

# Migration settings
MIGRATIONS_DIR = BASE_DIR / "migrations"

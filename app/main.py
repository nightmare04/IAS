"""
IAS Application - Main entry point.

Inspection/Failures App for aircraft maintenance tracking.
"""
import sys

from PyQt6.QtWidgets import QApplication

from app.config import APP_NAME, FUSION_STYLE
from app.database import run_migrations
from app.ui.windows.main_window import MainForm


def init_database() -> None:
    """Initialize database by running migrations."""
    run_migrations()


def main() -> int:
    """
    Application entry point.

    Returns:
        Exit code from QApplication
    """
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setStyle(FUSION_STYLE)

    # Initialize database
    init_database()

    # Create and show main window
    main_form = MainForm()
    main_form.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())

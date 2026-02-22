"""Custom buttons for IAS application."""
from typing import TYPE_CHECKING

from PyQt6.QtCore import QSize, pyqtSignal
from PyQt6.QtWidgets import QPushButton

if TYPE_CHECKING:
    from data.models import OsobBase, PlaneBase


class IASButton(QPushButton):
    """Styled button for IAS application."""

    def __init__(self, text: str = "", parent=None) -> None:
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                border-radius: 4px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)


class PlaneBtn(QPushButton):
    """Button representing an aircraft with status indicator."""

    open_signal = pyqtSignal(object)

    def __init__(self, plane: "PlaneBase", parent=None) -> None:
        super().__init__()
        self.plane = plane
        self.setText(str(plane.bort_number))
        self.setFixedSize(QSize(60, 40))
        self.setCheckable(False)
        self.clicked.connect(self.open_dialog)
        self.update_color()

    def open_dialog(self) -> None:
        """Emit open signal with this button."""
        self.open_signal.emit(self)

    def update_color(self) -> None:
        """Update button color based on failure status."""
        # Import here to avoid circular imports
        from data.models.failures import OtkazAgregateBase

        has_failures = (
            OtkazAgregateBase.select()
            .where(OtkazAgregateBase.plane == self.plane)
            .count()
            > 0
        )

        if has_failures:
            self.setStyleSheet("PlaneBtn{background-color: red;}")
        else:
            self.setStyleSheet("PlaneBtn{background-color: green;}")

class OsobBtn(IASButton):
    def __init__(self, osob:OsobBase, parent=None):
        super().__init__(osob.name, parent)
        self.osob = osob
        self.setCheckable(True)
        self.setChecked(False)
        self.toggled.connect(self.update_color)

    def update_color(self):
        if self.isChecked():
            self.setStyleSheet("OsobBtn{background-color: green;}")
        else:
            self.setStyleSheet("OsobBtn{background-color: red;}")
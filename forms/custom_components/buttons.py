from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QPushButton, QDialog

from data import PlaneBase
from forms.plane_ispravnost import PlaneIspravnost


class IASButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
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
    def __init__(self, plane: PlaneBase, parent=None):
        self.plane = plane
        super().__init__(self.plane.bort_number, parent)
        self.setFixedSize(QSize(60, 40))
        self.setCheckable(False)
        self.setStyleSheet("PlaneBtn{background-color: red;}"
                           "PlaneBtn:checked{background-color: green;}")
        self.clicked.connect(self.open_dialog)

    def open_dialog(self):
        dialog = PlaneIspravnost(self.plane)
        dialog.exec()

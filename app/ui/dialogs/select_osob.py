"""Dialog for selecting aircraft features."""
from typing import Any

from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QGroupBox,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from app.models.aircraft import PlaneBase
from app.models.osob import OsobBase, OsobPlaneBase


class SelectOsobDialog(QDialog):
    """Dialog for selecting features for an aircraft."""

    def __init__(self, plane: PlaneBase, parent: Any | None = None) -> None:
        super().__init__(parent)
        self.plane = plane
        self.setWindowTitle(f"Особенности самолета {plane.bort_number}")
        self.setModal(True)
        self.setMinimumSize(500, 400)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Info label
        info_label = QWidget()
        info_layout = QVBoxLayout(info_label)
        info_label.setLayout(info_layout)
        from PyQt6.QtWidgets import QLabel
        info_layout.addWidget(QLabel(f"Тип: {plane.plane_type.name}"))
        info_layout.addWidget(QLabel(f"Бортовой номер: {plane.bort_number}"))
        self.main_layout.addWidget(info_label)

        # Features group
        self.features_group = QGroupBox("Особенности")
        self.features_layout = QVBoxLayout()
        self.features_group.setLayout(self.features_layout)
        self.main_layout.addWidget(self.features_group)

        # Store checkboxes
        self.feature_checks: dict[int, QCheckBox] = {}

        # Load features
        self.load_features()

        # Buttons
        self.button_box = QDialogButtonBox()
        self.save_button = self.button_box.addButton("Сохранить", QDialogButtonBox.ButtonRole.AcceptRole)
        self.cancel_button = self.button_box.addButton("Отмена", QDialogButtonBox.ButtonRole.RejectRole)
        self.save_button.clicked.connect(self.save_selection)  # type: ignore
        self.cancel_button.clicked.connect(self.reject)  # type: ignore

        self.main_layout.addWidget(self.button_box)

    def load_features(self) -> None:
        """Load features for aircraft type."""
        # Get features for this aircraft type
        features = OsobBase.select().where(OsobBase.plane_type == self.plane.plane_type)

        # Get selected features for this aircraft
        selected_features = {
            op.osob.id for op in OsobPlaneBase.select().where(OsobPlaneBase.plane == self.plane)
        }

        if not features:
            from PyQt6.QtWidgets import QLabel
            self.features_layout.addWidget(QLabel("Нет доступных особенностей для этого типа самолета"))
            return

        for feature in features:
            cb = QCheckBox(feature.name)
            cb.setChecked(feature.id in selected_features)
            self.features_layout.addWidget(cb)
            self.feature_checks[feature.id] = cb

    def save_selection(self) -> None:
        """Save selected features for aircraft."""
        try:
            # Delete existing relations
            OsobPlaneBase.delete().where(OsobPlaneBase.plane == self.plane).execute()

            # Create new relations
            for feature_id, cb in self.feature_checks.items():
                if cb.isChecked():
                    feature = OsobBase.get_by_id(feature_id)
                    OsobPlaneBase.create(plane=self.plane, osob=feature)

            self.accept()

        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка при сохранении: {str(e)}")

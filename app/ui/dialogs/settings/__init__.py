"""Settings dialogs for managing reference data."""

from app.ui.dialogs.settings.agregate import AddAgregate, SettingsAgregate
from app.ui.dialogs.settings.base import SingleFieldMixin, UnAddEditDialog, UnDialog
from app.ui.dialogs.settings.group import AddGroup, SettingsGroup
from app.ui.dialogs.settings.osob import SettingsOsob
from app.ui.dialogs.settings.plane_type import AddPlaneType, SettingsPlaneType
from app.ui.dialogs.settings.planes import AddPlane, SettingsPlanes
from app.ui.dialogs.settings.podrazd import AddPodrazd, SettingsPodrazd
from app.ui.dialogs.settings.systems import AddSystem, SettingsSystem

__all__ = [
    # Base classes
    "UnDialog",
    "UnAddEditDialog",
    "SingleFieldMixin",
    # Settings dialogs
    "SettingsPlaneType",
    "SettingsPodrazd",
    "SettingsGroup",
    "SettingsSystem",
    "SettingsAgregate",
    "SettingsPlanes",
    "SettingsOsob",
    # Add/Edit dialogs
    "AddPlaneType",
    "AddPodrazd",
    "AddGroup",
    "AddSystem",
    "AddAgregate",
    "AddPlane",
]

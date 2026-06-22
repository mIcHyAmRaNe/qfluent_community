from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCheckBox, QWidget

from qfluent_community.core.base import FluentWidget
from qfluent_community.core.style import QssBuilder


class CheckBox(FluentWidget, QCheckBox):
    def __init__(
        self,
        text: str = "",
        checked: bool = False,
        accent_color: str = None,
        radius: int = None,
        tristate: bool = False,
        parent: Optional[QWidget] = None
    ):
        QCheckBox.__init__(self, parent)
        FluentWidget.__init__(self)

        self.setText(text)
        self._accent_color = accent_color
        self._box_radius = radius

        if tristate:
            self.setTristate(True)

        if checked:
            self.setChecked(True)

        self.refresh_style()

    def set_accent_color(self, color: str):
        self._accent_color = color
        self.refresh_style()

    def refresh_style(self):
        builder = QssBuilder()
        qss = builder.checkbox(accent_color=self._accent_color)
        self.setStyleSheet(qss)

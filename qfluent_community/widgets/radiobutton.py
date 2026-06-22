from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QRadioButton, QWidget

from qfluent_community.core.base import FluentWidget
from qfluent_community.core.style import QssBuilder


class RadioButton(FluentWidget, QRadioButton):
    def __init__(
        self,
        text: str = "",
        checked: bool = False,
        accent_color: str = None,
        parent: Optional[QWidget] = None
    ):
        QRadioButton.__init__(self, parent)
        FluentWidget.__init__(self)

        self.setText(text)
        self._accent_color = accent_color

        if checked:
            self.setChecked(True)

        self.refresh_style()

    def set_accent_color(self, color: str):
        self._accent_color = color
        self.refresh_style()

    def refresh_style(self):
        builder = QssBuilder()
        qss = builder.radio(accent_color=self._accent_color)
        self.setStyleSheet(qss)

from __future__ import annotations

from typing import Optional, List, Any

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QComboBox, QWidget

from qfluent_community.core.base import FluentWidget
from qfluent_community.core.style import QssBuilder


class ComboBox(FluentWidget, QComboBox):
    def __init__(
        self,
        items: Optional[List[str]] = None,
        placeholder: str = "",
        editable: bool = False,
        radius: int = None,
        accent_color: str = None,
        parent: Optional[QWidget] = None
    ):
        QComboBox.__init__(self, parent)
        FluentWidget.__init__(self)

        self._radius = radius
        self._accent_color = accent_color

        if placeholder:
            self.setPlaceholderText(placeholder)

        if items:
            self.addItems(items)

        if editable:
            self.setEditable(True)

        self.refresh_style()

    def refresh_style(self):
        builder = QssBuilder()
        qss = builder.combobox(radius=self._radius, accent_color=self._accent_color)
        self.setStyleSheet(qss)

    def set_items(self, items: List[str]):
        self.clear()
        self.addItems(items)

    def set_accent_color(self, color: str):
        self._accent_color = color
        self.refresh_style()

from __future__ import annotations

from typing import Optional, Union

from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QIcon, QColor, QPainter, QFont
from PyQt6.QtWidgets import QPushButton, QWidget, QSizePolicy

from qfluent_community.core.base import FluentWidget
from qfluent_community.core.theme import ThemeManager
from qfluent_community.core.icon import FluentIcon
from qfluent_community.core.style import QssBuilder


class Button(FluentWidget, QPushButton):
    def __init__(
        self,
        text: str = "",
        appearance: str = "default",
        size: str = "medium",
        icon=None,
        radius: int = None,
        bg_color: str = None,
        text_color: str = None,
        border_color: str = None,
        hover_color: str = None,
        pressed_color: str = None,
        disabled: bool = False,
        full_width: bool = False,
        parent: Optional[QWidget] = None
    ):
        QPushButton.__init__(self, parent)
        FluentWidget.__init__(self)

        self.setText(text)
        self._appearance = appearance
        self._size_mode = size
        self._radius = radius
        self._bg_color = bg_color
        self._text_color = text_color
        self._border_color = border_color
        self._hover_color = hover_color
        self._pressed_color = pressed_color
        self._full_width = full_width

        if icon is not None:
            self.set_icon(icon)

        if disabled:
            self.setEnabled(False)

        if full_width:
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self._apply_size()
        self.refresh_style()

    def set_appearance(self, appearance: str):
        self._appearance = appearance
        self.refresh_style()

    def set_icon(self, icon):
        super().setIcon(self._resolve_icon(icon))

    def set_radius(self, radius: int):
        self._radius = radius
        self.refresh_style()

    def set_custom_bg(self, color: str):
        self._bg_color = color
        self.refresh_style()

    def set_custom_text_color(self, color: str):
        self._text_color = color
        self.refresh_style()

    @staticmethod
    def _resolve_icon(icon):
        if isinstance(icon, FluentIcon):
            from qfluent_community.core.icon import get_fluent_icon_from_enum
            return get_fluent_icon_from_enum(icon)
        if isinstance(icon, str):
            return QIcon(icon)
        if isinstance(icon, QIcon):
            return icon
        return QIcon()

    def _apply_size(self):
        sizes = {
            "small": (24, 18, 8),
            "medium": (32, 18, 12),
            "large": (40, 20, 16),
        }
        h, fs, pad = sizes.get(self._size_mode, sizes["medium"])
        self.setFixedHeight(h)

    def refresh_style(self):
        builder = QssBuilder()
        qss = builder.button(
            appearance=self._appearance,
            radius=self._radius,
            bg_color=self._bg_color,
            text_color=self._text_color,
            border_color=self._border_color,
        )
        self.setStyleSheet(qss)

    @property
    def appearance(self) -> str:
        return self._appearance

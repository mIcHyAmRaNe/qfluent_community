from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSlider, QWidget

from qfluent_community.core.base import FluentWidget
from qfluent_community.core.style import QssBuilder


class Slider(FluentWidget, QSlider):
    def __init__(
        self,
        orientation: Qt.Orientation = Qt.Orientation.Horizontal,
        minimum: int = 0,
        maximum: int = 100,
        value: int = 0,
        single_step: int = 1,
        page_step: int = 10,
        accent_color: str = None,
        parent: Optional[QWidget] = None
    ):
        QSlider.__init__(self, orientation, parent)
        FluentWidget.__init__(self)

        self._accent_color = accent_color

        self.setRange(minimum, maximum)
        self.setValue(value)
        self.setSingleStep(single_step)
        self.setPageStep(page_step)

        self.setTickPosition(QSlider.TickPosition.NoTicks)

        self.refresh_style()

    def set_accent_color(self, color: str):
        self._accent_color = color
        self.refresh_style()

    def refresh_style(self):
        builder = QssBuilder()
        qss = builder.slider(accent_color=self._accent_color)
        self.setStyleSheet(qss)

from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve, pyqtProperty, pyqtSignal
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel

from qfluent_community.core.base import FluentWidget
from qfluent_community.core.theme import ThemeManager


class SwitchButton(FluentWidget, QWidget):
    toggled = pyqtSignal(bool)

    def __init__(
        self,
        text: str = "",
        checked: bool = False,
        accent_color: str = None,
        animation_duration: int = 180,
        parent: Optional[QWidget] = None
    ):
        QWidget.__init__(self, parent)
        FluentWidget.__init__(self)

        self._checked = checked
        self._custom_accent = accent_color is not None
        self._accent_color = accent_color or self._theme_manager.accent_color
        self._animation_duration = animation_duration
        self._knob_position = 1.0 if checked else 0.0

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self._track = _SwitchTrack(self, self)
        self._track.setFixedSize(40, 20)
        layout.addWidget(self._track)

        if text:
            self._label = QLabel(text)
            self._label.setObjectName("switchLabel")
            layout.addWidget(self._label)

        layout.addStretch(1)

        self.setFixedHeight(24)

        self._animation = QPropertyAnimation(self._track, b"knob_pos", self)
        self._animation.setDuration(animation_duration)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self._theme_manager.theme_changed.connect(self._track.update)

    def isChecked(self) -> bool:
        return self._checked

    def setChecked(self, checked: bool):
        self._checked = checked
        target = 1.0 if checked else 0.0
        if self._animation.state() == self._animation.State.Running:
            self._animation.stop()
        self._animation.setStartValue(self._track._knob_pos)
        self._animation.setEndValue(target)
        self._animation.start()

    def _on_accent_changed(self, color: str):
        if not self._custom_accent:
            self._accent_color = color
        self._track.update()

    def toggle(self):
        self.setChecked(not self._checked)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle()
            self.toggled.emit(self._checked)


class _SwitchTrack(QWidget):
    def __init__(self, parent_switch: SwitchButton, parent: QWidget):
        super().__init__(parent)
        self._switch = parent_switch
        self._knob_pos = 1.0 if parent_switch._checked else 0.0

    def get_knob_pos(self) -> float:
        return self._knob_pos

    def set_knob_pos(self, pos: float):
        self._knob_pos = pos
        self.update()

    knob_pos = pyqtProperty(float, get_knob_pos, set_knob_pos)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        track_radius = h // 2
        margin = 2
        knob_size = h - 2 * margin

        if self._switch._checked:
            track_color = self._switch._accent_color or self._switch._theme_manager.accent_color
        else:
            if self._switch._theme_manager.theme == "dark":
                track_color = "#3B3B3B"
            else:
                track_color = "#C4C4C4"

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(track_color))
        painter.drawRoundedRect(self.rect(), track_radius, track_radius)

        max_x = w - knob_size - 2 * margin
        knob_x = margin + int(self._knob_pos * max_x)

        if self._switch._checked:
            knob_color = "#FFFFFF"
        else:
            knob_color = "#A0A0A0" if self._switch._theme_manager.theme == "dark" else "#4C4C4C"

        painter.setBrush(QColor(knob_color))
        painter.drawEllipse(knob_x, margin, knob_size, knob_size)

        painter.end()

from __future__ import annotations

import ctypes
from typing import Optional

from PyQt6.QtCore import Qt, QRect, QPoint, QSize, QTimer
from PyQt6.QtGui import QColor, QPainter, QPalette, QAction
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QApplication,
    QSizePolicy
)

from qfluent_community.core.theme import ThemeManager
from qfluent_community.core.base import FluentWidget
from qfluent_community.core.style import StyleEngine
from qfluent_community.core.effects import WindowEffect, MicaController, ShadowEffect
from qfluent_community.window.title_bar import FluentTitleBar, TitleBarButtonType


class FluentWindow(QMainWindow):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._theme = ThemeManager.instance()
        self._style_engine = StyleEngine()
        self._window_effect = WindowEffect()
        self._mica = MicaController.instance()

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowMinimizeButtonHint |
            Qt.WindowType.WindowMaximizeButtonHint
        )

        self._central = QWidget()
        self._central.setObjectName("centralWidget")
        self.setCentralWidget(self._central)

        self._main_layout = QVBoxLayout(self._central)
        self._main_layout.setContentsMargins(0, 0, 0, 0)
        self._main_layout.setSpacing(0)

        self._title_bar = FluentTitleBar(self)
        self._main_layout.addWidget(self._title_bar)

        self._content_area = QWidget()
        self._content_area.setObjectName("contentArea")
        self._main_layout.addWidget(self._content_area, 1)

        self._content_layout = QHBoxLayout(self._content_area)
        self._content_layout.setContentsMargins(0, 0, 0, 0)
        self._content_layout.setSpacing(0)

        self._theme.theme_changed.connect(self._on_theme_changed)
        self._theme.accent_changed.connect(self._on_theme_changed)

    def _setup_window_effects(self):
        hwnd = int(self.winId())
        self._window_effect.set_window(hwnd)
        self._window_effect.set_dark_mode(self._theme.theme == "dark")
        self._window_effect.set_rounded_corners()

    def set_title(self, title: str):
        self._title_bar.set_title(title)

    def set_window_icon(self, icon):
        self._title_bar.set_icon(icon)

    def enable_mica(self, enabled: bool = True, alt: bool = False):
        hwnd = int(self.winId())
        if enabled:
            self._mica.apply(hwnd, self._theme.theme == "dark", alt)
        self._window_effect.set_window(hwnd)

    def enable_acrylic(self, enabled: bool = True):
        hwnd = int(self.winId())
        if enabled:
            self._mica.apply_acrylic(hwnd)
        self._window_effect.set_window(hwnd)

    def enable_blur(self, enabled: bool = True):
        hwnd = int(self.winId())
        if enabled:
            self._window_effect.set_blur(True)

    def enable_shadow(self, enabled: bool = True):
        hwnd = int(self.winId())
        if enabled:
            self._window_effect.add_shadow()
        else:
            self._window_effect.remove_shadow()

    def enable_dark_mode(self, enabled: bool = True):
        hwnd = int(self.winId())
        self._window_effect.set_dark_mode(enabled)

    def enable_rounded_corners(self):
        hwnd = int(self.winId())
        self._window_effect.set_rounded_corners()

    def central_widget(self) -> QWidget:
        return self._content_area

    def set_central_widget(self, widget: QWidget):
        self._content_layout.addWidget(widget)

    def title_bar(self) -> FluentTitleBar:
        return self._title_bar

    def _on_theme_changed(self):
        self._style_engine.apply_palette(self, self._theme.theme)
        self._style_engine.apply(self, self._style_engine.qss("QMainWindow"))
        self._title_bar._on_theme_changed()

    def _apply_window_effects(self):
        try:
            hwnd = int(self.winId())
            if hwnd:
                self._window_effect.set_window(hwnd)
                self._window_effect.set_dark_mode(self._theme.theme == "dark")
                self._window_effect.set_rounded_corners()
        except (OSError, ValueError, AttributeError):
            pass

    def showEvent(self, event):
        super().showEvent(event)
        if not hasattr(self, '_window_shown'):
            self._window_shown = True
            self._apply_window_effects()
            self._on_theme_changed()

    def resizeEvent(self, event):
        super().resizeEvent(event)

    def changeEvent(self, event):
        super().changeEvent(event)

    def mousePressEvent(self, event):
        if event.position().y() < self._title_bar.height():
            if event.button() == Qt.MouseButton.LeftButton:
                self._drag_pos = event.globalPosition().toPoint()
                self._dragging = True

    def mouseMoveEvent(self, event):
        if hasattr(self, '_dragging') and self._dragging:
            delta = event.globalPosition().toPoint() - self._drag_pos
            self.move(self.pos() + delta)
            self._drag_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = False

    def mouseDoubleClickEvent(self, event):
        if event.position().y() < self._title_bar.height():
            window = self.window()
            if window:
                if window.isMaximized():
                    window.showNormal()
                else:
                    window.showMaximized()

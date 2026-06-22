from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import QObject, Qt
from PyQt6.QtGui import QPaintEvent
from PyQt6.QtWidgets import QWidget

from qfluent_community.core.theme import ThemeManager
from qfluent_community.core.style import StyleEngine, QssBuilder


class FluentWidget:
    def __init__(self):
        self._theme_manager = ThemeManager.instance()
        self._style_engine = StyleEngine()
        self._qss_builder = QssBuilder()

        self._theme_manager.theme_changed.connect(self._on_theme_changed)
        self._theme_manager.accent_changed.connect(self._on_accent_changed)

    def _on_theme_changed(self):
        self.refresh_style()

    def _on_accent_changed(self, color: str):
        self.refresh_style()

    def refresh_style(self):
        pass

    @property
    def theme(self) -> ThemeManager:
        return self._theme_manager

    @property
    def style_engine(self) -> StyleEngine:
        return self._style_engine

    @property
    def qss(self) -> QssBuilder:
        return self._qss_builder

    def set_qss(self, qss: str):
        if isinstance(self, QWidget):
            self.setStyleSheet(qss)

    def apply_theme_qss(self):
        if isinstance(self, QWidget):
            self._style_engine.apply_theme(self)


class FluentMixin:
    _theme_manager = ThemeManager.instance()

    @classmethod
    def theme(cls) -> ThemeManager:
        return cls._theme_manager

    def fluent_init(self):
        self._theme_manager.theme_changed.connect(self._on_theme_changed)
        self._theme_manager.accent_changed.connect(self._on_accent_changed)

    def _on_theme_changed(self):
        self.refresh_style()

    def _on_accent_changed(self, color: str):
        self.refresh_style()

    def refresh_style(self):
        pass

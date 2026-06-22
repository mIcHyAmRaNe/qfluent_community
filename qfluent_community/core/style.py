from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import QObject, QRect
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QWidget

from qfluent_community.core.theme import ThemeManager


class StyleEngine(QObject):
    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self._theme = ThemeManager.instance()

    def qss(self, selector: str = "QWidget", extra: Optional[dict] = None) -> str:
        lines = [f"{selector} {{"]

        theme = self._theme.theme
        tokens = self._theme.tokens

        vars_map = {
            "background-color": "bg_primary",
            "color": "text_primary",
            "border": "border",
            "border-color": "border",
            "font-family": "font_family",
            "font-size": "font_size_body",
            "border-radius": "radius_medium",
        }

        for qss_prop, token_key in vars_map.items():
            value = self._theme.token(token_key)
            if value:
                if token_key.startswith("radius") or token_key.startswith("font_size"):
                    if token_key.startswith("font_size"):
                        lines.append(f"    {qss_prop}: {value}px;")
                    else:
                        lines.append(f"    {qss_prop}: {value}px;")
                else:
                    lines.append(f"    {qss_prop}: {value};")

        if extra:
            for prop, value in extra.items():
                lines.append(f"    {prop}: {value};")

        lines.append("}")
        return "\n".join(lines)

    def apply(self, widget: QWidget, qss: str):
        widget.setStyleSheet(qss)

    def apply_theme(self, widget: QWidget):
        widget.setStyleSheet(self.qss())

    @staticmethod
    def hex_to_qcolor(hex_color: str) -> QColor:
        return QColor(hex_color)

    @staticmethod
    def apply_palette(widget: QWidget, theme: str = "dark"):
        tm = ThemeManager.instance()
        palette = QPalette()

        bg = QColor(tm.token("bg_primary"))
        surface = QColor(tm.token("surface"))
        text = QColor(tm.token("text_primary"))
        text_secondary = QColor(tm.token("text_secondary"))
        accent = QColor(tm.accent_color)
        disabled = QColor(tm.token("text_disabled"))
        fill = QColor(tm.token("fill_default"))

        palette.setColor(QPalette.ColorGroup.Normal, QPalette.ColorRole.Window, bg)
        palette.setColor(QPalette.ColorGroup.Normal, QPalette.ColorRole.WindowText, text)
        palette.setColor(QPalette.ColorGroup.Normal, QPalette.ColorRole.Base, surface)
        palette.setColor(QPalette.ColorGroup.Normal, QPalette.ColorRole.Text, text)
        palette.setColor(QPalette.ColorGroup.Normal, QPalette.ColorRole.Button, fill)
        palette.setColor(QPalette.ColorGroup.Normal, QPalette.ColorRole.ButtonText, text)
        palette.setColor(QPalette.ColorGroup.Normal, QPalette.ColorRole.Highlight, accent)
        palette.setColor(QPalette.ColorGroup.Normal, QPalette.ColorRole.HighlightedText, QColor("#FFFFFF"))
        palette.setColor(QPalette.ColorGroup.Normal, QPalette.ColorRole.ToolTipBase, surface)
        palette.setColor(QPalette.ColorGroup.Normal, QPalette.ColorRole.ToolTipText, text)
        palette.setColor(QPalette.ColorGroup.Normal, QPalette.ColorRole.PlaceholderText, text_secondary)

        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, disabled)
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, disabled)
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, disabled)

        widget.setPalette(palette)


class QssBuilder:
    def __init__(self):
        self._theme = ThemeManager.instance()

    def button(self, appearance: str = "default", radius: int = None,
               bg_color: str = None, text_color: str = None,
               border_color: str = None) -> str:
        tm = self._theme
        radius = radius or tm.token("radius_medium")

        if bg_color:
            bg = bg_color
            hover_bg = bg_color
            pressed_bg = bg_color
        elif appearance == "accent":
            bg = tm.accent_color
            hover_bg = tm.token("accent_light")
            pressed_bg = tm.token("accent_dark")
        elif appearance == "transparent":
            bg = "transparent"
            hover_bg = "rgba(255, 255, 255, 0.08)" if tm.theme == "dark" else "rgba(0, 0, 0, 0.05)"
            pressed_bg = "rgba(255, 255, 255, 0.12)" if tm.theme == "dark" else "rgba(0, 0, 0, 0.08)"
        elif appearance == "outline":
            bg = "transparent"
            hover_bg = tm.token("fill_secondary")
            pressed_bg = tm.token("fill_tertiary")
        elif appearance == "danger":
            bg = "#E81123"
            hover_bg = "#F1707A"
            pressed_bg = "#C50F1F"
        elif appearance == "success":
            bg = "#107C10"
            hover_bg = "#359B35"
            pressed_bg = "#0B650B"
        else:
            bg = tm.token("fill_default")
            hover_bg = tm.token("fill_secondary")
            pressed_bg = tm.token("fill_tertiary")

        if not text_color:
            if appearance == "accent" or appearance == "danger" or appearance == "success":
                text_color = "#FFFFFF"
            elif appearance == "transparent":
                text_color = tm.token("text_primary")
            else:
                text_color = tm.token("text_primary")

        if not border_color:
            border_color = "transparent"

        return f"""
QPushButton {{
    background-color: {bg};
    color: {text_color};
    border: 1px solid {border_color};
    border-radius: {radius}px;
    padding: 5px 16px;
    font-size: {tm.token("font_size_body")}px;
    font-family: {tm.token("font_family")};
}}
QPushButton:hover {{
    background-color: {hover_bg};
}}
QPushButton:pressed {{
    background-color: {pressed_bg};
}}
QPushButton:disabled {{
    background-color: {tm.token("fill_disabled")};
    color: {tm.token("text_disabled")};
}}
"""

    def checkbox(self, accent_color: str = None) -> str:
        tm = self._theme
        accent = accent_color or tm.accent_color
        bg = tm.token("fill_default")
        text = tm.token("text_primary")
        border = tm.token("border")

        return f"""
QCheckBox {{
    color: {text};
    font-size: {tm.token("font_size_body")}px;
    font-family: {tm.token("font_family")};
    spacing: 8px;
}}
QCheckBox::indicator {{
    width: 20px;
    height: 20px;
    border-radius: 4px;
    border: 1px solid {border};
    background-color: {bg};
}}
QCheckBox::indicator:checked {{
    background-color: {accent};
    border-color: {accent};
}}
QCheckBox::indicator:hover {{
    border-color: {accent};
}}
"""

    def radio(self, accent_color: str = None) -> str:
        tm = self._theme
        accent = accent_color or tm.accent_color
        bg = tm.token("fill_default")
        text = tm.token("text_primary")

        return f"""
QRadioButton {{
    color: {text};
    font-size: {tm.token("font_size_body")}px;
    font-family: {tm.token("font_family")};
    spacing: 8px;
}}
QRadioButton::indicator {{
    width: 20px;
    height: 20px;
    border-radius: 10px;
    border: 1px solid {tm.token("border")};
    background-color: {bg};
}}
QRadioButton::indicator:checked {{
    background-color: {accent};
    border-color: {accent};
}}
"""

    def combobox(self, radius: int = None, accent_color: str = None) -> str:
        tm = self._theme
        radius = radius or tm.token("radius_medium")
        accent = accent_color or tm.accent_color
        bg = tm.token("fill_default")
        text = tm.token("text_primary")

        return f"""
QComboBox {{
    background-color: {bg};
    color: {text};
    border: 1px solid {tm.token("border")};
    border-radius: {radius}px;
    padding: 5px 12px;
    font-size: {tm.token("font_size_body")}px;
    font-family: {tm.token("font_family")};
}}
QComboBox:hover {{
    border-color: {accent};
}}
QComboBox::drop-down {{
    border: none;
    width: 30px;
}}
QComboBox QAbstractItemView {{
    background-color: {tm.token("surface_raised")};
    color: {text};
    border: 1px solid {tm.token("border")};
    border-radius: {radius}px;
    selection-background-color: {accent};
    selection-color: white;
    outline: none;
}}
"""

    def slider(self, accent_color: str = None) -> str:
        tm = self._theme
        accent = accent_color or tm.accent_color
        bg = tm.token("fill_default")
        text = tm.token("text_primary")

        return f"""
QSlider {{
    font-family: {tm.token("font_family")};
}}
QSlider::groove:horizontal {{
    height: 4px;
    background-color: {bg};
    border-radius: 2px;
}}
QSlider::handle:horizontal {{
    width: 20px;
    height: 20px;
    margin: -8px 0;
    background-color: {accent};
    border-radius: 10px;
}}
QSlider::sub-page:horizontal {{
    background-color: {accent};
    border-radius: 2px;
}}
QSlider::handle:hover {{
    background-color: {tm.token("accent_light")};
}}
QSlider::groove:vertical {{
    width: 4px;
    background-color: {bg};
    border-radius: 2px;
}}
QSlider::handle:vertical {{
    width: 20px;
    height: 20px;
    margin: 0 -8px;
    background-color: {accent};
    border-radius: 10px;
}}
QSlider::sub-page:vertical {{
    background-color: {accent};
    border-radius: 2px;
}}
"""

    def window(self) -> str:
        tm = self._theme
        bg = tm.token("bg_primary")
        text = tm.token("text_primary")
        border = tm.token("border")

        return f"""
QMainWindow {{
    background-color: {bg};
    color: {text};
    font-family: {tm.token("font_family")};
}}
QMainWindow::separator {{
    background-color: {border};
    width: 1px;
    height: 1px;
}}
"""

    def fluent_window(self) -> str:
        tm = self._theme
        bg = tm.token("bg_primary")
        text = tm.token("text_primary")
        border = tm.token("border")

        return f"""
QMainWindow {{
    background-color: {bg};
    color: {text};
}}
#titleBar {{
    background-color: {bg};
    border-bottom: 1px solid {border};
    min-height: 32px;
}}
#titleLabel {{
    color: {text};
    font-size: {tm.token("font_size_body")}px;
    font-family: {tm.token("font_family")};
}}
"""

    def tooltip(self) -> str:
        tm = self._theme
        return f"""
QToolTip {{
    background-color: {tm.token("surface_raised")};
    color: {tm.token("text_primary")};
    border: 1px solid {tm.token("border")};
    border-radius: {tm.token("radius_medium")}px;
    padding: 4px 8px;
    font-size: {tm.token("font_size_caption")}px;
    font-family: {tm.token("font_family")};
}}
"""

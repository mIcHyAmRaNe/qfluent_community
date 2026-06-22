from __future__ import annotations

import os
from enum import IntEnum
from typing import Optional

from PyQt6.QtCore import QRect, QRectF, Qt
from PyQt6.QtGui import QColor, QPainter, QPixmap
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from qfluent_community.core.icon import (
    FluentIcon,
    _icon_path,
    get_fluent_icon,
    get_fluent_icon_from_enum,
)
from qfluent_community.core.theme import ThemeManager


class TitleBarButtonType(IntEnum):
    MINIMIZE = 0
    MAXIMIZE = 1
    RESTORE = 2
    CLOSE = 3


class TitleBarButton(QPushButton):
    def __init__(
        self, button_type: TitleBarButtonType, parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self._type = button_type
        self.setFixedSize(46, 32)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.setObjectName(f"titleBarButton{button_type.name.capitalize()}")
        self._hovered = False
        self._pressed = False

        # Map button types to fluent icons
        # Using icons that exist in the resources
        self._icon_mapping = {
            TitleBarButtonType.MINIMIZE: FluentIcon.ARROW_MINIMIZE,  # ic_fluent_arrow_minimize_24_filled.svg
            TitleBarButtonType.MAXIMIZE: FluentIcon.ARROW_MAXIMIZE,  # ic_fluent_arrow_maximize_24_filled.svg
            TitleBarButtonType.RESTORE: FluentIcon.ARROW_MAXIMIZE,  # Fallback to maximize for restore (no restore icon available)
            TitleBarButtonType.CLOSE: FluentIcon.DISMISS,  # ic_fluent_dismiss_24_filled.svg (X icon)
        }

        self._theme = ThemeManager.instance()
        self._theme.theme_changed.connect(self.update)

    def set_type(self, button_type: TitleBarButtonType):
        self._type = button_type
        self.update()

    def enterEvent(self, event):
        self._hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self._pressed = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self._pressed = True
        self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._pressed = False
        self.update()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        is_dark = self._theme.theme == "dark"

        # Draw background/hover states
        if self._type == TitleBarButtonType.CLOSE and self._hovered:
            painter.fillRect(self.rect(), QColor("#E81123"))
        else:
            if self._pressed:
                hover_alpha = 30
            elif self._hovered:
                hover_alpha = 24
            else:
                hover_alpha = 0

            if hover_alpha:
                c = QColor(255, 255, 255) if is_dark else QColor(0, 0, 0)
                c.setAlpha(hover_alpha)
                painter.fillRect(self.rect(), c)

        # Draw icon with theme-aware color
        icon_enum = self._icon_mapping.get(self._type)
        if icon_enum:
            svg_path = _icon_path(icon_enum.value, True)
            if not os.path.isfile(svg_path):
                svg_path = _icon_path(icon_enum.value, False)

            if os.path.isfile(svg_path):
                is_close_hovered = self._type == TitleBarButtonType.CLOSE and self._hovered
                icon_color = "#FFFFFF" if (is_dark or is_close_hovered) else "#212121"

                renderer = QSvgRenderer(svg_path)
                px = QPixmap(16, 16)
                px.fill(Qt.GlobalColor.transparent)
                ip = QPainter(px)
                renderer.render(ip, QRectF(0, 0, 16, 16))
                ip.end()

                ip2 = QPainter(px)
                ip2.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
                ip2.fillRect(px.rect(), QColor(icon_color))
                ip2.end()

                icon_rect = QRect(
                    (self.width() - 16) // 2, (self.height() - 16) // 2, 16, 16
                )
                painter.drawPixmap(icon_rect, px)

        painter.end()


class FluentTitleBar(QWidget):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setObjectName("titleBar")
        self.setFixedHeight(32)

        self._theme = ThemeManager.instance()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Add left margin spacer (16px from left border)
        layout.addSpacing(16)

        self._icon_label = QLabel()
        self._icon_label.setFixedSize(16, 16)
        self._icon_label.setVisible(False)
        layout.addWidget(self._icon_label)

        # Add spacing between icon and title (16px)
        layout.addSpacing(16)

        self._title_label = QLabel("QFluent Community")
        self._title_label.setObjectName("titleLabel")
        layout.addWidget(self._title_label)

        # Add stretchable space
        layout.addStretch(1)

        # Add caption buttons without spacing between them
        self._min_btn = TitleBarButton(TitleBarButtonType.MINIMIZE)
        self._max_btn = TitleBarButton(TitleBarButtonType.MAXIMIZE)
        self._close_btn = TitleBarButton(TitleBarButtonType.CLOSE)
        layout.addWidget(self._min_btn)
        layout.addWidget(self._max_btn)
        layout.addWidget(self._close_btn)

        self._min_btn.clicked.connect(self._on_minimize)
        self._max_btn.clicked.connect(self._on_maximize)
        self._close_btn.clicked.connect(self._on_close)

        self._theme.theme_changed.connect(self._on_theme_changed)
        self._apply_label_color()

    def set_title(self, title: str):
        self._title_label.setText(title)

    def set_icon(self, icon):
        if isinstance(icon, str):
            qicon = get_fluent_icon(icon)
        else:
            qicon = get_fluent_icon_from_enum(icon)
        self._icon_label.setPixmap(qicon.pixmap(16, 16))
        self._icon_label.setVisible(True)

    def _on_minimize(self):
        window = self.window()
        if window:
            window.showMinimized()

    def _on_maximize(self):
        window = self.window()
        if window:
            if window.isMaximized():
                window.showNormal()
                self._max_btn.set_type(TitleBarButtonType.MAXIMIZE)
            else:
                window.showMaximized()
                self._max_btn.set_type(TitleBarButtonType.RESTORE)
            self._max_btn.update()

    def _on_close(self):
        window = self.window()
        if window:
            window.close()

    def _apply_label_color(self):
        color = self._theme.token("text_primary")
        weight = self._theme._tokens.font_weight_semibold
        size = self._theme.font_size("body")
        self._title_label.setStyleSheet(
            f"color: {color}; font-size: {size}px; font-weight: {weight};"
        )

    def _on_theme_changed(self):
        self._apply_label_color()
        self.update()

    def _window_active_changed(self, active: bool):
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        is_active = self.window().isActiveWindow() if self.window() else True
        alpha = 255 if is_active else 160

        if self._theme.theme == "dark":
            c = QColor("#202020")
        else:
            c = QColor("#F3F3F3")
        c.setAlpha(alpha)
        painter.fillRect(self.rect(), c)
        painter.end()

    def changeEvent(self, event):
        if event.type() == event.Type.ActivationChange:
            self._window_active_changed(
                self.window().isActiveWindow() if self.window() else True
            )
        super().changeEvent(event)

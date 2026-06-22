from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import Qt, QRect, QSize, QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QFont, QPixmap, QFontDatabase
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar,
    QApplication, QGraphicsDropShadowEffect, QSizePolicy
)

from qfluent_community.core.theme import ThemeManager
from qfluent_community.core.icon import IconWidget, FluentIcon
from qfluent_community.core.effects import ShadowEffect, WindowEffect


class SplashScreen(QWidget):
    finished = pyqtSignal()

    def __init__(self, icon=None, title: str = "QFluent Community",
                 subtitle: str = "", version: str = "1.0.0",
                 parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._theme = ThemeManager.instance()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.SplashScreen
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)

        size = QSize(480, 320)
        self.setFixedSize(size)

        screen = QApplication.primaryScreen()
        if screen:
            center = screen.availableGeometry().center()
            self.move(center.x() - size.width() // 2,
                      center.y() - size.height() // 2)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.setSpacing(12)

        layout.addStretch(1)

        self._icon_widget = IconWidget(icon, size=64)
        layout.addWidget(self._icon_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        self._title_label = QLabel(title)
        self._title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("Segoe UI Variable, Segoe UI", 24)
        font.setWeight(63)
        self._title_label.setFont(font)
        layout.addWidget(self._title_label)

        if subtitle:
            self._subtitle_label = QLabel(subtitle)
            self._subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            font = QFont("Segoe UI Variable, Segoe UI", 12)
            self._subtitle_label.setFont(font)
            layout.addWidget(self._subtitle_label)

        layout.addStretch(1)

        self._version_label = QLabel(f"v{version}")
        self._version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("Segoe UI Variable, Segoe UI", 10)
        self._version_label.setFont(font)
        layout.addWidget(self._version_label)

        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setValue(0)
        self._progress_bar.setFixedHeight(4)
        self._progress_bar.setTextVisible(False)
        layout.addWidget(self._progress_bar)

        self._theme.theme_changed.connect(self.update)

        self._window_effect = WindowEffect()

    def showEvent(self, event):
        super().showEvent(event)
        hwnd = int(self.winId())
        self._window_effect.set_window(hwnd)
        self._window_effect.set_dark_mode(self._theme.theme == "dark")
        self._window_effect.set_rounded_corners()

    def set_progress(self, value: int, message: str = ""):
        self._progress_bar.setValue(value)
        if message and hasattr(self, '_subtitle_label'):
            self._subtitle_label.setText(message)
        QApplication.processEvents()

    def finish(self):
        self.finished.emit()
        self.close()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self._theme.theme == "dark":
            painter.fillRect(self.rect(), QColor("#202020"))
            self._title_label.setStyleSheet("color: #FFFFFF;")
            self._version_label.setStyleSheet("color: #858585;")
            self._progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    background-color: #3B3B3B;
                    border: none;
                    border-radius: 2px;
                }}
                QProgressBar::chunk {{
                    background-color: {self._theme.accent_color};
                    border-radius: 2px;
                }}
            """)
        else:
            painter.fillRect(self.rect(), QColor("#FFFFFF"))
            self._title_label.setStyleSheet("color: #000000;")
            self._version_label.setStyleSheet("color: #616161;")
            self._progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    background-color: #E0E0E0;
                    border: none;
                    border-radius: 2px;
                }}
                QProgressBar::chunk {{
                    background-color: {self._theme.accent_color};
                    border-radius: 2px;
                }}
            """)
        painter.end()

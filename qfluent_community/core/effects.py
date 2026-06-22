from __future__ import annotations

import ctypes
import ctypes.wintypes
from enum import IntEnum
from typing import Optional

from PyQt6.QtCore import Qt, QRect, QPoint, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import (
    QPainter, QColor, QBrush, QPen, QPixmap, QImage,
    QPainterPath, QRegion, QPalette, QAction
)
from PyQt6.QtWidgets import (
    QWidget, QGraphicsEffect, QGraphicsDropShadowEffect, QApplication
)


class WindowCompositionAttribute(IntEnum):
    WCA_ACCENT_POLICY = 19


class AccentState(IntEnum):
    ACCENT_DISABLED = 0
    ACCENT_ENABLE_GRADIENT = 1
    ACCENT_ENABLE_TRANSPARENTGRADIENT = 2
    ACCENT_ENABLE_BLURBEHIND = 3
    ACCENT_ENABLE_ACRYLICBLURBEHIND = 4
    ACCENT_ENABLE_HOSTBACKDROP = 5


class DwmWindowAttribute(IntEnum):
    DWMWA_NCRENDERING_POLICY = 2
    DWMWA_TRANSITIONS_FORCEDISABLED = 3
    DWMWA_ALLOW_NCPAINT = 4
    DWMWA_CAPTION_BUTTON_BOUNDS = 5
    DWMWA_NONCLIENT_RTL_LAYOUT = 6
    DWMWA_FORCE_ICONIC_REPRESENTATION = 7
    DWMWA_FLIP3D_POLICY = 8
    DWMWA_EXTENDED_FRAME_BOUNDS = 9
    DWMWA_HAS_ICONIC_BITMAP = 10
    DWMWA_DISALLOW_PEEK = 11
    DWMWA_EXCLUDED_FROM_PEEK = 12
    DWMWA_CLOAK = 13
    DWMWA_CLOAKED = 14
    DWMWA_FREEZE_REPRESENTATION = 15
    DWMWA_USE_HOSTBACKDROPBRUSH = 17
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    DWMWA_WINDOW_CORNER_PREFERENCE = 33
    DWMWA_BORDER_COLOR = 34
    DWMWA_CAPTION_COLOR = 35
    DWMWA_TEXT_COLOR = 36
    DWMWA_VISIBLE_FRAME_BORDER_THICKNESS = 37
    DWMWA_MICA_EFFECT = 38
    DWMWA_SYSTEMBACKDROP_TYPE = 38


class DwmWindowCorner(IntEnum):
    DWMWCP_DEFAULT = 0
    DWMWCP_DONOTROUND = 1
    DWMWCP_ROUND = 2
    DWMWCP_ROUNDSMALL = 3


class SystemBackdropType(IntEnum):
    DWMSBT_AUTO = 0
    DWMSBT_NONE = 1
    DWMSBT_MAINWINDOW = 2
    DWMSBT_TRANSIENTWINDOW = 3
    DWMSBT_TABBEDWINDOW = 4


class WindowEffect:
    def __init__(self):
        self._hwnd = None
        self._dwm = ctypes.windll.dwmapi
        self._user32 = ctypes.windll.user32

    def set_window(self, hwnd: int):
        self._hwnd = hwnd

    @property
    def hwnd(self):
        if self._hwnd is None:
            return 0
        return self._hwnd

    def _dwm_set(self, attribute: int, value: int):
        hwnd = self.hwnd
        if not hwnd:
            return
        try:
            result = self._dwm.DwmSetWindowAttribute(
                ctypes.c_int(hwnd),
                ctypes.c_int(attribute),
                ctypes.byref(ctypes.c_int(value)),
                ctypes.c_int(4)
            )
        except Exception:
            pass

    def set_mica(self, enabled: bool = True, dark: bool = True):
        self._dwm_set(DwmWindowAttribute.DWMWA_SYSTEMBACKDROP_TYPE,
                       SystemBackdropType.DWMSBT_MAINWINDOW if enabled else SystemBackdropType.DWMSBT_AUTO)
        self.set_dark_mode(dark)

    def set_mica_alt(self, enabled: bool = True, dark: bool = True):
        self._dwm_set(DwmWindowAttribute.DWMWA_SYSTEMBACKDROP_TYPE,
                       SystemBackdropType.DWMSBT_TABBEDWINDOW if enabled else SystemBackdropType.DWMSBT_AUTO)
        self.set_dark_mode(dark)

    def set_acrylic(self, enabled: bool = True):
        if not self.hwnd:
            return
        try:
            data = (ctypes.c_int * 4)(AccentState.ACCENT_ENABLE_ACRYLICBLURBEHIND, 1, 0x003366, 1)
            comp_data = (ctypes.c_int * 8)()
            comp_data[0] = WindowCompositionAttribute.WCA_ACCENT_POLICY
            comp_data[1] = ctypes.sizeof(data)
            comp_data[2] = ctypes.addressof(data)
            self._user32.SetWindowCompositionAttribute(
                ctypes.c_int(self.hwnd),
                ctypes.byref(comp_data)
            )
        except Exception:
            pass

    def set_blur(self, enabled: bool = True):
        if not self.hwnd:
            return
        try:
            data = (ctypes.c_int * 4)(AccentState.ACCENT_ENABLE_BLURBEHIND, 0, 0, 0)
            comp_data = (ctypes.c_int * 8)()
            comp_data[0] = WindowCompositionAttribute.WCA_ACCENT_POLICY
            comp_data[1] = ctypes.sizeof(data)
            comp_data[2] = ctypes.addressof(data)
            self._user32.SetWindowCompositionAttribute(
                ctypes.c_int(self.hwnd),
                ctypes.byref(comp_data)
            )
        except Exception:
            pass

    def set_dark_mode(self, enabled: bool = True):
        self._dwm_set(DwmWindowAttribute.DWMWA_USE_IMMERSIVE_DARK_MODE, 1 if enabled else 0)

    def set_rounded_corners(self, corner: DwmWindowCorner = DwmWindowCorner.DWMWCP_ROUND):
        self._dwm_set(DwmWindowAttribute.DWMWA_WINDOW_CORNER_PREFERENCE, corner)

    def set_border_color(self, color: int = 0x00000000):
        """Set DWM window contour/ stroke color. ABGR format, 0 = transparent."""
        hwnd = self.hwnd
        if not hwnd:
            return
        try:
            self._dwm.DwmSetWindowAttribute(
                ctypes.c_int(hwnd),
                ctypes.c_int(DwmWindowAttribute.DWMWA_BORDER_COLOR),
                ctypes.byref(ctypes.c_uint(color)),
                ctypes.c_int(4)
            )
        except Exception:
            pass

    def set_window_backdrop(self, backdrop_type: int = 0):
        """Set the system backdrop type directly."""
        self._dwm_set(DwmWindowAttribute.DWMWA_SYSTEMBACKDROP_TYPE, backdrop_type)

    def set_visible_frame_thickness(self, thickness: int = 1):
        """Control the visible frame border thickness."""
        self._dwm_set(DwmWindowAttribute.DWMWA_VISIBLE_FRAME_BORDER_THICKNESS, thickness)

    def set_caption_color(self, color: int = 0x00000000):
        """Set caption bar background color. ABGR format."""
        hwnd = self.hwnd
        if not hwnd:
            return
        try:
            self._dwm.DwmSetWindowAttribute(
                ctypes.c_int(hwnd),
                ctypes.c_int(DwmWindowAttribute.DWMWA_CAPTION_COLOR),
                ctypes.byref(ctypes.c_uint(color)),
                ctypes.c_int(4)
            )
        except Exception:
            pass

    def remove_shadow(self):
        if not self.hwnd:
            return
        try:
            style = self._user32.GetWindowLongA(self.hwnd, -20)
            self._user32.SetWindowLongA(self.hwnd, -20, style | 0x80000)
        except Exception:
            pass

    def add_shadow(self):
        if not self.hwnd:
            return
        try:
            style = self._user32.GetWindowLongA(self.hwnd, -20)
            self._user32.SetWindowLongA(self.hwnd, -20, style & ~0x80000)
        except Exception:
            pass


class ShadowEffect(QGraphicsDropShadowEffect):
    def __init__(self, blur_radius: int = 32, opacity: float = 0.25,
                 x_offset: int = 0, y_offset: int = 8, color: str = "#000000",
                 parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setBlurRadius(blur_radius)
        self.setColor(QColor(color))
        self.setOffset(x_offset, y_offset)
        self.setOpacity(opacity)


class AcrylicBrush:
    def __init__(self, tint_color: str = "#2C2C2C", luminosity_color: str = "#1A1A2E",
                 tint_opacity: float = 0.6, blur_radius: int = 30):
        self._tint_color = QColor(tint_color)
        self._luminosity_color = QColor(luminosity_color)
        self._tint_opacity = tint_opacity
        self._blur_radius = blur_radius
        self._noise_pixmap: Optional[QPixmap] = None
        self._background_pixmap: Optional[QPixmap] = None
        self._dirty = True

    def set_tint_color(self, color: QColor, opacity: float = 0.6):
        self._tint_color = color
        self._tint_opacity = opacity
        self._dirty = True

    def set_luminosity_color(self, color: QColor):
        self._luminosity_color = color
        self._dirty = True

    def set_blur_radius(self, radius: int):
        self._blur_radius = radius
        self._dirty = True

    def grab_background(self, widget: QWidget):
        screen = widget.screen()
        if not screen:
            return
        pos = widget.mapToGlobal(QPoint(0, 0))
        rect = QRect(pos, widget.size())
        self._background_pixmap = screen.grabWindow(0, rect.x(), rect.y(), rect.width(), rect.height())
        self._dirty = False

    def paint(self, painter: QPainter, rect: QRect, clip_path: Optional[QPainterPath] = None):
        if self._background_pixmap is None or self._background_pixmap.isNull():
            return

        painter.save()
        if clip_path:
            painter.setClipPath(clip_path)

        bg = self._background_pixmap.copy(QRect(0, 0, rect.width(), rect.height()))
        blurred = bg
        painter.drawPixmap(rect.topLeft(), blurred)

        tint = QColor(self._tint_color)
        tint.setAlphaF(self._tint_opacity)
        painter.fillRect(rect, tint)

        luminosity = QColor(self._luminosity_color)
        luminosity.setAlphaF(0.3)
        painter.fillRect(rect, luminosity)

        painter.restore()

    def paint_widget(self, widget: QWidget):
        if self._dirty or self._background_pixmap is None:
            return
        painter = QPainter(widget)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        clip_path = QPainterPath()
        clip_path.addRoundedRect(
            widget.rect().adjusted(1, 1, -1, -1),
            8, 8
        )
        self.paint(painter, widget.rect(), clip_path)
        painter.end()


class MicaController:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._effect = WindowEffect()

    def apply(self, hwnd: int, dark: bool = True, alt: bool = False):
        self._effect.set_window(hwnd)
        if alt:
            self._effect.set_mica_alt(True, dark)
        else:
            self._effect.set_mica(True, dark)

    def apply_mica_with_contour(self, hwnd: int, dark: bool = True, alt: bool = False):
        """Apply Mica + proper Win11 window contour (1px stroke)."""
        self._effect.set_window(hwnd)
        self._effect.set_mica(True, dark) if not alt else self._effect.set_mica_alt(True, dark)
        self._effect.set_rounded_corners()
        self._effect.set_visible_frame_thickness(1)
        border_color = 0x00FFFFFF if dark else 0x00D1D1D1
        self._effect.set_border_color(border_color)

    def apply_acrylic(self, hwnd: int):
        self._effect.set_window(hwnd)
        self._effect.set_acrylic(True)

    def apply_dark_mode(self, hwnd: int, dark: bool = True):
        self._effect.set_window(hwnd)
        self._effect.set_dark_mode(dark)

    def apply_rounded_corners(self, hwnd: int):
        self._effect.set_window(hwnd)
        self._effect.set_rounded_corners()

    def apply_backdrop(self, hwnd: int, backdrop: int, dark: bool = True):
        """Direct backdrop type control."""
        self._effect.set_window(hwnd)
        self._effect.set_window_backdrop(backdrop)
        self._effect.set_dark_mode(dark)

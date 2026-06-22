from __future__ import annotations

import os
from enum import Enum
from typing import Optional

from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QIcon, QIconEngine, QImage, QPainter, QColor, QPixmap
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout

from qfluent_community.core.theme import ThemeManager


_ICON_CACHE: dict[str, QIcon] = {}


def _resolve_icon_dir() -> str:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(base, "resources", "icons", "fluent")
    if os.path.isdir(path):
        return path
    alt = os.path.join(os.path.dirname(os.path.dirname(base)), "resources", "icons", "fluent")
    if os.path.isdir(alt):
        return alt
    return path


_ICON_DIR = _resolve_icon_dir()


FluentIcon = Enum("FluentIcon", {
    "ADD": "add",
    "ADD_CIRCLE": "add_circle",
    "ALBUM": "album",
    "ALERT": "alert",
    "ALERT_OFF": "alert_off",
    "ARROW_DOWN": "arrow_down",
    "ARROW_LEFT": "arrow_left",
    "ARROW_RIGHT": "arrow_right",
    "ARROW_UP": "arrow_up",
    "ARROW_SORT": "arrow_sort",
    "ARROW_DOWNLOAD": "arrow_download",
    "ARROW_UPLOAD": "arrow_upload",
    "ARROW_EXPAND": "arrow_expand",
    "ARROW_MINIMIZE": "arrow_minimize",
    "ARROW_MAXIMIZE": "arrow_maximize",
    "ARROW_FORWARD": "arrow_forward",
    "ARROW_REPLY": "arrow_reply",
    "ARROW_UNDO": "arrow_undo",
    "ARROW_REDO": "arrow_redo",
    "ATTACH": "attach",
    "BACKSPACE": "backspace",
    "BADGE": "badge",
    "BATTERY_FULL": "battery_full",
    "BLOCK": "block",
    "BLUETOOTH": "bluetooth",
    "BOOK": "book",
    "BOOKMARK": "bookmark",
    "BRIEFCASE": "briefcase",
    "BROOM": "broom",
    "BUG": "bug",
    "BUILDING": "building",
    "CALENDAR": "calendar",
    "CALENDAR_MONTH": "calendar_month",
    "CALENDAR_WORK_WEEK": "calendar_work_week",
    "CALL": "call",
    "CAMERA": "camera",
    "CANCEL": "cancel",
    "CART": "cart",
    "CAST": "cast",
    "CHAT": "chat",
    "CHAT_HELP": "chat_help",
    "CHAT_MULTIPLE": "chat_multiple",
    "CHECK": "check",
    "CHECKBOX_CHECKED": "checkbox_checked",
    "CHECKBOX_UNCHECKED": "checkbox_unchecked",
    "CHECKMARK": "checkmark",
    "CHECKMARK_CIRCLE": "checkmark_circle",
    "CHEVRON_DOWN": "chevron_down",
    "CHEVRON_LEFT": "chevron_left",
    "CHEVRON_RIGHT": "chevron_right",
    "CHEVRON_UP": "chevron_up",
    "CLOCK": "clock",
    "CLOSE": "dismiss",
    "CLOUD": "cloud",
    "CODE": "code",
    "COLUMN": "column",
    "COMMENT": "comment",
    "COMPOSE": "compose",
    "CONNECTED": "connected",
    "COPY": "copy",
    "CROP": "crop",
    "CUT": "cut",
    "DATABASE": "database",
    "DELETE": "delete",
    "DESKTOP": "desktop",
    "DIALPAD": "dialpad",
    "DIRECTIONS": "directions",
    "DISMISS": "dismiss",
    "DISMISS_CIRCLE": "dismiss_circle",
    "DOCUMENT": "document",
    "DOCUMENT_ADD": "document_add",
    "DOCUMENT_COPY": "document_copy",
    "DOCUMENT_DISMISS": "document_dismiss",
    "DOCUMENT_EDIT": "document_edit",
    "DOWNLOAD": "download",
    "DRINK_COFFEE": "drink_coffee",
    "EDIT": "edit",
    "EMOJI": "emoji",
    "EMOJI_LAUGH": "emoji_laugh",
    "EMOJI_SAD": "emoji_sad",
    "ERASER": "eraser",
    "ERROR_CIRCLE": "error_circle",
    "EYE": "eye",
    "EYE_HIDE": "eye_hide",
    "FILTER": "filter",
    "FINGERPRINT": "fingerprint",
    "FIRE": "fire",
    "FLAG": "flag",
    "FLASH": "flash",
    "FOLDER": "folder",
    "FOLDER_ADD": "folder_add",
    "FONT": "font",
    "FOOD": "food",
    "GAME": "game",
    "GIF": "gif",
    "GLOBE": "globe",
    "GROUP": "group",
    "HAND": "hand",
    "HAPTIC": "haptic",
    "HEADPHONES": "headphones",
    "HEART": "heart",
    "HELP": "help",
    "HISTORY": "history",
    "HOME": "home",
    "IMAGE": "image",
    "IMAGE_ADD": "image_add",
    "IMAGE_COPY": "image_copy",
    "INFO": "info",
    "INFO_CIRCLE": "info_circle",
    "KEY": "key",
    "KEYBOARD": "keyboard",
    "LAPTOP": "laptop",
    "LAYER": "layer",
    "LEAF": "leaf",
    "LIBRARY": "library",
    "LIGHT": "light",
    "LIGHTBULB": "lightbulb",
    "LINK": "link",
    "LIST": "list",
    "LOCATION": "location",
    "LOCK": "lock",
    "MAIL": "mail",
    "MAIL_READ": "mail_read",
    "MAP": "map",
    "MEGAPHONE": "megaphone",
    "MENU": "menu",
    "MIC": "mic",
    "MIC_OFF": "mic_off",
    "MOBILE": "mobile",
    "MORE": "more",
    "MORE_CIRCLE": "more_circle",
    "MORE_VERTICAL": "more_vertical",
    "MOUSE": "mouse",
    "MUSIC": "music",
    "MUSIC_NOTE": "music_note",
    "NEWS": "news",
    "NOTE": "note",
    "NOTEBOOK": "notebook",
    "NOTIFICATION": "notification",
    "NOTIFICATION_OFF": "notification_off",
    "OPEN": "open",
    "OPEN_FOLDER": "open_folder",
    "OPTIONS": "options",
    "PAGE": "page",
    "PAINT": "paint",
    "PALETTE": "palette",
    "PARKING": "parking",
    "PASTE": "paste",
    "PAUSE": "pause",
    "PAUSE_CIRCLE": "pause_circle",
    "PEOPLE": "people",
    "PERSON": "person",
    "PERSON_ADD": "person_add",
    "PERSON_DELETE": "person_delete",
    "PHONE": "phone",
    "PICTURE": "picture",
    "PIN": "pin",
    "PIN_OFF": "pin_off",
    "PLAY": "play",
    "PLAY_CIRCLE": "play_circle",
    "POWER": "power",
    "PRINT": "print",
    "PROHIBITED": "prohibited",
    "PULSE": "pulse",
    "QR_CODE": "qr_code",
    "QUESTION": "question",
    "QUESTION_CIRCLE": "question_circle",
    "RECORD": "record",
    "REFRESH": "refresh",
    "REMOVE": "remove",
    "REORDER": "reorder",
    "REPEAT": "repeat",
    "REPEAT_ALL": "repeat_all",
    "REPLY": "reply",
    "REPORT": "report",
    "RESIZE": "resize",
    "RESTORE": "restore",
    "ROTATE": "rotate",
    "SAVE": "save",
    "SCAN": "scan",
    "SCREENSHOT": "screenshot",
    "SEARCH": "search",
    "SELECT": "select",
    "SEND": "send",
    "SETTINGS": "settings",
    "SHARE": "share",
    "SHIELD": "shield",
    "SHOP": "shop",
    "SIGNATURE": "signature",
    "SLEEP": "sleep",
    "SLIDE": "slide",
    "SPEAKER": "speaker",
    "SPEAKER_OFF": "speaker_off",
    "STAR": "star",
    "STAR_ADD": "star_add",
    "STAR_HALF": "star_half",
    "STAR_OFF": "star_off",
    "STATUS": "status",
    "STOP": "stop",
    "STORAGE": "storage",
    "SUBTRACT": "subtract",
    "SUN": "sun",
    "SWITCH": "switch",
    "SYNC": "sync",
    "TAB": "tab",
    "TABLE": "table",
    "TAG": "tag",
    "TASKS": "tasks",
    "TEXT": "text",
    "THUMB_DOWN": "thumb_down",
    "THUMB_UP": "thumb_up",
    "TICKET": "ticket",
    "TIME": "time",
    "TOGGLE": "toggle",
    "TOOLBOX": "toolbox",
    "TOP": "top",
    "TRANSLATE": "translate",
    "TROPHY": "trophy",
    "TV": "tv",
    "UNLINK": "unlink",
    "UNLOCK": "unlock",
    "UPLOAD": "upload",
    "USB": "usb",
    "USER": "user",
    "VIDEO": "video",
    "VIDEO_OFF": "video_off",
    "VIEW": "view",
    "VOICEMAIL": "voicemail",
    "VOLUME": "volume",
    "WALK": "walk",
    "WARNING": "warning",
    "WIFI": "wifi",
    "WIFI_OFF": "wifi_off",
    "WINDOW": "window",
    "WINDOW_AD": "window_ad",
    "ZOOM": "zoom",
    "ZOOM_IN": "zoom_in",
    "ZOOM_OUT": "zoom_out",
    "CHAT_EMPTY": "chat_empty",
    "DESKTOP_PULSE": "desktop_pulse",
    "MINIMIZE": "chrome_minimize",
    "MAXIMIZE": "chrome_maximize",
    "CLOSE_WINDOW": "chrome_close",
    "RESTORE_WINDOW": "chrome_restore",
})


def _icon_path(name: str, filled: bool = True) -> str:
    variant = "filled" if filled else "regular"
    filename = f"ic_fluent_{name}_24_{variant}.svg"
    return os.path.join(_ICON_DIR, filename)


def _icon_exists(name: str) -> bool:
    return os.path.isfile(_icon_path(name, True)) or os.path.isfile(_icon_path(name, False))



class FluentIconEngine(QIconEngine):
    def __init__(self, svg_path: str):
        super().__init__()
        self._svg_path = svg_path
        self._renderer = QSvgRenderer(svg_path) if os.path.isfile(svg_path) else None

    def paint(self, painter, rect, mode, state):
        if not self._renderer or not self._renderer.isValid():
            return
        if mode != QIcon.Mode.Normal:
            painter.setOpacity(0.5 if mode == QIcon.Mode.Disabled else 0.7)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self._renderer.render(painter, QRectF(rect))

    def clone(self):
        return FluentIconEngine(self._svg_path)

    def pixmap(self, size, mode, state):
        image = QImage(size, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.transparent)
        px = QPixmap.fromImage(image)
        painter = QPainter(px)
        self.paint(painter, QRectF(0, 0, size.width(), size.height()).toRect(), mode, state)
        painter.end()
        return px


def get_fluent_icon(name: str, filled: bool = True) -> QIcon:
    cache_key = f"{name}_{filled}"
    if cache_key in _ICON_CACHE:
        return _ICON_CACHE[cache_key]

    path = _icon_path(name, filled)
    if not os.path.isfile(path):
        path = _icon_path(name, not filled)
        if not os.path.isfile(path):
            _ICON_CACHE[cache_key] = QIcon()
            return _ICON_CACHE[cache_key]

    icon = QIcon(FluentIconEngine(path))
    _ICON_CACHE[cache_key] = icon
    return icon


def get_fluent_icon_from_enum(icon_enum, filled: bool = True) -> QIcon:
    if isinstance(icon_enum, Enum):
        return get_fluent_icon(icon_enum.value, filled)
    return QIcon()


class IconWidget(QWidget):
    def __init__(self, icon=None, size: int = 24, color: str = None,
                 parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self._color = QColor(color) if color else None
        self._renderer = None
        self._size = size

        if icon is not None:
            self.set_icon(icon)

    def set_icon(self, icon):
        svg_path = ""
        if isinstance(icon, Enum):
            svg_path = _icon_path(icon.value, True)
            if not os.path.isfile(svg_path):
                svg_path = _icon_path(icon.value, False)
        elif isinstance(icon, str):
            if os.path.isfile(icon):
                svg_path = icon
            else:
                svg_path = _icon_path(icon, True)
                if not os.path.isfile(svg_path):
                    svg_path = _icon_path(icon, False)

        if svg_path and os.path.isfile(svg_path):
            self._renderer = QSvgRenderer(svg_path)
        else:
            self._renderer = None
        self.update()

    def set_color(self, color: str):
        self._color = QColor(color)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

        if self._renderer and self._renderer.isValid():
            r = self.rect()
            if self._color:
                px = QPixmap(r.size())
                px.fill(Qt.GlobalColor.transparent)
                ip = QPainter(px)
                self._renderer.render(ip, QRectF(r))
                ip.end()
                mask = px.createMaskFromColor(QColor(0, 0, 0, 255), Qt.MaskMode.MaskOutColor)
                result = QPixmap(px.size())
                result.fill(self._color)
                result.setMask(mask)
                painter.drawPixmap(r, result)
            else:
                self._renderer.render(painter, QRectF(r))

        painter.end()


class IconLabel(QWidget):
    def __init__(self, icon=None, text: str = "", size: int = 16,
                 spacing: int = 6, parent: Optional[QWidget] = None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(spacing)

        self._icon_widget = IconWidget(icon, size)
        layout.addWidget(self._icon_widget)

        self._label = QLabel(text)
        self._label.setObjectName("iconLabel")
        layout.addWidget(self._label)

    def set_text(self, text: str):
        self._label.setText(text)

    def set_icon(self, icon):
        self._icon_widget.set_icon(icon)

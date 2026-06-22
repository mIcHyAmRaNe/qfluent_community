from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Optional

from PyQt6.QtCore import QObject, pyqtSignal


@dataclass
class ThemeTokens:
    # ── Accent ──────────────────────────────────────────────────────────
    accent: str = "#0078D4"
    accent_light: str = "#60CDFF"
    accent_dark: str = "#005A9E"

    # ── Theme surfaces (dark) ───────────────────────────────────────────
    dark_bg_primary: str = "#202020"
    dark_bg_secondary: str = "#2B2B2B"
    dark_bg_tertiary: str = "#363636"
    dark_surface: str = "#292929"
    dark_text_primary: str = "#FFFFFF"
    dark_text_secondary: str = "#ABABAB"
    dark_text_tertiary: str = "#858585"
    dark_text_disabled: str = "#5C5C5C"
    dark_border: str = "#404040"
    dark_border_light: str = "#4C4C4C"
    dark_fill_default: str = "#3B3B3B"
    dark_fill_secondary: str = "#323232"
    dark_fill_tertiary: str = "#2B2B2B"
    dark_fill_disabled: str = "#2B2B2B"
    dark_surface_raised: str = "#363636"
    dark_shadow: str = "#000000"
    dark_acrylic_tint: str = "#2C2C2C"
    dark_acrylic_luminosity: str = "#1A1A2E"

    # Win11 layer fills (placed over Mica to create the content layer)
    dark_layer_fill_default: str = "#2C2C2C"
    dark_layer_fill_alt: str = "#333333"
    dark_solid_bg_fill_base: str = "#2C2C2C"
    dark_solid_bg_fill_base_alt: str = "#333333"

    # ── Theme surfaces (light) ──────────────────────────────────────────
    light_bg_primary: str = "#FFFFFF"
    light_bg_secondary: str = "#F9F9F9"
    light_bg_tertiary: str = "#EFEFEF"
    light_surface: str = "#FFFFFF"
    light_text_primary: str = "#000000"
    light_text_secondary: str = "#616161"
    light_text_tertiary: str = "#9E9E9E"
    light_text_disabled: str = "#A0A0A0"
    light_border: str = "#D1D1D1"
    light_border_light: str = "#E5E5E5"
    light_fill_default: str = "#E0E0E0"
    light_fill_secondary: str = "#EAEAEA"
    light_fill_tertiary: str = "#F0F0F0"
    light_fill_disabled: str = "#EBEBE8"
    light_surface_raised: str = "#FFFFFF"
    light_shadow: str = "#000000"
    light_acrylic_tint: str = "#FCFCFC"
    light_acrylic_luminosity: str = "#EFEFEF"

    # Win11 layer fills (light)
    light_layer_fill_default: str = "#F3F3F3"
    light_layer_fill_alt: str = "#E8E8E8"
    light_solid_bg_fill_base: str = "#F3F3F3"
    light_solid_bg_fill_base_alt: str = "#E8E8E8"

    # ── Corner radius (Win11: 4px controls, 8px overlays) ──────────────
    radius_control: int = 4
    radius_overlay: int = 8
    radius_bar: int = 4
    radius_none: int = 0
    radius_full: int = 999

    # ── Elevation (shadow + contour) ────────────────────────────────────
    # Each value corresponds to the DWM elevation value used for shadows.
    # Stroke/contour is 1px for all elevated surfaces.
    elevation_window: int = 128
    elevation_dialog: int = 128
    elevation_flyout: int = 32
    elevation_tooltip: int = 16
    elevation_card: int = 8
    elevation_control: int = 2
    elevation_layer: int = 1
    stroke_width: int = 1

    # ── Typography (Segoe UI Variable, Win11 type ramp) ─────────────────
    font_family: str = "Segoe UI Variable,Segoe UI"
    font_size_caption: int = 12
    font_size_body: int = 14
    font_size_body_strong: int = 14
    font_size_body_large: int = 18
    font_size_body_large_strong: int = 18
    font_size_subtitle: int = 20
    font_size_title: int = 28
    font_size_title_large: int = 40
    font_size_display: int = 68
    font_weight_semibold: int = 600
    font_weight_regular: int = 400

    # ── Spacing (multiples of 4epx) ─────────────────────────────────────
    spacing_xs: int = 4
    spacing_sm: int = 8
    spacing_md: int = 12
    spacing_lg: int = 16
    spacing_xl: int = 24
    spacing_xxl: int = 32
    spacing_xxxl: int = 48
    spacing_xxxxl: int = 56

    # ── Motion timing (ms) ──────────────────────────────────────────────
    animation_duration_faster: int = 83
    animation_duration_fast: int = 167
    animation_duration_normal: int = 250
    animation_duration_slow: int = 333

    # ── Easing curves (cubic-bezier) ────────────────────────────────────
    easing_direct_entrance: str = "0,0,0,1"
    easing_existing_elements: str = "0.55,0.55,0,1"
    easing_direct_exit: str = "0,0,0,1"
    easing_gentle_exit: str = "1,0,1,1"
    easing_linear: str = "0,0,1,1"

    # ── Shadow presets ──────────────────────────────────────────────────
    # Base opacity/blur for elevation, scaled by elevation value.
    shadow_opacity_base: float = 0.10
    shadow_blur_scale: float = 1.5

    def get(self, key: str, theme: str = "dark"):
        prefix = f"{theme}_"
        full_key = f"{prefix}{key}"
        return getattr(self, full_key, getattr(self, key, None))

    def all_tokens(self, theme: str = "dark") -> dict:
        prefix = f"{theme}_"
        result = {}
        for attr_name in dir(self):
            if attr_name.startswith(prefix):
                key = attr_name[len(prefix):]
                result[key] = getattr(self, attr_name)
            elif not attr_name.startswith(("dark_", "light_", "_")):
                value = getattr(self, attr_name)
                if not callable(value):
                    result[attr_name] = value
        return result

    def as_qss_variables(self, theme: str = "dark") -> str:
        lines = []
        for key, value in self.all_tokens(theme).items():
            lines.append(f"    --{key}: {value};")
        return "\n".join(lines)


class ThemeManager(QObject):
    theme_changed = pyqtSignal()
    accent_changed = pyqtSignal(str)

    _instance = None

    @classmethod
    def instance(cls) -> "ThemeManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        super().__init__()
        self._tokens = ThemeTokens()
        self._theme: str = "dark"
        self._accent_color: str = "#0078D4"
        self._overrides: dict[str, str] = {}

    @property
    def theme(self) -> str:
        return self._theme

    def set_theme(self, theme: str):
        if theme not in ("dark", "light", "auto", "custom"):
            raise ValueError(f"Unknown theme: {theme}")
        self._theme = theme
        self.theme_changed.emit()

    def toggle_theme(self):
        self.set_theme("light" if self._theme == "dark" else "dark")

    @property
    def accent_color(self) -> str:
        return self._accent_color

    def set_accent_color(self, color: str):
        self._accent_color = color
        self.accent_changed.emit(color)
        self.theme_changed.emit()

    @property
    def tokens(self) -> ThemeTokens:
        return self._tokens

    def token(self, key: str) -> str:
        override_key = f"{self._theme}_{key}"
        if override_key in self._overrides:
            return self._overrides[override_key]
        if key in self._overrides:
            return self._overrides[key]
        return self._tokens.get(key, self._theme) or ""

    def set_token(self, key: str, value: str):
        self._overrides[key] = value
        self.theme_changed.emit()

    def load_from_dict(self, data: dict):
        for key, value in data.items():
            if hasattr(self._tokens, key):
                setattr(self._tokens, key, value)
            else:
                self._overrides[key] = str(value)
        if "accent" in data:
            self.set_accent_color(data["accent"])
        self.theme_changed.emit()

    def load_from_file(self, path: str):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        self.load_from_dict(data)

    def to_qss(self) -> str:
        return self._tokens.as_qss_variables(self._theme)

    def color(self, name: str) -> str:
        return self.token(name)

    def radius(self, kind: str = "control") -> int:
        return self._tokens.get(f"radius_{kind}", self._theme)

    def font_size(self, size: str = "body") -> int:
        return self._tokens.get(f"font_size_{size}", self._theme)

    def animation_duration(self, speed: str = "normal") -> int:
        return self._tokens.get(f"animation_duration_{speed}", self._theme)

    def elevation(self, surface: str = "control") -> int:
        return self._tokens.get(f"elevation_{surface}", self._theme)

    def spacing(self, size: str = "sm") -> int:
        return self._tokens.get(f"spacing_{size}", self._theme)

    def stroke(self) -> int:
        return self._tokens.stroke_width

    def shadow_for_elevation(self, elev: int) -> tuple:
        base_opacity = self._tokens.shadow_opacity_base
        blur = max(4, int(elev * self._tokens.shadow_blur_scale))
        offset_y = max(1, elev // 16)
        return (base_opacity, blur, offset_y)

    def easing(self, name: str = "direct_entrance") -> str:
        return self._tokens.get(f"easing_{name}", self._theme)

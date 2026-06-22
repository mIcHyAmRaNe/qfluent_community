# QFluent Community

A modern Fluent Design UI framework for PyQt6 — inspired by WinUI 3 / Windows 11.

## Philosophy

No explosion of classes. One configurable component per widget type.

```python
# Instead of this:
PrimaryPushButton()
DangerPushButton()
TransparentPushButton()
HyperlinkButton()

# Write this:
Button("Save", appearance="accent")
Button("Delete", appearance="danger")
Button("Cancel", appearance="transparent")
Button("Custom", bg_color="#881798", text_color="#FFFFFF", radius=16)
```

## Architecture

```
qfluent_community/
├── core/
│   ├── theme.py      # ThemeTokens, ThemeManager (singleton)
│   ├── style.py      # StyleEngine, QssBuilder
│   ├── animation.py  # AnimationEngine
│   ├── icon.py       # FluentIcon enum (150+ icons), IconWidget
│   ├── effects.py    # WindowEffect (DWM), AcrylicBrush, ShadowEffect, MicaController
│   └── base.py       # FluentWidget mixin
├── widgets/
│   ├── button.py     # Button (one class, 6+ appearances)
│   ├── checkbox.py   # CheckBox
│   ├── radiobutton.py # RadioButton
│   ├── switch.py     # SwitchButton
│   ├── combobox.py   # ComboBox
│   └── slider.py     # Slider
├── window/
│   ├── fluent_window.py # FluentWindow (frameless, Mica/acrylic/DWM)
│   ├── title_bar.py     # FluentTitleBar + TitleBarButton
│   └── splash_screen.py # SplashScreen
└── resources/
    └── icons/fluent/    # 137 Fluent UI SVG icons
```

## Design Tokens

All colors, fonts, radii, shadows, and animations are controlled by a central `ThemeTokens` system.

```python
theme = ThemeManager.instance()
theme.set_theme("dark")              # dark | light | auto | custom
theme.set_accent_color("#0078D4")    # any hex color
theme.toggle_theme()                 # switch dark/light
theme.set_token("radius_large", 8)  # override any token
theme.load_from_file("theme.json")   # load custom theme
```

## Components

| Component  | Parameters |
|------------|-----------|
| `Button` | `text`, `appearance`, `size`, `icon`, `radius`, `bg_color`, `text_color`, `border_color` |
| `CheckBox` | `text`, `checked`, `accent_color`, `tristate` |
| `RadioButton` | `text`, `checked`, `accent_color` |
| `SwitchButton` | `text`, `checked`, `accent_color`, `animation_duration` |
| `ComboBox` | `items`, `placeholder`, `editable`, `radius` |
| `Slider` | `orientation`, `minimum`, `maximum`, `value`, `accent_color` |
| `IconWidget` | `icon`, `size`, `color` |
| `FluentWindow` | Frameless window, title bar, DWM effects |
| `SplashScreen` | `icon`, `title`, `subtitle`, `version` |

## Button Appearances

- `default` — Standard button
- `accent` — Accent colored (primary action)
- `transparent` — No background, text only
- `outline` — Subtle border
- `danger` — Red (destructive action)
- `success` — Green (confirm action)

## Window Effects

```python
window = FluentWindow()
window.enable_mica(True)           # Windows 11 Mica
window.enable_acrylic(True)         # Acrylic blur
window.enable_blur(True)            # Classic blur
window.enable_rounded_corners()     # Win11 rounded
window.enable_dark_mode(True)       # Dark title bar
```

## Quick Start

```python
import sys
from PyQt6.QtWidgets import QApplication
from qfluent_community.window import FluentWindow
from qfluent_community.widgets import Button, CheckBox

app = QApplication(sys.argv)

window = FluentWindow()
window.set_title("My App")
window.setWindowIcon(get_fluent_icon("home"))

container = QWidget()
layout = QVBoxLayout(container)
layout.addWidget(Button("Save", appearance="accent"))
layout.addWidget(CheckBox("Remember me", checked=True))
window.set_central_widget(container)

window.show()
sys.exit(app.exec())
```

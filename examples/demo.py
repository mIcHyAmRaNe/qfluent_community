import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from qfluent_community.core.icon import FluentIcon, IconWidget, get_fluent_icon
from qfluent_community.core.style import StyleEngine
from qfluent_community.core.theme import ThemeManager
from qfluent_community.widgets import (
    Button,
    CheckBox,
    ComboBox,
    RadioButton,
    Slider,
    SwitchButton,
)
from qfluent_community.window import FluentWindow
from qfluent_community.window.splash_screen import SplashScreen


class DemoWindow(FluentWindow):
    def __init__(self):
        super().__init__()
        self.set_title("QFluent Community Demo")
        self.set_window_icon(get_fluent_icon("home"))
        self.resize(920, 680)

        theme = ThemeManager.instance()

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(16)

        title = QLabel("QFluent Community")
        title.setStyleSheet("font-size: 28px; font-weight: 600;")
        layout.addWidget(title)

        subtitle = QLabel("A modern Fluent Design UI framework for PyQt6")
        subtitle.setStyleSheet("font-size: 14px; color: #858585;")
        layout.addWidget(subtitle)

        controls = QHBoxLayout()
        theme_btn = Button("Toggle Theme", appearance="outline", size="small")
        theme_btn.clicked.connect(theme.toggle_theme)
        controls.addWidget(theme_btn)

        accent_combo = ComboBox(
            items=[
                "#0078D4 (Blue)",
                "#E81123 (Red)",
                "#107C10 (Green)",
                "#FF8C00 (Orange)",
                "#881798 (Purple)",
                "#00B7C3 (Teal)",
            ],
            radius=7,
        )
        accent_combo.setCurrentIndex(0)
        accent_combo.currentTextChanged.connect(
            lambda t: t and theme.set_accent_color(t.split(" ")[0])
        )
        controls.addWidget(accent_combo)
        controls.addStretch()
        layout.addLayout(controls)

        btn_grp = QGroupBox("Button")
        btn_layout = QVBoxLayout(btn_grp)
        r1 = QHBoxLayout()
        r1.addWidget(Button("Default"))
        r1.addWidget(Button("Accent", appearance="accent"))
        r1.addWidget(Button("Transparent", appearance="transparent"))
        r1.addWidget(Button("Outline", appearance="outline"))
        r1.addWidget(Button("Danger", appearance="danger"))
        r1.addWidget(Button("Success", appearance="success"))
        btn_layout.addLayout(r1)
        r2 = QHBoxLayout()
        r2.addWidget(Button("Small", size="small", appearance="accent"))
        r2.addWidget(Button("Medium", size="medium", appearance="accent"))
        r2.addWidget(Button("Large", size="large", appearance="accent"))
        r2.addWidget(Button("Custom", bg_color="#881798", text_color="#FFFFFF"))
        r2.addWidget(
            Button(
                "Border",
                radius=16,
                border_color="#FFAA00",
                bg_color="#2D2D2D",
                text_color="#FFAA00",
            )
        )
        btn_layout.addLayout(r2)
        layout.addWidget(btn_grp)

        input_grp = QGroupBox("Inputs")
        input_layout = QHBoxLayout(input_grp)
        col1 = QVBoxLayout()
        col1.addWidget(CheckBox("Check me"))
        col1.addWidget(CheckBox("Checked", checked=True))
        col1.addWidget(CheckBox("Tri-state", tristate=True))
        input_layout.addLayout(col1)
        col2 = QVBoxLayout()
        col2.addWidget(RadioButton("Option 1", checked=True))
        col2.addWidget(RadioButton("Option 2"))
        col2.addWidget(RadioButton("Option 3"))
        input_layout.addLayout(col2)
        col3 = QVBoxLayout()
        col3.addWidget(SwitchButton("Switch 1", checked=True))
        col3.addWidget(SwitchButton("Switch 2"))
        col3.addWidget(SwitchButton("Switch 3"))
        input_layout.addLayout(col3)
        col4 = QVBoxLayout()
        col4.addWidget(ComboBox(items=["Item 1", "Item 2", "Item 3", "Item 4"]))
        col4.addWidget(ComboBox(items=["Editable"], editable=True))
        col4.addWidget(Slider(value=50))
        input_layout.addLayout(col4)
        layout.addWidget(input_grp)

        icon_grp = QGroupBox("Icons")
        icon_layout = QHBoxLayout(icon_grp)
        for name in [
            "home",
            "settings",
            "search",
            "chat",
            "calendar",
            "delete",
            "edit",
            "save",
            "add",
            "dismiss",
            "check",
            "info",
            "alert",
            "mail",
            "heart",
        ]:
            iw = IconWidget(
                getattr(FluentIcon, name.upper().replace("-", "_")), size=24
            )
            iw.setToolTip(name)
            icon_layout.addWidget(iw)
        icon_layout.addStretch()
        layout.addWidget(icon_grp)

        self.set_central_widget(container)

    def show_with_splash(self):
        splash = SplashScreen(
            icon=get_fluent_icon("home"),
            title="QFluent Community",
            subtitle="Loading...",
            version="0.1.0",
        )
        splash.show()
        from PyQt6.QtCore import QTimer

        for i in range(0, 101, 20):
            QTimer.singleShot(
                i * 15, lambda v=i: splash.set_progress(v, f"Loading... {v}%")
            )

        QTimer.singleShot(1800, splash.finish)
        QTimer.singleShot(1900, self.show)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    theme = ThemeManager.instance()
    theme.set_theme("light")

    window = DemoWindow()
    window.show()

    sys.exit(app.exec())

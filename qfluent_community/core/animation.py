from __future__ import annotations

from typing import Optional, Callable

from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QAbstractAnimation, pyqtProperty
from PyQt6.QtWidgets import QWidget

from qfluent_community.core.theme import ThemeManager


class AnimationEngine:
    _tm = ThemeManager.instance()

    @staticmethod
    def _duration(speed: str = "normal") -> int:
        return AnimationEngine._tm.animation_duration(speed)

    @staticmethod
    def _easing(name: str = "direct_entrance") -> QEasingCurve:
        mapping = {
            "direct_entrance": QEasingCurve.Type.OutCubic,
            "existing_elements": QEasingCurve.Type.OutCubic,
            "direct_exit": QEasingCurve.Type.InCubic,
            "gentle_exit": QEasingCurve.Type.InCubic,
            "linear": QEasingCurve.Type.Linear,
        }
        return mapping.get(name, QEasingCurve.Type.OutCubic)

    @staticmethod
    def fade_in(widget: QWidget, duration: int = None, callback: Optional[Callable] = None):
        d = duration or AnimationEngine._duration("normal")
        widget.setWindowOpacity(0.0)
        anim = QPropertyAnimation(widget, b"windowOpacity")
        anim.setDuration(d)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(AnimationEngine._easing("direct_entrance"))
        if callback:
            anim.finished.connect(callback)
        anim.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
        return anim

    @staticmethod
    def fade_out(widget: QWidget, duration: int = None, callback: Optional[Callable] = None):
        d = duration or AnimationEngine._duration("fast")
        anim = QPropertyAnimation(widget, b"windowOpacity")
        anim.setDuration(d)
        anim.setStartValue(widget.windowOpacity())
        anim.setEndValue(0.0)
        anim.setEasingCurve(AnimationEngine._easing("direct_exit"))
        if callback:
            anim.finished.connect(callback)
        anim.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
        return anim

    @staticmethod
    def slide(widget: QWidget, start_x: int, end_x: int,
              start_y: int = 0, end_y: int = 0,
              duration: int = None):
        d = duration or AnimationEngine._duration("normal")
        anim = QPropertyAnimation(widget, b"pos")
        anim.setDuration(d)
        anim.setStartValue(widget.pos())
        anim.setEndValue(widget.pos() + __import__('PyQt6').QtCore.QPoint(end_x - start_x, end_y - start_y))
        anim.setEasingCurve(AnimationEngine._easing("existing_elements"))
        anim.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
        return anim

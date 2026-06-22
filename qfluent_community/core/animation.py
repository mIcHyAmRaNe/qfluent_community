from __future__ import annotations

from typing import Optional, Callable

from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QAbstractAnimation, pyqtProperty
from PyQt6.QtWidgets import QWidget


class AnimationEngine:
    @staticmethod
    def fade_in(widget: QWidget, duration: int = 267, callback: Optional[Callable] = None):
        widget.setWindowOpacity(0.0)
        anim = QPropertyAnimation(widget, b"windowOpacity")
        anim.setDuration(duration)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        if callback:
            anim.finished.connect(callback)
        anim.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
        return anim

    @staticmethod
    def fade_out(widget: QWidget, duration: int = 167, callback: Optional[Callable] = None):
        anim = QPropertyAnimation(widget, b"windowOpacity")
        anim.setDuration(duration)
        anim.setStartValue(widget.windowOpacity())
        anim.setEndValue(0.0)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        if callback:
            anim.finished.connect(callback)
        anim.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
        return anim

    @staticmethod
    def slide(widget: QWidget, start_x: int, end_x: int,
              start_y: int = 0, end_y: int = 0,
              duration: int = 267):
        anim = QPropertyAnimation(widget, b"pos")
        anim.setDuration(duration)
        anim.setStartValue(widget.pos())
        anim.setEndValue(widget.pos() + __import__('PyQt6').QtCore.QPoint(end_x - start_x, end_y - start_y))
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
        return anim

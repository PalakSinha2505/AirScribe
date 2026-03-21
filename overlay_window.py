# overlay_window.py
import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint
import win32gui

class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)  # click-through
        self.showFullScreen()

        self.lines = []  # [(startQPoint, endQPoint, color, thickness)]
        self.prev_window = None
        self.prev_draw = None

    def draw_line(self, start, end, color=(255, 0, 0), thickness=4):
        """Draw a line on overlay if movement is significant"""
        self.check_window_change()
        if start is not None and end is not None:
            dx = abs(end[0] - start[0])
            dy = abs(end[1] - start[1])
            if dx > 2 or dy > 2:  # ignore tiny jitter
                self.lines.append((QPoint(*start), QPoint(*end), QColor(*color), thickness))
                self.update()
                self.prev_draw = end

    def check_window_change(self):
        """Clear canvas if active window changes"""
        active_window = win32gui.GetForegroundWindow()
        if active_window != self.prev_window:
            self.lines.clear()
            self.prev_draw = None
            self.prev_window = active_window
            self.update()  # repaint empty canvas

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for line in self.lines:
            start, end, color, thickness = line
            pen = QPen(color, thickness, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(start, end)
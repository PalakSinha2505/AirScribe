import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint
import win32gui


class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()

        # ---------------- WINDOW SETUP ----------------
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)  # click-through
        self.showFullScreen()

        # ---------------- DRAW STATE ----------------
        self.lines = []  # (start, end, color, thickness)

        self.prev_window = None
        self.prev_draw = None

        # Optional safety limit (prevents memory explosion)
        self.MAX_LINES = 5000

    # ---------------- DRAW FUNCTION ----------------
    def draw_line(self, start, end, color=(255, 0, 0), thickness=4):
        """Draw a smooth line segment on overlay"""

        self.check_window_change()

        # Validate inputs
        if not start or not end:
            return

        # Ignore tiny jitter movements
        dx = abs(end[0] - start[0])
        dy = abs(end[1] - start[1])

        if dx < 2 and dy < 2:
            return

        # Add line
        self.lines.append(
            (
                QPoint(int(start[0]), int(start[1])),
                QPoint(int(end[0]), int(end[1])),
                QColor(*color),
                thickness
            )
        )

        # Prevent memory overload
        if len(self.lines) > self.MAX_LINES:
            self.lines = self.lines[-self.MAX_LINES:]

        self.prev_draw = end

        # Trigger repaint (optimized)
        self.update()

    # ---------------- WINDOW CONTEXT CHECK ----------------
    def check_window_change(self):
        """Clear canvas when user switches active application"""

        try:
            active_window = win32gui.GetForegroundWindow()
        except Exception:
            return

        # Only clear if actual change detected
        if active_window != self.prev_window:
            self.lines.clear()
            self.prev_draw = None
            self.prev_window = active_window
            self.update()

    # ---------------- RENDERING ----------------
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for start, end, color, thickness in self.lines:
            pen = QPen(color, thickness)
            pen.setCapStyle(Qt.RoundCap)
            pen.setJoinStyle(Qt.RoundJoin)

            painter.setPen(pen)
            painter.drawLine(start, end)
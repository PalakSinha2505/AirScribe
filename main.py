import sys
import cv2
import pyautogui
from PyQt5.QtWidgets import QApplication

from tracking.hand_tracker import HandTracker
from core.smoothing import Smoother
from control.mouse_controller import MouseController
from overlay_window import OverlayWindow


# -------------------- INIT --------------------
app = QApplication(sys.argv)
overlay = OverlayWindow()

hand_tracker = HandTracker()
smoother = Smoother(alpha=0.2)
mouse = MouseController()

cap = cv2.VideoCapture(0)

# Force stable camera settings (IMPORTANT FIX)
CAM_W, CAM_H = 640, 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_W)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_H)

screen_w, screen_h = pyautogui.size()

# -------------------- STATES --------------------
pinching = False
prev_draw = None
eraser_mode = False
prev_scroll_y = None

# Scroll tuning
SCROLL_THRESHOLD = 80
SCROLL_SPEED = 8
MIN_DELTA = 2


# -------------------- MAIN LOOP --------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hand_tracker.process(rgb)

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]
        landmarks = hand_tracker.get_landmarks(hand, frame.shape)

        # ---------------- PINCH DETECTION ----------------
        is_pinch, _ = hand_tracker.is_pinching(landmarks)

        if is_pinch and not pinching:
            mouse.click()
            pinching = True
        elif not is_pinch:
            pinching = False

        # ---------------- CURSOR CONTROL ----------------
        ix, iy = landmarks[8]

        sx, sy = smoother.smooth(ix, iy)

        # Normalize safely (avoid division by zero)
        screen_x = int((sx / CAM_W) * screen_w)
        screen_y = int((sy / CAM_H) * screen_h)

        mouse.move(sx, sy, CAM_W, CAM_H)

        # ---------------- SCROLL CONTROL ----------------
        mx, my = landmarks[12]

        finger_dist = ((ix - mx) ** 2 + (iy - my) ** 2) ** 0.5
        avg_y = (iy + my) / 2

        if finger_dist > SCROLL_THRESHOLD:
            if prev_scroll_y is not None:
                delta = prev_scroll_y - avg_y
                if abs(delta) > MIN_DELTA:
                    pyautogui.scroll(int(delta * SCROLL_SPEED))
            prev_scroll_y = avg_y
        else:
            prev_scroll_y = None

        # ---------------- DRAWING / ERASER ----------------
        if is_pinch:
            color = (255, 255, 255) if eraser_mode else (0, 0, 255)
            thickness = 15 if eraser_mode else 4

            current_point = (screen_x, screen_y)

            if overlay.prev_draw is not None:
                overlay.draw_line(
                    overlay.prev_draw,
                    current_point,
                    color=color,
                    thickness=thickness
                )

            overlay.prev_draw = current_point
        else:
            overlay.prev_draw = None

    else:
        overlay.prev_draw = None
        prev_scroll_y = None

    # ---------------- DEBUG WINDOW ----------------
    cv2.imshow("Hand Tracking (Debug)", frame)

    # ---------------- KEY CONTROLS ----------------
    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC
        break

    elif key in [ord('e'), ord('E')]:
        eraser_mode = not eraser_mode

# -------------------- CLEANUP --------------------
cap.release()
cv2.destroyAllWindows()
sys.exit(app.exec_())
# main.py
import sys
import cv2
import pyautogui
from PyQt5.QtWidgets import QApplication
from tracking.hand_tracker import HandTracker
from core.smoothing import Smoother
from control.mouse_controller import MouseController
from overlay_window import OverlayWindow

# --- PyQt Overlay ---
app = QApplication(sys.argv)
overlay = OverlayWindow()

# --- Hand Tracking ---
hand_tracker = HandTracker()
smoother = Smoother(alpha=0.2)
mouse = MouseController()
cap = cv2.VideoCapture(0)

# States
pinching = False
prev_draw = None
eraser_mode = False  # toggle with keyboard

# Scroll parameters
SCROLL_THRESHOLD = 80
SCROLL_SPEED = 8
MIN_DELTA = 2
prev_scroll_y = None

screen_w, screen_h = pyautogui.size()
cam_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
cam_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# --- Main Loop ---
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hand_results = hand_tracker.process(rgb)

    if hand_results.multi_hand_landmarks:
        hand = hand_results.multi_hand_landmarks[0]
        landmarks = hand_tracker.get_landmarks(hand, frame.shape)

        # Pinch detection
        is_pinch, dist = hand_tracker.is_pinching(landmarks)

        # Mouse click
        if is_pinch and not pinching:
            mouse.click()
            pinching = True
        elif not is_pinch:
            pinching = False

        # Cursor mapping
        cursor_x, cursor_y = landmarks[8]
        sx, sy = smoother.smooth(cursor_x, cursor_y)
        screen_x = int(sx * screen_w / cam_w)
        screen_y = int(sy * screen_h / cam_h)
        mouse.move(sx, sy, cam_w, cam_h)

        # Scroll
        index_x, index_y = landmarks[8]
        middle_x, middle_y = landmarks[12]
        finger_dist = ((index_x - middle_x)**2 + (index_y - middle_y)**2)**0.5
        avg_y = (index_y + middle_y) / 2
        if finger_dist > SCROLL_THRESHOLD:
            if prev_scroll_y is not None:
                delta = prev_scroll_y - avg_y
                if abs(delta) > MIN_DELTA:
                    pyautogui.scroll(int(delta * SCROLL_SPEED))
            prev_scroll_y = avg_y
        else:
            prev_scroll_y = None

        # Draw / Eraser
        if is_pinch:
            color = (255, 255, 255) if eraser_mode else (255, 0, 0)
            thickness = 15 if eraser_mode else 4
            if overlay.prev_draw is not None:
                overlay.draw_line(overlay.prev_draw, (screen_x, screen_y), color=color, thickness=thickness)
            else:
                overlay.prev_draw = (screen_x, screen_y)
        else:
            overlay.prev_draw = None
    else:
        overlay.prev_draw = None
        prev_scroll_y = None

    # Show camera for debugging
    cv2.imshow("Hand Tracking (Debug)", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break
    elif key == ord('e') or key == ord('E'):  # toggle eraser
        eraser_mode = not eraser_mode

cap.release()
cv2.destroyAllWindows()
sys.exit(app.exec_())
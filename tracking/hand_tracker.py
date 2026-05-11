import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

    def process(self, frame_rgb):
        return self.hands.process(frame_rgb)

    def get_landmarks(self, hand_landmarks, frame_shape):
        h, w, _ = frame_shape
        points = []

        for lm in hand_landmarks.landmark:
            points.append((int(lm.x * w), int(lm.y * h)))

        return points

    def is_pinching(self, landmarks):
        # Safety check
        if len(landmarks) < 9:
            return False, 999

        # Thumb tip (4) & index tip (8)
        x1, y1 = landmarks[4]
        x2, y2 = landmarks[8]

        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        # Normalized pinch threshold 
        threshold = 50

        return distance < threshold, distance
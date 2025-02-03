import os
import logging
import cv2
import mediapipe as mp
import numpy as np

# Suppress TensorFlow and oneDNN warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

logging.getLogger('mediapipe').setLevel(logging.ERROR)

class HandGestureRecognizer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )

    def calculate_angle(self, a, b, c):
        """Calculate angle between three points."""
        a = np.array([a.x, a.y])
        b = np.array([b.x, b.y])
        c = np.array([c.x, c.y])

        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
        return np.degrees(angle)

    def recognize_gesture(self, hand_landmarks):
        """Recognizes different hand gestures."""
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
        wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]

        # Calculate key angles
        index_middle_angle = self.calculate_angle(
            hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP],
            hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP],
            hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP]
        )
        
        thumb_index_distance = np.linalg.norm(
            np.array([thumb_tip.x, thumb_tip.y]) - np.array([index_tip.x, index_tip.y])
        )
        # 👍 Thumbs Up (Thumb extended, other fingers curled)
        if thumb_tip.y < wrist.y and all(tip.y > hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].y for tip in [index_tip, middle_tip, ring_tip, pinky_tip]):
            return "👍 Thumbs Up"

        # ✌️ Peace Sign (Index and Middle fingers up, others curled)
        if index_tip.y < wrist.y and middle_tip.y < wrist.y and \
           ring_tip.y > hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP].y and \
           pinky_tip.y > hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_MCP].y:
            return "✌️ Peace Sign"

        # 👊 Fist (All fingers curled close to the wrist)
        if all(tip.y > wrist.y for tip in [thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip]):
            return "👊 Fist"

        # 🤘 Rock Sign (Index and pinky extended, middle and ring curled)
        if index_tip.y < middle_tip.y and pinky_tip.y < middle_tip.y and \
           ring_tip.y > middle_tip.y:
            return "🤘 Rock Sign"

        # 👌 OK Sign (Thumb and index forming a circle, others extended)
        if thumb_index_distance < 0.05 and all(tip.y < wrist.y for tip in [middle_tip, ring_tip, pinky_tip]):
            return "👌 OK Sign"

        # 🖐️ Open Palm (All fingers fully extended)
        if all(tip.y < wrist.y for tip in [thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip]) and \
           all(tip.y < hand_landmarks.landmark[finger_mcp].y for tip, finger_mcp in zip(
               [index_tip, middle_tip, ring_tip, pinky_tip], 
               [self.mp_hands.HandLandmark.INDEX_FINGER_MCP, 
                self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
                self.mp_hands.HandLandmark.RING_FINGER_MCP,
                self.mp_hands.HandLandmark.PINKY_MCP])):
            return "🖐️ Open Palm"

        return "Gesture not recognized"

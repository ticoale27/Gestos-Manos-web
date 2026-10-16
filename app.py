import cv2
import math
import time
from collections import Counter, deque
from enum import Enum
from typing import Deque, Dict, List, Optional, Tuple

import mediapipe as mp
import numpy as np
import streamlit as st
from streamlit_webrtc import RTCConfiguration, VideoProcessorBase, webrtc_streamer

st.set_page_config(page_title="Control por Gestos - Demo Web", layout="wide")

st.title("🖐️ Control por Gestos (Lógica Avanzada)")
st.write(
    "Haz clic en **Start** para activar la cámara. La app analiza la orientación de tu índice, "
    "palma/dorso y aplica un algoritmo de estabilización anti-falsos positivos."
)

# ----------------------------------------------------------------------------
# Lógica y Parámetros
# ----------------------------------------------------------------------------
EXTENDED_RATIO = 1.5
DIRECTION_TOLERANCE_DEG = 35.0
STAB_WINDOW = 10
STAB_ENTER_RATIO = 0.7
STAB_EXIT_RATIO = 0.3

WRIST = 0
INDEX_MCP = 5
PINKY_MCP = 17

FINGERS: Dict[str, Tuple[int, int]] = {
    "index": (5, 8),
    "middle": (9, 12),
    "ring": (13, 16),
    "pinky": (17, 20),
}

Point = Tuple[float, float]


class Gesture(Enum):
    FIST = "PUNO CERRADO"
    OPEN_PALM = "MANO ABIERTA"
    POINT_UP = "INDICE ARRIBA"
    POINT_RIGHT = "INDICE DERECHA"
    POINT_LEFT = "INDICE IZQUIERDA"


def _dist(a: Point, b: Point) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def fingers_extended(pts: List[Point]) -> Optional[Dict[str, bool]]:
    wrist = pts[WRIST]
    states: Dict[str, bool] = {}
    for name, (mcp, tip) in FINGERS.items():
        base = _dist(pts[mcp], wrist)
        if base < 1e-6:
            return None
        states[name] = (_dist(pts[tip], wrist) / base) > EXTENDED_RATIO
    return states


def palm_faces_camera(pts: List[Point], handedness: Optional[str]) -> bool:
    if handedness not in ("Left", "Right"):
        return False
    ax, ay = pts[INDEX_MCP][0] - pts[WRIST][0], pts[INDEX_MCP][1] - pts[WRIST][1]
    bx, by = pts[PINKY_MCP][0] - pts[WRIST][0], pts[PINKY_MCP][1] - pts[WRIST][1]
    cross = ax * by - ay * bx
    return cross > 0 if handedness == "Right" else cross < 0


def index_direction_deg(pts: List[Point]) -> float:
    dx = pts[8][0] - pts[INDEX_MCP][0]
    dy_up = -(pts[8][1] - pts[INDEX_MCP][1])
    return math.degrees(math.atan2(dy_up, dx))


def classify_gesture(pts: List[Point], handedness: Optional[str]) -> Optional[Gesture]:
    ext = fingers_extended(pts)
    if ext is None:
        return None
    count = sum(ext.values())

    if count == 0:
        return Gesture.FIST

    if count == 4:
        return Gesture.OPEN_PALM if palm_faces_camera(pts, handedness) else None

    if count == 1 and ext["index"]:
        angle = index_direction_deg(pts)
        if abs(angle - 90.0) <= DIRECTION_TOLERANCE_DEG:
            return Gesture.POINT_UP
        if abs(angle) <= DIRECTION_TOLERANCE_DEG:
            return Gesture.POINT_RIGHT
        if abs(angle) >= 180.0 - DIRECTION_TOLERANCE_DEG:
            return Gesture.POINT_LEFT

    return None


class GestureStabilizer:
    def __init__(self, window: int = STAB_WINDOW, enter_ratio: float = STAB_ENTER_RATIO, exit_ratio: float = STAB_EXIT_RATIO):
        self._buf: Deque[Optional[Gesture]] = deque(maxlen=window)
        self._window = window
        self._enter = enter_ratio
        self._exit = exit_ratio
        self.current: Optional[Gesture] = None

    def update(self, raw: Optional[Gesture]) -> Optional[Gesture]:
        self._buf.append(raw)
        counts = Counter(g for g in self._buf if g is not None)

        if counts:
            candidate, n = counts.most_common(1)[0]
            if n / self._window >= self._enter:
                self.current = candidate
                return self.current

        if self.current is not None and counts[self.current] / self._window < self._exit:
            self.current = None
        return self.current


# ----------------------------------------------------------------------------
# Importaciones de MediaPipe
# ----------------------------------------------------------------------------
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


# ----------------------------------------------------------------------------
# Procesador de Video de Streamlit WebRTC
# ----------------------------------------------------------------------------
class AdvancedGestureProcessor(VideoProcessorBase):
    def __init__(self):
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
        )
        self.stabilizer = GestureStabilizer()

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1)  # Modo espejo
        height, width = img.shape[:2]
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = self.hands.process(img_rgb)

        raw_gesture = None
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = results.multi_hand_landmarks[0].landmark
            pts = [(p.x * width, p.y * height) for p in landmarks]
            label = None
            if results.multi_handedness:
                label = results.multi_handedness[0].classification[0].label

            raw_gesture = classify_gesture(pts, label)

        stable_gesture = self.stabilizer.update(raw_gesture)

        # Dibujar HUD
        text = stable_gesture.value if stable_gesture else "SIN GESTO"
        color = (0, 255, 0) if stable_gesture else (180, 180, 180)

        cv2.rectangle(img, (10, 10), (480, 60), (0, 0, 0), -1)
        cv2.putText(img, f"Gesto: {text}", (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA)

        return frame.from_ndarray(img, format="bgr24")


# Servidor STUN público de Google para negociar conexiones WebRTC en Streamlit Cloud
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

webrtc_streamer(
    key="advanced-gesture-detection",
    video_processor_factory=AdvancedGestureProcessor,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True, "audio": False},
)

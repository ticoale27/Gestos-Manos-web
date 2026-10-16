import cv2
import math
from enum import Enum
from typing import Dict, List, Optional, Tuple
import numpy as np
import streamlit as st
import mediapipe as mp

st.set_page_config(page_title="Control por Gestos - Demo Web", layout="wide")

st.title("🖐️ Control por Gestos con Visión Computacional")
st.write(
    "Aplicación de clasificación de gestos en tiempo real utilizando OpenCV y MediaPipe. "
    "Puedes tomar una captura con tu cámara web o subir una imagen."
)

# Carga optimizada del modelo MediaPipe en caché
@st.cache_resource
def load_hand_detector():
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    detector = mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=1,
        min_detection_confidence=0.5
    )
    return detector, mp_hands, mp_drawing

# Lógica de detección geométrica de gestos
EXTENDED_RATIO = 1.5
DIRECTION_TOLERANCE_DEG = 35.0
WRIST, INDEX_MCP, PINKY_MCP = 0, 5, 17
FINGERS = {"index": (5, 8), "middle": (9, 12), "ring": (13, 16), "pinky": (17, 20)}
Point = Tuple[float, float]

class Gesture(Enum):
    FIST = "PUÑO CERRADO"
    OPEN_PALM = "MANO ABIERTA"
    POINT_UP = "ÍNDICE ARRIBA"
    POINT_RIGHT = "ÍNDICE DERECHA"
    POINT_LEFT = "ÍNDICE IZQUIERDA"

def _dist(a: Point, b: Point) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])

def fingers_extended(pts: List[Point]) -> Optional[Dict[str, bool]]:
    wrist = pts[WRIST]
    states = {}
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

def process_frame(cv_img):
    detector, mp_hands, mp_drawing = load_hand_detector()
    height, width = cv_img.shape[:2]
    img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    results = detector.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(cv_img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        landmarks = results.multi_hand_landmarks[0].landmark
        pts = [(p.x * width, p.y * height) for p in landmarks]
        label = results.multi_handedness[0].classification[0].label if results.multi_handedness else None
        detected = classify_gesture(pts, label)
        gesture_text = detected.value if detected else "SIN GESTO RECONOCIDO"
    else:
        gesture_text = "NO SE DETECTÓ NINGUNA MANO"

    return cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB), gesture_text

# Interfaz en dos columnas
col1, col2 = st.columns(2)

with col1:
    st.subheader("📷 Capturar con la Cámara")
    camera_img = st.camera_input("Haz un gesto hacia la cámara y presiona 'Tomar foto'")
    if camera_img is not None:
        bytes_data = camera_img.getvalue()
        cv_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        res_img, text = process_frame(cv_img)
        st.image(res_img, caption="Análisis en Tiempo Real", use_column_width=True)
        st.success(f"Gesto Detectado: **{text}**")

with col2:
    st.subheader("📁 Cargar Imagen")
    uploaded_file = st.file_uploader("Sube una imagen de una mano (JPG/PNG)", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        cv_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        res_img, text = process_frame(cv_img)
        st.image(res_img, caption="Análisis de Imagen", use_column_width=True)
        st.success(f"Gesto Detectado: **{text}**")

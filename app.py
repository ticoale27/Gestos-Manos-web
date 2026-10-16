import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Control por Gestos en Vivo", layout="wide")

st.title("🖐️ Control por Gestos en Tiempo Real (Demo en Vivo)")
st.write(
    "Reconocimiento de gestos a 30 FPS procesado directamente desde la webcam. "
    "Acepta el permiso de la cámara si el navegador lo solicita."
)

# Código HTML5 + JavaScript embebido con MediaPipe Hands
html_code = """
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js" crossorigin="anonymous"></script>
  <style>
    body {
      margin: 0;
      background-color: #0e1117;
      color: white;
      font-family: system-ui, -apple-system, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }
    .container {
      position: relative;
      width: 640px;
      height: 480px;
      margin-top: 10px;
    }
    video { display: none; }
    canvas {
      width: 640px;
      height: 480px;
      transform: scaleX(-1);
      border-radius: 12px;
      box-shadow: 0 8px 20px rgba(0,0,0,0.6);
      border: 2px solid #262730;
    }
    #hud {
      position: absolute;
      top: 20px;
      left: 20px;
      background: rgba(0, 0, 0, 0.85);
      color: #00ff00;
      padding: 12px 24px;
      font-size: 22px;
      font-weight: bold;
      border-radius: 8px;
      border: 2px solid #00ff00;
      letter-spacing: 1px;
      box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
  </style>
</head>
<body>
  <div class="container">
    <video id="webcam" autoplay playsinline></video>
    <canvas id="output_canvas" width="640" height="480"></canvas>
    <div id="hud">Gesto: INICIALIZANDO CÁMARA...</div>
  </div>

  <script>
    const videoElement = document.getElementById('webcam');
    const canvasElement = document.getElementById('output_canvas');
    const canvasCtx = canvasElement.getContext('2d');
    const hud = document.getElementById('hud');

    function dist(a, b) {
      return Math.hypot(a.x - b.x, a.y - b.y);
    }

    function classifyGesture(landmarks) {
      const wrist = landmarks[0];
      const indexMcp = landmarks[5], indexTip = landmarks[8];
      const middleMcp = landmarks[9], middleTip = landmarks[12];
      const ringMcp = landmarks[13], ringTip = landmarks[16];
      const pinkyMcp = landmarks[17], pinkyTip = landmarks[20];

      function isExt(mcp, tip) {
        const base = dist(mcp, wrist);
        if (base < 1e-5) return false;
        return (dist(tip, wrist) / base) > 1.45;
      }

      const extIdx = isExt(indexMcp, indexTip);
      const extMid = isExt(middleMcp, middleTip);
      const extRng = isExt(ringMcp, ringTip);
      const extPnk = isExt(pinkyMcp, pinkyTip);

      const count = (extIdx?1:0) + (extMid?1:0) + (extRng?1:0) + (extPnk?1:0);

      if (count === 0) return "PUÑO CERRADO";
      if (count === 4) return "MANO ABIERTA";
      if (count === 1 && extIdx) {
        // Invertimos dx para que coincida con el modo espejo del video
        const dx = -(indexTip.x - indexMcp.x);
        const dy = -(indexTip.y - indexMcp.y);
        let angle = Math.atan2(dy, dx) * (180 / Math.PI);

        if (Math.abs(angle - 90) <= 35) return "ÍNDICE ARRIBA";
        if (Math.abs(angle) <= 35) return "ÍNDICE DERECHA";
        if (Math.abs(angle) >= 145) return "ÍNDICE IZQUIERDA";
      }
      return "GESTO NO RECONOCIDO";
    }

    function onResults(results) {
      canvasCtx.save();
      canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
      canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

      if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
        for (const landmarks of results.multiHandLandmarks) {
          drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS, {color: '#00FF00', lineWidth: 4});
          drawLandmarks(canvasCtx, landmarks, {color: '#FF0000', lineWidth: 2, radius: 4});
        }
        const gesture = classifyGesture(results.multiHandLandmarks[0]);
        hud.innerText = "Gesto: " + gesture;
        hud.style.color = "#00FF00";
        hud.style.borderColor = "#00FF00";
      } else {
        hud.innerText = "Gesto: BUSCANDO MANO...";
        hud.style.color = "#aaaaaa";
        hud.style.borderColor = "#aaaaaa";
      }
      canvasCtx.restore();
    }

    const hands = new Hands({
      locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
    });

    hands.setOptions({
      maxNumHands: 1,
      modelComplexity: 1,
      minDetectionConfidence: 0.6,
      minTrackingConfidence: 0.6
    });

    hands.onResults(onResults);

    const camera = new Camera(videoElement, {
      onFrame: async () => {
        await hands.send({image: videoElement});
      },
      width: 640,
      height: 480
    });
    camera.start();
  </script>
</body>
</html>
"""

# Renderizar el componente en Streamlit
components.html(html_code, height=520)

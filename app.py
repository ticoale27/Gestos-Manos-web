import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Control por Gestos en Vivo", layout="wide")

st.title("🖐️ Control por Gestos en Tiempo Real (Demo en Vivo)")
st.write(
    "Reconocimiento de gestos a 30 FPS procesado directamente desde la webcam. "
    "Muestra tu mano a la cámara para ver la clasificación en vivo."
)

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
      z-index: 10;
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
      
      // Puntas de los dedos y nudillos medios (PIP)
      const fingers = [
        { tip: landmarks[8],  pip: landmarks[6]  }, // Índice
        { tip: landmarks[12], pip: landmarks[10] }, // Medio
        { tip: landmarks[16], pip: landmarks[14] }, // Anular
        { tip: landmarks[20], pip: landmarks[18] }  // Meñique
      ];

      // Un dedo está extendido si la punta está más lejos de la muñeca que su nudillo medio
      const extended = fingers.map(f => dist(f.tip, wrist) > (dist(f.pip, wrist) * 1.05));

      const extIdx = extended[0];
      const extMid = extended[1];
      const extRng = extended[2];
      const extPnk = extended[3];

      const count = extended.filter(Boolean).length;

      if (count === 0) return "PUÑO CERRADO";
      if (count === 4) return "MANO ABIERTA";

      if (count === 1 && extIdx) {
        const indexMcp = landmarks[5];
        const indexTip = landmarks[8];
        
        // Vectores horizontal y vertical ajustados al modo espejo
        const dx = indexTip.x - indexMcp.x;
        const dy = indexMcp.y - indexTip.y; // positivo hacia arriba
        
        let angle = Math.atan2(dy, dx) * (180 / Math.PI);

        if (Math.abs(angle - 90) <= 35) return "ÍNDICE ARRIBA";
        if (Math.abs(angle) <= 35) return "ÍNDICE IZQUIERDA";
        if (Math.abs(angle) >= 145 || Math.abs(angle) <= -145) return "ÍNDICE DERECHA";
      }

      return "GESTO RECONOCIDO";
    }

    function onResults(results) {
      try {
        canvasCtx.save();
        canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
        
        // Modo espejo en canvas
        canvasCtx.translate(canvasElement.width, 0);
        canvasCtx.scale(-1, 1);
        canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

        if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
          const landmarks = results.multiHandLandmarks[0];
          
          if (typeof drawConnectors !== 'undefined' && typeof HAND_CONNECTIONS !== 'undefined') {
            drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS, {color: '#00FF00', lineWidth: 4});
          }
          if (typeof drawLandmarks !== 'undefined') {
            drawLandmarks(canvasCtx, landmarks, {color: '#FF0000', lineWidth: 2, radius: 4});
          }

          canvasCtx.restore();

          const gesture = classifyGesture(landmarks);
          hud.innerText = "Gesto: " + gesture;
          hud.style.color = "#00FF00";
          hud.style.borderColor = "#00FF00";
        } else {
          canvasCtx.restore();
          hud.innerText = "Gesto: BUSCANDO MANO...";
          hud.style.color = "#aaaaaa";
          hud.style.borderColor = "#aaaaaa";
        }
      } catch (err) {
        console.error(err);
        hud.innerText = "Error: " + err.message;
      }
    }

    const hands = new Hands({
      locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
    });

    hands.setOptions({
      maxNumHands: 1,
      modelComplexity: 1,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5
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

components.html(html_code, height=520)

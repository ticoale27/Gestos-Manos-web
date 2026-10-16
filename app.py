import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Control por Gestos - Diapositivas", layout="wide")

st.title("🖐️ Control Remoto por Gestos en Tiempo Real")
st.write(
    "Usa tu mano frente a la cámara para navegar entre las pestañas de la presentación: "
    "👉 **Derecha** (Siguiente), 👈 **Izquierda** (Anterior), 🖐️ **Mano Abierta** (Inicio)."
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
      flex-direction: row;
      gap: 20px;
      padding: 10px;
    }
    
    /* Panel de la Cámara */
    .cam-container {
      position: relative;
      width: 480px;
      height: 360px;
      flex-shrink: 0;
    }
    video { display: none; }
    canvas {
      width: 480px;
      height: 360px;
      border-radius: 12px;
      border: 2px solid #262730;
      box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    #hud {
      position: absolute;
      top: 15px;
      left: 15px;
      background: rgba(0, 0, 0, 0.85);
      color: #00ff00;
      padding: 8px 16px;
      font-size: 16px;
      font-weight: bold;
      border-radius: 6px;
      border: 2px solid #00ff00;
      z-index: 10;
    }

    /* Panel de Presentación / Pestañas */
    .presentation-container {
      flex-grow: 1;
      background: #161b22;
      border: 2px solid #30363d;
      border-radius: 12px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      height: 320px;
    }

    .tabs-header {
      display: flex;
      gap: 10px;
      border-bottom: 2px solid #30363d;
      padding-bottom: 10px;
    }

    .tab-btn {
      padding: 8px 16px;
      background: #21262d;
      border: none;
      color: #8b949e;
      border-radius: 6px;
      font-weight: bold;
      font-size: 14px;
    }

    .tab-btn.active {
      background: #238636;
      color: white;
    }

    .slide-content {
      display: none;
      animation: fadeIn 0.3s ease-in-out;
    }

    .slide-content.active {
      display: block;
    }

    .slide-title {
      color: #58a6ff;
      margin-top: 0;
      font-size: 24px;
    }

    .slide-body {
      color: #c9d1d9;
      font-size: 16px;
      line-height: 1.5;
    }

    .action-flash {
      color: #ffa657;
      font-weight: bold;
      font-size: 14px;
      height: 20px;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(5px); }
      to { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>
<body>

  <!-- Izquierda: Cámara y Reconocimiento -->
  <div class="cam-container">
    <video id="webcam" autoplay playsinline></video>
    <canvas id="output_canvas" width="480" height="360"></canvas>
    <div id="hud">Cámara: Iniciando...</div>
  </div>

  <!-- Derecha: Pestañas Interactivas -->
  <div class="presentation-container">
    <div>
      <div class="tabs-header">
        <div class="tab-btn active" id="tab-0">1. Inicio</div>
        <div class="tab-btn" id="tab-1">2. Arquitectura</div>
        <div class="tab-btn" id="tab-2">3. Algoritmo</div>
        <div class="tab-btn" id="tab-3">4. Conclusión</div>
      </div>

      <!-- Diapositiva 1 -->
      <div class="slide-content active" id="slide-0">
        <h2 class="slide-title">👋 Proyecto: Control por Gestos</h2>
        <p class="slide-body">
          ¡Bienvenido a la presentación interactiva!<br><br>
          • Apunta con tu <b>Índice a la DERECHA</b> 👉 para avanzar.<br>
          • Muestra la <b>MANO ABIERTA</b> 🖐️ para volver a esta portada.
        </p>
      </div>

      <!-- Diapositiva 2 -->
      <div class="slide-content" id="slide-1">
        <h2 class="slide-title">⚙️ Arquitectura Edge-Computing</h2>
        <p class="slide-body">
          • La captura de video y la IA corren 100% en el cliente (Navegador).<br>
          • Cero latencia de red y procesamiento a 30 FPS mediante WebGL/GPU.<br>
          • No sobrecarga los servidores de Streamlit Cloud.
        </p>
      </div>

      <!-- Diapositiva 3 -->
      <div class="slide-content" id="slide-2">
        <h2 class="slide-title">📐 Algoritmo y Trigonometría</h2>
        <p class="slide-body">
          • MediaPipe extrae 21 puntos clave de las articulaciones de la mano.<br>
          • Se calcula el ángulo vectorial ($\theta$) entre la muñeca y las falanges.<br>
          • Clasificación tolerante a rotaciones e inclinaciones de la mano.
        </p>
      </div>

      <!-- Diapositiva 4 -->
      <div class="slide-content" id="slide-3">
        <h2 class="slide-title">🚀 Casos de Uso y Aplicaciones</h2>
        <p class="slide-body">
          • Quiófanos y entornos estériles (interacción sin contacto).<br>
          • Control de presentaciones y Smart TVs sin control remoto.<br>
          • Accesibilidad y tecnologías asistivas.
        </p>
      </div>
    </div>

    <div class="action-flash" id="action-status">Esperando gesto...</div>
  </div>

  <script>
    const videoElement = document.getElementById('webcam');
    const canvasElement = document.getElementById('output_canvas');
    const canvasCtx = canvasElement.getContext('2d');
    const hud = document.getElementById('hud');
    const actionStatus = document.getElementById('action-status');

    let currentTab = 0;
    const totalTabs = 4;
    let lastActionTime = 0;
    const ACTION_COOLDOWN = 1200; // 1.2 segundos entre acciones

    function switchTab(index) {
      if (index < 0 || index >= totalTabs) return;
      document.querySelectorAll('.tab-btn').forEach((btn, i) => {
        btn.classList.toggle('active', i === index);
      });
      document.querySelectorAll('.slide-content').forEach((slide, i) => {
        slide.classList.toggle('active', i === index);
      });
      currentTab = index;
    }

    function handleAction(gesture) {
      const now = Date.now();
      if (now - lastActionTime < ACTION_COOLDOWN) return;

      if (gesture === "ÍNDICE DERECHA") {
        if (currentTab < totalTabs - 1) {
          switchTab(currentTab + 1);
          showAction("👉 Pestaña Siguiente");
          lastActionTime = now;
        }
      } else if (gesture === "ÍNDICE IZQUIERDA") {
        if (currentTab > 0) {
          switchTab(currentTab - 1);
          showAction("👈 Pestaña Anterior");
          lastActionTime = now;
        }
      } else if (gesture === "MANO ABIERTA") {
        if (currentTab !== 0) {
          switchTab(0);
          showAction("🖐️ Regreso al Inicio");
          lastActionTime = now;
        }
      }
    }

    function showAction(msg) {
      actionStatus.innerText = "Acción ejecutada: " + msg;
      setTimeout(() => {
        actionStatus.innerText = "Esperando gesto...";
      }, 1500);
    }

    function dist(a, b) {
      return Math.hypot(a.x - b.x, a.y - b.y);
    }

    function classifyGesture(landmarks) {
      const wrist = landmarks[0];
      const fingers = [
        { tip: landmarks[8],  pip: landmarks[6]  },
        { tip: landmarks[12], pip: landmarks[10] },
        { tip: landmarks[16], pip: landmarks[14] },
        { tip: landmarks[20], pip: landmarks[18] }
      ];

      const extended = fingers.map(f => dist(f.tip, wrist) > (dist(f.pip, wrist) * 1.05));
      const extIdx = extended[0];
      const count = extended.filter(Boolean).length;

      if (count === 0) return "PUÑO CERRADO";
      if (count === 4) return "MANO ABIERTA";

      if (count === 1 && extIdx) {
        const indexMcp = landmarks[5];
        const indexTip = landmarks[8];
        const dx = indexTip.x - indexMcp.x;
        const dy = indexMcp.y - indexTip.y;
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
        canvasCtx.translate(canvasElement.width, 0);
        canvasCtx.scale(-1, 1);
        canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

        if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
          const landmarks = results.multiHandLandmarks[0];
          
          if (typeof drawConnectors !== 'undefined' && typeof HAND_CONNECTIONS !== 'undefined') {
            drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS, {color: '#00FF00', lineWidth: 3});
          }
          if (typeof drawLandmarks !== 'undefined') {
            drawLandmarks(canvasCtx, landmarks, {color: '#FF0000', lineWidth: 2, radius: 3});
          }

          canvasCtx.restore();

          const gesture = classifyGesture(landmarks);
          hud.innerText = "Gesto: " + gesture;
          handleAction(gesture);
        } else {
          canvasCtx.restore();
          hud.innerText = "Buscando mano...";
        }
      } catch (err) {
        console.error(err);
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
      width: 480,
      height: 360
    });
    camera.start();
  </script>
</body>
</html>
"""

components.html(html_code, height=400)

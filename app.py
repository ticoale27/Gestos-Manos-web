import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Control por Gestos - Presentación Interactiva",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS generales para la página de Streamlit
st.markdown("""
<style>
    .main { background-color: #0d1117; }
    h1 { color: #58a6ff; font-weight: 700; text-align: center; margin-bottom: 0px; }
    p.subtitle { text-align: center; color: #8b949e; font-size: 1.1rem; margin-bottom: 25px; }
</style>
""", unsafe_allow_html=True)

st.title("🖐️ Sistema de Control por Gestos en Tiempo Real")
st.markdown(
    "<p class='subtitle'>Demostración interactiva de Visión Computacional y Edge Computing para interfaces Hombre-Máquina (HCI)</p>",
    unsafe_allow_html=True
)

html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js" crossorigin="anonymous"></script>
  <style>
    :root {
      --bg-dark: #0d1117;
      --card-bg: #161b22;
      --border-color: #30363d;
      --accent-blue: #58a6ff;
      --accent-green: #2ea043;
      --text-main: #c9d1d9;
      --text-muted: #8b949e;
    }

    * { box-sizing: border-box; }
    body {
      margin: 0;
      padding: 10px;
      background-color: var(--bg-dark);
      color: var(--text-main);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      display: flex;
      gap: 20px;
      justify-content: center;
    }
    
    /* Panel de la Cámara */
    .cam-card {
      width: 440px;
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      align-items: center;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    .cam-container {
      position: relative;
      width: 408px;
      height: 306px;
      border-radius: 12px;
      overflow: hidden;
      border: 2px solid var(--border-color);
    }

    video { display: none; }
    canvas {
      width: 100%;
      height: 100%;
      background-color: #000;
    }

    .hud-badge {
      position: absolute;
      top: 12px;
      left: 12px;
      background: rgba(13, 17, 23, 0.9);
      color: #00ff88;
      padding: 6px 14px;
      font-size: 13px;
      font-weight: 700;
      border-radius: 20px;
      border: 1px solid #00ff88;
      letter-spacing: 0.5px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.6);
      backdrop-filter: blur(4px);
    }

    .instructions-box {
      margin-top: 14px;
      width: 100%;
      background: rgba(255, 255, 255, 0.03);
      border-radius: 10px;
      padding: 12px;
      border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .instructions-title {
      font-size: 12px;
      font-weight: 700;
      color: var(--accent-blue);
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 8px;
    }

    .gesture-guide {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
      font-size: 12px;
      color: var(--text-muted);
    }

    .gesture-guide span { font-weight: 600; color: var(--text-main); }

    /* Panel de la Presentación */
    .presentation-card {
      flex: 1;
      max-width: 780px;
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
      min-height: 480px;
    }

    .tabs-header {
      display: flex;
      gap: 8px;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 14px;
    }

    .tab-btn {
      padding: 10px 16px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid transparent;
      color: var(--text-muted);
      border-radius: 8px;
      font-weight: 600;
      font-size: 13px;
      transition: all 0.25s ease;
    }

    .tab-btn.active {
      background: var(--accent-blue);
      color: #ffffff;
      border-color: var(--accent-blue);
      box-shadow: 0 0 15px rgba(88, 166, 255, 0.4);
    }

    .slide-content {
      display: none;
      padding: 15px 5px;
      animation: fadeInSlide 0.4s ease-out;
    }

    .slide-content.active { display: block; }

    .slide-badge {
      display: inline-block;
      padding: 4px 10px;
      background: rgba(88, 166, 255, 0.15);
      color: var(--accent-blue);
      border-radius: 12px;
      font-size: 12px;
      font-weight: 600;
      margin-bottom: 10px;
    }

    .slide-title {
      color: #ffffff;
      font-size: 22px;
      font-weight: 700;
      margin: 0 0 14px 0;
    }

    .slide-body {
      color: var(--text-main);
      font-size: 14.5px;
      line-height: 1.6;
    }

    .slide-body ul {
      margin: 8px 0;
      padding-left: 20px;
    }

    .slide-body li {
      margin-bottom: 8px;
    }

    .highlight {
      color: var(--accent-blue);
      font-weight: 600;
    }

    .code-tag {
      background: rgba(110, 118, 129, 0.2);
      padding: 2px 6px;
      border-radius: 4px;
      font-family: monospace;
      font-size: 13px;
      color: #f0f6fc;
    }

    .footer-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid var(--border-color);
      padding-top: 14px;
      margin-top: 10px;
    }

    .action-status {
      font-size: 13px;
      font-weight: 600;
      color: var(--accent-green);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .slide-counter {
      font-size: 12px;
      color: var(--text-muted);
      font-weight: 600;
    }

    @keyframes fadeInSlide {
      from { opacity: 0; transform: translateY(8px); }
      to { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>
<body>

  <!-- Panel Izquierdo: Cámara e Indicadores -->
  <div class="cam-card">
    <div class="cam-container">
      <video id="webcam" autoplay playsinline></video>
      <canvas id="output_canvas" width="408" height="306"></canvas>
      <div id="hud" class="hud-badge">Iniciando Sensor...</div>
    </div>

    <div class="instructions-box">
      <div class="instructions-title">Comandos de Control Remoto</div>
      <div class="gesture-guide">
        <div>👉 <span>Índice Derecha:</span> Siguiente</div>
        <div>👈 <span>Índice Izquierda:</span> Anterior</div>
        <div>🖐️ <span>Mano Abierta:</span> Ir al Inicio</div>
        <div>✊ <span>Puño Cerrado:</span> En Espera</div>
      </div>
    </div>
  </div>

  <!-- Panel Derecho: Diapositivas Explicativas Ampliadas -->
  <div class="presentation-card">
    <div>
      <div class="tabs-header">
        <div class="tab-btn active" id="tab-0">1. Introducción</div>
        <div class="tab-btn" id="tab-1">2. Arquitectura Edge</div>
        <div class="tab-btn" id="tab-2">3. Lógica Vectorial</div>
        <div class="tab-btn" id="tab-3">4. Aplicaciones</div>
      </div>

      <!-- Diapositiva 1 -->
      <div class="slide-content active" id="slide-0">
        <span class="slide-badge">Módulo 01 — Contexto & Propósito</span>
        <h2 class="slide-title">Interacción Hombre-Máquina Sin Contacto (Touchless HCI)</h2>
        <div class="slide-body">
          Esta aplicación demuestra cómo reemplazar dispositivos tradicionales de entrada (como mouse o teclados) mediante la interpretación gestual en tiempo real utilizando visión computacional.
          <ul>
            <li><span class="highlight">Reconocimiento Natural:</span> Permite navegar la interfaz a través de movimientos intuitivos de la mano capturados por una webcam convencional.</li>
            <li><span class="highlight">Procesamiento Local:</span> Elimina la dependencia de hardware especializado como cámaras de profundidad (LiDAR o Depth Sensors), operando directamente con video RGB estándar.</li>
            <li><span class="highlight">Control de Flujo:</span> Navega dinámicamente entre estos módulos informativos mediante los gestos indicados en el panel izquierdo.</li>
          </ul>
        </div>
      </div>

      <!-- Diapositiva 2 -->
      <div class="slide-content" id="slide-1">
        <span class="slide-badge">Módulo 02 — Infraestructura Técnica</span>
        <h2 class="slide-title">Procesamiento Edge vs. Servidor (30 FPS)</h2>
        <div class="slide-body">
          Para garantizar una experiencia fluida y mitigar cuellos de botella en la red, se adoptó una arquitectura de <span class="highlight">Edge Computing</span> (procesamiento en el cliente).
          <ul>
            <li><span class="highlight">Despliegue Navegador-Nativo:</span> La captura del fotograma y la inferencia de inteligencia artificial ocurren 100% dentro del navegador usando JavaScript y WebGL.</li>
            <li><span class="highlight">Baja Latencia:</span> Se evita el envío continuo de video vía streaming (WebRTC/UDP) hacia el servidor de Streamlit Cloud, previniendo saturación de ancho de banda y bloqueos de red.</li>
            <li><span class="highlight">Eficiencia de Recursos:</span> Aprovecha la aceleración por GPU local del dispositivo del usuario, logrando una tasa estable de 30 fotogramas por segundo.</li>
          </ul>
        </div>
      </div>

      <!-- Diapositiva 3 -->
      <div class="slide-content" id="slide-2">
        <span class="slide-badge">Módulo 03 — Algoritmo Geométrica</span>
        <h2 class="slide-title">Extracción de Landmarks y Clasificación Trigonometría</h2>
        <div class="slide-body">
          El motor utiliza el pipeline de <span class="highlight">MediaPipe Hands</span> para mapear 21 puntos clave (landmarks 3D) de la articulación de la mano.
          <ul>
            <li><span class="highlight">Detección de Extensión:</span> Evalúa la distancia entre las puntas de los dedos y la muñeca (<span class="code-tag">Wrist Point 0</span>) comparándola contra los nudillos intermedios (PIP). Un dedo se considera extendido si la punta supera proporcionalmente la articulación base.</li>
            <li><span class="highlight">Cálculo de Ángulo Dirección:</span> Al aislar el índice, se calcula el vector del segmento <span class="code-tag">MCP (5) ➔ TIP (8)</span> determinando su ángulo mediante la función arcotangente2:
              <br><span class="code-tag">&theta; = atan2(&Delta;Y, &Delta;X) &times; (180 / &pi;)</span></li>
            <li><span class="highlight">Tolerancia Anti-Ruido:</span> Un umbral angular de &plusmn;35&deg; y un filtro de enfriamiento (cooldown) previenen activaciones accidentales por micro-temblores de la mano.</li>
          </ul>
        </div>
      </div>

      <!-- Diapositiva 4 -->
      <div class="slide-content" id="slide-3">
        <span class="slide-badge">Módulo 04 — Impacto Industrial</span>
        <h2 class="slide-title">Casos de Uso Real y Proyección Futura</h2>
        <div class="slide-body">
          Los sistemas de control por visión computacional tienen un papel transformador en múltiples campos de la industria:
          <ul>
            <li><span class="highlight">Entornos Médicos y Quirúrgicos:</span> Control de monitores e imágenes médicas dentro de quirófanos sin romper la esterilización de las manos.</li>
            <li><span class="highlight">Industria y Manufactura:</span> Manejo de maquinaria pesada o consulta de planos digitales en entornos con guantes o suciedad donde las pantallas táctiles fallan.</li>
            <li><span class="highlight">Tecnologías Asistivas:</span> Interfaces adaptadas para personas con movilidad reducida o diversidad funcional.</li>
            <li><span class="highlight">Sistemas Inmersivos:</span> Control intuitivo en experiencias de Realidad Virtual/Aumentada (VR/AR).</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Barra Inferior -->
    <div class="footer-bar">
      <div class="action-status" id="action-status">⚡ Sistema listo • Esperando movimiento</div>
      <div class="slide-counter" id="slide-counter">Diapositiva 1 de 4</div>
    </div>
  </div>

  <script>
    const videoElement = document.getElementById('webcam');
    const canvasElement = document.getElementById('output_canvas');
    const canvasCtx = canvasElement.getContext('2d');
    const hud = document.getElementById('hud');
    const actionStatus = document.getElementById('action-status');
    const slideCounter = document.getElementById('slide-counter');

    let currentTab = 0;
    const totalTabs = 4;
    let lastActionTime = 0;
    const ACTION_COOLDOWN = 1300; // 1.3s para evitar saltos dobles

    function switchTab(index) {
      if (index < 0 || index >= totalTabs) return;
      document.querySelectorAll('.tab-btn').forEach((btn, i) => {
        btn.classList.toggle('active', i === index);
      });
      document.querySelectorAll('.slide-content').forEach((slide, i) => {
        slide.classList.toggle('active', i === index);
      });
      currentTab = index;
      slideCounter.innerText = `Diapositiva ${currentTab + 1} de ${totalTabs}`;
    }

    function handleAction(gesture) {
      const now = Date.now();
      if (now - lastActionTime < ACTION_COOLDOWN) return;

      if (gesture === "ÍNDICE DERECHA") {
        if (currentTab < totalTabs - 1) {
          switchTab(currentTab + 1);
          showAction("👉 Avanzando a la siguiente diapositiva");
          lastActionTime = now;
        }
      } else if (gesture === "ÍNDICE IZQUIERDA") {
        if (currentTab > 0) {
          switchTab(currentTab - 1);
          showAction("👈 Regresando a la diapositiva anterior");
          lastActionTime = now;
        }
      } else if (gesture === "MANO ABIERTA") {
        if (currentTab !== 0) {
          switchTab(0);
          showAction("🖐️ Reiniciando presentación (Inicio)");
          lastActionTime = now;
        }
      }
    }

    function showAction(msg) {
      actionStatus.innerHTML = "✨ " + msg;
      setTimeout(() => {
        actionStatus.innerHTML = "⚡ Sistema activo • Esperando gesto";
      }, 1600);
    }

    function dist(a, b) {
      return Math.hypot(a.x - b.x, a.y - b.y);
    }

    function classifyGesture(landmarks) {
      const wrist = landmarks[0];
      const fingers = [
        { tip: landmarks[8],  pip: landmarks[6]  }, // Índice
        { tip: landmarks[12], pip: landmarks[10] }, // Medio
        { tip: landmarks[16], pip: landmarks[14] }, // Anular
        { tip: landmarks[20], pip: landmarks[18] }  // Meñique
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

      return "GESTO DETECTADO";
    }

    function onResults(results) {
      try {
        canvasCtx.save();
        canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
        
        // Efecto Espejo horizontal
        canvasCtx.translate(canvasElement.width, 0);
        canvasCtx.scale(-1, 1);
        canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

        if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
          const landmarks = results.multiHandLandmarks[0];
          
          if (typeof drawConnectors !== 'undefined' && typeof HAND_CONNECTIONS !== 'undefined') {
            drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS, {color: '#58a6ff', lineWidth: 3});
          }
          if (typeof drawLandmarks !== 'undefined') {
            drawLandmarks(canvasCtx, landmarks, {color: '#00ff88', lineWidth: 2, radius: 3});
          }

          canvasCtx.restore();

          const gesture = classifyGesture(landmarks);
          hud.innerText = gesture;
          hud.style.color = "#00ff88";
          hud.style.borderColor = "#00ff88";
          
          handleAction(gesture);
        } else {
          canvasCtx.restore();
          hud.innerText = "Buscando Mano...";
          hud.style.color = "#8b949e";
          hud.style.borderColor = "#30363d";
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
      width: 408,
      height: 306
    });
    camera.start();
  </script>
</body>
</html>
"""

components.html(html_code, height=530)

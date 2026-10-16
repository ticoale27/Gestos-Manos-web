import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Control por Gestos - Presentación Técnica",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos globales para la interfaz de Streamlit
st.markdown("""
<style>
    .main { background-color: #0d1117; }
    .stApp { background-color: #0d1117; }
    h1 { color: #58a6ff; font-weight: 700; text-align: center; margin-bottom: 0px; }
    p.subtitle { text-align: center; color: #8b949e; font-size: 1.05rem; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

st.title("🖐️ Sistema de Control por Gestos en Tiempo Real")
st.markdown(
    "<p class='subtitle'>Demostración de Visión Computacional, Pipeline de MediaPipe y Arquitectura Edge Computing para Interfaces Hombre-Máquina (HCI)</p>",
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
      --accent-gold: #e3b341;
      --text-main: #c9d1d9;
      --text-muted: #8b949e;
    }

    * { box-sizing: border-box; }
    body {
      margin: 0;
      padding: 5px;
      background-color: var(--bg-dark);
      color: var(--text-main);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      display: flex;
      gap: 20px;
      justify-content: center;
    }
    
    /* Panel Izquierdo: Sensor y Cámara */
    .cam-card {
      width: 410px;
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
      width: 378px;
      height: 284px;
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
      background: rgba(13, 17, 23, 0.92);
      color: #00ff88;
      padding: 6px 14px;
      font-size: 12.5px;
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
      font-size: 11px;
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
      font-size: 11.5px;
      color: var(--text-muted);
    }

    .gesture-guide span { font-weight: 600; color: var(--text-main); }

    /* Panel Derecho: Diapositivas e Información */
    .presentation-card {
      flex: 1;
      max-width: 800px;
      background: var(--card-bg);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
      min-height: 500px;
    }

    .tabs-header {
      display: flex;
      gap: 6px;
      border-bottom: 1px solid var(--border-color);
      padding-bottom: 12px;
      overflow-x: auto;
    }

    .tab-btn {
      padding: 8px 12px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid transparent;
      color: var(--text-muted);
      border-radius: 8px;
      font-weight: 600;
      font-size: 12px;
      white-space: nowrap;
      transition: all 0.25s ease;
      cursor: pointer;
    }

    .tab-btn.active {
      background: var(--accent-blue);
      color: #ffffff;
      border-color: var(--accent-blue);
      box-shadow: 0 0 12px rgba(88, 166, 255, 0.35);
    }

    .slide-content {
      display: none;
      padding: 12px 4px;
      animation: fadeInSlide 0.35s ease-out;
    }

    .slide-content.active { display: block; }

    .slide-badge {
      display: inline-block;
      padding: 3px 10px;
      background: rgba(88, 166, 255, 0.15);
      color: var(--accent-blue);
      border-radius: 12px;
      font-size: 11px;
      font-weight: 700;
      margin-bottom: 10px;
      letter-spacing: 0.5px;
    }

    .slide-title {
      color: #ffffff;
      font-size: 20px;
      font-weight: 700;
      margin: 0 0 12px 0;
    }

    .slide-body {
      color: var(--text-main);
      font-size: 13.8px;
      line-height: 1.6;
    }

    .slide-body ul {
      margin: 8px 0;
      padding-left: 18px;
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
      font-size: 12px;
      color: #f0f6fc;
      border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .info-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-top: 10px;
    }

    .info-box {
      background: rgba(255, 255, 255, 0.025);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      padding: 10px 12px;
    }

    .info-box h4 {
      margin: 0 0 4px 0;
      color: var(--accent-gold);
      font-size: 12.5px;
      font-weight: 700;
    }

    .info-box p {
      margin: 0;
      font-size: 12px;
      color: var(--text-muted);
    }

    .footer-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid var(--border-color);
      padding-top: 12px;
      margin-top: 10px;
    }

    .action-status {
      font-size: 12.5px;
      font-weight: 600;
      color: var(--accent-green);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .slide-counter {
      font-size: 11.5px;
      color: var(--text-muted);
      font-weight: 600;
    }

    @keyframes fadeInSlide {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>
<body>

  <!-- Panel Izquierdo: Sensor y Guía -->
  <div class="cam-card">
    <div class="cam-container">
      <video id="webcam" autoplay playsinline></video>
      <canvas id="output_canvas" width="378" height="284"></canvas>
      <div id="hud" class="hud-badge">Iniciando Sensor...</div>
    </div>

    <div class="instructions-box">
      <div class="instructions-title">Comandos de Control Remoto</div>
      <div class="gesture-guide">
        <div>👉 <span>Índice Derecha:</span> Siguiente Cap.</div>
        <div>👈 <span>Índice Izquierda:</span> Cap. Anterior</div>
        <div>🖐️ <span>Mano Abierta:</span> Ir al Inicio</div>
        <div>✊ <span>Puño Cerrado:</span> En Espera</div>
      </div>
    </div>
  </div>

  <!-- Panel Derecho: 6 Capítulos Detallados para Exposición -->
  <div class="presentation-card">
    <div>
      <div class="tabs-header">
        <div class="tab-btn active" id="tab-0">1. Introducción</div>
        <div class="tab-btn" id="tab-1">2. Arquitectura Edge</div>
        <div class="tab-btn" id="tab-2">3. Pipeline MediaPipe</div>
        <div class="tab-btn" id="tab-3">4. Trigonometría</div>
        <div class="tab-btn" id="tab-4">5. Aplicaciones</div>
        <div class="tab-btn" id="tab-5">6. Desafíos & Futuro</div>
      </div>

      <!-- CAPÍTULO 1 -->
      <div class="slide-content active" id="slide-0">
        <span class="slide-badge">CAPÍTULO 01 • CONTEXTO & PROPÓSITO</span>
        <h2 class="slide-title">Interacción Hombre-Máquina Sin Contacto (Touchless HCI)</h2>
        <div class="slide-body">
          Esta aplicación demuestra cómo interpretar la biomecánica de la mano en tiempo real mediante visión computacional, eliminando la necesidad de periféricos físicos como mouse, teclados o pantallas táctiles.
          <ul>
            <li><span class="highlight">Evolución de las HCI:</span> Transición desde las interfaces de comandos (CLI) y gráficas (GUI) hacia las interfaces naturales de usuario (NUI) basadas en gestos y voz.</li>
            <li><span class="highlight">Captura RGB Convencional:</span> Funciona con cualquier cámara web estándar, sin requerir sensores infrarrojos o cámaras de profundidad especializadas (LiDAR o Depth Sensors).</li>
            <li><span class="highlight">Control de Flujo:</span> Navega dinámicamente entre estas diapositivas en tiempo real apuntando con el dedo índice a la derecha o izquierda.</li>
          </ul>
        </div>
      </div>

      <!-- CAPÍTULO 2 -->
      <div class="slide-content" id="slide-1">
        <span class="slide-badge">CAPÍTULO 02 • INFRAESTRUCTURA TÉCNICA</span>
        <h2 class="slide-title">Arquitectura Edge Computing y Rendimiento (30 FPS)</h2>
        <div class="slide-body">
          Para garantizar una respuesta instantánea y mitigar cuellos de botella en la red, se implementó un paradigma de <span class="highlight">Edge Computing</span> (procesamiento distribuido en el cliente).
          <div class="info-grid">
            <div class="info-box">
              <h4>🚀 Ejecución Client-Side</h4>
              <p>La captura de video y la inferencia de la IA ocurren 100% dentro del navegador web mediante WebGL y JavaScript.</p>
            </div>
            <div class="info-box">
              <h4>⚡ Sin Sobrecarga de Servidor</h4>
              <p>Se evita transmitir video continuo (WebRTC/UDP) hacia Streamlit Cloud, previniendo caídas de socket y latencia de red.</p>
            </div>
          </div>
          <p style="margin-top: 10px;">
            <span class="highlight">Tasa de Refresco:</span> Logra una velocidad constante de <b>30 fotogramas por segundo</b> aprovechando la aceleración por hardware de la GPU local.
          </p>
        </div>
      </div>

      <!-- CAPÍTULO 3 -->
      <div class="slide-content" id="slide-2">
        <span class="slide-badge">CAPÍTULO 03 • PIPELINE DE IA</span>
        <h2 class="slide-title">Detección de Palmas y Mapeo de 21 Landmarks 3D</h2>
        <div class="slide-body">
          El procesamiento utiliza el pipeline de dos etapas optimizado de <span class="highlight">MediaPipe Hands</span>:
          <ul>
            <li><b>1. Detector de Palmas (BlazePalm):</b> Un modelo convolucional que escanea todo el fotograma para encontrar la caja delimitadora (bounding box) de la mano, tolerante a rotaciones severas.</li>
            <li><b>2. Modelo de Puntos Clave (Landmark Model):</b> Mapea 21 articulaciones en coordenadas 3D relativas dentro del área recortada por el detector.</li>
            <li><b>Reducción de Carga Computacional:</b> Tras encontrar la mano en el primer fotograma, los siguientes fotogramas solo usan el modelo de landmarks siguiendo el rastreo previa, re-ejecutando el detector únicamente si se pierde el seguimiento.</li>
          </ul>
        </div>
      </div>

      <!-- CAPÍTULO 4 -->
      <div class="slide-content" id="slide-3">
        <span class="slide-badge">CAPÍTULO 04 • LÓGICA MATEMÁTICA</span>
        <h2 class="slide-title">Clasificación Geométrica y Trigonometría Vectorial</h2>
        <div class="slide-body">
          El algoritmo no depende de posiciones absolutas de la pantalla, sino de relaciones geométricas proporcionales:
          <ul>
            <li><b>Estado de Extensión:</b> Compara la distancia desde la muñeca (<span class="code-tag">WRIST 0</span>) a la punta del dedo (<span class="code-tag">TIP</span>) contra la distancia a la articulación base (<span class="code-tag">PIP</span>). Si supera la proporción de 1.05x, se clasifica como extendido.</li>
            <li><b>Dirección Angular del Índice:</b> Se aísla el segmento vectorial entre el nudillo base (<span class="code-tag">INDEX_MCP 5</span>) y la punta (<span class="code-tag">INDEX_TIP 8</span>), calculando su ángulo polar:
              <br><span class="code-tag">&theta; = atan2(&Delta;Y, &Delta;X) &times; (180 / &pi;)</span></li>
            <li><b>Estabilización Anti-Parpadeo:</b> Se aplica una ventana angular de &plusmn;35&deg; y un tiempo de enfriamiento (<span class="highlight">cooldown</span>) de 1.3s para ignorar variaciones involuntarias de la mano.</li>
          </ul>
        </div>
      </div>

      <!-- CAPÍTULO 5 -->
      <div class="slide-content" id="slide-4">
        <span class="slide-badge">CAPÍTULO 05 • APLICACIONES INDUSTRIALES</span>
        <h2 class="slide-title">Casos de Uso Real y Transferencia Tecnológica</h2>
        <div class="slide-body">
          Las interfaces gestuales mediante visión computacional ofrecen valor directo en múltiples áreas profesionales:
          <div class="info-grid">
            <div class="info-box">
              <h4>🏥 Entornos Quirúrgicos</h4>
              <p>Permite a cirujanos manipular tomografías e imágenes médicas sin tocar pantallas, conservando la esterilidad.</p>
            </div>
            <div class="info-box">
              <h4>🏭 Industria Pesada</h4>
              <p>Consulta de planos digitales en fábricas donde los operarios usan guantes de protección gruesos o grasa.</p>
            </div>
            <div class="info-box">
              <h4>🦾 Accesibilidad</h4>
              <p>Sistemas adaptados para personas con movilidad reducida y control intuitivo de prótesis robóticas.</p>
            </div>
            <div class="info-box">
              <h4>🥽 Realidad Virtual (AR/VR)</h4>
              <p>Navegación espacial inmersiva en visores sin requerir controles plásticos físicos.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- CAPÍTULO 6 -->
      <div class="slide-content" id="slide-5">
        <span class="slide-badge">CAPÍTULO 06 • EVALUACIÓN Y FUTURO</span>
        <h2 class="slide-title">Desafíos Técnicos y Líneas de Trabajo Futuras</h2>
        <div class="slide-body">
          Análisis de las limitaciones actuales y las potenciales mejoras para futuras versiones del proyecto:
          <ul>
            <li><span class="highlight">Condiciones de Iluminación:</span> La precisión del modelo disminuye ante sombras fuertes o ambientes con poca luz. Trabajo futuro: integrar filtros de ecualización de histograma adaptativo (CLAHE).</li>
            <li><span class="highlight">Oclusión Parcial:</span> Cuando los dedos se cruzan o la mano se coloca de perfil, se pierden algunos puntos clave. Solución: combinar modelos dinámicos basados en secuencias temporales (LSTM o Transformer networks).</li>
            <li><span class="highlight">Ampliación de Comandos:</span> Posibilidad de integrar reconocimiento dinámico de gestos continuos (p.ej. deslizar, pellizcar para hacer zoom o rotación 3D).</li>
          </ul>
        </div>
      </div>

    </div>

    <!-- Barra Inferior de Estado -->
    <div class="footer-bar">
      <div class="action-status" id="action-status">⚡ Sistema activo • Esperando movimiento</div>
      <div class="slide-counter" id="slide-counter">Capítulo 1 de 6</div>
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
    const totalTabs = 6;
    let lastActionTime = 0;
    const ACTION_COOLDOWN = 1300; // 1.3s para evitar saltos múltiples

    function switchTab(index) {
      if (index < 0 || index >= totalTabs) return;
      document.querySelectorAll('.tab-btn').forEach((btn, i) => {
        btn.classList.toggle('active', i === index);
      });
      document.querySelectorAll('.slide-content').forEach((slide, i) => {
        slide.classList.toggle('active', i === index);
      });
      currentTab = index;
      slideCounter.innerText = `Capítulo ${currentTab + 1} de ${totalTabs}`;
    }

    function handleAction(gesture) {
      const now = Date.now();
      if (now - lastActionTime < ACTION_COOLDOWN) return;

      if (gesture === "ÍNDICE DERECHA") {
        if (currentTab < totalTabs - 1) {
          switchTab(currentTab + 1);
          showAction("👉 Avanzando al siguiente capítulo");
          lastActionTime = now;
        }
      } else if (gesture === "ÍNDICE IZQUIERDA") {
        if (currentTab > 0) {
          switchTab(currentTab - 1);
          showAction("👈 Regresando al capítulo anterior");
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
        
        // Espejo horizontal
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
      width: 378,
      height: 284
    });
    camera.start();
  </script>
</body>
</html>
"""

components.html(html_code, height=580)

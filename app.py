import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Gestos de Superhéroe - Interfaz de Visión Computacional",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos base de Streamlit
st.markdown("""
<style>
    .main { background-color: #07090e; }
    .stApp { background-color: #07090e; }
</style>
""", unsafe_allow_html=True)

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
      --bg-dark: #07090e;
      --card-bg: #0f131d;
      --border-color: #1f293d;
      --spidey-red: #e62429;
      --spidey-blue: #00d2ff;
      --hero-gold: #ffb700;
      --bat-dark: #161b26;
      --text-main: #e2e8f0;
      --text-muted: #94a3b8;
    }

    * { box-sizing: border-box; }
    body {
      margin: 0;
      padding: 10px;
      background-color: var(--bg-dark);
      color: var(--text-main);
      font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    /* Encabezado Épico */
    .hero-header {
      text-align: center;
      margin-bottom: 15px;
      width: 100%;
    }

    .hero-title {
      font-size: 26px;
      font-weight: 900;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      background: linear-gradient(90deg, #e62429, #ffb700, #00d2ff);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin: 0;
      text-shadow: 0 0 20px rgba(230, 36, 41, 0.3);
    }

    .hero-subtitle {
      font-size: 13px;
      color: var(--text-muted);
      margin-top: 4px;
      font-weight: 600;
      letter-spacing: 0.5px;
    }

    .main-container {
      display: flex;
      gap: 20px;
      width: 100%;
      max-width: 1250px;
      justify-content: center;
    }
    
    /* Panel Radar / Cámara */
    .cam-card {
      width: 420px;
      background: var(--card-bg);
      border: 2px solid var(--border-color);
      border-radius: 18px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      align-items: center;
      box-shadow: 0 0 25px rgba(0, 210, 255, 0.15);
      position: relative;
    }

    .cam-container {
      position: relative;
      width: 388px;
      height: 291px;
      border-radius: 14px;
      overflow: hidden;
      border: 2px solid #2a364f;
      box-shadow: 0 0 15px rgba(230, 36, 41, 0.2);
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
      background: rgba(7, 9, 14, 0.88);
      color: var(--hero-gold);
      padding: 6px 14px;
      font-size: 12px;
      font-weight: 800;
      border-radius: 8px;
      border: 1.5px solid var(--hero-gold);
      letter-spacing: 1px;
      box-shadow: 0 0 10px rgba(255, 183, 0, 0.4);
      backdrop-filter: blur(5px);
    }

    .instructions-box {
      margin-top: 14px;
      width: 100%;
      background: rgba(22, 27, 38, 0.8);
      border-radius: 12px;
      padding: 12px 14px;
      border: 1px solid #2a364f;
    }

    .instructions-title {
      font-size: 11px;
      font-weight: 800;
      color: var(--spidey-blue);
      text-transform: uppercase;
      letter-spacing: 1px;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .gesture-guide {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      font-size: 11.5px;
      color: var(--text-muted);
    }

    .gesture-guide span { font-weight: 700; color: #ffffff; }

    /* Panel Presentación Estilo Batcomputadora / Archivos Stark */
    .presentation-card {
      flex: 1;
      background: var(--card-bg);
      border: 2px solid var(--border-color);
      border-radius: 18px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 0 25px rgba(230, 36, 41, 0.1);
      min-height: 480px;
    }

    .tabs-header {
      display: flex;
      gap: 8px;
      border-bottom: 2px solid var(--border-color);
      padding-bottom: 12px;
    }

    .tab-btn {
      padding: 10px 14px;
      background: #141a26;
      border: 1px solid #2a364f;
      color: var(--text-muted);
      border-radius: 10px;
      font-weight: 700;
      font-size: 12px;
      transition: all 0.3s ease;
      cursor: pointer;
    }

    .tab-btn.active {
      background: linear-gradient(135deg, var(--spidey-red), #b30f14);
      color: #ffffff;
      border-color: var(--spidey-red);
      box-shadow: 0 0 15px rgba(230, 36, 41, 0.5);
    }

    .slide-content {
      display: none;
      padding: 15px 5px;
      animation: heroFadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .slide-content.active { display: block; }

    .slide-badge {
      display: inline-block;
      padding: 4px 10px;
      background: rgba(0, 210, 255, 0.12);
      color: var(--spidey-blue);
      border: 1px solid rgba(0, 210, 255, 0.3);
      border-radius: 6px;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 1px;
      text-transform: uppercase;
      margin-bottom: 10px;
    }

    .slide-title {
      color: #ffffff;
      font-size: 20px;
      font-weight: 800;
      margin: 0 0 12px 0;
    }

    .slide-body {
      color: var(--text-main);
      font-size: 13.5px;
      line-height: 1.6;
    }

    .hero-card-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-top: 10px;
    }

    .hero-subcard {
      background: rgba(22, 27, 38, 0.7);
      border: 1px solid #2a364f;
      border-radius: 10px;
      padding: 12px;
    }

    .hero-subcard h4 {
      margin: 0 0 6px 0;
      color: var(--hero-gold);
      font-size: 13px;
      font-weight: 700;
    }

    .hero-subcard p {
      margin: 0;
      font-size: 12px;
      color: var(--text-muted);
    }

    .highlight {
      color: var(--spidey-blue);
      font-weight: 700;
    }

    .code-tag {
      background: rgba(0, 210, 255, 0.15);
      padding: 2px 6px;
      border-radius: 4px;
      font-family: monospace;
      font-size: 12px;
      color: var(--spidey-blue);
      border: 1px solid rgba(0, 210, 255, 0.3);
    }

    .footer-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 2px solid var(--border-color);
      padding-top: 12px;
      margin-top: 10px;
    }

    .action-status {
      font-size: 12px;
      font-weight: 700;
      color: var(--hero-gold);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .slide-counter {
      font-size: 11px;
      color: var(--text-muted);
      font-weight: 700;
      letter-spacing: 0.5px;
    }

    @keyframes heroFadeIn {
      from { opacity: 0; transform: translateY(10px) scale(0.98); }
      to { opacity: 1; transform: translateY(0) scale(1); }
    }
  </style>
</head>
<body>

  <div class="hero-header">
    <h1 class="hero-title">🕷️ VISIÓN HEROICA • CONTROL POR GESTOS</h1>
    <div class="hero-subtitle">Módulo de Inteligencia Artificial & Interacción Hombre-Máquina al estilo Liga de la Justicia</div>
  </div>

  <div class="main-container">

    <!-- Panel Izquierdo: Sensor / Cámara con Esqueleto Neón -->
    <div class="cam-card">
      <div class="cam-container">
        <video id="webcam" autoplay playsinline></video>
        <canvas id="output_canvas" width="388" height="291"></canvas>
        <div id="hud" class="hud-badge">SISTEMA LISTO</div>
      </div>

      <div class="instructions-box">
        <div class="instructions-title">🕷️ COMANDOS DE SUPERPODER</div>
        <div class="gesture-guide">
          <div>👉 <span>Índice Derecha:</span> Siguiente Cap.</div>
          <div>👈 <span>Índice Izquierda:</span> Cap. Anterior</div>
          <div>🖐️ <span>Mano Abierta:</span> Volver al Inicio</div>
          <div>✊ <span>Puño Cerrado:</span> Modo Escudo</div>
        </div>
      </div>
    </div>

    <!-- Panel Derecho: Capítulos Detallados para Exposición -->
    <div class="presentation-card">
      <div>
        <div class="tabs-header">
          <div class="tab-btn active" id="tab-0">🕷️ 1. Origen & Sentido Aracneo</div>
          <div class="tab-btn" id="tab-1">⚡ 2. Velocidad Flash (Edge 30 FPS)</div>
          <div class="tab-btn" id="tab-2">🦇 3. Batcomputadora Vectorial</div>
          <div class="tab-btn" id="tab-3">🛡️ 4. Misiones en el Mundo Real</div>
        </div>

        <!-- CAPÍTULO 1 -->
        <div class="slide-content active" id="slide-0">
          <span class="slide-badge">CAPÍTULO 01 • SENSADO Y VISIÓN DIGITAL</span>
          <h2 class="slide-title">🕷️ El "Sentido Arácnido": Visión Computacional Touchless</h2>
          <div class="slide-body">
            En los cómics, el "Sentido Arácnido" le permite a Spider-Man percibir el entorno en milisegundos sin tocar nada. En este proyecto, le otorgamos a la computadora ese mismo "superpoder" visual.
            <div class="hero-card-grid">
              <div class="hero-subcard">
                <h4>🖐️ Interacción Sin Contacto</h4>
                <p>Reemplaza teclados y controles físicos capturando el movimiento biológico de la mano con una cámara RGB común.</p>
              </div>
              <div class="hero-subcard">
                <h4>🎯 Sensado Biométrico 3D</h4>
                <p>Detecta gestos de manera natural sin requerir trajes especiales, sensores LiDAR o guantes hápticos costosos.</p>
              </div>
            </div>
            <p style="margin-top: 10px;">
              <b>Propósito Técnico:</b> Demostrar cómo los algoritmos de redes neuronales convolucionales ligeras pueden procesar la biomecánica de los dedos para controlar interfaces web dinámicas.
            </p>
          </div>
        </div>

        <!-- CAPÍTULO 2 -->
        <div class="slide-content" id="slide-1">
          <span class="slide-badge">CAPÍTULO 02 • VELOCIDAD SOBREHUMANA</span>
          <h2 class="slide-title">⚡ Velocidad de Flash: Procesamiento Edge a 30 FPS</h2>
          <div class="slide-body">
            Para lograr una respuesta instantánea (como los reflejos de Flash), procesamos todo el flujo de video directamente en el navegador del usuario en lugar de enviarlo a servidores remotos.
            <div class="hero-card-grid">
              <div class="hero-subcard">
                <h4>🚀 Inferencia Local (Client-Side)</h4>
                <p>La IA corre dentro del motor de JavaScript del navegador mediante WebGL. Cero latencia de transmisión por Internet.</p>
              </div>
              <div class="hero-subcard">
                <h4>🛡️ Inmune a Caídas de Red</h4>
                <p>Al no transmitir video continuo por sockets (WebRTC/UDP), la app nunca colapsa el servidor de Streamlit Cloud ni consume ancho de banda.</p>
              </div>
            </div>
            <p style="margin-top: 10px;">
              <span class="highlight">Rendimiento:</span> Mantiene una tasa fluida de <b>30 fotogramas por segundo</b> aprovechando la aceleración por hardware de la GPU del equipo local.
            </p>
          </div>
        </div>

        <!-- CAPÍTULO 3 -->
        <div class="slide-content" id="slide-2">
          <span class="slide-badge">CAPÍTULO 03 • GEOMETRÍA Y TRIGONOMETRÍA</span>
          <h2 class="slide-title">🦇 Mapeo de Telaraña: 21 Puntos y Trigonometría Vectorial</h2>
          <div class="slide-body">
            Al estilo de la Batcomputadora o JARVIS, el sistema construye una malla virtual con 21 puntos clave (landmarks) sobre las articulaciones de la mano.
            <ul>
              <li><b>Detección de Falanges:</b> Un dedo se clasifica como extendido si la distancia de la punta (<span class="code-tag">TIP</span>) a la muñeca (<span class="code-tag">WRIST 0</span>) es mayor que la de su nudillo base (<span class="code-tag">PIP</span>).</li>
              <li><b>Dirección Angular del Índice:</b> Aislando el dedo índice, calculamos el ángulo vectorial de orientación:
                <br><span class="code-tag">&theta; = atan2(&Delta;Y, &Delta;X) &times; (180 / &pi;)</span></li>
              <li><b>Filtro Anti-Falsos Positivos:</b> Se aplica un umbral de &plusmn;35&deg; y un tiempo de recarga (<span class="highlight">cooldown</span>) de 1.3s para evitar movimientos involuntarios.</li>
            </ul>
          </div>
        </div>

        <!-- CAPÍTULO 4 -->
        <div class="slide-content" id="slide-3">
          <span class="slide-badge">CAPÍTULO 04 • IMPACTO EN LA SOCIEDAD</span>
          <h2 class="slide-title">🛡️ Misiones en el Mundo Real: Aplicaciones Útiles</h2>
          <div class="slide-body">
            Esta tecnología de visión computacional no es solo un truco visual, tiene aplicaciones directas en la industria moderna:
            <div class="hero-card-grid">
              <div class="hero-subcard">
                <h4>🏥 Quirófanos y Salud</h4>
                <p>Permite a médicos cirujanos manipular tomografías y monitores en medio de operaciones sin tocar pantallas estériles.</p>
              </div>
              <div class="hero-subcard">
                <h4>🦾 Robótica y Accesibilidad</h4>
                <p>Sistemas de asistencia para personas con discapacidad motriz e interfaces para prótesis robóticas inteligentes.</p>
              </div>
              <div class="hero-subcard">
                <h4>🏭 Industria Pesada</h4>
                <p>Manejo de maquinaria pesada o consulta de planos digitales en entornos donde el operario lleva guantes o grasa.</p>
              </div>
              <div class="hero-subcard">
                <h4>🥽 Realidad Virtual (AR/VR)</h4>
                <p>Control natural e inmersivo en visores de Realidad Aumentada sin necesidad de mandos plásticos en las manos.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Barra Inferior -->
      <div class="footer-bar">
        <div class="action-status" id="action-status">✨ RADAR DE SUPERHÉROE ACTIVO • ESPERANDO GESTO</div>
        <div class="slide-counter" id="slide-counter">CAPÍTULO 1 DE 4</div>
      </div>
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
    const ACTION_COOLDOWN = 1300;

    function switchTab(index) {
      if (index < 0 || index >= totalTabs) return;
      document.querySelectorAll('.tab-btn').forEach((btn, i) => {
        btn.classList.toggle('active', i === index);
      });
      document.querySelectorAll('.slide-content').forEach((slide, i) => {
        slide.classList.toggle('active', i === index);
      });
      currentTab = index;
      slideCounter.innerText = `CAPÍTULO ${currentTab + 1} DE ${totalTabs}`;
    }

    function handleAction(gesture) {
      const now = Date.now();
      if (now - lastActionTime < ACTION_COOLDOWN) return;

      if (gesture === "ÍNDICE DERECHA") {
        if (currentTab < totalTabs - 1) {
          switchTab(currentTab + 1);
          showAction("👉 AVANZANDO AL SIGUIENTE CAPÍTULO");
          lastActionTime = now;
        }
      } else if (gesture === "ÍNDICE IZQUIERDA") {
        if (currentTab > 0) {
          switchTab(currentTab - 1);
          showAction("👈 REGRESANDO AL CAPÍTULO ANTERIOR");
          lastActionTime = now;
        }
      } else if (gesture === "MANO ABIERTA") {
        if (currentTab !== 0) {
          switchTab(0);
          showAction("🖐️ VOLVIENDO AL ORIGEN (CAPÍTULO 1)");
          lastActionTime = now;
        }
      }
    }

    function showAction(msg) {
      actionStatus.innerHTML = "💥 " + msg;
      setTimeout(() => {
        actionStatus.innerHTML = "✨ RADAR DE SUPERHÉROE ACTIVO • ESPERANDO GESTO";
      }, 1600);
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
        
        // Espejo horizontal
        canvasCtx.translate(canvasElement.width, 0);
        canvasCtx.scale(-1, 1);
        canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

        if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
          const landmarks = results.multiHandLandmarks[0];
          
          // Dibujar telaraña / esqueleto de héroe (Azul Spidey Neón y Nodos Rojos)
          if (typeof drawConnectors !== 'undefined' && typeof HAND_CONNECTIONS !== 'undefined') {
            drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS, {color: '#00d2ff', lineWidth: 3});
          }
          if (typeof drawLandmarks !== 'undefined') {
            drawLandmarks(canvasCtx, landmarks, {color: '#e62429', lineWidth: 2, radius: 4});
          }

          canvasCtx.restore();

          const gesture = classifyGesture(landmarks);
          hud.innerText = gesture;
          hud.style.color = "#ffb700";
          hud.style.borderColor = "#ffb700";
          
          handleAction(gesture);
        } else {
          canvasCtx.restore();
          hud.innerText = "BUSCANDO MANO...";
          hud.style.color = "#94a3b8";
          hud.style.borderColor = "#2a364f";
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
      width: 388,
      height: 291
    });
    camera.start();
  </script>
</body>
</html>
"""

components.html(html_code, height=560)

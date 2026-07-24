import streamlit as st
import requests
import json

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Colsubsidio - Mi Camino VIS", layout="wide", initial_sidebar_state="expanded")

# --- CSS PROFESIONAL CON IDENTIDAD CROMÁTICA OFICIAL Y FONDO ANIMADO ---
st.markdown("""
<style>
    /* Fondo Animado Profesional con los colores corporativos */
    .stApp { 
        background: linear-gradient(135deg, #f8fafc 0%, #edf2f7 50%, #e2e8f0 100%);
        position: relative;
        overflow-x: hidden;
    }
    
    /* Patrón y ondas de fondo animadas sin imágenes externas */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: radial-gradient(rgba(0, 103, 177, 0.04) 2px, transparent 2px), radial-gradient(rgba(255, 208, 0, 0.04) 2px, transparent 2px);
        background-size: 40px 40px;
        background-position: 0 0, 20px 20px;
        z-index: 0;
        pointer-events: none;
    }

    /* Cabecera Inmersiva Corporativa */
    .game-header { 
        background: linear-gradient(135deg, #0067b1 0%, #004d85 100%); 
        padding: 35px; 
        color: white; 
        text-align: center; 
        border-radius: 0 0 35px 35px; 
        margin-top: -60px; 
        margin-bottom: 30px; 
        box-shadow: 0 10px 30px rgba(0, 103, 177, 0.2); 
        border-bottom: 6px solid #ffd000; 
        position: relative;
        z-index: 1;
    }
    .game-header h1 { color: #ffd000 !important; font-weight: 900; font-size: 2.8rem; letter-spacing: -0.5px; text-shadow: 0 2px 4px rgba(0,0,0,0.2); }

    /* Roadmap Visual */
    .roadmap-container { display: flex; justify-content: space-between; align-items: center; position: relative; margin: 20px auto 50px auto; padding: 0 5%; max-width: 1000px; z-index: 1; }
    .roadmap-step { display: flex; flex-direction: column; align-items: center; position: relative; z-index: 2; width: 20%; }
    .roadmap-icon { font-size: 2.2rem; background: white; border: 4px solid #cbd5e1; border-radius: 50%; width: 75px; height: 75px; display: flex; justify-content: center; align-items: center; z-index: 2; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .step-active .roadmap-icon { border-color: #ffd000; background: #fffbeb; transform: scale(1.15); box-shadow: 0 0 20px rgba(255, 208, 0, 0.5); }
    .step-done .roadmap-icon { border-color: #10b981; background: #d1fae5; color: #065f46; }
    .step-label { font-weight: 700; margin-top: 12px; color: #575756; font-size: 0.95rem; text-align: center; text-transform: uppercase; letter-spacing: 0.5px; }
    .step-active .step-label { color: #0067b1; font-size: 1.05rem; }
    .roadmap-line { position: absolute; top: 37px; left: 10%; right: 10%; height: 5px; background: #cbd5e1; z-index: 1; border-radius: 3px; }
    
    /* Contenedor Principal (Tarjetas de Etapa) */
    .stage-container { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(12px); border-radius: 24px; padding: 45px; text-align: center; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08); margin: 0 auto 40px auto; border: 1px solid rgba(255, 255, 255, 0.8); max-width: 900px; position: relative; z-index: 1; }
    .house-graphic { font-size: 110px; line-height: 1; margin-bottom: 25px; filter: drop-shadow(0 10px 15px rgba(0,0,0,0.1)); animation: popIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
    
    /* Caja de Narrativa Estilizada */
    .narrative-box { background: #f0f7ff; border-left: 6px solid #0067b1; padding: 25px 30px; border-radius: 0 16px 16px 0; text-align: left; margin: 0 auto 35px auto; font-size: 1.15rem; color: #575756; line-height: 1.6; box-shadow: inset 0 2px 4px rgba(0,0,0,0.01); }
    .narrative-title { font-weight: 800; color: #0067b1; margin-bottom: 12px; font-size: 1.3rem; text-transform: uppercase; letter-spacing: 0.5px; }
    
    /* Botones y Radio Buttons Corporativos */
    .stButton > button { background-color: #0067b1 !important; color: white !important; font-weight: bold; border-radius: 12px; border: none; padding: 0.6rem 1.5rem; transition: all 0.3s ease; box-shadow: 0 4px 10px rgba(0, 103, 177, 0.3); }
    .stButton > button:hover { background-color: #004d85 !important; transform: translateY(-2px); box-shadow: 0 6px 15px rgba(0, 103, 177, 0.4); }
    
    .stSlider > label, .stNumberInput > label, .stRadio > label, .stSelectbox > label { display: none; }
    div.row-widget.stRadio > div { flex-direction: row; flex-wrap: wrap; gap: 12px; justify-content: center; }
    div.row-widget.stRadio > div > label { background: white; padding: 12px 25px; border-radius: 30px; border: 2px solid #e2e8f0; cursor: pointer; transition: all 0.2s; font-weight: 600; color: #575756; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
    div.row-widget.stRadio > div > label:hover { border-color: #0067b1; background: #f0f7ff; color: #0067b1; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    
    @keyframes popIn { 0% { transform: scale(0.5); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE API REAL ---
BASE_URL = "https://composite-suing-grandly.ngrok-free.dev"
API_KEY = "AQ.Ab8RN6J3asN8cwgzqstvEKBAFnmZbvAR-ZRdhIodoktURTk_og"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "ngrok-skip-browser-warning": "true"
}

def api_get_afiliado(cedula):
    """Consulta real al endpoint GET /afiliados/{id_usuario} con manejo seguro de errores"""
    try:
        url = f"{BASE_URL}/afiliados/{cedula}"
        response = requests.get(url, headers=HEADERS, timeout=5)
        if response.status_code == 200:
            return response.json()
        return {"afiliado": False}
    except Exception:
        return {"afiliado": False}

def api_post_perfilar(payload):
    try:
        url = f"{BASE_URL}/perfilar"
        response = requests.post(url, headers=HEADERS, json=payload, timeout=10)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            return {"error": f"Error del servidor: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": f"Falla de conexión: {e}"}

# --- INICIALIZACIÓN DE ESTADOS ---
def get_empty_lead(cedula=""):
    return {
        "id_usuario": str(cedula),
        "nombre": "",
        "afiliado": False,
        "categoria": "A",
        "antiguedad_meses": 0,
        "tipo_cotizante": "dependiente",
        "ingresos_mensuales": 0.0,
        "grupo_sisben": "N/A",
        "edad": 30,
        "personas_a_cargo": 0,
        "condiciones_especiales": {"cabeza_de_hogar": False, "discapacidad_hogar": False, "mayor_65_anos": False},
        "propietario_vivienda": False,
        "subsidio_previo": False,
        "subsidio_previo_fue_arrendamiento": False,
        "finanzas": {"cesantias": 0.0, "ahorros": 0.0, "credito_preaprobado": False},
        "tipo_empresa": "Medianas",
        "zona_preferida": "Soacha",
        "valor_vivienda_deseada": 150000000.0,
        "origen": "organico"
    }

if 'nivel' not in st.session_state: st.session_state.nivel = 0
if 'lead' not in st.session_state: st.session_state.lead = get_empty_lead()
if 'api_response' not in st.session_state: st.session_state.api_response = None

# --- PANEL LATERAL (MOCHILA) ---
with st.sidebar:
    st.markdown("<h2 style='color: #0067b1; text-align: center; margin-bottom: 20px; font-weight: 800;'>🎒 Tu Mochila VIS</h2>", unsafe_allow_html=True)
    st.progress(st.session_state.nivel / 4)
    st.caption(f"Progreso actual: Nivel {st.session_state.nivel} de 4")
    st.divider()
    
    if st.session_state.nivel > 0:
        afil = "✅ Afiliado Colsubsidio" if st.session_state.lead['afiliado'] else "❌ Usuario Externo"
        st.markdown(f"**Identidad:**<br>{afil}", unsafe_allow_html=True)
        st.write("")
        
    if st.session_state.nivel > 1:
        zona = st.session_state.lead['zona_preferida']
        st.markdown(f"**Destino Elegido:**<br>📍 {zona}", unsafe_allow_html=True)
        st.write("")
        
    if st.session_state.nivel > 2:
        oro = st.session_state.lead['finanzas']['cesantias'] + st.session_state.lead['finanzas']['ahorros']
        st.markdown(f"**Cofre de Ahorros:**<br>💰 ${oro:,.0f}", unsafe_allow_html=True)

# --- CABECERA ---
st.markdown("<div class='game-header'><h1>🏠 El Camino hacia tu Casa Propia</h1><p style='color: #e2e8f0; font-size: 1.1rem; margin-top: 5px;'>Asesor Digital Inteligente — Colsubsidio</p></div>", unsafe_allow_html=True)

# --- MAPA VISUAL ---
etapas = [("🔐", "Identidad"), ("📐", "Planos"), ("🧱", "Cimientos"), ("🏗️", "Estructura"), ("🔑", "La Llave")]
mapa_html = '<div class="roadmap-container"><div class="roadmap-line"></div>'
for i, (icono, nombre) in enumerate(etapas):
    clase = "step-active" if i == st.session_state.nivel else ("step-done" if i < st.session_state.nivel else "")
    mapa_html += f'<div class="roadmap-step {clase}"><div class="roadmap-icon">{icono}</div><div class="step-label">{nombre}</div></div>'
mapa_html += '</div>'
st.markdown(mapa_html, unsafe_allow_html=True)

# --- FLUJO DE JUEGO ---
with st.container():
    
    # NIVEL 0: IDENTIFICACIÓN (GET API BLINDADO)
    if st.session_state.nivel == 0:
        st.markdown("<div class='stage-container'><div class='house-graphic'>🏕️</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='narrative-box'>
            <div class='narrative-title'>Paso 1: Explorando el Terreno</div>
            ¡Hola! Para verificar si tienes subsidios automáticos en nuestra Caja de Compensación y agilizar tu proceso, comparte tu documento de identidad.
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            cedula = st.text_input("Documento", placeholder="Escribe tu cédula...", key="input_cedula")
            st.write("")
            if st.button("🔍 Consultar Cédula (API GET)", use_container_width=True):
                if cedula:
                    with st.spinner("Conectando con el servidor seguro de Colsubsidio..."):
                        datos_api = api_get_afiliado(cedula)
                        st.session_state.lead = get_empty_lead(cedula)
                        
                        # Validación segura usando .get() para evitar KeyErrors
                        es_afil = False
                        if isinstance(datos_api, dict):
                            es_afil = datos_api.get("afiliado", False) or ("datos" in datos_api and datos_api.get("datos") is not None)
                        
                        if es_afil:
                            info = datos_api.get("datos", datos_api) if isinstance(datos_api, dict) else {}
                            st.session_state.lead['afiliado'] = True
                            st.session_state.lead['nombre'] = info.get("nombre", "Afiliado")
                            st.session_state.lead['personas_a_cargo'] = info.get("personas_a_cargo", 0)
                            st.session_state.lead['categoria'] = info.get("categoria", "A")
                            st.session_state.lead['antiguedad_meses'] = info.get("antiguedad_meses", 12)
                            st.success("¡Afiliación encontrada en línea con éxito!")
                        else:
                            st.info("No se encontró afiliación activa en el servidor. Continuaremos el proceso como usuario independiente.")
                            
                        st.session_state.nivel = 1
                        st.rerun()
                else:
                    st.warning("Debes ingresar un número de documento válido.")
        st.markdown("</div>", unsafe_allow_html=True)

    # NIVEL 1: PLANOS
    elif st.session_state.nivel == 1:
        st.markdown("<div class='stage-container'><div class='house-graphic'>📐</div>", unsafe_allow_html=True)
        afiliado = st.session_state.lead['afiliado']
        
        mensaje = "¡Tus datos de afiliado se cargaron automáticamente!" if afiliado else "Por favor completa tus datos básicos para diseñar tu ruta."
        st.markdown(f"<div class='narrative-box'><div class='narrative-title'>Paso 2: Dibujando los Planos</div>{mensaje}</div>", unsafe_allow_html=True)
        
        if not afiliado:
            st.markdown("**¿Cómo te llamas?**")
            st.session_state.lead['nombre'] = st.text_input("Nombres", placeholder="Tus nombres...")
            st.markdown("**¿Cuáles son tus ingresos mensuales? (COP)**")
            st.session_state.lead['ingresos_mensuales'] = st.number_input("Ingresos", step=100000, value=1500000)
            
        st.markdown("**Desliza para indicar tu edad:**")
        edad = st.slider("Edad", 18, 80, 30)
        st.markdown("**¿En qué zona deseas tu hogar?**")
        zona = st.radio("Zona", ["Soacha", "Bogotá", "Tocancipá", "Girardot"])
        
        st.write("")
        if st.button("✅ Aprobar Planos", use_container_width=True):
            st.session_state.lead['edad'] = edad
            st.session_state.lead['zona_preferida'] = zona
            st.session_state.nivel = 2
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # NIVEL 2: CIMIENTOS
    elif st.session_state.nivel == 2:
        st.markdown("<div class='stage-container'><div class='house-graphic'>🧱</div>", unsafe_allow_html=True)
        st.markdown("<div class='narrative-box'><div class='narrative-title'>Paso 3: Vertiendo los Cimientos</div>Registra tus cesantías y ahorros para calcular tu capacidad de cuota inicial.</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        cesantias = c1.number_input("Cesantías (COP):", min_value=0.0, step=500000.0, value=2000000.0)
        ahorros = c2.number_input("Ahorros (COP):", min_value=0.0, step=500000.0, value=2000000.0)
        
        st.write("")
        if st.button("💪 Cimientos Listos", use_container_width=True):
            st.session_state.lead['finanzas']['cesantias'] = float(cesantias)
            st.session_state.lead['finanzas']['ahorros'] = float(ahorros)
            st.session_state.nivel = 3
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # NIVEL 3: ESTRUCTURA
    elif st.session_state.nivel == 3:
        st.markdown("<div class='stage-container'><div class='house-graphic'>🏗️</div>", unsafe_allow_html=True)
        st.markdown("<div class='narrative-box'><div class='narrative-title'>Paso 4: Levantando Estructura</div>Validamos condiciones especiales de ley y filtros de elegibilidad del motor de reglas.</div>", unsafe_allow_html=True)
        
        cabeza = st.toggle("👑 Cabeza de Hogar")
        cred_aprobado = st.toggle("💳 Crédito hipotecario pre-aprobado")
        propiedades = st.toggle("🚫 ¿Ya posee propiedad raíz a su nombre?")
        
        st.write("")
        if st.button("🔨 Finalizar y Evaluar Perfil (API POST)", use_container_width=True):
            st.session_state.lead['condiciones_especiales']['cabeza_de_hogar'] = bool(cabeza)
            st.session_state.lead['finanzas']['credito_preaprobado'] = bool(cred_aprobado)
            st.session_state.lead['propietario_vivienda'] = bool(propiedades)
            
            with st.spinner("Procesando motor de reglas e inteligencia artificial..."):
                st.session_state.api_response = api_post_perfilar(st.session_state.lead)
                
            st.session_state.nivel = 4
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # NIVEL 4: RESULTADO / MENTORÍA
    elif st.session_state.nivel == 4:
        st.markdown("<div class='stage-container'><div class='house-graphic'>🏠✨</div>", unsafe_allow_html=True)
        
        res = st.session_state.api_response
        
        if res and "error" not in res:
            st.markdown(f"<div class='narrative-box' style='background:#d1fae5; color:#065f46; border-left-color:#10b981;'><div class='narrative-title' style='color:#065f46;'>¡Perfilamiento Exitoso!</div>{res.get('ai_summary', 'Proceso completado correctamente.')}</div>", unsafe_allow_html=True)
            
            st.markdown("### 🎯 Proyecto Recomendado")
            for proj in res.get("matching_projects", []):
                st.success(f"**{proj['proyecto']}** ({proj['municipio']}) - Match: {proj['match_score']}% | Precio: ${proj['precio']:,.0f}")
                st.caption(proj['motivo'])
                
            st.markdown("### 🎒 Mochila de Radicación (Documentos Oficiales)")
            st.link_button("📝 Descargar Formulario de Postulación", "https://www.colsubsidio.com/hubfs/documentos/colsubsidio/formulario-postulacion-subsidio-vivienda-colsubsidio-radicacion-digital.pdf", use_container_width=True)
            
        else:
            st.markdown("""
            <div class='narrative-box' style='background:#fef3c7; color:#92400E; border-left-color:#f59e0b;'>
                <div class='narrative-title' style='color:#b45309;'>Programa de Acompañamiento PerteneSer</div>
                Estamos afinando los últimos detalles de conexión con el servidor central, pero ponemos a tu disposición los canales oficiales y de ahorro de Colsubsidio.
            </div>
            """, unsafe_allow_html=True)
            st.link_button("📝 Formulario de Postulación Oficial", "https://www.colsubsidio.com/hubfs/documentos/colsubsidio/formulario-postulacion-subsidio-vivienda-colsubsidio-radicacion-digital.pdf", use_container_width=True)

        st.divider()
        with st.expander("💻 Ver JSON enviado a /perfilar"):
            st.json(st.session_state.lead)
        with st.expander("💻 Ver JSON recibido de la API"):
            st.json(res)
            
        st.write("")
        if st.button("🔄 Reiniciar Aventura", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("🔄 Reiniciar Aventura", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

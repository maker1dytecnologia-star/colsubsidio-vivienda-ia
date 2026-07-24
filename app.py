import streamlit as st
import requests
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Colsubsidio - Mi Camino VIS", layout="wide", initial_sidebar_state="expanded")

# --- CSS EXTREMADAMENTE VISUAL (Fondo Animado y Layout) ---
st.markdown("""
<style>
    .stApp { 
        background: linear-gradient(-45deg, #F0F4F8, #E2E8F0, #F8FAFC, #EEF2FF);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        background-image: radial-gradient(rgba(0, 45, 114, 0.05) 1px, transparent 1px);
        background-size: 20px 20px;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .game-header { background: #002D72; padding: 30px; color: white; text-align: center; border-radius: 0 0 30px 30px; margin-top: -60px; margin-bottom: 30px; box-shadow: 0 10px 25px rgba(0,0,0,0.15); border-bottom: 5px solid #FFCD00; }
    .game-header h1 { color: #FFCD00 !important; font-weight: 900; font-size: 2.8rem; letter-spacing: -1px; }

    .roadmap-container { display: flex; justify-content: space-between; align-items: center; position: relative; margin: 20px auto 50px auto; padding: 0 5%; max-width: 1000px; }
    .roadmap-step { display: flex; flex-direction: column; align-items: center; position: relative; z-index: 2; width: 20%; }
    .roadmap-icon { font-size: 2.5rem; background: white; border: 5px solid #E2E8F0; border-radius: 50%; width: 80px; height: 80px; display: flex; justify-content: center; align-items: center; z-index: 2; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
    .step-active .roadmap-icon { border-color: #FFCD00; background: #FEF3C7; transform: scale(1.2); box-shadow: 0 0 20px rgba(255, 205, 0, 0.6); }
    .step-done .roadmap-icon { border-color: #10B981; background: #D1FAE5; }
    .step-label { font-weight: bold; margin-top: 15px; color: #64748B; font-size: 1rem; text-align: center; text-transform: uppercase; letter-spacing: 1px; }
    .step-active .step-label { color: #002D72; font-size: 1.1rem; }
    .roadmap-line { position: absolute; top: 40px; left: 10%; right: 10%; height: 6px; background: #E2E8F0; z-index: 1; border-radius: 3px; }
    
    .stage-container { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border-radius: 25px; padding: 50px; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.1); margin: 0 auto 40px auto; border: 1px solid rgba(255,255,255,0.5); max-width: 900px; }
    .house-graphic { font-size: 120px; line-height: 1; margin-bottom: 30px; filter: drop-shadow(0 10px 15px rgba(0,0,0,0.15)); animation: popIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
    
    .narrative-box { background: #F8FAFC; border-left: 8px solid #4F46E5; padding: 25px 35px; border-radius: 0 15px 15px 0; text-align: left; margin: 0 auto 40px auto; font-size: 1.2rem; color: #334155; line-height: 1.7; box-shadow: inset 0 2px 4px rgba(0,0,0,0.02); }
    .narrative-title { font-weight: 900; color: #4F46E5; margin-bottom: 15px; font-size: 1.4rem; text-transform: uppercase; letter-spacing: 0.5px; }
    
    .stSlider > label, .stNumberInput > label, .stRadio > label, .stSelectbox > label { display: none; }
    div.row-widget.stRadio > div { flex-direction: row; flex-wrap: wrap; gap: 15px; justify-content: center; }
    div.row-widget.stRadio > div > label { background: white; padding: 15px 30px; border-radius: 50px; border: 2px solid #E2E8F0; cursor: pointer; transition: all 0.2s; font-weight: bold; color: #475569; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    div.row-widget.stRadio > div > label:hover { border-color: #002D72; background: #F0F4F8; transform: translateY(-2px); }
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 2px solid #F1F5F9; }
    @keyframes popIn { 0% { transform: scale(0.5); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE API REAL ---
BASE_URL = "https://composite-suing-grandly.ngrok-free.dev"
API_KEY = "AQ.Ab8RN6J3asN8cwgzqstvEKBAFnmZbvAR-ZRdhIodoktURTk_og"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "ngrok-skip-browser-warning": "true" # Necesario para evitar la página de advertencia de ngrok
}

def api_get_afiliado(cedula):
    """Consulta real al endpoint GET /afiliados/{id_usuario}"""
    try:
        url = f"{BASE_URL}/afiliados/{cedula}"
        response = requests.get(url, headers=HEADERS, timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.warning(f"No se pudo conectar al servidor de afiliados: {e}")
        return None

def api_post_perfilar(payload):
    """Petición real al endpoint POST /perfilar"""
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
        "datos_personales": {"tipo_documento": "CC", "numero_documento": cedula, "nombres": "", "apellidos": "", "celular": "", "correo": ""},
        "afiliacion_colsubsidio": {"es_afiliado": False, "tipo_afiliado": "Independiente", "antiguedad_meses": 0, "categoria": "No Afiliado", "segmento_poblacional": "N/A", "personas_a_cargo_registradas": 0},
        "datos_financieros_declarados": {"ingresos_mensuales_hogar": 0.0, "cesantias_inmovilizadas": 0.0, "ahorro_programado": 0.0, "tiene_credito": False, "monto_credito_aprobado": 0.0},
        "preferencias_e_intencion": {"zona_interes": "Soacha", "proyecto_interes": "", "posee_vivienda_propia": False},
        "informacion_socioeconomica_externa": {"tiene_registro_sisben": False, "grupo_sisben": "N/A", "tiene_subsidios_previos": False, "tiene_propiedades_snr": 0},
        "condiciones_especiales_ley": {"cabeza_de_hogar": False, "discapacidad_hogar": False, "mayor_65_anos": False}
    }

if 'nivel' not in st.session_state: st.session_state.nivel = 0
if 'lead' not in st.session_state: st.session_state.lead = get_empty_lead()
if 'api_response' not in st.session_state: st.session_state.api_response = None

# --- PANEL LATERAL (MOCHILA) ---
with st.sidebar:
    st.markdown("<h2 style='color: #002D72; text-align: center; margin-bottom: 30px;'>🎒 Tu Mochila VIS</h2>", unsafe_allow_html=True)
    st.progress(st.session_state.nivel / 4)
    st.caption(f"Progreso: Nivel {st.session_state.nivel} de 4")
    st.divider()
    
    if st.session_state.nivel > 0:
        afil = "✅ Afiliado" if st.session_state.lead['afiliacion_colsubsidio']['es_afiliado'] else "❌ No Afiliado"
        st.markdown(f"**Identidad:**<br>{afil}", unsafe_allow_html=True)
        st.write("")
        
    if st.session_state.nivel > 1:
        zona = st.session_state.lead['preferencias_e_intencion']['zona_interes']
        st.markdown(f"**Destino Elegido:**<br>📍 {zona}", unsafe_allow_html=True)
        st.write("")
        
    if st.session_state.nivel > 2:
        oro = st.session_state.lead['datos_financieros_declarados']['cesantias_inmovilizadas'] + st.session_state.lead['datos_financieros_declarados']['ahorro_programado']
        st.markdown(f"**Cofre de Ahorros:**<br>💰 ${oro:,.0f}", unsafe_allow_html=True)

# --- CABECERA ---
st.markdown("<div class='game-header'><h1>🏠 El Camino hacia tu Casa Propia</h1></div>", unsafe_allow_html=True)

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
    
    # NIVEL 0: IDENTIFICACIÓN (GET API)
    if st.session_state.nivel == 0:
        st.markdown("<div class='stage-container'><div class='house-graphic'>🏕️</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='narrative-box'>
            <div class='narrative-title'>Paso 1: Explorando el Terreno</div>
            ¡Hola! Para verificar si tienes subsidios automáticos en nuestra Caja de Compensación, comparte tu documento de identidad.
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            cedula = st.text_input("Documento", placeholder="Escribe tu cédula...", key="input_cedula")
            st.write("")
            if st.button("🔍 Consultar Cédula (API GET)", type="primary", use_container_width=True):
                if cedula:
                    with st.spinner("Conectando con el servidor de Colsubsidio..."):
                        datos_api = api_get_afiliado(cedula)
                        st.session_state.lead = get_empty_lead(cedula)
                        
                        if datos_api and datos_api.get("afiliado"):
                            info = datos_api.get("datos", {})
                            st.session_state.lead['afiliacion_colsubsidio']['es_afiliado'] = True
                            st.session_state.lead['datos_personales']['nombres'] = info.get("nombre", "Afiliado")
                            st.session_state.lead['afiliacion_colsubsidio']['personas_a_cargo_registradas'] = info.get("personas_a_cargo", 0)
                            st.session_state.lead['afiliacion_colsubsidio']['categoria'] = info.get("categoria", "A")
                            st.success("¡Afiliación encontrada en línea!")
                        else:
                            st.info("No se encontró afiliación activa. Continuaremos como usuario independiente.")
                            
                        st.session_state.nivel = 1
                        st.rerun()
                else:
                    st.warning("Ingresa un número válido.")
        st.markdown("</div>", unsafe_allow_html=True)

    # NIVEL 1: PLANOS
    elif st.session_state.nivel == 1:
        st.markdown("<div class='stage-container'><div class='house-graphic'>📐</div>", unsafe_allow_html=True)
        afiliado = st.session_state.lead['afiliacion_colsubsidio']['es_afiliado']
        
        mensaje = "¡Tus datos de afiliado llegaron con éxito!" if afiliado else "Por favor completa tus datos básicos para iniciar."
        st.markdown(f"<div class='narrative-box'><div class='narrative-title'>Paso 2: Dibujando los Planos</div>{mensaje}</div>", unsafe_allow_html=True)
        
        if not afiliado:
            st.markdown("**¿Cómo te llamas?**")
            st.session_state.lead['datos_personales']['nombres'] = st.text_input("Nombres", placeholder="Tus nombres...")
            st.markdown("**¿Cuáles son tus ingresos mensuales? (COP)**")
            st.session_state.lead['datos_financieros_declarados']['ingresos_mensuales_hogar'] = st.number_input("Ingresos", step=100000, value=1500000)
            
        st.markdown("**Desliza para indicar tu edad:**")
        edad = st.slider("Edad", 18, 80, 30)
        st.markdown("**¿En qué zona deseas tu hogar?**")
        zona = st.radio("Zona", ["Soacha", "Bogotá", "Tocancipá", "Girardot"])
        
        if st.button("✅ Aprobar Planos", type="primary", use_container_width=True):
            st.session_state.lead['datos_personales']['edad'] = edad
            st.session_state.lead['preferencias_e_intencion']['zona_interes'] = zona
            st.session_state.nivel = 2
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # NIVEL 2: CIMIENTOS
    elif st.session_state.nivel == 2:
        st.markdown("<div class='stage-container'><div class='house-graphic'>🧱</div>", unsafe_allow_html=True)
        st.markdown("<div class='narrative-box'><div class='narrative-title'>Paso 3: Vertiendo los Cimientos</div>Registra tus cesantías y ahorros para calcular tu cuota inicial.</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        cesantias = c1.number_input("Cesantías (COP):", min_value=0, step=500000, value=2000000)
        ahorros = c2.number_input("Ahorros (COP):", min_value=0, step=500000, value=2000000)
        
        if st.button("💪 Cimientos Listos", type="primary", use_container_width=True):
            st.session_state.lead['datos_financieros_declarados']['cesantias_inmovilizadas'] = cesantias
            st.session_state.lead['datos_financieros_declarados']['ahorro_programado'] = ahorros
            st.session_state.nivel = 3
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

   # ---------------------------------------------------------
    # NIVEL 3: ESTRUCTURA (Blindaje de Tipos de Datos)
    # ---------------------------------------------------------
    elif st.session_state.nivel == 3:
        st.markdown("<div class='stage-container'><div class='house-graphic'>🏗️</div>", unsafe_allow_html=True)
        st.markdown("<div class='narrative-box'><div class='narrative-title'>Paso 4: Levantando Estructura</div>Validamos condiciones especiales y filtros legales.</div>", unsafe_allow_html=True)
        
        cabeza = st.toggle("👑 Cabeza de Hogar")
        cred_aprobado = st.toggle("💳 Crédito hipotecario pre-aprobado")
        propiedades = st.toggle("🚫 ¿Ya posee propiedad a su nombre?")
        
        # Opcional: si quieres pedir un monto rápido de crédito en caso de que lo tenga
        monto_credito = 0.0
        if cred_aprobado:
            monto_credito = st.number_input("Monto aproximado del crédito pre-aprobado (COP):", min_value=0.0, step=1000000.0, value=100000000.0)

        st.write("")
        if st.button("🔨 Finalizar y Evaluar Perfil (API POST)", type="primary", use_container_width=True):
            # 1. Aseguramos condiciones especiales
            st.session_state.lead['condiciones_especiales_ley']['cabeza_de_hogar'] = bool(cabeza)
            
            # 2. Blindamos finanzas para evitar nulls o NoneTypes que causan el error 500
            finanzas = st.session_state.lead['datos_financieros_declarados']
            finanzas['tiene_credito'] = bool(cred_aprobado)
            finanzas['tiene_credito_hipotecario_aprobado'] = bool(cred_aprobado)
            finanzas['monto_credito_aprobado'] = float(monto_credito if cred_aprobado else 0.0)
            
            # Asegurar que ingresos y ahorros nunca sean None
            if finanzas.get('ingresos_mensuales_hogar') is None:
                finanzas['ingresos_mensuales_hogar'] = 0.0
            if finanzas.get('cesantias_inmovilizadas') is None:
                finanzas['cesantias_inmovilizadas'] = 0.0
            if finanzas.get('ahorro_programado') is None:
                finanzas['ahorro_programado'] = 0.0

            # 3. Blindamos socioeconómica externa
            ext = st.session_state.lead['informacion_socioeconomica_externa']
            ext['tiene_propiedades_snr'] = int(1 if propiedades else 0)

            with st.spinner("Enviando JSON al motor de reglas..."):
                st.session_state.api_response = api_post_perfilar(st.session_state.lead)
                
            st.session_state.nivel = 4
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # NIVEL 4: RESULTADO / MENTORÍA
    elif st.session_state.nivel == 4:
        st.markdown("<div class='stage-container'><div class='house-graphic'>🏠✨</div>", unsafe_allow_html=True)
        
        res = st.session_state.api_response
        
        if res and "error" not in res:
            # Si el backend respondió correctamente con el JSON acordado
            st.markdown(f"<div class='narrative-box' style='background:#D1FAE5; color:#065F46;'><div class='narrative-title'>¡Perfilamiento Exitoso!</div>{res.get('ai_summary', 'Proceso completado.')}</div>", unsafe_allow_html=True)
            
            st.markdown("### 🎯 Proyecto Recomendado")
            for proj in res.get("matching_projects", []):
                st.success(f"**{proj['proyecto']}** ({proj['municipio']}) - Match: {proj['match_score']}% | Precio: ${proj['precio']:,.0f}")
                st.caption(proj['motivo'])
                
            st.markdown("### 🎒 Mochila de Radicación (Documentos Oficiales)")
            st.link_button("📝 Descargar Formulario de Postulación", "https://www.colsubsidio.com/hubfs/documentos/colsubsidio/formulario-postulacion-subsidio-vivienda-colsubsidio-radicacion-digital.pdf", use_container_width=True)
            
        else:
            # Ruta de Mentoría / Plan B (PerteneSer) si la API no está arriba o retorna rechazo
            st.markdown("""
            <div class='narrative-box' style='background:#FEF3C7; color:#92400E; border-left-color:#F59E0B;'>
                <div class='narrative-title'>Programa de Acompañamiento PerteneSer</div>
                Estamos afinando detalles con el servidor central, pero te invitamos a conocer nuestro plan de fortalecimiento de ahorro y Subsidio de Arrendamiento Colsubsidio.
            </div>
            """, unsafe_allow_html=True)
            st.link_button("📝 Formulario de Postulación Oficial", "https://www.colsubsidio.com/hubfs/documentos/colsubsidio/formulario-postulacion-subsidio-vivienda-colsubsidio-radicacion-digital.pdf", use_container_width=True)

        st.divider()
        with st.expander("💻 Ver JSON enviado a /perfilar"):
            st.json(st.session_state.lead)
        with st.expander("💻 Ver JSON recibido de la API"):
            st.json(res)
            
        if st.button("🔄 Reiniciar Aventura", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

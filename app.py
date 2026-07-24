import streamlit as st
import requests
import json
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Colsubsidio - Misión VIS", layout="wide", initial_sidebar_state="expanded")

# --- CSS: FONDO DINÁMICO (BLUEPRINT EN MOVIMIENTO) Y GAMIFICACIÓN ---
st.markdown("""
<style>
    /* Fondo Dinámico: Patrón de planos que se mueve suavemente */
    .stApp {
        background-color: #f0f7ff;
        background-image: 
            linear-gradient(rgba(0, 103, 177, 0.07) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 103, 177, 0.07) 1px, transparent 1px),
            linear-gradient(rgba(0, 103, 177, 0.03) 2px, transparent 2px),
            linear-gradient(90deg, rgba(0, 103, 177, 0.03) 2px, transparent 2px);
        background-size: 100px 100px, 100px 100px, 20px 20px, 20px 20px;
        background-position: -2px -2px, -2px -2px, -1px -1px, -1px -1px;
        animation: panBlueprint 60s linear infinite;
    }

    @keyframes panBlueprint {
        0% { background-position: 0px 0px, 0px 0px, 0px 0px, 0px 0px; }
        100% { background-position: 500px 500px, 500px 500px, 500px 500px, 500px 500px; }
    }

    /* Cabecera RPG */
    .game-header { 
        background: linear-gradient(135deg, #0067b1 0%, #003a66 100%); 
        padding: 25px; color: white; text-align: center; border-radius: 0 0 40px 40px; 
        margin-top: -60px; margin-bottom: 35px; box-shadow: 0 15px 35px rgba(0, 103, 177, 0.25); 
        border-bottom: 5px solid #ffd000; position: relative; z-index: 1;
    }
    .game-header h1 { color: #ffd000 !important; font-weight: 900; font-size: 2.8rem; text-shadow: 0 4px 6px rgba(0,0,0,0.3); }

    /* Contenedor Principal Estilo Tarjeta de Misión */
    .stage-container { 
        background: rgba(255, 255, 255, 0.9); 
        backdrop-filter: blur(10px);
        border-radius: 20px; padding: 40px; text-align: center; 
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1); 
        margin: 0 auto 30px auto; max-width: 800px; 
        border: 2px solid rgba(0, 103, 177, 0.15); 
    }
    .house-graphic { font-size: 90px; margin-bottom: 15px; filter: drop-shadow(0 10px 15px rgba(0,0,0,0.15)); }
    
    /* Caja de Narrativa Estilo "Master del Juego" */
    .narrative-box { background: #ffffff; border-left: 8px solid #ffd000; padding: 20px 30px; border-radius: 8px; text-align: left; margin: 0 auto 30px auto; font-size: 1.15rem; color: #333; line-height: 1.6; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    .narrative-title { font-weight: 900; color: #0067b1; margin-bottom: 8px; font-size: 1.3rem; text-transform: uppercase; letter-spacing: 1px;}
    
    /* Modificación de Formularios para Gamificación */
    [data-testid="stForm"] { border: none !important; padding: 0 !important; background: transparent !important; box-shadow: none !important; }
    .stButton > button { background-color: #0067b1 !important; color: white !important; font-weight: 800; border-radius: 30px; border: none; padding: 0.8rem 2rem; transition: transform 0.2s, box-shadow 0.2s; box-shadow: 0 4px 15px rgba(0, 103, 177, 0.3); width: 100%; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 1px;}
    .stButton > button:hover { transform: translateY(-3px) scale(1.02); box-shadow: 0 8px 20px rgba(0, 103, 177, 0.5); background-color: #00508a !important; }
    
    [data-testid="stSidebar"] { background-color: rgba(255,255,255,0.95); border-right: 2px solid #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE API (Mocks temporales para la UI) ---
def api_get_afiliado(cedula):
    time.sleep(1) # Simular carga para el efecto de juego
    if cedula == "1018300400":
        return {"afiliado": True, "datos": {"nombre": "Diana Carolina Rangel", "categoria": "A", "antiguedad_meses": 24, "personas_a_cargo": 2}}
    return {"afiliado": False}

def api_post_perfilar(payload):
    time.sleep(1.5)
    return {
        "matching_projects": [{"proyecto": "Ciudadela Maiporé - Soacha", "municipio": payload.get("zona_preferida", "Soacha"), "precio": 150000000, "match_score": 94.5, "motivo": "Alto nivel de coincidencia con tu perfil."}],
        "ai_summary": "¡Misión completada! Tienes un perfil altamente compatible con nuestros subsidios."
    }

def get_empty_lead(cedula=""):
    return {"id_usuario": str(cedula), "nombre": "", "afiliado": False, "ingresos_mensuales": 0.0, "edad": 30, "condiciones_especiales": {"cabeza_de_hogar": False}, "finanzas": {"cesantias": 0.0, "ahorros": 0.0, "credito_preaprobado": False}, "zona_preferida": "Soacha"}

if 'nivel' not in st.session_state: st.session_state.nivel = 0
if 'lead' not in st.session_state: st.session_state.lead = get_empty_lead()

# --- PANEL LATERAL (INVENTARIO DEL JUGADOR) ---
with st.sidebar:
    st.markdown("<h2 style='color: #0067b1; text-align: center; font-weight: 900;'>🛡️ Tu Inventario</h2>", unsafe_allow_html=True)
    st.progress(st.session_state.nivel / 4)
    st.caption(f"⭐ Nivel de Misión: {st.session_state.nivel} / 4")
    st.divider()
    if st.session_state.nivel > 0:
        st.markdown(f"**Clase:**<br>{'🔵 Afiliado VIP' if st.session_state.lead['afiliado'] else '⚪ Explorador Externo'}", unsafe_allow_html=True)
    if st.session_state.nivel > 1:
        st.markdown(f"<br>**Territorio:**<br>📍 {st.session_state.lead['zona_preferida']}", unsafe_allow_html=True)
    if st.session_state.nivel > 2:
        oro = st.session_state.lead['finanzas']['cesantias'] + st.session_state.lead['finanzas']['ahorros']
        st.markdown(f"<br>**Oro Acumulado:**<br>💰 ${oro:,.0f}", unsafe_allow_html=True)

# --- CABECERA ---
st.markdown("<div class='game-header'><h1>🏠 Operación: Casa Propia</h1><p style='color: #ffffff; font-size: 1.1rem; font-weight: 500;'>Guía Interactiva VIS Colsubsidio</p></div>", unsafe_allow_html=True)

# --- FLUJO DE JUEGO ---
with st.container():
    
    # MISION 1
    if st.session_state.nivel == 0:
        st.markdown("<div class='stage-container'><div class='house-graphic'>🏕️</div>", unsafe_allow_html=True)
        st.markdown("<div class='narrative-box'><div class='narrative-title'>Misión 1: El Escaneo Inicial</div>¡Bienvenido, explorador! Para descubrir si el oráculo de Colsubsidio tiene recompensas ocultas para ti, debes revelar tu identidad. (Presiona Enter para avanzar)</div>", unsafe_allow_html=True)
        
        # El uso de st.form permite atrapar el "Enter"
        with st.form(key="form_nivel_0"):
            cedula = st.text_input("Ingresa tu número de documento de identidad:")
            submit = st.form_submit_button("🔍 Escanear Identidad")
            
            if submit:
                if cedula:
                    datos_api = api_get_afiliado(cedula)
                    st.session_state.lead = get_empty_lead(cedula)
                    
                    if datos_api.get("afiliado"):
                        st.session_state.lead['afiliado'] = True
                        st.session_state.lead['nombre'] = datos_api["datos"].get("nombre", "")
                        st.toast('¡Objeto Legendario Encontrado: Carnet de Afiliado! 🌟', icon='🔥')
                    else:
                        st.toast('Modo Explorador Activado. ¡Vamos a construir tu ruta! 🗺️', icon='🧭')
                        
                    st.session_state.nivel = 1
                    st.rerun()
                else:
                    st.warning("El campo no puede estar vacío.")
        st.markdown("</div>", unsafe_allow_html=True)

    # MISION 2
    elif st.session_state.nivel == 1:
        st.markdown("<div class='stage-container'><div class='house-graphic'>🗺️</div>", unsafe_allow_html=True)
        afiliado = st.session_state.lead['afiliado']
        mensaje = f"¡Te reconocemos, {st.session_state.lead['nombre']}! Tu data está segura." if afiliado else "Necesitamos crear tu avatar en el sistema."
        st.markdown(f"<div class='narrative-box'><div class='narrative-title'>Misión 2: Trazando el Mapa</div>{mensaje} Define las coordenadas de tu futuro hogar. (Llena los datos y presiona Enter)</div>", unsafe_allow_html=True)
        
        with st.form(key="form_nivel_1"):
            if not afiliado:
                nombre = st.text_input("¿Cuál es el nombre de tu Avatar?")
                ingresos = st.number_input("Poder adquisitivo mensual (Ingresos en COP):", step=100000, value=1500000)
            
            edad = st.slider("Nivel de Experiencia (Tu edad actual):", 18, 80, 30)
            zona = st.selectbox("Selecciona el territorio a conquistar:", ["Soacha", "Bogotá", "Tocancipá", "Girardot"])
            
            submit = st.form_submit_button("⚔️ Fijar Coordenadas")
            
            if submit:
                if not afiliado:
                    st.session_state.lead['nombre'] = nombre
                    st.session_state.lead['ingresos_mensuales'] = ingresos
                st.session_state.lead['edad'] = int(edad)
                st.session_state.lead['zona_preferida'] = str(zona)
                st.toast('¡Mapa actualizado! Nueva zona desbloqueada. 🔓', icon='✅')
                st.session_state.nivel = 2
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # MISION 3
    elif st.session_state.nivel == 2:
        st.markdown("<div class='stage-container'><div class='house-graphic'>🧱</div>", unsafe_allow_html=True)
        st.markdown("<div class='narrative-box'><div class='narrative-title'>Misión 3: La Bóveda de Recursos</div>Un castillo necesita cimientos fuertes. ¿Cuánto oro has logrado acumular en tus aventuras pasadas?</div>", unsafe_allow_html=True)
        
        with st.form(key="form_nivel_2"):
            c1, c2 = st.columns(2)
            cesantias = c1.number_input("Tus Cesantías inmovilizadas (COP):", min_value=0.0, step=500000.0, value=2000000.0)
            ahorros = c2.number_input("Tus Ahorros voluntarios (COP):", min_value=0.0, step=500000.0, value=2000000.0)
            
            submit = st.form_submit_button("💰 Guardar en la Bóveda")
            
            if submit:
                st.session_state.lead['finanzas']['cesantias'] = float(cesantias)
                st.session_state.lead['finanzas']['ahorros'] = float(ahorros)
                st.toast('¡Recursos asegurados! 💎', icon='🏰')
                st.session_state.nivel = 3
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # MISION 4
    elif st.session_state.nivel == 3:
        st.markdown("<div class='stage-container'><div class='house-graphic'>⚖️</div>", unsafe_allow_html=True)
        st.markdown("<div class='narrative-box'><div class='narrative-title'>Batalla Final: El Filtro del Oráculo</div>Estamos a punto de consultar a la Inteligencia Artificial. Activa tus modificadores especiales antes de enviar tu perfil.</div>", unsafe_allow_html=True)
        
        with st.form(key="form_nivel_3"):
            st.markdown("### Modificadores de Perfil")
            cabeza = st.checkbox("👑 Habilidad: Cabeza de Hogar")
            cred_aprobado = st.checkbox("📜 Pergamino: Crédito Pre-aprobado")
            
            submit = st.form_submit_button("🚀 Consultar al Oráculo (Enviar Misión)")
            
            if submit:
                st.session_state.lead['condiciones_especiales']['cabeza_de_hogar'] = bool(cabeza)
                st.session_state.lead['finanzas']['credito_preaprobado'] = bool(cred_aprobado)
                st.session_state.api_response = api_post_perfilar(st.session_state.lead)
                st.toast('¡Análisis completado! 🎉', icon='✨')
                st.session_state.nivel = 4
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # FINAL
    elif st.session_state.nivel == 4:
        st.markdown("<div class='stage-container'><div class='house-graphic'>🏆</div>", unsafe_allow_html=True)
        st.markdown("<div class='narrative-box' style='border-left-color:#10b981;'><div class='narrative-title' style='color:#065f46;'>¡Misión Cumplida, Héroe!</div>Tu perfil ha sido analizado. Aquí están las recompensas y el camino a seguir.</div>", unsafe_allow_html=True)
        
        res = st.session_state.api_response
        for proj in res.get("matching_projects", []):
            st.success(f"**🏠 {proj['proyecto']}** - Afinidad: {proj['match_score']}%")
            
        st.link_button("📥 Reclamar Recompensa (Descargar Formularios)", "https://www.colsubsidio.com/hubfs/documentos/colsubsidio/formulario-postulacion-subsidio-vivienda-colsubsidio-radicacion-digital.pdf", use_container_width=True)
        
        if st.button("🔄 Jugar de Nuevo", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

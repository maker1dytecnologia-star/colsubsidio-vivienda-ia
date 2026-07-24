import streamlit as st
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Mi Camino VIS", layout="wide", initial_sidebar_state="collapsed")

# --- CSS EXTREMADAMENTE VISUAL (Roadmap y Construcción) ---
st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; }
    
    /* Título principal */
    .game-header { background: #002D72; padding: 20px; color: white; text-align: center; border-radius: 0 0 20px 20px; margin-top: -60px; margin-bottom: 20px; }
    .game-header h1 { color: #FFCD00 !important; font-weight: 900; }

    /* Mapa del Camino (Visual Roadmap) */
    .roadmap-container { display: flex; justify-content: space-between; align-items: center; position: relative; margin: 30px 0 50px 0; padding: 0 20px; }
    .roadmap-step { display: flex; flex-direction: column; align-items: center; position: relative; z-index: 2; width: 20%; }
    .roadmap-icon { font-size: 2.5rem; background: white; border: 5px solid #E2E8F0; border-radius: 50%; width: 70px; height: 70px; display: flex; justify-content: center; align-items: center; z-index: 2; transition: all 0.3s; }
    .step-active .roadmap-icon { border-color: #FFCD00; background: #FEF3C7; transform: scale(1.15); box-shadow: 0 0 15px rgba(255, 205, 0, 0.5); }
    .step-done .roadmap-icon { border-color: #10B981; background: #D1FAE5; }
    .step-label { font-weight: bold; margin-top: 10px; color: #64748B; font-size: 0.9rem; text-align: center; }
    .step-active .step-label { color: #002D72; font-size: 1rem; }
    
    /* Línea conectora del mapa */
    .roadmap-line { position: absolute; top: 35px; left: 10%; right: 10%; height: 5px; background: #E2E8F0; z-index: 1; }
    
    /* Escenario Central (Donde se construye la casa) */
    .stage-container { background: white; border-radius: 20px; padding: 40px 20px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.05); margin-bottom: 30px; border: 2px solid #F1F5F9; }
    .house-graphic { font-size: 100px; line-height: 1; margin-bottom: 20px; text-shadow: 0 10px 20px rgba(0,0,0,0.1); animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
    
    /* Narrativa de Mentoría */
    .narrative-box { background: #EEF2FF; border-left: 6px solid #4F46E5; padding: 20px 30px; border-radius: 10px; text-align: left; margin: 0 auto 30px auto; max-width: 800px; font-size: 1.15rem; color: #1E293B; line-height: 1.6; }
    .narrative-title { font-weight: 900; color: #4F46E5; margin-bottom: 10px; font-size: 1.3rem; }
    
    /* Ocultar UI aburrida */
    .stSlider > label, .stNumberInput > label, .stRadio > label, .stSelectbox > label { display: none; }
    div.row-widget.stRadio > div { flex-direction: row; flex-wrap: wrap; gap: 10px; justify-content: center; }
    div.row-widget.stRadio > div > label { background: #F1F5F9; padding: 15px 25px; border-radius: 12px; border: 2px solid transparent; cursor: pointer; }
    
    /* Animación */
    @keyframes popIn { 0% { transform: scale(0.5); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE JSON BLINDADO (Evita KeyError) ---
def get_empty_lead():
    return {
        "datos_personales": {"numero_documento": "", "nombres": "", "edad": 30},
        "afiliacion_colsubsidio": {"es_afiliado": False, "personas_a_cargo_registradas": 0},
        "datos_financieros_declarados": {"ingresos_mensuales_hogar": 0, "cesantias_inmovilizadas": 0, "ahorro_programado": 0, "tiene_credito": False},
        "preferencias_e_intencion": {"zona_interes": "Soacha", "plazo_compra": "Corto plazo"},
        "informacion_socioeconomica_externa": {"grupo_sisben": "N/A", "tiene_propiedades_snr": 0, "tiene_subsidios_previos": False},
        "condiciones_especiales_ley": {"cabeza_de_hogar": False, "discapacidad": False, "mayor_65": False}
    }

if 'nivel' not in st.session_state: st.session_state.nivel = 0
if 'lead' not in st.session_state: st.session_state.lead = get_empty_lead()

# --- MOCK API ---
def api_get_afiliado(cedula):
    db = {"1018300400": {"nombres": "Diana Carolina", "ingresos": 2800000, "personas_cargo": 2}}
    time.sleep(0.5)
    return db.get(cedula, None)

# --- CABECERA ---
st.markdown("<div class='game-header'><h1>🏠 El Camino hacia tu Casa Propia</h1></div>", unsafe_allow_html=True)

# --- RENDERIZADO DEL MAPA (ROADMAP VISUAL) ---
etapas = [("🔐", "Identidad"), ("📐", "Planos"), ("🧱", "Cimientos"), ("🏗️", "Estructura"), ("🏠", "La Llave")]
mapa_html = '<div class="roadmap-container"><div class="roadmap-line"></div>'
for i, (icono, nombre) in enumerate(etapas):
    clase = "step-active" if i == st.session_state.nivel else ("step-done" if i < st.session_state.nivel else "")
    mapa_html += f'<div class="roadmap-step {clase}"><div class="roadmap-icon">{icono}</div><div class="step-label">{nombre}</div></div>'
mapa_html += '</div>'
st.markdown(mapa_html, unsafe_allow_html=True)

# --- ÁREA CENTRAL DE JUEGO ---
with st.container():
    # ---------------------------------------------------------
    # NIVEL 0: EL TERRENO (Identificación)
    # ---------------------------------------------------------
    if st.session_state.nivel == 0:
        st.markdown("<div class='stage-container'><div class='house-graphic'>🏕️</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='narrative-box'>
            <div class='narrative-title'>Paso 1: Explorando el Terreno</div>
            ¡Hola! Todo gran proyecto comienza eligiendo el terreno adecuado. Para saber si tienes acceso a materiales exclusivos o subsidios automáticos de nuestra Caja de Compensación, solo necesito que me compartas tu documento de identidad. ¡Sin papeleos largos!
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            cedula = st.text_input("Documento", placeholder="Escribe aquí tu número de cédula...")
            if st.button("🔍 Iniciar Exploración", type="primary", use_container_width=True):
                if cedula:
                    st.session_state.lead = get_empty_lead() # Reiniciamos limpio
                    st.session_state.lead['datos_personales']['numero_documento'] = cedula
                    datos = api_get_afiliado(cedula)
                    if datos:
                        st.session_state.lead['afiliacion_colsubsidio']['es_afiliado'] = True
                        st.session_state.lead['datos_personales']['nombres'] = datos['nombres']
                        st.session_state.lead['datos_financieros_declarados']['ingresos_mensuales_hogar'] = datos['ingresos']
                        st.session_state.lead['afiliacion_colsubsidio']['personas_a_cargo_registradas'] = datos['personas_cargo']
                    st.session_state.nivel = 1
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # NIVEL 1: LOS PLANOS (Nombre, Edad, Zona)
    # ---------------------------------------------------------
    elif st.session_state.nivel == 1:
        st.markdown("<div class='stage-container'><div class='house-graphic'>📐</div>", unsafe_allow_html=True)
        
        afiliado = st.session_state.lead['afiliacion_colsubsidio']['es_afiliado']
        nombre_mostrar = st.session_state.lead['datos_personales']['nombres']
        
        mensaje = f"¡Qué alegría verte, {nombre_mostrar}! El sistema me chismeó que eres afiliado y ya guardé tus ingresos, así que nos saltamos esa parte aburrida." if afiliado else "¡Gusto en conocerte! Como eres nuevo por aquí, necesito hacerte un par de preguntas básicas para arrancar."
        
        st.markdown(f"""
        <div class='narrative-box'>
            <div class='narrative-title'>Paso 2: Dibujando los Planos</div>
            {mensaje} Ahora vamos a dibujar los planos de tu vida. Necesito saber <b>dónde</b> quieres vivir y <b>tu edad</b>. ¿Por qué la edad? Porque existen subsidios especiales y bonos extra para el segmento "Joven". ¡Queremos aprovechar todo lo que la ley nos dé!
        </div>
        """, unsafe_allow_html=True)
        
        if not afiliado:
            st.session_state.lead['datos_personales']['nombres'] = st.text_input("¿Cómo te llamas?", placeholder="Tu nombre...")
            
            # --- SOLUCIÓN: Agregamos el texto explicativo para el input oculto ---
            st.markdown("<br>**¿Cuáles son tus ingresos mensuales aproximados? (COP)**", unsafe_allow_html=True)
            st.session_state.lead['datos_financieros_declarados']['ingresos_mensuales_hogar'] = st.number_input("Ingresos", step=100000)
            
        st.markdown("<br>**1. Desliza para indicar tu edad actual:**", unsafe_allow_html=True)
        edad = st.slider("Edad", 18, 80, 30)
        
        st.markdown("**2. ¿En qué zona de Cundinamarca imaginas tu hogar?**")
        zona = st.radio("Zona", ["Soacha", "Bogotá", "Tocancipá", "Girardot"])
        
        if st.button("✅ Aprobar Planos", type="primary"):
            st.session_state.lead['datos_personales']['edad'] = edad
            st.session_state.lead['preferencias_e_intencion']['zona_interes'] = zona
            st.session_state.nivel = 2
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # NIVEL 2: LOS CIMIENTOS (Ahorros)
    # ---------------------------------------------------------
    elif st.session_state.nivel == 2:
        st.markdown("<div class='stage-container'><div class='house-graphic'>🧱</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='narrative-box'>
            <div class='narrative-title'>Paso 3: Vertiendo los Cimientos</div>
            Para que una casa no se caiga, necesita cimientos financieros sólidos. En el mundo real, estos cimientos son <b>tus ahorros y cesantías</b>. Sumaremos todo tu esfuerzo acumulado para calcular si alcanzas a cubrir la cuota inicial del proyecto que dibujamos en los planos.
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**¿Cuántas Cesantías inmovilizadas tienes? (COP)**")
            cesantias = st.number_input("Cesantías", min_value=0, step=500000, value=2000000)
        with c2:
            st.markdown("**¿Cuánto tienes en ahorros propios? (COP)**")
            ahorros = st.number_input("Ahorros", min_value=0, step=500000, value=3000000)
            
        if st.button("💪 Cimientos Listos", type="primary"):
            st.session_state.lead['datos_financieros_declarados']['cesantias_inmovilizadas'] = cesantias
            st.session_state.lead['datos_financieros_declarados']['ahorro_programado'] = ahorros
            st.session_state.nivel = 3
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # NIVEL 3: LA ESTRUCTURA (Familia y Ley)
    # ---------------------------------------------------------
    elif st.session_state.nivel == 3:
        st.markdown("<div class='stage-container'><div class='house-graphic'>🏗️</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='narrative-box'>
            <div class='narrative-title'>Paso 4: Levantando la Estructura</div>
            Las paredes y la estructura existen para proteger a los que más quieres. Aquí evaluamos a tu núcleo familiar. Además, ¡tenemos que esquivar un par de rocas gigantes! 🪨 La Ley de Vivienda nos exige validar que nadie en tu hogar tenga propiedades ni subsidios previos para poder darte luz verde.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**🌟 Beneficios de Familia (Actívalos si aplican para ganar Score Legal):**")
        c1, c2, c3 = st.columns(3)
        cabeza = c1.toggle("👑 Madre/Padre Cabeza de Hogar")
        discapacidad = c2.toggle("♿ Miembro con Discapacidad")
        mayor = c3.toggle("👴 Miembro Mayor de 65 años")
        
        st.markdown("<br>**📜 Clasificación Sisbén (Clave para subsidios del Gobierno):**", unsafe_allow_html=True)
        sisben = st.radio("Sisbén", ["No tengo", "A1-A5", "B1-B7", "C1-C18", "D1-D21"])
        
        st.markdown("<br>**🪨 Obstáculos Legales (Responde con honestidad):**", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        sub_previo = col1.toggle("🚫 Ya recibimos un subsidio de vivienda antes")
        propiedades = col2.toggle("🚫 Alguien en casa ya tiene una propiedad a su nombre")
        
        if st.button("🔨 Ensamblar Estructura", type="primary"):
            # Asignaciones seguras al diccionario pre-inicializado
            st.session_state.lead['condiciones_especiales_ley']['cabeza_de_hogar'] = cabeza
            st.session_state.lead['condiciones_especiales_ley']['discapacidad'] = discapacidad
            st.session_state.lead['condiciones_especiales_ley']['mayor_65'] = mayor
            st.session_state.lead['informacion_socioeconomica_externa']['grupo_sisben'] = sisben.split("-")[0] if "-" in sisben else sisben
            st.session_state.lead['informacion_socioeconomica_externa']['tiene_subsidios_previos'] = sub_previo
            st.session_state.lead['informacion_socioeconomica_externa']['tiene_propiedades_snr'] = 1 if propiedades else 0
            
            st.session_state.nivel = 4
            st.balloons()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # NIVEL 4: LA CASA TERMINADA (Consola Final)
    # ---------------------------------------------------------
    elif st.session_state.nivel == 4:
        st.markdown("<div class='stage-container'><div class='house-graphic'>🏠</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='narrative-box' style='border-left-color: #10B981; color: #065F46; background: #D1FAE5;'>
            <div class='narrative-title' style='color: #065F46;'>¡Misión Cumplida! Te entregamos las Llaves</div>
            Hemos recolectado con éxito toda la información. Ahora, el cerebro de Inteligencia Artificial tomará estos planos, cimientos y estructura (JSON) y los cruzará con los compradores históricos para entregarte el Score y el Proyecto perfecto.
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📦 Inspeccionar Datos Recolectados (Payload API JSON)", expanded=False):
            st.json(st.session_state.lead)
            
        if st.button("🔄 Volver a Empezar el Camino"):
            st.session_state.clear()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

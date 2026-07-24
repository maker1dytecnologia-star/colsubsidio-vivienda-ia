import streamlit as st
import json
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Colsubsidio - Mi Camino VIS", layout="wide", initial_sidebar_state="collapsed")

# --- CSS PERSONALIZADO (UI/UX Gamificada) ---
st.markdown("""
<style>
    /* Colores corporativos Colsubsidio: Azul #002D72, Amarillo #FFCD00 */
    .hero-header { background: linear-gradient(135deg, #002D72 0%, #001A42 100%); padding: 30px; color: white; text-align: center; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    .hero-header h1 { color: #FFCD00 !important; font-size: 2.5rem; margin-bottom: 5px; }
    
    /* Tarjetas de Estación */
    .station-card { background-color: #ffffff; border-top: 6px solid #FFCD00; padding: 25px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); transition: transform 0.2s; }
    .station-card:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(0,0,0,0.1); }
    
    /* Burbujas de diálogo del Asesor */
    .bot-bubble { background-color: #E8F0FE; border-left: 5px solid #1A73E8; padding: 15px 20px; border-radius: 0 15px 15px 15px; margin-bottom: 20px; color: #1F2937; font-size: 1.05rem; }
    
    /* Panel lateral de Inventario/Consola */
    .inventory-panel { background-color: #F8F9FA; padding: 20px; border-radius: 12px; border: 1px solid #E5E7EB; }
    .inventory-item { display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #E5E7EB; }
    .status-badge-ok { background-color: #D1FAE5; color: #065F46; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 0.8rem; }
    .status-badge-wait { background-color: #FEE2E2; color: #991B1B; padding: 4px 10px; border-radius: 20px; font-weight: bold; font-size: 0.8rem; }
    
    /* Ocultar etiquetas por defecto de Streamlit para un look más limpio */
    .stTextInput > div > div > input { border-radius: 8px; }
    .stSelectbox > div > div > div { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# --- SIMULACIÓN DE ENDPOINTS (MOCKS) ---
def api_get_afiliado(cedula):
    db_colsubsidio = {
        "1018300400": {
            "datos_personales": {"tipo_documento": "CC", "numero_documento": "1018300400", "nombres": "Diana Carolina", "apellidos": "Rangel"},
            "afiliacion_colsubsidio": {"es_afiliado": True, "tipo_afiliado": "Dependiente", "antiguedad_meses": 24, "categoria": "A"},
            "datos_financieros_declarados": {"ingresos_verificados_pila": 2800000.0, "ingresos_mensuales_hogar": 2800000.0, "cesantias_inmovilizadas": 0.0, "ahorro_programado": 0.0},
            "preferencias_e_intencion": {"zona_interes": ""},
            "condiciones_especiales_ley": {"cabeza_de_hogar": False}
        }
    }
    time.sleep(0.5) 
    return db_colsubsidio.get(cedula, None)

# --- INICIALIZACIÓN DE ESTADOS ---
if 'estacion_actual' not in st.session_state:
    st.session_state.estacion_actual = 0
if 'lead' not in st.session_state:
    st.session_state.lead = {}

# --- CABECERA VISUAL ---
st.markdown("""
<div class="hero-header">
    <h1>🏠 Mi Camino VIS</h1>
    <p>Construyamos juntos el sueño de tu casa propia, paso a paso.</p>
</div>
""", unsafe_allow_html=True)

# --- VISUAL STEPPER (Barra de progreso gráfica) ---
def render_stepper(current_step):
    steps = [
        ("🔐", "Ingreso"), ("💭", "Planos"), 
        ("🪙", "Cimientos"), ("⚡", "Estructura"), ("🏠", "La Llave")
    ]
    cols = st.columns(5)
    for i, (icon, name) in enumerate(steps):
        with cols[i]:
            if i < current_step:
                st.success(f"{icon} {name}")
            elif i == current_step:
                st.info(f"{icon} **{name}**")
            else:
                st.markdown(f"<div style='opacity: 0.4; text-align: center; padding: 10px;'>{icon} {name}</div>", unsafe_allow_html=True)

render_stepper(st.session_state.estacion_actual)
st.write("") # Espaciador

# --- LAYOUT PRINCIPAL ---
col_juego, espaciador, col_consola = st.columns([5.5, 0.5, 4])

with col_juego:
    # ==========================================
    # ESTACIÓN 0: IDENTIFICACIÓN
    # ==========================================
    if st.session_state.estacion_actual == 0:
        st.markdown('<div class="station-card">', unsafe_allow_html=True)
        st.markdown("<div class='bot-bubble'>¡Hola! Soy tu guía en este viaje. Para empezar a construir, necesito verificar tu identidad. Si eres afiliado, ¡tendrás ventajas!</div>", unsafe_allow_html=True)
        
        cedula_input = st.text_input("Ingresa tu documento (Ej: 1018300400):", placeholder="Tu número de cédula...")
        
        if st.button("🚪 Abrir la puerta", type="primary", use_container_width=True):
            with st.spinner("Buscando en los registros mágicos..."):
                datos = api_get_afiliado(cedula_input)
                if datos:
                    st.session_state.lead = datos
                    st.toast('¡Afiliado detectado!', icon='🎉')
                else:
                    st.session_state.lead = {"datos_personales": {"numero_documento": cedula_input, "nombres": ""}, "afiliacion_colsubsidio": {"es_afiliado": False}, "datos_financieros_declarados": {"ingresos_mensuales_hogar": 0.0, "cesantias_inmovilizadas": 0.0, "ahorro_programado": 0.0}, "preferencias_e_intencion": {"zona_interes": ""}, "condiciones_especiales_ley": {"cabeza_de_hogar": False}}
            st.session_state.estacion_actual = 1
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # ESTACIÓN 1: EL SUEÑO (Planos)
    # ==========================================
    if st.session_state.estacion_actual == 1:
        st.markdown('<div class="station-card">', unsafe_allow_html=True)
        
        if st.session_state.lead['afiliacion_colsubsidio']['es_afiliado']:
            nombre = st.session_state.lead['datos_personales']['nombres']
            st.markdown(f"<div class='bot-bubble'>¡Bienvenido de vuelta, {nombre}! 🌟<br>Ya tengo tus datos de ingresos registrados. Ahora cuéntame, ¿dónde te gustaría que construyamos?</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='bot-bubble'>¡Encantado de conocerte! Como eres nuevo por aquí, necesito conocerte un poco mejor para dibujar los planos correctos.</div>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            st.session_state.lead['datos_personales']['nombres'] = c1.text_input("✍️ Tu nombre:")
            st.session_state.lead['datos_financieros_declarados']['ingresos_mensuales_hogar'] = c2.number_input("💵 Tus ingresos mensuales:", min_value=0.0, step=100000.0)
            
        zona = st.radio("📍 Elige la zona de tu futuro hogar:", ["Soacha", "Bogotá", "Tocancipá"], horizontal=True)
        
        if st.button("✅ Fijar Planos y Avanzar", type="primary", use_container_width=True):
            if not st.session_state.lead['datos_personales']['nombres']:
                st.warning("No olvides decirme tu nombre.")
            else:
                st.session_state.lead['preferencias_e_intencion']['zona_interes'] = zona
                st.session_state.estacion_actual = 2
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # ESTACIÓN 2: EL COFRE (Cimientos)
    # ==========================================
    if st.session_state.estacion_actual == 2:
        st.markdown('<div class="station-card">', unsafe_allow_html=True)
        st.markdown("<div class='bot-bubble'>Los cimientos de una casa son tus ahorros. 🪙<br>No te preocupes si no es mucho, todo suma. ¿Qué recursos tienes guardados en tu cofre?</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        cesantias = c1.number_input("💼 Cesantías (COP):", min_value=0.0, step=500000.0)
        ahorro = c2.number_input("🏦 Ahorros Extra (COP):", min_value=0.0, step=500000.0)
        
        if st.button("🏗️ Verter los Cimientos", type="primary", use_container_width=True):
            st.session_state.lead['datos_financieros_declarados']['cesantias_inmovilizadas'] = cesantias
            st.session_state.lead['datos_financieros_declarados']['ahorro_programado'] = ahorro
            st.session_state.estacion_actual = 3
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # ESTACIÓN 3: TUS PODERES
    # ==========================================
    if st.session_state.estacion_actual == 3:
        st.markdown('<div class="station-card">', unsafe_allow_html=True)
        st.markdown("<div class='bot-bubble'>¡Casi terminamos! ⚡ Para fortalecer la estructura, veamos si posees alguna condición especial que nos otorgue ventajas o subsidios adicionales.</div>", unsafe_allow_html=True)
        
        cabeza_hogar = st.toggle("🛡️ Soy Cabeza de Familia")
        sisben = st.selectbox("📋 ¿Tienes Sisbén?", ["No aplica", "A1-A5", "B1-B7", "C1-C18"])
        
        if st.button("🏠 Terminar mi Casa", type="primary", use_container_width=True):
            st.session_state.lead['condiciones_especiales_ley']['cabeza_de_hogar'] = cabeza_hogar
            st.session_state.estacion_actual = 4
            st.balloons()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # ESTACIÓN 4: COMPLETADO
    # ==========================================
    if st.session_state.estacion_actual == 4:
        st.markdown('<div class="station-card" style="text-align:center;">', unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/7514/7514032.png", width=150) # Icono de casa 3D
        st.markdown("### ¡Felicidades! Has completado tu Camino VIS 🎉")
        st.markdown("He enviado tus planos y tu cofre a la central. Revisa el panel de la derecha para ver qué proyecto te recomendamos.")
        if st.button("🔄 Jugar de Nuevo", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

with col_consola:
    # --- PANEL LATERAL DE INVENTARIO Y ESTADO ---
    st.markdown('<div class="inventory-panel">', unsafe_allow_html=True)
    st.markdown("### 🎒 Tu Inventario")
    
    # Lógica visual para saber si completó pasos
    identidad_ok = st.session_state.estacion_actual > 0
    planos_ok = st.session_state.estacion_actual > 1
    cofre_ok = st.session_state.estacion_actual > 2
    
    st.markdown(f"""
    <div class="inventory-item">
        <span>👤 <b>Identidad:</b></span>
        <span class="{'status-badge-ok' if identidad_ok else 'status-badge-wait'}">{'Verificada' if identidad_ok else 'Pendiente'}</span>
    </div>
    <div class="inventory-item">
        <span>📍 <b>Ubicación:</b></span>
        <span class="{'status-badge-ok' if planos_ok else 'status-badge-wait'}">{st.session_state.lead['preferencias_e_intencion']['zona_interes'] if planos_ok else 'Pendiente'}</span>
    </div>
    <div class="inventory-item">
        <span>🪙 <b>Ahorros Total:</b></span>
        <span class="{'status-badge-ok' if cofre_ok else 'status-badge-wait'}">
            ${(st.session_state.lead['datos_financieros_declarados'].get('cesantias_inmovilizadas', 0) + st.session_state.lead['datos_financieros_declarados'].get('ahorro_programado', 0)):,.0f}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Consola de Backend (Solo aparece al final)
    if st.session_state.estacion_actual == 4:
        st.markdown("### 💻 Consola Backend (JSON)")
        st.success("JSON listo para envío POST")
        with st.expander("Ver JSON Generado", expanded=False):
            st.json(st.session_state.lead)
            
    st.markdown('</div>', unsafe_allow_html=True)

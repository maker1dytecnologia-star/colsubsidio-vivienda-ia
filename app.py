import streamlit as st
import pandas as pd
import json

# --- CONFIGURACIÓN DE PÁGINA Y ESTILOS VISUALES ---
st.set_page_config(page_title="Colsubsidio - Mi Camino VIS", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .gamification-header { background-color: #002D72; padding: 20px; color: white; text-align: center; border-radius: 10px; margin-bottom: 20px; }
    .station-card { background-color: #F8F9FA; border-left: 5px solid #FFCD00; padding: 20px; border-radius: 5px; margin-bottom: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    .locked-station { opacity: 0.5; pointer-events: none; }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE ESTADOS DEL JUEGO ---
if 'estacion_actual' not in st.session_state:
    st.session_state.estacion_actual = 0
if 'datos_juego' not in st.session_state:
    st.session_state.datos_juego = {}
if 'progreso_casa' not in st.session_state:
    st.session_state.progreso_casa = "Terreno Vacío 🏕️"

# --- SIMULACIÓN DE API (GATEKEEPER) ---
MOCK_API_RESPONSE = {
    "1018300400": {
        "nombre": "Diana Martínez", "afiliado": True, "categoria": "B", "ingresos_mensuales": 2900000, 
        "personas_a_cargo": 2, "tipo_empresa": "Medianas", "tipo_cotizante": "dependiente"
    }
}

st.markdown('<div class="gamification-header"><h1>🏠 Construye tu Sueño: Mi Camino VIS</h1></div>', unsafe_allow_html=True)

# Barra de progreso visual (La casa se va construyendo)
progreso_porcentaje = (st.session_state.estacion_actual / 5) * 100
st.progress(int(progreso_porcentaje))
st.markdown(f"**Estado de tu obra:** {st.session_state.progreso_casa}")
st.divider()

col_juego, col_consola = st.columns([6, 4])

with col_juego:
    # ==========================================
    # ESTACIÓN 0: IDENTIFICACIÓN (GATEKEEPER)
    # ==========================================
    if st.session_state.estacion_actual == 0:
        st.markdown("### 🔐 Estación 0: La Puerta de Entrada")
        cedula_input = st.text_input("Ingresa tu número de cédula para abrir la puerta:")
        if st.button("Comenzar Aventura"):
            if cedula_input in MOCK_API_RESPONSE:
                st.session_state.lead = MOCK_API_RESPONSE[cedula_input]
                st.session_state.lead['id_usuario'] = cedula_input
                st.success(f"¡Bienvenida de nuevo, {st.session_state.lead['nombre']}! Ya tenemos tus bases listas.")
            else:
                st.session_state.lead = {"id_usuario": cedula_input, "nombre": "", "afiliado": False, "ingresos_mensuales": 0}
                st.info("¡Nuevo constructor! Deberemos tomar algunas medidas extra.")
            
            st.session_state.estacion_actual = 1
            st.session_state.progreso_casa = "Planos Aprobados 📐"
            st.rerun()

    # ==========================================
    # ESTACIÓN 1: EL SUEÑO
    # ==========================================
    if st.session_state.estacion_actual >= 1:
        with st.container():
            st.markdown('<div class="station-card">', unsafe_allow_html=True)
            st.markdown("### 💭 Estación 1: El Sueño")
            
            if not st.session_state.lead.get('afiliado'):
                st.session_state.lead['nombre'] = st.text_input("¿Cuál es tu nombre?")
                st.session_state.lead['ingresos_mensuales'] = st.number_input("Tus ingresos mensuales (COP):", min_value=0, step=100000)
            else:
                st.write(f"Conocemos tus ingresos (${st.session_state.lead['ingresos_mensuales']:,}) y tu empresa. ¡Saltamos el papeleo!")

            zona = st.selectbox("¿En qué zona de Cundinamarca imaginas tu hogar?", ["Soacha", "Tocancipá", "Girardot", "Bogotá"])
            
            if st.session_state.estacion_actual == 1 and st.button("Fijar Cimientos 🧱"):
                st.session_state.datos_juego['zona_preferida'] = zona
                st.session_state.estacion_actual = 2
                st.session_state.progreso_casa = "Cimientos Listos 🧱"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # ESTACIÓN 2: EL COFRE
    # ==========================================
    if st.session_state.estacion_actual >= 2:
        with st.container():
            st.markdown('<div class="station-card">', unsafe_allow_html=True)
            st.markdown("### 🪙 Estación 2: Mi Cofre")
            cesantias = st.number_input("¿Cuántas monedas tienes en Cesantías? (COP)", min_value=0, value=3000000, step=500000)
            ahorros = st.number_input("Ahorros voluntarios (COP):", min_value=0, value=5000000, step=500000)
            
            if st.session_state.estacion_actual == 2 and st.button("Levantar Estructura 🏗️"):
                st.session_state.datos_juego['cesantias'] = cesantias
                st.session_state.datos_juego['ahorros'] = ahorros
                st.session_state.estacion_actual = 3
                st.session_state.progreso_casa = "Estructura y Paredes 🏗️"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # ESTACIÓN 3: TUS PODERES
    # ==========================================
    if st.session_state.estacion_actual >= 3:
        with st.container():
            st.markdown('<div class="station-card">', unsafe_allow_html=True)
            st.markdown("### ⚡ Estación 3: Tus Súper Poderes")
            grupo_sisben = st.selectbox("Grupo Sisbén (Para invocar a Mi Casa Ya):", ["No aplica", "A1-A5", "B1-B7", "C1-C18", "D1-D21"], index=3)
            
            if st.session_state.estacion_actual == 3 and st.button("Poner el Techo 🛖"):
                st.session_state.datos_juego['grupo_sisben'] = grupo_sisben
                st.session_state.estacion_actual = 4
                st.session_state.progreso_casa = "Techo Terminado 🛖"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # ESTACIÓN 4: MI RESPALDO (REGLA ENDEUDAMIENTO)
    # ==========================================
    if st.session_state.estacion_actual >= 4:
        with st.container():
            st.markdown('<div class="station-card">', unsafe_allow_html=True)
            st.markdown("### 🛡️ Estación 4: Mi Respaldo Financiero")
            st.info("Para cuidar tus finanzas (Ley de Vivienda), debemos conocer tus batallas actuales.")
            
            credito = st.checkbox("¿Tienes crédito hipotecario preaprobado?")
            otras_deudas = st.number_input("Suma lo que pagas al mes en otras deudas (Tarjetas, libre inversión, etc):", min_value=0, value=200000, step=50000)
            
            if st.session_state.estacion_actual == 4 and st.button("Forjar La Llave 🔑"):
                st.session_state.datos_juego['credito_preaprobado'] = credito
                st.session_state.datos_juego['otras_deudas'] = otras_deudas
                st.session_state.estacion_actual = 5
                st.session_state.progreso_casa = "Casa Completada 🏠✨"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

with col_consola:
    # ==========================================
    # ESTACIÓN 5: LA LLAVE (RESOLUCIÓN Y JSON)
    # ==========================================
    if st.session_state.estacion_actual == 5:
        st.markdown("### 💻 Consola del Asesor (Backend)")
        
        ingresos = st.session_state.lead['ingresos_mensuales']
        deudas = st.session_state.datos_juego['otras_deudas']
        
        # CÁLCULO DE CAPACIDAD DE ENDEUDAMIENTO GLOBAL (30% para VIS)
        tope_maximo_ley = ingresos * 0.30
        capacidad_disponible_cuota = tope_maximo_ley - deudas
        
        st.write(f"**Ingresos Mensuales:** ${ingresos:,.0f}")
        st.write(f"**Tope Legal (30% VIS):** ${tope_maximo_ley:,.0f}")
        st.write(f"**Menos deudas actuales:** -${deudas:,.0f}")
        
        if capacidad_disponible_cuota > 0:
            st.success(f"**Capacidad para cuota mensual:** ${capacidad_disponible_cuota:,.0f} COP")
            estado_juego = "WIN"
            mensaje_mentoria = "¡Cumples los requisitos! Recomendamos el proyecto Ciudadela Maiporé."
        else:
            st.error("⚠️ Capacidad de endeudamiento saturada.")
            estado_juego = "MENTORIA"
            mensaje_mentoria = "Tus deudas actuales consumen tu capacidad. Te enrutamos a nuestro programa 'PerteneSER' para hacer un plan de saneamiento financiero de 6 meses o al Subsidio de Arrendamiento."
        
        st.info(f"💡 **Mentoría Activa:** {mensaje_mentoria}")
        
        # Construcción del Payload JSON final
        payload_backend = {
            "id_usuario": st.session_state.lead.get('id_usuario'),
            "afiliado": st.session_state.lead.get('afiliado'),
            "ingresos_mensuales": ingresos,
            "finanzas": {
                "cesantias": st.session_state.datos_juego['cesantias'],
                "ahorros": st.session_state.datos_juego['ahorros'],
                "credito_preaprobado": st.session_state.datos_juego['credito_preaprobado'],
                "pago_deudas_actuales": deudas,
                "capacidad_cuota_vis": capacidad_disponible_cuota
            },
            "zona_preferida": st.session_state.datos_juego['zona_preferida'],
            "origen": "juego_interactivo"
        }
        
        with st.expander("Ver JSON generado para el Motor de Reglas"):
            st.json(payload_backend)
            
        if st.button("Jugar de Nuevo"):
            for key in ['estacion_actual', 'datos_juego', 'progreso_casa', 'lead']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

import streamlit as st
import time

# --- CONFIGURACIÓN Y ESTILOS ---
st.set_page_config(page_title="Mi Camino VIS", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    /* Fondo principal sutil para no verse tan "blanco" */
    .stApp { background-color: #F3F4F6; }
    
    /* Cabecera inmersiva */
    .hero-header { background: linear-gradient(135deg, #002D72 0%, #0055A5 100%); padding: 35px; color: white; text-align: center; border-radius: 0 0 30px 30px; margin-top: -60px; margin-bottom: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
    .hero-header h1 { color: #FFCD00 !important; font-weight: 800; font-size: 2.8rem; }
    
    /* Tarjetas de Nivel (Misiones) */
    .level-card { background-color: #FFFFFF; border-left: 6px solid #FFCD00; padding: 30px; border-radius: 15px; margin-bottom: 25px; box-shadow: 0 6px 12px rgba(0,0,0,0.06); }
    
    /* Chatbots y Narrativa */
    .avatar-bot { font-size: 2rem; margin-right: 15px; }
    .bot-bubble { background-color: #E8F0FE; border: 1px solid #D2E3FC; padding: 18px 25px; border-radius: 20px 20px 20px 0px; color: #1F2937; font-size: 1.1rem; display: flex; align-items: center; margin-bottom: 25px; box-shadow: 2px 2px 8px rgba(26,115,232,0.1); }
    
    /* Panel Lateral (Inventario) */
    .inventory-panel { background-color: #FFFFFF; padding: 25px; border-radius: 15px; border: 2px dashed #002D72; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
    
    /* Ocultar labels aburridos de Streamlit para un look app */
    .stSlider > label { display: none; }
    .stRadio > label { display: none; }
    .stNumberInput > label { display: none; }
    
    /* Botones de selección rápida (Radio buttons simulando pills) */
    div.row-widget.stRadio > div { flex-direction: row; align-items: stretch; }
    div.row-widget.stRadio > div > label { background-color: #F3F4F6; padding: 10px 20px; border-radius: 10px; margin-right: 10px; border: 1px solid #E5E7EB; }
</style>
""", unsafe_allow_html=True)

# --- SIMULACIÓN DE API ---
def api_get_afiliado(cedula):
    # Mock básico
    db = {"1018300400": {"nombres": "Diana", "es_afiliado": True, "ingresos": 2800000, "personas_cargo": 2}}
    time.sleep(0.5)
    return db.get(cedula, None)

# --- ESTADO DEL JUEGO ---
if 'nivel' not in st.session_state: st.session_state.nivel = 0
if 'lead' not in st.session_state: 
    # Plantilla JSON Completa Acordada
    st.session_state.lead = {
        "datos_personales": {"numero_documento": "", "nombres": "", "edad": 30},
        "afiliacion_colsubsidio": {"es_afiliado": False, "personas_a_cargo_registradas": 0},
        "datos_financieros_declarados": {"ingresos_mensuales_hogar": 0, "cesantias_inmovilizadas": 0, "ahorro_programado": 0, "tiene_credito": False},
        "preferencias_e_intencion": {"zona_interes": "Soacha", "plazo_compra": "Corto plazo"},
        "informacion_socioeconomica_externa": {"grupo_sisben": "N/A", "tiene_propiedades_snr": 0, "tiene_subsidios_previos": False},
        "condiciones_especiales_ley": {"cabeza_de_hogar": False, "discapacidad": False, "mayor_65": False}
    }

# --- HEADER VISUAL ---
st.markdown("<div class='hero-header'><h1>🏠 Tu Aventura VIS</h1><p>Conquista tu casa propia superando estas misiones.</p></div>", unsafe_allow_html=True)

# Layout: Izquierda (Juego) 70% | Derecha (Inventario) 30%
col_juego, col_inv = st.columns([7, 3])

with col_juego:
    # ---------------------------------------------------------
    # NIVEL 0: EL PÓRTICO (Identidad)
    # ---------------------------------------------------------
    if st.session_state.nivel == 0:
        st.markdown("<div class='level-card'>", unsafe_allow_html=True)
        st.markdown("<div class='bot-bubble'><span class='avatar-bot'>🦉</span><div>¡Hola viajero! Para dejarte pasar y ver si tienes beneficios de afiliado, escribe el número de tu documento de identidad mágico.</div></div>", unsafe_allow_html=True)
        
        cedula = st.text_input("Ingresa tu cédula:", placeholder="Ej: 1018300400")
        if st.button("🔑 Desbloquear la Puerta", type="primary"):
            datos = api_get_afiliado(cedula)
            st.session_state.lead['datos_personales']['numero_documento'] = cedula
            if datos:
                st.session_state.lead['afiliacion_colsubsidio']['es_afiliado'] = True
                st.session_state.lead['datos_personales']['nombres'] = datos['nombres']
                st.session_state.lead['datos_financieros_declarados']['ingresos_mensuales_hogar'] = datos['ingresos']
                st.session_state.lead['afiliacion_colsubsidio']['personas_a_cargo_registradas'] = datos['personas_cargo']
            st.session_state.nivel = 1
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # NIVEL 1: LOS PLANOS (Edad, Nombre, Zona, Plazo)
    # ---------------------------------------------------------
    elif st.session_state.nivel == 1:
        st.markdown("<div class='level-card'>", unsafe_allow_html=True)
        afiliado = st.session_state.lead['afiliacion_colsubsidio']['es_afiliado']
        saludo = f"¡Qué gusto {st.session_state.lead['datos_personales']['nombres']}!" if afiliado else "¡Bienvenido nuevo constructor!"
        
        st.markdown(f"<div class='bot-bubble'><span class='avatar-bot'>📐</span><div>{saludo} Para buscar el proyecto ideal en nuestro mapa y ver si aplicas al bono 'Joven', necesito un par de datos de tu visión.</div></div>", unsafe_allow_html=True)
        
        if not afiliado:
            st.markdown("**¿Cómo te llamas?**")
            st.session_state.lead['datos_personales']['nombres'] = st.text_input("Tu nombre", placeholder="Escribe aquí tu nombre...")
            
        st.markdown("**¿Cuántos años tienes? (Desliza para responder)**")
        edad = st.slider("Edad", 18, 80, 30)
        
        st.markdown("**¿En qué reino quieres tu casa?**")
        zona = st.radio("Zona", ["Soacha 🏙️", "Bogotá 🌆", "Tocancipá ⛰️", "Girardot ☀️"], horizontal=True)
        
        st.markdown("**¿Qué tan pronto quieres mudarte? (La urgencia de tu misión)**")
        plazo = st.radio("Plazo", ["Corto plazo (Menos de 6 meses) 🏃", "Mediano (6 - 12 meses) 🚶", "Largo plazo (Más de 1 año) 🧘"], horizontal=True)
        
        if st.button("✅ Confirmar Planos", type="primary"):
            st.session_state.lead['datos_personales']['edad'] = edad
            st.session_state.lead['preferencias_e_intencion']['zona_interes'] = zona.split(" ")[0] # Quitamos el emoji para el JSON
            st.session_state.lead['preferencias_e_intencion']['plazo_compra'] = plazo
            st.session_state.nivel = 2
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # NIVEL 2: LA TRIPULACIÓN Y PODERES (Familia y Ley)
    # ---------------------------------------------------------
    elif st.session_state.nivel == 2:
        st.markdown("<div class='level-card'>", unsafe_allow_html=True)
        st.markdown("<div class='bot-bubble'><span class='avatar-bot'>👨‍👩‍👧‍👦</span><div>Toda gran aventura requiere compañía. ¿Quiénes van contigo? Y más importante, veamos si tu grupo familiar tiene poderes especiales ante la ley.</div></div>", unsafe_allow_html=True)
        
        if not st.session_state.lead['afiliacion_colsubsidio']['es_afiliado']:
            st.markdown("**¿Cuántas personas dependen económicamente de ti? (Desliza)**")
            personas = st.slider("Personas a cargo", 0, 10, 0)
        else:
            personas = st.session_state.lead['afiliacion_colsubsidio']['personas_a_cargo_registradas']
            st.success(f"🪄 La Caja me dice que tienes {personas} personas a cargo registradas.")
            
        st.markdown("**🌟 Activa los poderes de tu hogar si los tienes (Suman mucho puntaje):**")
        c1, c2, c3 = st.columns(3)
        cabeza = c1.toggle("👑 Madre/Padre cabeza de hogar")
        discapacidad = c2.toggle("♿ Miembro con discapacidad")
        mayor = c3.toggle("👴 Miembro mayor de 65 años")
        
        st.markdown("**📜 El Pergamino de Mi Casa Ya (Sisbén):**")
        sisben = st.radio("Grupo Sisbén", ["No tengo ❌", "A1-A5 🟢", "B1-B7 🟡", "C1-C18 🟠", "D1-D21 🔴"], horizontal=True)
        
        if st.button("✅ Tripulación Lista", type="primary"):
            st.session_state.lead['afiliacion_colsubsidio']['personas_a_cargo_registradas'] = personas
            st.session_state.lead['condiciones_especiales_ley']['cabeza_de_hogar'] = cabeza
            st.session_state.lead['condiciones_especiales_ley']['discapacidad'] = discapacidad
            st.session_state.lead['condiciones_especiales_ley']['mayor_65'] = mayor
            st.session_state.lead['informacion_socioeconomica_externa']['grupo_sisben'] = sisben.split(" ")[0]
            st.session_state.nivel = 3
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # NIVEL 3: EL COFRE Y EL ESCUDO LEGAL (Finanzas y Exclusiones)
    # ---------------------------------------------------------
    elif st.session_state.nivel == 3:
        st.markdown("<div class='level-card'>", unsafe_allow_html=True)
        st.markdown("<div class='bot-bubble'><span class='avatar-bot'>🪙</span><div>¡Última parada! Vamos a contar el oro de tu cofre y revisar que tu historial legal esté impecable para reclamar los subsidios.</div></div>", unsafe_allow_html=True)
        
        if not st.session_state.lead['afiliacion_colsubsidio']['es_afiliado']:
            st.markdown("**¿Cuáles son los ingresos totales de tu hogar al mes? (Importante para el límite del subsidio)**")
            ingresos = st.number_input("Ingresos", min_value=0, step=100000, value=2000000)
        else:
            ingresos = st.session_state.lead['datos_financieros_declarados']['ingresos_mensuales_hogar']
            
        c1, c2 = st.columns(2)
        st.markdown("**💰 Tu Cofre de Ahorros:**")
        cesantias = c1.number_input("Cesantías guardadas (COP)", step=500000, value=2000000)
        ahorros = c2.number_input("Ahorros propios (COP)", step=500000, value=3000000)
        
        st.markdown("**🛡️ Tu Escudo Legal (Responde con la verdad):**")
        credito = st.toggle("💳 Ya tengo un crédito pre-aprobado (¡Acelera el proceso!)")
        propiedades = st.toggle("🚫 Alguien en mi hogar ya es propietario de una casa (Cuidado: Bloquea el subsidio)")
        sub_previo = st.toggle("🚫 Ya recibimos un subsidio de vivienda antes")
        
        if st.button("🚀 Evaluar mi Perfil (Finalizar)", type="primary"):
            st.session_state.lead['datos_financieros_declarados']['ingresos_mensuales_hogar'] = ingresos
            st.session_state.lead['datos_financieros_declarados']['cesantias_inmovilizadas'] = cesantias
            st.session_state.lead['datos_financieros_declarados']['ahorro_programado'] = ahorros
            st.session_state.lead['datos_financieros_declarados']['tiene_credito'] = credito
            st.session_state.lead['informacion_socioeconomica_externa']['tiene_propiedades_snr'] = 1 if propiedades else 0
            st.session_state.lead['informacion_socioeconomica_externa']['tiene_subsidios_previos'] = sub_previo
            st.session_state.nivel = 4
            st.balloons()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # NIVEL 4: RESULTADO (CONSOLA)
    # ---------------------------------------------------------
    elif st.session_state.nivel == 4:
        st.markdown("<div class='level-card'>", unsafe_allow_html=True)
        st.success("🎯 **¡Misión Completada! El motor de inteligencia artificial de Colsubsidio está listo para procesar tu Score.**")
        
        st.markdown("### 📦 El JSON generado para la API (/perfilar)")
        st.json(st.session_state.lead)
        
        if st.button("🔄 Reiniciar Aventura"):
            st.session_state.clear()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

with col_inv:
    # --- PANEL LATERAL DE INVENTARIO GAMIFICADO ---
    st.markdown("<div class='inventory-panel'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #002D72; font-weight: bold;'>🎒 Tu Mochila</h3>", unsafe_allow_html=True)
    
    # Progreso
    st.progress(st.session_state.nivel / 4)
    st.caption(f"Nivel {st.session_state.nivel} de 4")
    st.divider()
    
    # Items recolectados dinámicamente
    if st.session_state.nivel > 0:
        afil = "✅ Afiliado" if st.session_state.lead['afiliacion_colsubsidio']['es_afiliado'] else "❌ No Afiliado"
        st.markdown(f"**Identidad:** {afil}")
        
    if st.session_state.nivel > 1:
        zona = st.session_state.lead['preferencias_e_intencion']['zona_interes']
        st.markdown(f"**Destino:** {zona}")
        
    if st.session_state.nivel > 2:
        pts = sum(st.session_state.lead['condiciones_especiales_ley'].values())
        sisb = st.session_state.lead['informacion_socioeconomica_externa']['grupo_sisben']
        st.markdown(f"**Poderes Extra:** {pts} activados")
        st.markdown(f"**Sisbén:** {sisb}")
        
    if st.session_state.nivel > 3:
        oro = st.session_state.lead['datos_financieros_declarados']['cesantias_inmovilizadas'] + st.session_state.lead['datos_financieros_declarados']['ahorro_programado']
        st.markdown(f"**Oro acumulado:** ${oro:,.0f}")
        
        if st.session_state.lead['informacion_socioeconomica_externa']['tiene_propiedades_snr'] > 0:
            st.error("⚠️ Infracción: Ya posee propiedades")

    st.markdown("</div>", unsafe_allow_html=True)

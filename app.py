import streamlit as st
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Colsubsidio - Mi Camino VIS", layout="wide", initial_sidebar_state="expanded")

# --- CSS EXTREMADAMENTE VISUAL (Fondo Animado y Layout) ---
st.markdown("""
<style>
    /* Fondo Animado con CSS Puro (Gradiente en movimiento + Patrón sutil) */
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
    
    /* Cabecera Inmersiva (Hero) */
    .game-header { background: #002D72; padding: 30px; color: white; text-align: center; border-radius: 0 0 30px 30px; margin-top: -60px; margin-bottom: 30px; box-shadow: 0 10px 25px rgba(0,0,0,0.15); border-bottom: 5px solid #FFCD00; }
    .game-header h1 { color: #FFCD00 !important; font-weight: 900; font-size: 2.8rem; letter-spacing: -1px; }

    /* Mapa del Camino (Visual Roadmap Ampliado) */
    .roadmap-container { display: flex; justify-content: space-between; align-items: center; position: relative; margin: 20px auto 50px auto; padding: 0 5%; max-width: 1000px; }
    .roadmap-step { display: flex; flex-direction: column; align-items: center; position: relative; z-index: 2; width: 20%; }
    .roadmap-icon { font-size: 2.5rem; background: white; border: 5px solid #E2E8F0; border-radius: 50%; width: 80px; height: 80px; display: flex; justify-content: center; align-items: center; z-index: 2; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
    .step-active .roadmap-icon { border-color: #FFCD00; background: #FEF3C7; transform: scale(1.2); box-shadow: 0 0 20px rgba(255, 205, 0, 0.6); }
    .step-done .roadmap-icon { border-color: #10B981; background: #D1FAE5; }
    .step-label { font-weight: bold; margin-top: 15px; color: #64748B; font-size: 1rem; text-align: center; text-transform: uppercase; letter-spacing: 1px; }
    .step-active .step-label { color: #002D72; font-size: 1.1rem; }
    
    /* Línea conectora del mapa */
    .roadmap-line { position: absolute; top: 40px; left: 10%; right: 10%; height: 6px; background: #E2E8F0; z-index: 1; border-radius: 3px; }
    
    /* Escenario Central (Zona de Construcción) */
    .stage-container { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border-radius: 25px; padding: 50px; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.1); margin: 0 auto 40px auto; border: 1px solid rgba(255,255,255,0.5); max-width: 900px; }
    .house-graphic { font-size: 120px; line-height: 1; margin-bottom: 30px; filter: drop-shadow(0 10px 15px rgba(0,0,0,0.15)); animation: popIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
    
    /* Narrativa de Mentoría (Burbuja amplia) */
    .narrative-box { background: #F8FAFC; border-left: 8px solid #4F46E5; padding: 25px 35px; border-radius: 0 15px 15px 0; text-align: left; margin: 0 auto 40px auto; font-size: 1.2rem; color: #334155; line-height: 1.7; box-shadow: inset 0 2px 4px rgba(0,0,0,0.02); }
    .narrative-title { font-weight: 900; color: #4F46E5; margin-bottom: 15px; font-size: 1.4rem; text-transform: uppercase; letter-spacing: 0.5px; }
    
    /* Ocultar UI estándar y mejorar botones */
    .stSlider > label, .stNumberInput > label, .stRadio > label, .stSelectbox > label { display: none; }
    div.row-widget.stRadio > div { flex-direction: row; flex-wrap: wrap; gap: 15px; justify-content: center; }
    div.row-widget.stRadio > div > label { background: white; padding: 15px 30px; border-radius: 50px; border: 2px solid #E2E8F0; cursor: pointer; transition: all 0.2s; font-weight: bold; color: #475569; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    div.row-widget.stRadio > div > label:hover { border-color: #002D72; background: #F0F4F8; transform: translateY(-2px); }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 2px solid #F1F5F9; }
    
    /* Animaciones */
    @keyframes popIn { 0% { transform: scale(0.5); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZACIÓN DE JSON BLINDADO ---
def get_empty_lead():
    return {
        "datos_personales": {"numero_documento": "", "nombres": "", "edad": 30},
        "afiliacion_colsubsidio": {"es_afiliado": False, "personas_a_cargo_registradas": 0, "tipo_cotizante": "Dependiente"},
        "datos_financieros_declarados": {"ingresos_mensuales_hogar": 0, "cesantias_inmovilizadas": 0, "ahorro_programado": 0, "tiene_credito": False},
        "preferencias_e_intencion": {"zona_interes": "Soacha", "plazo_compra": "Corto plazo"},
        "informacion_socioeconomica_externa": {"grupo_sisben": "N/A", "tiene_propiedades_snr": 0, "tiene_subsidios_previos": False},
        "condiciones_especiales_ley": {"cabeza_de_hogar": False, "discapacidad": False, "mayor_65": False}
    }

if 'nivel' not in st.session_state: st.session_state.nivel = 0
if 'lead' not in st.session_state: st.session_state.lead = get_empty_lead()

# --- MOCK API ---
def api_get_afiliado(cedula):
    db = {"1018300400": {"nombres": "Diana Carolina", "ingresos": 2800000, "personas_cargo": 2, "tipo_cotizante": "Dependiente"}}
    time.sleep(0.8)
    return db.get(cedula, None)

# --- PANEL LATERAL (INVENTARIO Y PROGRESO) ---
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
        st.write("")
        
    if st.session_state.nivel > 3:
        pts = sum(st.session_state.lead['condiciones_especiales_ley'].values())
        sisb = st.session_state.lead['informacion_socioeconomica_externa']['grupo_sisben']
        st.markdown(f"**Poderes Legales:**<br>⚡ {pts} Condición(es)<br>📜 Sisbén: {sisb}", unsafe_allow_html=True)
        
        if st.session_state.lead['informacion_socioeconomica_externa']['tiene_propiedades_snr'] > 0:
            st.error("⚠️ Alerta: Ya posee propiedades")

# --- CABECERA ---
st.markdown("<div class='game-header'><h1>🏠 El Camino hacia tu Casa Propia</h1></div>", unsafe_allow_html=True)

# --- RENDERIZADO DEL MAPA (ROADMAP VISUAL) ---
etapas = [("🔐", "Identidad"), ("📐", "Planos"), ("🧱", "Cimientos"), ("🏗️", "Estructura"), ("🔑", "La Llave")]
mapa_html = '<div class="roadmap-container"><div class="roadmap-line"></div>'
for i, (icono, nombre) in enumerate(etapas):
    clase = "step-active" if i == st.session_state.nivel else ("step-done" if i < st.session_state.nivel else "")
    mapa_html += f'<div class="roadmap-step {clase}"><div class="roadmap-icon">{icono}</div><div class="step-label">{nombre}</div></div>'
mapa_html += '</div>'
st.markdown(mapa_html, unsafe_allow_html=True)

# --- ÁREA CENTRAL DE JUEGO (ZONA DE CONSTRUCCIÓN) ---
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
            cedula = st.text_input("Documento", placeholder="Escribe aquí tu número de cédula...", key="input_cedula")
            st.write("")
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
                        st.session_state.lead['afiliacion_colsubsidio']['tipo_cotizante'] = datos['tipo_cotizante']
                    st.session_state.nivel = 1
                    st.rerun()
                else:
                    st.warning("Debes ingresar un documento para iniciar.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # NIVEL 1: LOS PLANOS (Nombre, Edad, Ocupación, Zona)
    # ---------------------------------------------------------
    elif st.session_state.nivel == 1:
        st.markdown("<div class='stage-container'><div class='house-graphic'>📐</div>", unsafe_allow_html=True)
        
        afiliado = st.session_state.lead['afiliacion_colsubsidio']['es_afiliado']
        nombre_mostrar = st.session_state.lead['datos_personales']['nombres']
        
        mensaje = f"¡Qué alegría verte, {nombre_mostrar}! El sistema me chismeó que eres afiliado y ya guardé tus ingresos, así que nos saltamos esa parte." if afiliado else "¡Gusto en conocerte! Como eres nuevo por aquí, necesito hacerte un par de preguntas básicas para arrancar."
        
        st.markdown(f"""
        <div class='narrative-box'>
            <div class='narrative-title'>Paso 2: Dibujando los Planos</div>
            {mensaje} Ahora vamos a dibujar los planos de tu vida. Necesito saber <b>dónde</b> quieres vivir y <b>tu edad</b>. ¿Por qué la edad? Porque existen bonos extra para el segmento "Joven" que no podemos desaprovechar.
        </div>
        """, unsafe_allow_html=True)
        
        if not afiliado:
            c1, c2 = st.columns(2)
            st.markdown("<br>**¿Cómo te llamas?**", unsafe_allow_html=True)
            st.session_state.lead['datos_personales']['nombres'] = st.text_input("Nombre", placeholder="Tu nombre...")
            
            st.markdown("<br>**¿Cuáles son tus ingresos mensuales aproximados? (COP)**", unsafe_allow_html=True)
            st.session_state.lead['datos_financieros_declarados']['ingresos_mensuales_hogar'] = st.number_input("Ingresos", step=100000, value=1300000)
            
            st.markdown("<br>**¿A qué te dedicas actualmente? (Nos ayuda a organizar tus trámites)**", unsafe_allow_html=True)
            tipo = st.radio("Ocupación", ["Dependiente (Empleado) 🏢", "Independiente 💼", "Pensionado 👴"])
            st.session_state.lead['afiliacion_colsubsidio']['tipo_cotizante'] = tipo.split(" ")[0]
            
        st.markdown("<br>**1. Desliza para indicar tu edad actual:**", unsafe_allow_html=True)
        edad = st.slider("Edad", 18, 80, 30)
        
        st.markdown("<br>**2. ¿En qué zona de Cundinamarca imaginas tu hogar?**", unsafe_allow_html=True)
        zona = st.radio("Zona", ["Soacha", "Bogotá", "Tocancipá", "Girardot"])
        
        st.write("")
        if st.button("✅ Aprobar Planos", type="primary", use_container_width=True):
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
            Para que una casa resista el tiempo, necesita cimientos financieros sólidos. En el mundo real, estos cimientos son <b>tus ahorros y cesantías</b>. Sumaremos tu esfuerzo acumulado para calcular si alcanzas a cubrir la cuota inicial del proyecto.
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**¿Cuántas Cesantías inmovilizadas tienes? (COP)**")
            cesantias = st.number_input("Cesantías", min_value=0, step=500000, value=2000000)
        with c2:
            st.markdown("**¿Cuánto tienes en ahorros voluntarios? (COP)**")
            ahorros = st.number_input("Ahorros", min_value=0, step=500000, value=3000000)
            
        st.write("")
        st.write("")
        if st.button("💪 Cimientos Listos", type="primary", use_container_width=True):
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
            Aquí evaluamos a tu núcleo familiar. Además, ¡tenemos que esquivar rocas legales! 🪨 La Ley nos exige validar que nadie en tu hogar tenga propiedades ni subsidios previos.
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
        col1, col2, col3 = st.columns(3)
        cred_aprobado = col1.toggle("💳 Ya tengo crédito pre-aprobado")
        sub_previo = col2.toggle("🚫 Recibí un subsidio antes")
        propiedades = col3.toggle("🚫 Ya tengo casa a mi nombre")
        
        st.write("")
        if st.button("🔨 Ensamblar Estructura", type="primary", use_container_width=True):
            st.session_state.lead['condiciones_especiales_ley']['cabeza_de_hogar'] = cabeza
            st.session_state.lead['condiciones_especiales_ley']['discapacidad'] = discapacidad
            st.session_state.lead['condiciones_especiales_ley']['mayor_65'] = mayor
            st.session_state.lead['informacion_socioeconomica_externa']['grupo_sisben'] = sisben.split("-")[0] if "-" in sisben else sisben
            st.session_state.lead['informacion_socioeconomica_externa']['tiene_subsidios_previos'] = sub_previo
            st.session_state.lead['informacion_socioeconomica_externa']['tiene_propiedades_snr'] = 1 if propiedades else 0
            st.session_state.lead['datos_financieros_declarados']['tiene_credito'] = cred_aprobado
            
            st.session_state.nivel = 4
            st.balloons()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # NIVEL 4: LA CASA TERMINADA (Mentoría y Documentos)
    # ---------------------------------------------------------
    elif st.session_state.nivel == 4:
        # Lógica rápida para determinar la ruta (En producción esto lo decide el API)
        tiene_credito = st.session_state.lead['datos_financieros_declarados']['tiene_credito']
        ahorros_totales = st.session_state.lead['datos_financieros_declarados']['cesantias_inmovilizadas'] + st.session_state.lead['datos_financieros_declarados']['ahorro_programado']
        cierre_viable = tiene_credito and ahorros_totales > 0

        if cierre_viable:
            # --- RUTA 1: CIERRE FINANCIERO VIABLE (ENTREGA DE DOCUMENTOS) ---
            st.markdown("<div class='stage-container'><div class='house-graphic'>🏠✨</div>", unsafe_allow_html=True)
            st.markdown("""
            <div class='narrative-box' style='border-left-color: #10B981; color: #065F46; background: #D1FAE5;'>
                <div class='narrative-title' style='color: #065F46;'>¡Misión Cumplida! Estás a un paso de las Llaves</div>
                Tu perfil financiero es sólido. Hemos preparado tu <b>Mochila de Radicación</b> con los documentos exactos que necesitas llenar. Descárgalos aquí mismo y no hagas filas innecesarias.
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 📥 Descarga tus Documentos Oficiales")
            
            c1, c2 = st.columns(2)
            with c1:
                st.link_button("📝 Descargar Formulario de Postulación", "https://www.colsubsidio.com/hubfs/documentos/colsubsidio/formulario-postulacion-subsidio-vivienda-colsubsidio-radicacion-digital.pdf", use_container_width=True)
            with c2:
                if st.session_state.lead['condiciones_especiales_ley']['cabeza_de_hogar']:
                    st.link_button("📄 Formato de Estado Civil (Cabeza de Hogar)", "https://www.colsubsidio.com/hubfs/documentos/colsubsidio/formato-declaracion-de-estado-civil-y-condicion-especial-sfv.pdf", use_container_width=True)
            
            st.info("💡 **Tip de radicación:** Recuerda anexar las fotocopias legibles de las cédulas y tu carta de aprobación de crédito (vigencia no mayor a 90 días).")

        else:
            # --- RUTA 2: MENTORÍA Y ACOMPAÑAMIENTO (PERTENESER) ---
            st.markdown("<div class='stage-container'><div class='house-graphic'>🌱🏗️</div>", unsafe_allow_html=True)
            st.markdown("""
            <div class='narrative-box' style='border-left-color: #F59E0B; color: #92400E; background: #FEF3C7;'>
                <div class='narrative-title' style='color: #92400E;'>¡Tu sueño está en construcción!</div>
                Notamos que aún necesitas fortalecer tu escudo financiero (crédito y ahorros) para alcanzar la meta. En Colsubsidio nunca te dejamos solo. Te damos la bienvenida a nuestro programa de acompañamiento <b>PerteneSER</b>. Aquí tienes tu plan de acción:
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### 🗺️ Tu Plan de Entrenamiento Financiero")
            
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.markdown("""
                <div style='background: white; padding: 20px; border-radius: 12px; border: 2px solid #FCD34D; height: 100%;'>
                    <h4 style='color: #D97706; margin-top: 0;'>1. Subsidio de Arrendamiento</h4>
                    <p>Mientras ahorras para tu cuota inicial, postúlate para recibir <b>0.6 SMMLV mensuales durante 24 meses</b> para el pago de tu arriendo actual.</p>
                </div>
                """, unsafe_allow_html=True)
            with col_m2:
                st.markdown("""
                <div style='background: white; padding: 20px; border-radius: 12px; border: 2px solid #60A5FA; height: 100%;'>
                    <h4 style='color: #2563EB; margin-top: 0;'>2. Gestión de Cesantías</h4>
                    <p>Las cesantías inmovilizadas suman muchos puntos. Te asesoramos para trasladarlas y bloquearlas exclusivamente para la compra de tu futura vivienda.</p>
                </div>
                """, unsafe_allow_html=True)

            st.write("")
            st.button("🎯 Agendar Asesoría Gratuita PerteneSER", type="primary", use_container_width=True)

        st.divider()
        with st.expander("💻 Ver JSON Generado para el Motor (Auditoría Jurados)", expanded=False):
            st.json(st.session_state.lead)
            
        if st.button("🔄 Volver a Empezar el Camino", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
            
        if st.button("🔄 Reiniciar la Aventura", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

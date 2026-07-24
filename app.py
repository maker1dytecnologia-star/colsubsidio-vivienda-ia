import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Colsubsidio Vivienda - Perfilamiento Inteligente",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Preloaded data path
CSV_PATH = '/workspace/knowledge/hackathon_VIVIENDAv2.xlsx_-_CV_SSS_VIV_PENETRACION_PERFIL_C.csv'

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(CSV_PATH)
        # Clean price format (divide by 10,000 as per data documentation)
        if 'VLR_VIVIENDA' in df.columns:
            df['VLR_VIVIENDA_CLEAN'] = df['VLR_VIVIENDA'].apply(
                lambda x: float(str(x).replace(',', '')) / 10000 if pd.notna(x) else 0
            )
        else:
            df['VLR_VIVIENDA_CLEAN'] = 0
        return df
    except Exception as e:
        st.error(f"Error cargando base de datos: {e}")
        return None

df = load_data()

# 2026 Financial Constants
SMMLV_2026 = 1750905
VIP_TOPE = 90 * SMMLV_2026      # $157,581,450
VIS_TOPE_NACIONAL = 135 * SMMLV_2026 # $236,372,175
VIS_TOPE_BOGOTA = 150 * SMMLV_2026   # $262,635,750

# Predefined Real-World Projects from Colsubsidio Portfolio
PROJECTS = [
    {"nombre": "La Macarena (Soacha)", "tipo": "VIS", "precio": 149182800, "area": "34.94 m²", "municipio": "Soacha"},
    {"nombre": "Monguí (Soacha)", "tipo": "VIS", "precio": 173491500, "area": "45.05 m²", "municipio": "Soacha"},
    {"nombre": "Zarzal (Soacha)", "tipo": "VIS", "precio": 219400000, "area": "43 m²", "municipio": "Soacha"},
    {"nombre": "Pamplona I (Soacha)", "tipo": "VIS", "precio": 206407500, "area": "50.25 m²", "municipio": "Soacha"},
    {"nombre": "Bosque de Arrayán", "tipo": "VIS", "precio": 191503455, "area": "45.53 m²", "municipio": "Tocancipá"},
    {"nombre": "Payandé", "tipo": "VIS", "precio": 194524000, "area": "44 m²", "municipio": "Ricaurte"},
    {"nombre": "Samán", "tipo": "VIS", "precio": 258500000, "area": "52 m²", "municipio": "Ricaurte"},
    {"nombre": "Reserva de Guayacán", "tipo": "VIS", "precio": 239500000, "area": "52.98 m²", "municipio": "Girardot"},
    {"nombre": "Vibo Once (Bogotá)", "tipo": "VIS", "precio": 281300000, "area": "36 m²", "municipio": "Bogotá"},
    {"nombre": "Nuva Park", "tipo": "NO VIS", "precio": 360000000, "area": "36 m²", "municipio": "Bogotá"},
    {"nombre": "Lúmina 77", "tipo": "NO VIS", "precio": 375000000, "area": "37 m²", "municipio": "Bogotá"},
    {"nombre": "Calia (Bogotá Norte)", "tipo": "NO VIS", "precio": 2950000000, "area": "36 m²", "municipio": "Bogotá"}
]

# Custom CSS for Colsubsidio Branding & WhatsApp simulator
st.markdown("""
<style>
    .top-bar {
        background-color: #002D72;
        padding: 15px;
        color: #FFCD00;
        text-align: center;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    .top-bar h1 {
        color: #FFCD00 !important;
        margin: 0;
    }
    .whatsapp-container {
        background-color: #E5DDD5;
        border-radius: 15px;
        padding: 15px;
        border: 2px solid #128C7E;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        min-height: 600px;
    }
    .whatsapp-header {
        background-color: #075E54;
        color: white;
        padding: 10px;
        border-radius: 10px 10px 0 0;
        font-weight: bold;
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }
    .chat-bubble-received {
        background-color: white;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 85%;
        text-align: left;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .chat-bubble-sent {
        background-color: #DCF8C6;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        margin-left: auto;
        max-width: 85%;
        text-align: right;
        box-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .station-badge {
        background-color: #128C7E;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    .salesforce-container {
        background-color: #F3F5F9;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #D8DDE6;
    }
    .salesforce-header {
        background-color: #1589EE;
        color: white;
        padding: 10px;
        border-radius: 10px 10px 0 0;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .score-badge-high {
        background-color: #4BCA81;
        color: white;
        padding: 8px 15px;
        border-radius: 5px;
        font-weight: bold;
        display: inline-block;
    }
    .score-badge-medium {
        background-color: #FFB75D;
        color: white;
        padding: 8px 15px;
        border-radius: 5px;
        font-weight: bold;
        display: inline-block;
    }
    .score-badge-low {
        background-color: #C23934;
        color: white;
        padding: 8px 15px;
        border-radius: 5px;
        font-weight: bold;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Application Title
st.markdown('<div class="top-bar"><h1>🏠 HACKATHON COLSUBSIDIO: PERFILAMIENTO INTELIGENTE DE VIVIENDA</h1><p>Demo interactiva de doble pantalla: Chat de WhatsApp (Lado Izquierdo) vs. CRM Salesforce (Lado Derecho)</p></div>', unsafe_allow_html=True)

# ----------------- SESSION STATE INITIALIZATION -----------------
if 'station' not in st.session_state:
    st.session_state.station = 1
if 'selected_affiliate' not in st.session_state:
    st.session_state.selected_affiliate = "Diana Carolina (Categoría Básico - 1.5 SMMLV)"
if 'answers' not in st.session_state:
    st.session_state.answers = {
        "sueño_municipio": "Soacha",
        "sueño_familia": "Pareja y 1 Hijo",
        "ahorros": 15000000,
        "subsidio_gobierno": "Sí, clasificado en Sisbén A/B (30 SMMLV)",
        "credito_aprobado": 80000000,
        "tiene_vivienda": "No"
    }

# Pre-defined profiles reflecting the Excel & PPT resource distribution
PRESETS = {
    "Diana Carolina (Categoría Básico - 1.5 SMMLV)": {
        "cotizante": "Diana Carolina",
        "afiliado": True,
        "categoria": "Básico",
        "salario_base": 1.5 * SMMLV_2026,
        "personas_cargo": 2,
        "grupo_familiar": "Monoparental",
        "edad": "20 a 35 años",
        "empresa": "TELEPERFORMANCE"
    },
    "Jonathan Herrera (Categoría Joven - 2.2 SMMLV)": {
        "cotizante": "Jonathan Herrera",
        "afiliado": True,
        "categoria": "Joven",
        "salario_base": 2.2 * SMMLV_2026,
        "personas_cargo": 0,
        "grupo_familiar": "Unifamiliar",
        "edad": "Menor de 30 años",
        "empresa": "CONSORCIO EXPRESS S A S"
    },
    "Carlos Gómez (Categoría Medio - 3.5 SMMLV)": {
        "cotizante": "Carlos Gómez",
        "afiliado": True,
        "categoria": "Medio",
        "salario_base": 3.5 * SMMLV_2026,
        "personas_cargo": 3,
        "grupo_familiar": "Pareja Conyugal",
        "edad": "36 a 45 años",
        "empresa": "COLSUBSIDIO"
    },
    "María Beltrán (Categoría Alto - 6.5 SMMLV)": {
        "cotizante": "María Beltrán",
        "afiliado": True,
        "categoria": "Alto",
        "salario_base": 6.5 * SMMLV_2026,
        "personas_cargo": 1,
        "grupo_familiar": "Pareja con hijo",
        "edad": "46 a 55 años",
        "empresa": "MERCADOLIBRE"
    },
    "Invitado No Afiliado - 2.5 SMMLV": {
        "cotizante": "Andrés Felipe",
        "afiliado": False,
        "categoria": "No Afiliado",
        "salario_base": 2.5 * SMMLV_2026,
        "personas_cargo": 1,
        "grupo_familiar": "Monoparental",
        "edad": "20 a 35 años",
        "empresa": "Independiente"
    }
}

# --- Sidebar for Sandbox Control & Dataset Inspection ---
with st.sidebar:
    st.header("⚙️ Panel de Control de la Hackatón")
    st.write("Simula diferentes estados y visualiza el comportamiento de la base de datos.")
    
    # Profile Selector
    selected_name = st.selectbox(
        "👤 Selecciona el Afiliado a Perfilar:",
        list(PRESETS.keys()),
        key="selected_profile"
    )
    st.session_state.selected_affiliate = selected_name
    profile = PRESETS[selected_name]
    
    st.divider()
    st.write("📊 **Datos de Acompañamiento Social (PerteneSer):**")
    st.info("Si el lead no cierra financieramente, se guardará en la base de preparación PerteneSer de Colsubsidio y se le ofrecerá Subsidio de Arrendamiento con opción de compra.")
    
    st.divider()
    if df is not None:
        st.write(f"📈 **Registros de Compradores Históricos (Excel):** {len(df):,}")
        # Display small sample of historical projects matched
        sample_projects = df['NOMBRE_PROYECTO'].value_counts().head(5)
        st.bar_chart(sample_projects)

# Get active profile values
active_profile = PRESETS[st.session_state.selected_affiliate]

# ----------------- APP COLUMNS (DUAL SCREEN) -----------------
col_chat, col_crm = st.columns([5, 6])

# =========================================================================
# LADO IZQUIERDO: CHAT DE WHATSAPP / MOCK DE TELEGRAM ("MI CAMINO VIS")
# =========================================================================
with col_chat:
    st.markdown('<div class="whatsapp-header">💬 WhatsApp de Vivienda Colsubsidio</div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        st.write(f"📱 **Camino de Rol del Usuario: Mi Camino VIS**")
        
        # Display Stations Roadmap
        st_cols = st.columns(5)
        stations_titles = ["1. Sueño", "2. Ahorros", "3. Poderes", "4. Respaldo", "5. Llave"]
        for idx, title in enumerate(stations_titles, 1):
            if st.session_state.station == idx:
                st_cols[idx-1].success(f"📍 **{title}**")
            elif st.session_state.station > idx:
                st_cols[idx-1].info(f"✅ {title}")
            else:
                st_cols[idx-1].text_input(f"🔒 {title}", key=f"title_{idx}", disabled=True, label_visibility="collapsed")

        st.divider()

        # Simulated Chat History Box
        st.markdown('<div class="whatsapp-container">', unsafe_allow_html=True)
        
        # Station 1 messages
        st.markdown(f'<div class="chat-bubble-received"><b>Asesor Digital:</b> ¡Hola <b>{active_profile["cotizante"]}</b>! Veo en nuestro sistema que eres afiliado Categoría {active_profile["categoria"]} en Colsubsidio. Cuéntame, ¿con quién sueñas vivir en tu nuevo hogar y en qué municipio de Cundinamarca te gustaría estar?</div>', unsafe_allow_html=True)
        
        if st.session_state.station >= 2:
            st.markdown(f'<div class="chat-bubble-sent"><b>{active_profile["cotizante"]}:</b> Me imagino viviendo en {st.session_state.answers["sueño_municipio"]} con mi {st.session_state.answers["sueño_familia"]}.</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-bubble-received"><b>Asesor Digital:</b> ¡Qué gran proyecto de vida! Soacha y Cundinamarca tienen excelentes opciones. Ahora hablemos de tu "cofre de ahorros" 🪙. ¿Con cuánto cuentas aproximadamente hoy entre cesantías, ahorros o pagos que ya le hayas hecho a alguna constructora?</div>', unsafe_allow_html=True)

        # Station 2 messages
        if st.session_state.station >= 3:
            st.markdown(f'<div class="chat-bubble-sent"><b>{active_profile["cotizante"]}:</b> Tengo aprox ${st.session_state.answers["ahorros"]:,} COP en ahorros.</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-bubble-received"><b>Asesor Digital:</b> ¡Excelente! Esos recursos suman un gran valor. Ahora desbloqueemos tus "Súper Poderes" (Subsidios) 🌟. Basado en tus ingresos, Colsubsidio te otorga un subsidio de vivienda. Además, evaluemos si aplicas a Mi Casa Ya del Gobierno Nacional.</div>', unsafe_allow_html=True)

        # Station 3 messages
        if st.session_state.station >= 4:
            st.markdown(f'<div class="chat-bubble-sent"><b>{active_profile["cotizante"]}:</b> {st.session_state.answers["subsidio_gobierno"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-bubble-received"><b>Asesor Digital:</b> ¡Maravilloso! Tus subsidios están listos. Por último, hablemos de tu crédito hipotecario (tu escudo financiero) 🛡️. ¿Tienes ya un cupo de crédito preaprobado o aprobado por Colsubsidio o algún banco, o deseas que simulemos tu cuota mensual?</div>', unsafe_allow_html=True)

        # Station 4 messages
        if st.session_state.station >= 5:
            st.markdown(f'<div class="chat-bubble-sent"><b>{active_profile["cotizante"]}:</b> Sí, tengo preaprobado un crédito de ${st.session_state.answers["credito_aprobado"]:,} COP.</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-bubble-received"><b>Asesor Digital:</b> ¡Tenemos todo! Permíteme calcular tu cierre financiero y entregarte la llave de tu hogar ideal en la siguiente pantalla... 🔑</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.divider()

        # Chat inputs depending on the current station
        st.write(f"📝 **Completa la Estación {st.session_state.station}:**")
        
        if st.session_state.station == 1:
            m_col1, m_col2 = st.columns(2)
            s_mun = m_col1.selectbox("Municipio de interés:", ["Soacha", "Bogotá", "Tocancipá", "Girardot", "Ricaurte"])
            s_fam = m_col2.selectbox("¿Con quién vivirás?", ["Soltero", "Pareja Conyugal", "Pareja y 1 Hijo", "Grupo Familiar Grande"])
            if st.button("Enviar Respuestas ➔ Estación 2"):
                st.session_state.answers["sueño_municipio"] = s_mun
                st.session_state.answers["sueño_familia"] = s_fam
                st.session_state.station = 2
                st.rerun()

        elif st.session_state.station == 2:
            ahorros_val = st.number_input("Tus ahorros totales (COP):", min_value=0, value=int(st.session_state.answers["ahorros"]), step=1000000)
            tiene_vivienda_val = st.radio("¿Tienes alguna vivienda propia a tu nombre en Colombia?", ["No", "Sí"])
            if st.button("Enviar Respuestas ➔ Estación 3"):
                st.session_state.answers["ahorros"] = savings_val = ahorros_val
                st.session_state.answers["tiene_vivienda"] = tiene_vivienda_val
                st.session_state.station = 3
                st.rerun()

        elif st.session_state.station == 3:
            sub_gob = st.selectbox("¿Calificas para subsidio Mi Casa Ya del Gobierno (Sisbén IV A1-D20)?", [
                "Sí, clasificado en Sisbén A1-C7 (30 SMMLV)",
                "Sí, clasificado en Sisbén C8-D20 (20 SMMLV)",
                "No aplico / No tengo Sisbén"
            ])
            if st.button("Enviar Respuestas ➔ Estación 4"):
                st.session_state.answers["subsidio_gobierno"] = sub_gob
                st.session_state.station = 4
                st.rerun()

        elif st.session_state.station == 4:
            cred_val = st.number_input("Monto de crédito hipotecario preaprobado (COP):", min_value=0, value=int(st.session_state.answers["credito_aprobado"]), step=5000000)
            if st.button("Enviar Respuestas ➔ Estación 5"):
                st.session_state.answers["credito_aprobado"] = cred_val
                st.session_state.station = 5
                st.rerun()

        elif st.session_state.station == 5:
            st.success("¡Camino VIS Completado con éxito! Revisa en el panel derecho (Salesforce) la recomendación y la prioridad asignada.")
            if st.button("Reiniciar Aventura del Juego"):
                st.session_state.station = 1
                st.rerun()

# =========================================================================
# LADO DERECHO: CONSOLA DE SALESFORCE (CRM COMPLETO)
# =========================================================================
with col_crm:
    st.markdown('<div class="salesforce-header">📊 Consola del Asesor Comercial (Salesforce Mockup)</div>', unsafe_allow_html=True)
    
    # 1. Profile Core Details loaded without friction from Colsubsidio DB
    st.subheader("👤 Datos Básicos del Afiliado (Carga Transaccional de la Caja)")
    det1, det2, det3 = st.columns(3)
    det1.metric("Nombre del Lead", active_profile["cotizante"])
    det2.metric("Categoría de Caja", active_profile["categoria"])
    det3.metric("Ingresos PILA Base", f"${active_profile['salario_base']:,} COP")

    st.write(f"🏢 **Empresa Registrada en PILA:** {active_profile['empresa']} | **Personas a Cargo:** {active_profile['personas_cargo']}")
    
    st.divider()

    # 2. Logic and Calculations for Subsidies & Golden Rule (40%)
    st.subheader("⚙️ Motor de Simulación Financiera (Año 2026)")
    
    # Calculate Caja Subsidio based on standard rules
    if not active_profile["afiliado"]:
        subsidio_caja = 0
    else:
        # Categoría Básico or low income gets 30 SMMLV, others get 20 SMMLV
        if active_profile["salario_base"] <= 2 * SMMLV_2026:
            subsidio_caja = 30 * SMMLV_2026 # $52,527,150
        elif active_profile["salario_base"] <= 4 * SMMLV_2026:
            subsidio_caja = 20 * SMMLV_2026 # $35,018,100
        else:
            subsidio_caja = 0 # No VIS or income > 4 SMMLV

    # Calculate Mi Casa Ya
    if "A1-C7" in st.session_state.answers["subsidio_gobierno"]:
        subsidio_gobierno_val = 30 * SMMLV_2026
    elif "C8-D20" in st.session_state.answers["subsidio_gobierno"]:
        subsidio_gobierno_val = 20 * SMMLV_2026
    else:
        subsidio_gobierno_val = 0

    # Total subsidy
    subsidios_totales = subsidio_caja + subsidio_gobierno_val

    # Golden Rule: 40% income cap for monthly credit payment
    cuota_maxima_permitida = active_profile["salario_base"] * 0.40
    
    # Estimate actual monthly payment based on recommended VIS credit
    # Let's assume a standard VIS mortgage interest rate of 12% E.A. over 20 years
    m_rate = 0.01 # Approx 1% monthly
    n_months = 240
    if st.session_state.answers["credito_aprobado"] > 0:
        cuota_mensual_estimada = st.session_state.answers["credito_aprobado"] * (m_rate * (1 + m_rate)**n_months) / (((1 + m_rate)**n_months) - 1)
    else:
        cuota_mensual_estimada = 0

    # Project Match Selection based on Location and Budget
    presupuesto_total = st.session_state.answers["ahorros"] + subsidios_totales + st.session_state.answers["credito_aprobado"]
    
    # Select matches
    matched_projects = []
    category_assigned = "Pendiente"
    
    if presupuesto_total < VIP_TOPE:
        category_assigned = "VIP (Vivienda de Interés Prioritario)"
    elif presupuesto_total <= VIS_TOPE_BOGOTA:
        category_assigned = "VIS (Vivienda de Interés Social)"
    else:
        category_assigned = "NO VIS (Vivienda Premium)"

    # Filter real portfolio projects that fit budget and location
    for p in PROJECTS:
        if p["precio"] <= presupuesto_total:
            # Match location or default
            if p["municipio"].lower() == st.session_state.answers["sueño_municipio"].lower():
                matched_projects.append(p)
    
    if not matched_projects:
        # Fallback to closest available in the portfolio
        matched_projects = [p for p in PROJECTS if p["precio"] <= presupuesto_total][:2]

    # Rule checks
    excluido_propiedad = st.session_state.answers["tiene_vivienda"] == "Sí"
    supera_ingresos_subsidio = active_profile["salario_base"] > 4 * SMMLV_2026
    
    # Check if budget is enough for the chosen project
    selected_match = matched_projects[0] if matched_projects else PROJECTS[0]
    brecha = selected_match["precio"] - presupuesto_total
    
    # Golden rule status
    cumple_regla_40 = cuota_mensual_estimada <= cuota_maxima_permitida

    # 3. SCORE EVALUATION
    # Prioridad Alta: No properties, qualifies for subsidies, budget covers the project (brecha <= 0), cumple regla 40
    # Prioridad Media: Qualifies but has a positive financial breach (brecha > 0), gets PerteneSER enrutamiento
    # Prioridad Baja: Excluido (already owns a house) or income too high for VIS but has no credit preapproval
    if excluido_propiedad:
        priority_label = "Prioridad Baja (🔴 Excluido - Ya posee vivienda)"
        priority_css = "score-badge-low"
        suggested_action = "Notificar exclusión legal de subsidio. Ofrecer línea de crédito estándar libre inversión."
    elif supera_ingresos_subsidio:
        priority_label = "Prioridad Media (🟡 Rango Salarial NO VIS)"
        priority_css = "score-badge-medium"
        suggested_action = "Enrutar a portafolio NO VIS en Bogotá Norte / Chapinero (Lúmina 77 o Calia)."
    elif not cumple_regla_40:
        priority_label = "Prioridad Media (🟡 Alerta Ley de Vivienda)"
        priority_css = "score-badge-medium"
        suggested_action = "Ajustar plazo de crédito en Salesforce o enrutar al programa PerteneSER para ahorro programado."
    elif brecha > 0:
        priority_label = "Prioridad Media (🟡 Requiere Maduración)"
        priority_css = "score-badge-medium"
        suggested_action = "Enrutar a Subsidio de Arrendamiento Colsubsidio (Ahorro de cuota inicial por 24 meses)."
    else:
        priority_label = "Prioridad Alta (🟢 Listo para Cierre)"
        priority_css = "score-badge-high"
        suggested_action = f"Llamar de inmediato para separar apartamento en {selected_match['nombre']}. Cierre financiero completo."

    st.markdown(f"**Calificación del Lead:** <span class='{priority_css}'>{priority_label}</span>", unsafe_allow_html=True)
    st.write(f"💡 **Acción Comercial Sugerida:** {suggested_action}")

    st.divider()

    # 4. Verification Checklist (Cruces Internos vs Externos)
    st.subheader("🕵️ Checklist de Validación (Cruces Integrados)")
    v_col1, v_col2 = st.columns(2)
    
    with v_col1:
        st.write("**Cruces Internos (Colsubsidio):**")
        st.write("✅ **Afiliación Activa:** Validado con Aportes")
        st.write("✅ **Antigüedad > 6 meses:** Validado")
        st.write("✅ **Consistencia Familiar:** Validado con Registro Civil")
    
    with v_col2:
        st.write("**Cruces Externos (Validaciones de Ley):**")
        st.write("❌ **Propietario SNR:** " + ("Tiene propiedad (Bloqueado)" if excluido_propiedad else "No posee vivienda (Aprobado) ✅"))
        st.write("✅ **Historial RUAV (No Subsidios Previos):** Aprobado")
        st.write("✅ **Crédito DataCrédito / TransUnion:** " + (f"Viable cuota mensual (${cuota_mensual_estimada:,.0f} COP)" if cumple_regla_40 else f"No viable: supera el 40% de ingresos max: (${cuota_maxima_permitida:,.0f} COP)"))

    st.divider()

    # 5. Financial Summary Table
    st.subheader("📊 Tabla de Cierre Financiero Estimado")
    
    fin_data = {
        "Concepto Financiero": [
            "Valor de la Vivienda Recomendada",
            "Subsidio Caja Colsubsidio (2026)",
            "Subsidio Mi Casa Ya (DNP)",
            "Ahorros / Recursos Propios",
            "Crédito Hipotecario Preaprobado",
            "Brecha Financiera de Cierre"
        ],
        "Valor (COP)": [
            f"${selected_match['precio']:,} COP",
            f"${subsidio_caja:,} COP",
            f"${subsidio_gobierno_val:,} COP",
            f"${st.session_state.answers['ahorros']:,} COP",
            f"${st.session_state.answers['credito_aprobado']:,} COP",
            f"${max(0, brecha):,} COP" if brecha > 0 else "$0 COP (Cierre Exitoso! 🎉)"
        ],
        "Valor en SMMLV (2026)": [
            f"{selected_match['precio']/SMMLV_2026:.1f} SMMLV",
            f"{subsidio_caja/SMMLV_2026:.1f} SMMLV",
            f"{subsidio_gobierno_val/SMMLV_2026:.1f} SMMLV",
            f"{st.session_state.answers['ahorros']/SMMLV_2026:.1f} SMMLV",
            f"{st.session_state.answers['credito_aprobado']/SMMLV_2026:.1f} SMMLV",
            f"{max(0, brecha)/SMMLV_2026:.1f} SMMLV" if brecha > 0 else "0.0 SMMLV"
        ]
    }
    st.table(pd.DataFrame(fin_data))

    # 6. Suggested Match Cards
    st.subheader("🔑 Proyecto Recomendado para el Match")
    st.info(f"**Proyecto:** {selected_match['nombre']} | **Categoría:** {category_assigned} | **Área desde:** {selected_match['area']} | **Precio:** ${selected_match['precio']:,} COP")

st.divider()
st.write("🚀 **Estrategia del Pitch:** Utilicen esta demo en vivo para mostrar cómo la IA cualifica al lead en segundo plano y cómo se pasa de 'interrogar' a 'entender los sueños' del afiliado.")
    
    # Tabla Financiera Transparente
    st.subheader("💰 Resumen Financiero Consolidado")
    fin_data = {
        "Concepto": ["Subsidio Automático (Caja)", "Ahorros Propios", "Crédito Declarado", "Poder Adquisitivo Total"],
        "Valor (COP)": [f"${subsidio_caja:,.0f}", f"${st.session_state.answers['ahorros']:,.0f}", f"${st.session_state.answers['credito_aprobado']:,.0f}", f"${presupuesto_total:,.0f}"]
    }
    st.table(pd.DataFrame(fin_data))

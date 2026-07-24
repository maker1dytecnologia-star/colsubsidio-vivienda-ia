import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Colsubsidio Vivienda - Perfilamiento Inteligente",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Preloaded data path (Asegúrate de que esta ruta sea la correcta en tu repo, si está en la misma carpeta usa solo el nombre del archivo)
# Preloaded data path (Apunta directamente al archivo en la raíz del repo)
DATA_PATH = 'hackathon_VIVIENDAv2.xlsx'

@st.cache_data
def load_data():
    try:
        # Se cambia read_csv por read_excel ya que el archivo es .xlsx
        df = pd.read_excel(DATA_PATH, sheet_name=0)
        
        # Limpieza de formato de precio (dividir por 10,000 según documentación)
        if 'VLR_VIVIENDA' in df.columns:
            # En pandas leyendo excel directo, usualmente ya es numérico, pero aseguramos
            df['VLR_VIVIENDA_CLEAN'] = pd.to_numeric(df['VLR_VIVIENDA'], errors='coerce').fillna(0) / 10000
        else:
            df['VLR_VIVIENDA_CLEAN'] = 0
            
        return df
    except Exception as e:
        st.error(f"Error cargando base de datos histórica: {e}. Se usarán proyectos por defecto.")
        return pd.DataFrame()

df = load_data()

# 2026 Financial Constants
SMMLV_2026 = 1750905
VIP_TOPE = 90 * SMMLV_2026      # $157,581,450
VIS_TOPE_BOGOTA = 150 * SMMLV_2026   # $262,635,750

# Custom CSS for Colsubsidio Branding & WhatsApp simulator
st.markdown("""
<style>
    .top-bar { background-color: #002D72; padding: 15px; color: #FFCD00; text-align: center; border-radius: 5px; margin-bottom: 20px; }
    .top-bar h1 { color: #FFCD00 !important; margin: 0; }
    .whatsapp-container { background-color: #E5DDD5; border-radius: 15px; padding: 15px; border: 2px solid #128C7E; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); min-height: 600px; }
    .whatsapp-header { background-color: #075E54; color: white; padding: 10px; border-radius: 10px 10px 0 0; font-weight: bold; display: flex; align-items: center; margin-bottom: 15px; }
    .chat-bubble-received { background-color: white; padding: 10px; border-radius: 10px; margin-bottom: 10px; max-width: 85%; text-align: left; box-shadow: 1px 1px 2px rgba(0,0,0,0.1); }
    .chat-bubble-sent { background-color: #DCF8C6; padding: 10px; border-radius: 10px; margin-bottom: 10px; margin-left: auto; max-width: 85%; text-align: right; box-shadow: 1px 1px 2px rgba(0,0,0,0.1); }
    .salesforce-container { background-color: #F3F5F9; border-radius: 15px; padding: 20px; border: 1px solid #D8DDE6; }
    .salesforce-header { background-color: #1589EE; color: white; padding: 10px; border-radius: 10px 10px 0 0; font-weight: bold; margin-bottom: 15px; }
    .score-badge-high { background-color: #4BCA81; color: white; padding: 8px 15px; border-radius: 5px; font-weight: bold; display: inline-block; }
    .score-badge-medium { background-color: #FFB75D; color: white; padding: 8px 15px; border-radius: 5px; font-weight: bold; display: inline-block; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="top-bar"><h1>🏠 HACKATHON COLSUBSIDIO: PERFILAMIENTO INTELIGENTE</h1><p>Demo interactiva de doble pantalla: Chat de WhatsApp (IA) vs. CRM Salesforce</p></div>', unsafe_allow_html=True)

# ----------------- SESSION STATE & PRESETS -----------------
if 'station' not in st.session_state:
    st.session_state.station = 1
if 'answers' not in st.session_state:
    st.session_state.answers = {"sueño_municipio": "Soacha", "sueño_familia": "Pareja y 1 Hijo", "ahorros": 15000000, "credito_aprobado": 80000000, "tiene_vivienda": "No"}

# Mapeo de usuarios simulados cruzando la info transaccional con la nomenclatura del Excel
PRESETS = {
    "Diana Carolina (Categoría Básico)": {
        "cotizante": "Diana Carolina", "afiliado": True, "categoria": "Básico", "salario_base": 1.5 * SMMLV_2026, 
        "personas_cargo": 2, "empresa": "TELEPERFORMANCE", 
        "excel_categoria": "OMEGA", "excel_edad": "20 - 35 años", "excel_piramide": "RHO"
    },
    "Jonathan Herrera (Categoría Joven)": {
        "cotizante": "Jonathan Herrera", "afiliado": True, "categoria": "Joven", "salario_base": 2.2 * SMMLV_2026, 
        "personas_cargo": 0, "empresa": "CONSORCIO EXPRESS S A S", 
        "excel_categoria": "TAU", "excel_edad": "Menor a 20 años", "excel_piramide": "ALPHA"
    }
}

with st.sidebar:
    st.header("⚙️ Simulación de Lead")
    selected_name = st.selectbox("👤 Selecciona el Afiliado:", list(PRESETS.keys()))
    active_profile = PRESETS[selected_name]
    
    if st.button("Reiniciar Interacción"):
        st.session_state.station = 1
        st.rerun()

col_chat, col_crm = st.columns([5, 6])

# =========================================================================
# LADO IZQUIERDO: CHAT INTELIGENTE (GATEKEEPER)
# =========================================================================
with col_chat:
    st.markdown('<div class="whatsapp-header">💬 Asesor IA Colsubsidio</div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        st.markdown('<div class="whatsapp-container">', unsafe_allow_html=True)
        
        # Estación 1: Contexto Inteligente (Evita preguntar lo que ya sabe)
        st.markdown(f'<div class="chat-bubble-received"><b>Asesor Digital:</b> ¡Hola <b>{active_profile["cotizante"]}</b>! 👋<br><br>Veo en nuestro sistema que trabajas en {active_profile["empresa"]} y tienes a {active_profile["personas_cargo"]} personas a cargo registradas. ¡Ese es un gran paso!<br><br>Para no aburrirte con formularios, ya calculé tu subsidio de vivienda automático. Solo cuéntame: ¿En qué municipio te gustaría vivir con ellos?</div>', unsafe_allow_html=True)
        
        if st.session_state.station >= 2:
            st.markdown(f'<div class="chat-bubble-sent"><b>{active_profile["cotizante"]}:</b> Me encantaría en {st.session_state.answers["sueño_municipio"]}.</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-bubble-received"><b>Asesor Digital:</b> ¡Perfecto! Para buscar en nuestra base de datos los proyectos donde familias como la tuya han invertido exitosamente, dime: ¿Con cuántos ahorros cuentas actualmente (incluyendo cesantías) y qué preaprobado de crédito tienes?</div>', unsafe_allow_html=True)

        if st.session_state.station >= 3:
            st.markdown(f'<div class="chat-bubble-sent"><b>{active_profile["cotizante"]}:</b> Tengo ${st.session_state.answers["ahorros"]:,} ahorrados y un preaprobado de ${st.session_state.answers["credito_aprobado"]:,}.</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-bubble-received"><b>Asesor Digital:</b> ¡Excelente perfil! 🚀 Ya estoy cruzando tus datos con nuestro modelo predictivo. Mira el panel de la derecha para ver tu recomendación oficial.</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Inputs de usuario
        st.divider()
        if st.session_state.station == 1:
            s_mun = st.selectbox("Municipio de interés:", ["Soacha", "Bogotá", "Tocancipá", "Girardot"])
            if st.button("Enviar Respuesta"):
                st.session_state.answers["sueño_municipio"] = s_mun
                st.session_state.station = 2
                st.rerun()

        elif st.session_state.station == 2:
            col_in1, col_in2 = st.columns(2)
            ahorros_val = col_in1.number_input("Ahorros Totales (COP):", value=15000000, step=1000000)
            cred_val = col_in2.number_input("Crédito Preaprobado (COP):", value=80000000, step=5000000)
            if st.button("Calcular Cierre y Match"):
                st.session_state.answers["ahorros"] = ahorros_val
                st.session_state.answers["credito_aprobado"] = cred_val
                st.session_state.station = 3
                st.rerun()

# =========================================================================
# LADO DERECHO: CONSOLA CRM Y MOTOR DE MATCHING
# =========================================================================
with col_crm:
    st.markdown('<div class="salesforce-header">📊 Consola del Asesor Comercial (Salesforce)</div>', unsafe_allow_html=True)
    
    st.subheader(f"👤 Prospecto: {active_profile['cotizante']} ({active_profile['categoria']})")
    
    # Cálculos Financieros
    subsidio_caja = 30 * SMMLV_2026 if active_profile["salario_base"] <= 2 * SMMLV_2026 else 20 * SMMLV_2026
    presupuesto_total = st.session_state.answers["ahorros"] + subsidio_caja + st.session_state.answers["credito_aprobado"]
    cuota_maxima = active_profile["salario_base"] * 0.40 # Ley 40%
    
    # Motor de Matching Predictivo (Pandas)
    st.subheader("🎯 Recomendación de Inteligencia Artificial")
    
    if not df.empty:
        # Filtrar el histórico por similitud con el perfil detectado
        match_df = df[(df['CATEGORIA'] == active_profile["excel_categoria"]) & 
                      (df['RANGO_EDAD'] == active_profile["excel_edad"])]
        
        # Si el usuario eligió un municipio, intentamos filtrar por coincidencias de texto
        if st.session_state.answers["sueño_municipio"] != "Bogotá":
             match_df = match_df[match_df['NOMBRE_PROYECTO'].str.contains(st.session_state.answers["sueño_municipio"], case=False, na=False)]
        
        if not match_df.empty:
            # Obtener el proyecto más exitoso para este segmento
            top_proyecto = match_df['NOMBRE_PROYECTO'].value_counts().index[0]
            familias_similares = match_df['NOMBRE_PROYECTO'].value_counts().iloc[0]
            precio_promedio = match_df[match_df['NOMBRE_PROYECTO'] == top_proyecto]['VLR_VIVIENDA_CLEAN'].mean()
            brecha = precio_promedio - presupuesto_total
            
            st.success(f"**Proyecto Recomendado:** {top_proyecto}")
            st.caption(f"💡 *Explicabilidad IA:* Basado en el análisis de datos históricos, **{familias_similares} familias** del segmento '{active_profile['categoria']}' y con ingresos similares han invertido exitosamente en este proyecto.")
            
            # Prioridad de Lead
            if brecha <= 0:
                st.markdown(f"**Calificación del Lead:** <span class='score-badge-high'>Prioridad Alta (🟢 Listo para Cierre)</span>", unsafe_allow_html=True)
                st.write(f"🚀 Presupuesto total (${presupuesto_total:,.0f}) cubre el valor del inmueble (${precio_promedio:,.0f}).")
            else:
                st.markdown(f"**Calificación del Lead:** <span class='score-badge-medium'>Prioridad Media (🟡 Requiere Maduración)</span>", unsafe_allow_html=True)
                st.write(f"⚠️ Brecha financiera de **${brecha:,.0f} COP**. Enrutar a programa PerteneSER (Ahorro Programado).")
                
        else:
            st.warning("No hay suficientes datos históricos para este municipio específico con tu segmento. Sugerimos revisar inventario general.")
    else:
        st.error("Base de datos no conectada. Revisa la ruta del CSV.")

    st.divider()
    
    # Tabla Financiera Transparente
    st.subheader("💰 Resumen Financiero Consolidado")
    fin_data = {
        "Concepto": ["Subsidio Automático (Caja)", "Ahorros Propios", "Crédito Declarado", "Poder Adquisitivo Total"],
        "Valor (COP)": [f"${subsidio_caja:,.0f}", f"${st.session_state.answers['ahorros']:,.0f}", f"${st.session_state.answers['credito_aprobado']:,.0f}", f"${presupuesto_total:,.0f}"]
    }
    st.table(pd.DataFrame(fin_data))

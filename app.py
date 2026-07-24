import streamlit as st
import pandas as pd
import json

# Configuración de página responsive
st.set_page_config(
    page_title="Colsubsidio Vivienda - Motor Inteligente de Matching",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado (WhatsApp / Salesforce)
st.markdown("""
<style>
    .phone-container { background-color: #efeae2; border: 12px solid #333; border-radius: 36px; padding: 20px; height: 650px; overflow-y: auto; }
    .chat-header { background-color: #075e54; color: white; padding: 10px; border-radius: 10px 10px 0 0; margin: -20px -20px 15px -20px; font-weight: bold;}
    .chat-bubble-received { background-color: white; color: #303030; padding: 10px 15px; border-radius: 0 15px 15px 15px; margin-bottom: 10px; max-width: 85%; box-shadow: 0 1px 2px rgba(0,0,0,0.1); }
    .chat-bubble-sent { background-color: #d9fdd3; color: #303030; padding: 10px 15px; border-radius: 15px 0 15px 15px; margin-bottom: 10px; margin-left: auto; max-width: 85%; box-shadow: 0 1px 2px rgba(0,0,0,0.1); text-align: right; }
    .salesforce-container { background-color: #f3f2f1; border: 2px solid #dddbda; border-radius: 8px; padding: 20px; height: 650px; overflow-y: auto; }
    .salesforce-header { background-color: #1589ee; color: white; padding: 12px; border-radius: 6px 6px 0 0; margin: -20px -20px 20px -20px; font-weight: bold; }
    .priority-high { background-color: #3b7a13; color: white; font-weight: bold; padding: 5px 10px; border-radius: 12px; text-align: center; }
</style>
""", unsafe_allow_class=True)

SMMLV_2026 = 1750905

# ---------------- CARGA Y PROCESAMIENTO DE DATOS HISTÓRICOS ----------------
@st.cache_data
def cargar_datos_historicos():
    try:
        # Cargar la primera hoja del Excel
        df = pd.read_excel("hackathon_VIVIENDAv2.xlsx", sheet_name=0)
        # Limpiar el formato de ceros en el valor de la vivienda (ej: 1495000000000 -> 149.500.000)
        df['VLR_VIVIENDA_CLEAN'] = df['VLR_VIVIENDA'] / 10000
        return df
    except Exception as e:
        st.error(f"Error cargando el Excel: {e}. Verifica que 'hackathon_VIVIENDAv2.xlsx' esté en la misma carpeta.")
        return pd.DataFrame()

df_compradores = cargar_datos_historicos()

# ---------------- MOCK DE DATOS Y MATCHING ----------------
AFILIADOS_DB = {
    "10118444": {
        "nombre": "Diana Carolina Rangel",
        "categoria_caja": "Básico (Cat A)",
        "salario": 2100000,
        "ahorro_cesantias": 6500000,
        # Variables para cruzar con el Excel
        "categoria_excel": "OMEGA", 
        "rango_edad": "20 - 35 años",
        "piramide_excel": "RHO"
    },
    "80118445": {
        "nombre": "Jonathan Herrera",
        "categoria_caja": "Medio (Cat B)",
        "salario": 4200000,
        "ahorro_cesantias": 14000000,
        "categoria_excel": "TAU",
        "rango_edad": "36 - 45 años",
        "piramide_excel": "ALPHA"
    }
}

def calcular_match_score(df, categoria, rango_edad, piramide):
    """Calcula la similitud de proyectos basados en compradores históricos similares"""
    if df.empty: return pd.DataFrame()
    
    # Filtrar el histórico por similitud con el usuario actual
    match_df = df[
        (df['CATEGORIA'] == categoria) & 
        (df['RANGO_EDAD'] == rango_edad)
    ]
    
    if match_df.empty:
        # Relajar el filtro si no hay match exacto
        match_df = df[df['CATEGORIA'] == categoria]
        
    # Contar los proyectos más comprados por este segmento
    top_proyectos = match_df['NOMBRE_PROYECTO'].value_counts().reset_index()
    top_proyectos.columns = ['Proyecto', 'Coincidencias']
    
    # Normalizar a un Score sobre 100
    max_coincidencias = top_proyectos['Coincidencias'].max()
    top_proyectos['Match_Score'] = (top_proyectos['Coincidencias'] / max_coincidencias) * 100
    
    # Obtener el precio promedio limpio por proyecto
    precios = match_df.groupby('NOMBRE_PROYECTO')['VLR_VIVIENDA_CLEAN'].mean().reset_index()
    precios.columns = ['Proyecto', 'Precio_Promedio_Historico']
    
    # Unir resultados
    resultados = pd.merge(top_proyectos, precios, on='Proyecto').head(3)
    return resultados

# ---------------- INTERFAZ GRÁFICA ----------------
st.title("💡 Colsubsidio - Motor Inteligente de Matching de Vivienda")

st.sidebar.title("🔐 Simulación de Lead")
id_seleccionado = st.sidebar.selectbox("Selecciona al Afiliado:", list(AFILIADOS_DB.keys()), format_func=lambda x: f"{x} - {AFILIADOS_DB[x]['nombre']}")
afiliado = AFILIADOS_DB[id_seleccionado]

ahorros_adicionales = st.sidebar.slider("Ahorros en el chat ($):", 0, 30000000, 5000000, step=1000000)
total_ahorros = afiliado["ahorro_cesantias"] + ahorros_adicionales

col1, col2 = st.columns([4, 6])

with col1:
    st.markdown("### 📱 Chat Inteligente (Extracción de Datos)")
    chat_html = f"""
    <div class="phone-container">
        <div class="chat-header">💬 Asesor Digital Colsubsidio</div>
        <div class="chat-bubble-received">¡Hola, <strong>{afiliado['nombre']}</strong>! ✨ Qué alegría saludarte. Vemos que estás en la categoría {afiliado['categoria_excel']}. ¿En qué zona te gustaría vivir?</div>
        <div class="chat-bubble-sent">Hola, busco algo cerca a Bogotá. Tengo ahorrados <strong>${ahorros_adicionales:,}</strong> adicionales a mis cesantías.</div>
        <div class="chat-bubble-received">¡Excelente! Ya estoy cruzando tu perfil con cientos de familias como la tuya para encontrar tu proyecto ideal...</div>
    </div>
    """
    st.markdown(chat_html, unsafe_allow_class=True)

with col2:
    st.markdown("### ☁️ Consola Salesforce CRM (Asesor)")
    st.markdown(f'<div class="salesforce-container"><div class="salesforce-header">☁️ LEAD CONSOLE - {afiliado["nombre"].upper()}</div>', unsafe_allow_class=True)
    
    st.write(f"**Segmento Detectado:** {afiliado['categoria_excel']} | **Edad:** {afiliado['rango_edad']} | **Pirámide:** {afiliado['piramide_excel']}")
    st.write(f"💰 **Capacidad Inicial:** ${total_ahorros:,} COP (Ahorros + Cesantías)")
    
    st.divider()
    st.markdown("#### 🎯 Top 3 Proyectos Recomendados (Basado en Histórico de Compradores)")
    
    if not df_compradores.empty:
        matches = calcular_match_score(df_compradores, afiliado['categoria_excel'], afiliado['rango_edad'], afiliado['piramide_excel'])
        
        if not matches.empty:
            for index, row in matches.iterrows():
                score_formateado = f"{row['Match_Score']:.1f}%"
                precio_formateado = f"${int(row['Precio_Promedio_Historico']):,} COP"
                
                st.success(f"**{row['Proyecto']}** - Match: **{score_formateado}** (Precio Histórico: {precio_formateado})")
                st.caption(f"💡 *Por qué lo recomendamos:* {int(row['Coincidencias'])} familias del segmento {afiliado['categoria_excel']} ({afiliado['rango_edad']}) invirtieron exitosamente aquí.")
        else:
            st.warning("No se encontraron coincidencias exactas en la base histórica.")
    else:
        st.error("Base de datos histórica no cargada.")
    
    st.markdown('</div>', unsafe_allow_class=True)

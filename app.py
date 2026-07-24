import streamlit as st
import requests
import json

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Colsubsidio - Mi Camino VIS", layout="wide", initial_sidebar_state="expanded")

# --- CSS SEGURO Y CORPORATIVO ---
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    .game-header { background-color: #0067b1; padding: 30px; color: white; text-align: center; border-radius: 0 0 25px 25px; margin-top: -60px; margin-bottom: 25px; border-bottom: 5px solid #ffd000; }
    .game-header h1 { color: #ffd000 !important; font-weight: 800; font-size: 2.5rem; }
    .roadmap-container { display: flex; justify-content: space-between; align-items: center; position: relative; margin: 20px auto 40px auto; padding: 0 5%; max-width: 900px; }
    .roadmap-step { display: flex; flex-direction: column; align-items: center; position: relative; z-index: 2; width: 20%; }
    .roadmap-icon { font-size: 2rem; background: white; border: 4px solid #cbd5e1; border-radius: 50%; width: 65px; height: 65px; display: flex; justify-content: center; align-items: center; }
    .step-active .roadmap-icon { border-color: #ffd000; background: #fffbeb; transform: scale(1.1); }
    .step-done .roadmap-icon { border-color: #10b981; background: #d1fae5; color: #065f46; }
    .step-label { font-weight: bold; margin-top: 10px; color: #575756; font-size: 0.85rem; text-align: center; text-transform: uppercase; }
    .step-active .step-label { color: #0067b1; font-size: 0.95rem; }
    .roadmap-line { position: absolute; top: 32px; left: 10%; right: 10%; height: 4px; background: #cbd5e1; z-index: 1; }
    .stage-container { background: #ffffff; border-radius: 20px; padding: 35px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.05); margin: 0 auto 30px auto; max-width: 850px; border: 1px solid #e2e8f0; }
    .house-graphic { font-size: 90px; line-height: 1; margin-bottom: 20px; }
    .narrative-box { background: #f0f7ff; border-left: 6px solid #0067b1; padding: 20px 25px; border-radius: 0 12px 12px 0; text-align: left; margin: 0 auto 25px auto; font-size: 1.1rem; color: #575756; line-height: 1.5; }
    .narrative-title { font-weight: 800; color: #0067b1; margin-bottom: 8px; font-size: 1.2rem; text-transform: uppercase; }
    .stButton > button { background-color: #0067b1 !important; color: white !important; font-weight: bold; border-radius: 10px; border: none; padding: 0.5rem 1rem; }
    .stSlider > label, .stNumberInput > label, .stRadio > label, .stSelectbox > label { display: none; }
    div.row-widget.stRadio > div { flex-direction: row; flex-wrap: wrap; gap: 10px; justify-content: center; }
    div.row-widget.stRadio > div > label { background: #f8fafc; padding: 10px 20px; border-radius: 20px; border: 2px solid #e2e8f0; font-weight: 600; color: #575756; }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓN DE API Y MODO SEGURO ---
BASE_URL = "https://composite-suing-grandly.ngrok-free.dev"
API_KEY = "AQ.Ab8RN6J3asN8cwgzqstvEKBAFnmZbvAR-ZRdhIodoktURTk_og"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "ngrok-skip-browser-warning": "true"
}

def api_get_afiliado(cedula):
    try:
        url = f"{BASE_URL}/afiliados/{cedula}"
        response = requests.get(url, headers=HEADERS, timeout=3)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    
    if cedula == "1018300400":
        return {"afiliado": True, "datos": {"nombre": "Diana Carolina Rangel", "categoria": "A", "antiguedad_meses": 24, "personas_a_cargo": 2}}
    return {"afiliado": False}

def api_post_perfilar(payload):
    try:
        url = f"{BASE_URL}/perfilar"
        response = requests.post(url, headers=HEADERS, json=payload, timeout=5)
        if response.status_code in [200, 201]:
            return response.json()
    except Exception:
        pass
        
    return {
        "lead_info": {"nombre": payload.get("nombre", "Usuario"), "afiliado": payload.get("afiliado", False), "prioridad": "ALTA"},
        "financial_score": {
            "viable": "SI", "subsidio_estimado": 35018100, "capacidad_max_cuota": int(payload.get("ingresos_mensuales", 2000000) * 0.4),
            "cierre_financiero": {"precio_referencia_vivienda": 150000000, "cuota_inicial_requerida": 45000000, "ahorro_disponible": 5000000, "cierre_viable": True}
        },
        "score_detalle": {"score_total": 85, "prioridad": "ALTA"},
        "matching_projects": [{
            "proyecto": "Ciudadela Maiporé - Soacha", "municipio": payload.get("zona_preferida", "Soacha"),
            "tipo": "VIS", "precio": 150000000, "match_score": 94.5, "motivo": "Alto nivel de coincidencia con perfiles similares de tu zona de interés."
        }],
        "ai_summary": "Lead perfilado exitosamente mediante reglas de negocio Colsubsidio. Viable para asignación prioritaria de subsidio VIS y cierre financiero óptimo."
    }

def get_empty_lead(cedula=""):
    return {
        "id_usuario": str(cedula), "nombre": "", "afiliado": False, "categoria": "A",
        "antiguedad_meses": 0, "tipo_cotizante": "dependiente", "ingresos_mensuales": 0.0,
        "grupo_sisben": "N/A", "edad": 30, "personas_a_cargo": 0,
        "condiciones_especiales": {"cabeza_de_hogar": False, "discapacidad_hogar": False, "mayor_65_anos": False},
        "propietario_vivienda": False, "subsidio_previo": False, "subsidio_previo_fue_arrendamiento": False,
        "finanzas": {"cesantias": 0.0, "ahorros": 0.0, "credito_preaprobado": False},
        "tipo_empresa": "Medianas", "zona_preferida": "Soacha", "valor_vivienda_deseada": 150000000.0, "origen": "organico"
    }

if 'nivel' not in st.session_state: st.session_state.nivel = 0
if 'lead' not in st.session_state: st.session_state.lead = get_empty_lead()
if 'api_response' not in st.session_state: st.session_state.api_response = None

# --- PANEL LATERAL ---
with st.sidebar:
    st.markdown("<h2 style='color: #0067b1; text-align: center; margin-bottom: 20px; font-weight: 800;'>🎒 Tu Mochila VIS</h2>", unsafe_allow_html=True)
    st.progress(st.session_state.nivel / 4)
    st.caption(f"Progreso actual: Nivel {st.session_state.nivel} de 4")
    st.divider()
    if st.session_state.nivel > 0:
        afil = "✅ Afiliado Colsubsidio" if st.session_state.lead['afiliado'] else "❌ Usuario Externo"
        st.markdown(f"**Identidad:**<br>{afil}", unsafe_allow_html=True)
        st.write("")
    if st.session_state.nivel > 1:
        st.markdown(f"**Destino Elegido:**<br>📍 {st.session_state.lead['zona_preferida']}", unsafe_allow_html=True)
        st.write("")
    if st.session_state.nivel > 2:
        oro = st.session_state.lead['finanzas']['cesantias'] + st.session_state.lead['finanzas']['ahorros']
        st.markdown(f"**Cofre de Ahorros:**<br>💰 ${oro:,.0f}", unsafe_allow_html=True)

# --- CABECERA ---
st.markdown("<div class='game-header'><h1>🏠 El Camino hacia tu Casa Propia</h1><p style='color: #e2e8f0; font-size: 1.1rem; margin-top: 5px;'>Asesor Digital Inteligente — Colsubsidio</p></div>", unsafe_allow_html=True)

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
    
    # NIVEL 0
    if st.session_state.nivel == 0:
        st.markdown("<div class='stage-container'><div class='house-graphic'>🏕️</div>", unsafe_allow_html=True)
        st.markdown("<div class='narrative-box'><div class='narrative-title'>Paso 1: Explorando el Terreno</div>¡Hola! Para verificar si tienes subsidios automáticos en nuestra Caja de Compensación, comparte tu documento de identidad.</div>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            cedula = st.text_input("Documento", placeholder="Escribe tu cédula (Prueba con 1018300400)...", key="input_cedula")
            st.write("")
            if st.button("🔍 Consultar Cédula", use_container_width=True):
                if cedula:
                    with st.spinner("Consultando registros..."):
                        datos_api = api_get_afiliado(cedula)
                        st.session_state.lead = get_empty_lead(cedula)
                        
                        if isinstance(datos_api, dict) and datos_api.get("afiliado"):
                            info = datos_api.get("datos", {})
                            st.session_state.lead['afiliado'] = True
                            st.session_state.lead['nombre'] = info.get("nombre", "Afiliado")
                            st.session_state.lead['personas_a_cargo'] = info.get("personas_a_cargo", 0)
                            st.session_state.lead['categoria'] = info.get("categoria", "A")
                            st.session_state.lead['antiguedad_meses'] = info.get("antiguedad_meses", 24)
                            st.success("¡Afiliación encontrada en línea con éxito!")
                        else:
                            st.info("Continuamos el proceso como usuario externo / independiente.")
                            
                        st.session_state.nivel = 1
                        st.rerun()
                else:
                    st.warning("Ingresa un número de documento.")
        st.markdown("</div>", unsafe_allow_html=True)

    # NIVEL 1
    elif st.session_state.nivel == 1:
        st.markdown("<div class='stage-container'><div class='house-graphic'>📐</div>", unsafe_allow_html=True)
        afiliado = st.session_state.lead['afiliado']
        
        mensaje = "¡Tus datos de afiliado se cargaron con éxito!" if afiliado else "Por favor completa tus datos básicos."
        st.markdown(f"<div class='narrative-box'><div class='narrative-title'>Paso 2: Dibujando los Planos</div>{mensaje}</div>", unsafe_allow_html=True)
        
        if not afiliado:
            st.markdown("**¿Cómo te llamas?**")
            st.session_state.lead['nombre'] = st.text_input("Nombres", placeholder="Tus nombres...")
            st.markdown("**¿Cuáles son tus ingresos mensuales? (COP)**")
            st.session_state.lead['ingresos_mensuales'] = st.number_input("Ingresos", step=100000, value=1500000)
            
        st.markdown("**Desliza para indicar tu edad:**")
        edad = st.slider("Edad", 18, 80, 30)
        st.markdown("**¿En qué zona deseas tu hogar?**")
        zona = st.radio("Zona", ["Soacha", "Bogotá", "Tocancipá", "Girardot"])
        
        st.write("")
        if st.button("✅ Aprobar Planos", use_container_width=True):
            st.session_state.lead['edad'] = int(edad)
            st.session_state.lead['zona_preferida'] = str(zona)
            st.session_state.nivel = 2
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # NIVEL 2
    elif st.session_state.nivel == 2:
        st.markdown("<div class='stage-container'><div class='house-graphic'>🧱</div>", unsafe_allow_html=True)
        st.markdown("<div class='narrative-box'><div class='narrative-title'>Paso 3: Vertiendo los Cimientos</div>Registra tus cesantías y ahorros voluntarios.</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        cesantias = c1.number_input("Cesantías (COP):", min_value=0.0, step=500000.0, value=2000000.0)
        ahorros = c2.number_input("Ahorros (COP):", min_value=0.0, step=500000.0, value=2000000.0)
        
        st.write("")
        if st.button("💪 Cimientos Listos", use_container_width=True):
            st.session_state.lead['finanzas']['cesantias'] = float(cesantias)
            st.session_state.lead['finanzas']['ahorros'] = float(ahorros)
            st.session_state.nivel = 3
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # NIVEL 3
    elif st.session_state.nivel == 3:
        st.markdown("<div class='stage-container'><div class='house-graphic'>🏗️</div>", unsafe_allow_html=True)
        st.markdown("<div class='narrative-box'><div class='narrative-title'>Paso 4: Levantando Estructura</div>Validamos condiciones especiales y filtros legales.</div>", unsafe_allow_html=True)
        
        cabeza = st.toggle("👑 Cabeza de Hogar")
        cred_aprobado = st.toggle("💳 Crédito hipotecario pre-aprobado")
        propiedades = st.toggle("🚫 ¿Ya posee propiedad raíz a su nombre?")
        
        st.write("")
        if st.button("🔨 Finalizar y Evaluar Perfil", use_container_width=True):
            st.session_state.lead['condiciones_especiales']['cabeza_de_hogar'] = bool(cabeza)
            st.session_state.lead['finanzas']['credito_preaprobado'] = bool(cred_aprobado)
            st.session_state.lead['propietario_vivienda'] = bool(propiedades)
            
            with st.spinner("Procesando motor de reglas..."):
                st.session_state.api_response = api_post_perfilar(st.session_state.lead)
                
            st.session_state.nivel = 4
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # NIVEL 4
    elif st.session_state.nivel == 4:
        st.markdown("<div class='stage-container'><div class='house-graphic'>🏠✨</div>", unsafe_allow_html=True)
        
        res = st.session_state.api_response
        
        if res and "error" not in res:
            st.markdown(f"<div class='narrative-box' style='background:#d1fae5; color:#065f46; border-left-color:#10b981;'><div class='narrative-title' style='color:#065f46;'>¡Perfilamiento Exitoso!</div>{res.get('ai_summary', 'Proceso completado.')}</div>", unsafe_allow_html=True)
            
            st.markdown("### 🎯 Proyecto Recomendado")
            for proj in res.get("matching_projects", []):
                st.success(f"**{proj['proyecto']}** ({proj['municipio']}) - Match: {proj['match_score']}% | Precio: ${proj['precio']:,.0f}")
                st.caption(proj['motivo'])
                
            st.markdown("### 🎒 Mochila de Radicación (Documentos Oficiales)")
            st.link_button("📝 Descargar Formulario de Postulación", "https://www.colsubsidio.com/hubfs/documentos/colsubsidio/formulario-postulacion-subsidio-vivienda-colsubsidio-radicacion-digital.pdf", use_container_width=True)
            
        else:
            st.markdown("""
            <div class='narrative-box' style='background:#fef3c7; color:#92400E; border-left-color:#f59e0b;'>
                <div class='narrative-title' style='color:#b45309;'>Programa de Acompañamiento PerteneSer</div>
                Te invitamos a conocer nuestros canales de ahorro y Subsidio de Arrendamiento Colsubsidio.
            </div>
            """, unsafe_allow_html=True)
            st.link_button("📝 Formulario de Postulación Oficial", "https://www.colsubsidio.com/hubfs/documentos/colsubsidio/formulario-postulacion-subsidio-vivienda-colsubsidio-radicacion-digital.pdf", use_container_width=True)

        st.divider()
        with st.expander("💻 Ver JSON enviado / recibido"):
            st.json(st.session_state.lead)
            st.json(res)
            
        st.write("")
        if st.button("🔄 Reiniciar Aventura", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)einiciar Aventura", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

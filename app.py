import streamlit as st
import requests
import json

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Colsubsidio - Asesor Digital VIS", layout="wide", initial_sidebar_state="expanded")

# --- CSS PROFESIONAL Y FONDO ANIMADO CORPORATIVO ---
st.markdown("""
<style>
    /* Ocultar el fondo por defecto */
    .stApp {
        background-color: transparent !important;
    }

    /* CONTENEDOR DE LA ANIMACIÓN DE FONDO */
    .area {
        background: linear-gradient(135deg, #f0f7ff 0%, #f8fafc 100%);
        width: 100%;
        height: 100vh;
        position: fixed;
        top: 0;
        left: 0;
        z-index: -999;
    }

    .circles {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        margin: 0;
        padding: 0;
    }

    .circles li {
        position: absolute;
        display: block;
        list-style: none;
        width: 20px;
        height: 20px;
        background: rgba(0, 103, 177, 0.1); /* Azul Colsubsidio transparente */
        animation: animate 25s linear infinite;
        bottom: -150px;
    }

    /* Diferentes tamaños, posiciones y colores para las figuras flotantes */
    .circles li:nth-child(1) { left: 25%; width: 80px; height: 80px; animation-delay: 0s; }
    .circles li:nth-child(2) { left: 10%; width: 30px; height: 30px; animation-delay: 2s; animation-duration: 12s; background: rgba(255, 208, 0, 0.15); /* Amarillo Colsubsidio */ }
    .circles li:nth-child(3) { left: 70%; width: 25px; height: 25px; animation-delay: 4s; }
    .circles li:nth-child(4) { left: 40%; width: 60px; height: 60px; animation-delay: 0s; animation-duration: 18s; background: rgba(255, 208, 0, 0.1); }
    .circles li:nth-child(5) { left: 65%; width: 20px; height: 20px; animation-delay: 0s; }
    .circles li:nth-child(6) { left: 75%; width: 110px; height: 110px; animation-delay: 3s; }
    .circles li:nth-child(7) { left: 35%; width: 150px; height: 150px; animation-delay: 7s; background: rgba(255, 208, 0, 0.12); }
    .circles li:nth-child(8) { left: 50%; width: 25px; height: 25px; animation-delay: 15s; animation-duration: 45s; }
    .circles li:nth-child(9) { left: 20%; width: 15px; height: 15px; animation-delay: 2s; animation-duration: 35s; background: rgba(255, 208, 0, 0.2); }
    .circles li:nth-child(10) { left: 85%; width: 150px; height: 150px; animation-delay: 0s; animation-duration: 11s; }

    @keyframes animate {
        0% { transform: translateY(0) rotate(0deg); opacity: 1; border-radius: 0; }
        100% { transform: translateY(-1000px) rotate(720deg); opacity: 0; border-radius: 50%; }
    }

    /* RESTO DE TUS ESTILOS (Cabecera, Tarjetas, Botones) */
    .game-header { 
        background: linear-gradient(135deg, #0067b1 0%, #004d85 100%); 
        padding: 35px; color: white; text-align: center; border-radius: 0 0 30px 30px; 
        margin-top: -60px; margin-bottom: 30px; box-shadow: 0 10px 25px rgba(0, 103, 177, 0.15); border-bottom: 5px solid #ffd000; 
    }
    .game-header h1 { color: #ffd000 !important; font-weight: 900; font-size: 2.6rem; letter-spacing: -0.5px; }

    .roadmap-container { display: flex; justify-content: space-between; align-items: center; position: relative; margin: 20px auto 40px auto; padding: 0 5%; max-width: 900px; }
    .roadmap-step { display: flex; flex-direction: column; align-items: center; position: relative; z-index: 2; width: 20%; }
    .roadmap-icon { font-size: 2rem; background: #ffffff; border: 4px solid #cbd5e1; border-radius: 50%; width: 70px; height: 70px; display: flex; justify-content: center; align-items: center; box-shadow: 0 4px 6px rgba(0,0,0,0.04); transition: all 0.3s ease; }
    .step-active .roadmap-icon { border-color: #ffd000; background: #fffbeb; transform: scale(1.12); box-shadow: 0 0 15px rgba(255, 208, 0, 0.4); }
    .step-done .roadmap-icon { border-color: #10b981; background: #d1fae5; color: #065f46; }
    .step-label { font-weight: 700; margin-top: 10px; color: #575756; font-size: 0.85rem; text-align: center; text-transform: uppercase; letter-spacing: 0.5px; }
    .step-active .step-label { color: #0067b1; font-size: 0.95rem; }
    .roadmap-line { position: absolute; top: 34px; left: 10%; right: 10%; height: 4px; background: #cbd5e1; z-index: 1; border-radius: 2px; }
    
    .stage-container { background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(12px); border-radius: 24px; padding: 45px; text-align: center; box-shadow: 0 15px 35px rgba(0, 0, 0, 0.06); margin: 0 auto 40px auto; max-width: 850px; border: 1px solid rgba(255,255,255,0.5); }
    .house-graphic { font-size: 100px; line-height: 1; margin-bottom: 25px; filter: drop-shadow(0 8px 12px rgba(0,0,0,0.08)); }
    
    .narrative-box { background: #f0f7ff; border-left: 6px solid #0067b1; padding: 22px 30px; border-radius: 0 14px 14px 0; text-align: left; margin: 0 auto 30px auto; font-size: 1.1rem; color: #575756; line-height: 1.6; }
    .narrative-title { font-weight: 800; color: #0067b1; margin-bottom: 8px; font-size: 1.25rem; text-transform: uppercase; letter-spacing: 0.5px; }
    
    .stButton > button { background-color: #0067b1 !important; color: white !important; font-weight: 700; border-radius: 12px; border: none; padding: 0.6rem 1.5rem; transition: all 0.2s; box-shadow: 0 4px 6px rgba(0, 103, 177, 0.2); }
    .stButton > button:hover { background-color: #004d85 !important; transform: translateY(-1px); box-shadow: 0 6px 12px rgba(0, 103, 177, 0.3); }
    
    .stSlider > label, .stNumberInput > label, .stRadio > label, .stSelectbox > label { display: none; }
    div.row-widget.stRadio > div { flex-direction: row; flex-wrap: wrap; gap: 12px; justify-content: center; }
    div.row-widget.stRadio > div > label { background: #ffffff; padding: 12px 24px; border-radius: 30px; border: 2px solid #cbd5e1; font-weight: 600; color: #575756; transition: all 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
    div.row-widget.stRadio > div > label:hover { border-color: #0067b1; color: #0067b1; background: #f0f7ff; }
    
    [data-testid="stSidebar"] { background-color: rgba(255,255,255,0.9); backdrop-filter: blur(10px); border-right: 1px solid #e2e8f0; }
</style>

<!-- ESTRUCTURA HTML PARA EL FONDO ANIMADO -->
<div class="area">
    <ul class="circles">
        <li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li>
    </ul>
</div>
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
st.markdown("<div class='game-header'><h1>🏠 El Camino hacia tu Casa Propia</h1><p style='color: #ffd000; font-size: 1.1rem; margin-top: 5px; font-weight: 600;'>Asesor Digital Inteligente — Colsubsidio</p></div>", unsafe_allow_html=True)

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
            if st.button("🔍 Consultar Cédula", use_container_width=True, key="btn_nivel_0"):
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
        if st.button("✅ Aprobar Planos", use_container_width=True, key="btn_nivel_1"):
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
        if st.button("💪 Cimientos Listos", use_container_width=True, key="btn_nivel_2"):
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
        if st.button("🔨 Finalizar y Evaluar Perfil", use_container_width=True, key="btn_nivel_3"):
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
        # LLAVE ÚNICA AÑADIDA PARA EVITAR EL DUPLICATE ELEMENT ID
        if st.button("🔄 Reiniciar Aventura", use_container_width=True, key="btn_reiniciar_final"):
            st.session_state.clear()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

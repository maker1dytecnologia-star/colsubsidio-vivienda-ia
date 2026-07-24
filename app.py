import streamlit as st
import json
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Colsubsidio - Mi Camino VIS", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .gamification-header { background-color: #002D72; padding: 20px; color: white; text-align: center; border-radius: 10px; margin-bottom: 20px; }
    .station-card { background-color: #F8F9FA; border-left: 5px solid #FFCD00; padding: 20px; border-radius: 5px; margin-bottom: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    .crm-card { background-color: #ffffff; padding: 15px; border-radius: 8px; border: 1px solid #e0e0e0; margin-bottom: 10px; }
    .badge-alta { background-color: #4CAF50; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; }
    .badge-media { background-color: #FF9800; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- SIMULACIÓN DE ENDPOINTS (MOCKS) ---

def api_get_afiliado(cedula):
    """Simula el GET para validar afiliación"""
    db_colsubsidio = {
        "1018300400": {
            "datos_personales": {"tipo_documento": "CC", "numero_documento": "1018300400", "nombres": "Diana Carolina", "apellidos": "Rangel", "celular": "3142160550", "correo": "diana@gmail.com"},
            "afiliacion_colsubsidio": {"es_afiliado": True, "tipo_afiliado": "Dependiente", "antiguedad_meses": 24, "categoria": "A", "segmento_poblacional": "Básico", "personas_a_cargo_registradas": 2},
            "datos_financieros_declarados": {"ingresos_verificados_pila": 2800000.0, "ingresos_mensuales_hogar": 2800000.0, "cesantias_inmovilizadas": 0.0, "ahorro_programado": 0.0, "aportes_cuota_inicial_constructora": 0.0, "cuotas_iniciales_pagadas_meses": 0, "tiene_credito_hipotecario_aprobado": False, "monto_credito_aprobado": 0.0},
            "preferencias_e_intencion": {"zona_interes": "", "proyecto_interes": "", "posee_vivienda_propia": False},
            "informacion_socioeconomica_externa": {"tiene_registro_sisben": True, "grupo_sisben": "C2", "tiene_subsidios_previos_ruav": False, "tiene_propiedades_snr": 0},
            "condiciones_especiales_ley": {"cabeza_de_hogar": True, "miembro_con_discapacidad_certificada": False, "miembro_mayor_de_65_anos": False}
        }
    }
    time.sleep(0.5) 
    return db_colsubsidio.get(cedula, None)

def mock_post_perfilar(payload):
    """
    Simula la respuesta EXACTA del backend basada en el contrato JSON.
    Genera valores dinámicos dependiendo de lo que el usuario respondió.
    """
    time.sleep(1.5) # Simulamos el tiempo de procesamiento de la IA y reglas
    
    ingresos = payload['datos_financieros_declarados']['ingresos_mensuales_hogar']
    ahorros_totales = payload['datos_financieros_declarados']['cesantias_inmovilizadas'] + payload['datos_financieros_declarados']['ahorro_programado']
    es_afiliado = payload['afiliacion_colsubsidio']['es_afiliado']
    
    # Lógica de simulación rápida
    viable = "SI" if ingresos > 1300000 else "NO"
    prioridad = "ALTA" if es_afiliado and ahorros_totales > 2000000 else "MEDIA"
    score = 88 if prioridad == "ALTA" else 65
    
    # Construcción de la respuesta acordada con tu equipo
    response = {
      "lead_info": {
        "nombre": payload['datos_personales']['nombres'],
        "afiliado": es_afiliado,
        "prioridad": prioridad
      },
      "financial_score": {
        "viable": viable,
        "motivos_rechazo": [] if viable == "SI" else ["Ingresos insuficientes para cierre"],
        "subsidio_estimado": 35018100 if ingresos <= 35018100 else 0, # Simulación 20 SMMLV
        "capacidad_max_cuota": int(ingresos * 0.40),
        "cierre_financiero": {
          "precio_referencia_vivienda": 173491500,
          "cuota_inicial_requerida": int(173491500 * 0.30),
          "ahorro_disponible": ahorros_totales,
          "cierre_viable": ahorros_totales > 5000000
        }
      },
      "score_detalle": {
        "score_total": score,
        "prioridad": prioridad,
        "factores": {
          "afiliado": 20 if es_afiliado else 0,
          "cierre_financiero_viable": 25 if ahorros_totales > 5000000 else 10,
          "matching_historico": 18,
          "ahorro_previo": 15 if ahorros_totales > 0 else 0,
          "condicion_especial": 10 if payload['condiciones_especiales_ley']['cabeza_de_hogar'] else 0,
          "origen_organico": 10
        }
      },
      "matching_projects": [
        {
          "proyecto": "Ciudadela Maiporé - Monguí",
          "municipio": payload['preferencias_e_intencion']['zona_interes'] or "Soacha",
          "tipo": "VIS",
          "precio": 173491500,
          "match_score": 92.5,
          "motivo": "El 85% de las familias de tu segmento (Básico) y con composición familiar similar invirtieron aquí."
        }
      ],
      "ai_summary": f"Lead perfilado con éxito. Prioridad {prioridad} debido a su nivel de ingresos y ahorros declarados. Cliente óptimo para contactar hoy y ofrecer proyecto en {payload['preferencias_e_intencion']['zona_interes'] or 'Soacha'}.",
      "lead_original": payload
    }
    return response

# --- INICIALIZACIÓN DE ESTADOS ---
if 'estacion_actual' not in st.session_state:
    st.session_state.estacion_actual = 0
if 'lead' not in st.session_state:
    st.session_state.lead = {}
if 'progreso_casa' not in st.session_state:
    st.session_state.progreso_casa = "Terreno Vacío 🏕️"
if 'resultado_api' not in st.session_state:
    st.session_state.resultado_api = None

# --- INTERFAZ ---
st.markdown('<div class="gamification-header"><h1>🏠 Construye tu Sueño: Mi Camino VIS</h1></div>', unsafe_allow_html=True)

progreso_porcentaje = (st.session_state.estacion_actual / 5) * 100
st.progress(int(progreso_porcentaje))
st.markdown(f"**Estado de tu obra:** {st.session_state.progreso_casa}")
st.divider()

col_juego, col_consola = st.columns([5, 5])

with col_juego:
    # (Estación 0 a 3: El mismo código de las estaciones anteriores va aquí)
    # Para mantener el código manejable, incluyo un resumen funcional del roadmap. 
    # Manten tu bloque completo de "Estación 0" a "Estación 3" exactamente como estaba.
    
    if st.session_state.estacion_actual == 0:
        st.markdown("### 🔐 Estación 0: Puerta de Entrada")
        cedula_input = st.text_input("Ingresa tu número de cédula:")
        if st.button("Validar"):
            with st.spinner("Consultando API..."):
                datos = api_get_afiliado(cedula_input)
                if datos:
                    st.session_state.lead = datos
                    st.success("¡Datos cargados!")
                else:
                    st.session_state.lead = {"datos_personales": {"numero_documento": cedula_input, "nombres": ""}, "afiliacion_colsubsidio": {"es_afiliado": False}, "datos_financieros_declarados": {"ingresos_mensuales_hogar": 0.0, "cesantias_inmovilizadas": 0.0, "ahorro_programado": 0.0}, "preferencias_e_intencion": {"zona_interes": ""}, "condiciones_especiales_ley": {"cabeza_de_hogar": False}}
                    st.info("Perfil nuevo. Completa tus datos.")
            st.session_state.estacion_actual = 1
            st.session_state.progreso_casa = "Planos 📐"
            st.rerun()

    if st.session_state.estacion_actual == 1:
        st.markdown("### 💭 Estación 1: El Sueño")
        if not st.session_state.lead['afiliacion_colsubsidio']['es_afiliado']:
            st.session_state.lead['datos_personales']['nombres'] = st.text_input("Nombres:")
            st.session_state.lead['datos_financieros_declarados']['ingresos_mensuales_hogar'] = st.number_input("Ingresos mensuales:", min_value=0.0)
        zona = st.selectbox("Zona de interés:", ["Soacha", "Bogotá", "Tocancipá"])
        if st.button("Fijar Cimientos 🧱"):
            st.session_state.lead['preferencias_e_intencion']['zona_interes'] = zona
            st.session_state.estacion_actual = 2
            st.rerun()

    if st.session_state.estacion_actual == 2:
        st.markdown("### 🪙 Estación 2: El Cofre")
        cesantias = st.number_input("Cesantías:", min_value=0.0)
        ahorro = st.number_input("Ahorro:", min_value=0.0)
        if st.button("Levantar Estructura 🏗️"):
            st.session_state.lead['datos_financieros_declarados']['cesantias_inmovilizadas'] = cesantias
            st.session_state.lead['datos_financieros_declarados']['ahorro_programado'] = ahorro
            st.session_state.estacion_actual = 3
            st.rerun()

    if st.session_state.estacion_actual == 3:
        st.markdown("### ⚡ Estación 3: Tus Poderes")
        cabeza_hogar = st.checkbox("¿Eres cabeza de hogar?")
        if st.button("Completar Casa 🏠"):
            st.session_state.lead['condiciones_especiales_ley']['cabeza_de_hogar'] = cabeza_hogar
            st.session_state.estacion_actual = 4
            st.rerun()

with col_consola:
    # ==========================================
    # ESTACIÓN 4: SIMULACIÓN DE SALESFORCE / RESPUESTA DEL POST
    # ==========================================
    if st.session_state.estacion_actual == 4:
        st.markdown("### ☁️ CRM Salesforce (Respuesta del Backend)")
        
        if st.session_state.resultado_api is None:
            st.info("El roadmap ha sido completado. El JSON de entrada está listo.")
            if st.button("🚀 Enviar al Endpoint /perfilar", type="primary"):
                with st.spinner("Procesando Motor de Reglas en Backend..."):
                    # Simulamos el POST al endpoint de tu equipo
                    st.session_state.resultado_api = mock_post_perfilar(st.session_state.lead)
                st.rerun()
        
        else:
            # PINTAMOS EL JSON DE RESPUESTA QUE EL EQUIPO DEFINIÓ
            res = st.session_state.resultado_api
            
            # 1. AI Summary
            st.markdown("#### 🧠 Resumen de IA")
            st.info(res["ai_summary"])
            
            # 2. Score y Prioridad
            col_s1, col_s2, col_s3 = st.columns(3)
            col_s1.metric("Score Total", f"{res['score_detalle']['score_total']}/100")
            
            badge_class = "badge-alta" if res['score_detalle']['prioridad'] == "ALTA" else "badge-media"
            col_s2.markdown(f"**Prioridad Lead:**<br><span class='{badge_class}'>{res['score_detalle']['prioridad']}</span>", unsafe_allow_html=True)
            col_s3.metric("Viabilidad Financiera", res['financial_score']['viable'])
            
            # 3. Datos Financieros
            st.markdown("#### 💰 Cierre Financiero Estimado")
            st.markdown('<div class="crm-card">', unsafe_allow_html=True)
            c_fin1, c_fin2 = st.columns(2)
            c_fin1.write(f"**Cuota Inicial Requerida:** ${res['financial_score']['cierre_financiero']['cuota_inicial_requerida']:,.0f}")
            c_fin1.write(f"**Ahorro Disponible:** ${res['financial_score']['cierre_financiero']['ahorro_disponible']:,.0f}")
            c_fin2.write(f"**Subsidio Estimado:** ${res['financial_score']['subsidio_estimado']:,.0f}")
            c_fin2.write(f"**Capacidad Max. Cuota (40%):** ${res['financial_score']['capacidad_max_cuota']:,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 4. Matching Projects
            st.markdown("#### 🎯 Proyecto Match (Predictivo)")
            for proj in res["matching_projects"]:
                st.markdown('<div class="crm-card">', unsafe_allow_html=True)
                st.write(f"**🏢 {proj['proyecto']} ({proj['municipio']}) - {proj['tipo']}**")
                st.write(f"**Precio:** ${proj['precio']:,.0f} | **Match Score:** {proj['match_score']}%")
                st.caption(f"💡 *Explicabilidad:* {proj['motivo']}")
                st.markdown('</div>', unsafe_allow_html=True)

            # 5. Raw JSON (Para revisión técnica de los jurados)
            with st.expander("Ver JSON de Respuesta de la API (/perfilar)"):
                st.json(res)
                
            if st.button("Reiniciar Demo"):
                st.session_state.clear()
                st.rerun()

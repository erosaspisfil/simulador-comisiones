import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Configuración de página
st.set_page_config(
    page_title="Comparador de Esquemas de Comisiones",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    }
    
    .main-header h1 {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .main-header p {
        color: #a0aec0;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        text-align: center;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        color: #64748b;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .actual { color: #818cf8; }
    .nuevo { color: #34d399; }
    .diferencia-positiva { color: #22c55e; }
    .diferencia-negativa { color: #f43f5e; }
    
    .info-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-left: 4px solid #0ea5e9;
        padding: 1.2rem 1.5rem;
        border-radius: 0 12px 12px 0;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        padding: 1.2rem 1.5rem;
        border-radius: 0 12px 12px 0;
        margin: 1rem 0;
    }
    
    .success-box {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 4px solid #10b981;
        padding: 1.2rem 1.5rem;
        border-radius: 0 12px 12px 0;
        margin: 1rem 0;
    }
    
    .danger-box {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 4px solid #ef4444;
        padding: 1.2rem 1.5rem;
        border-radius: 0 12px 12px 0;
        margin: 1rem 0;
    }
    
    .zone-indicator {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    .zone-red { background: #fee2e2; color: #dc2626; }
    .zone-yellow { background: #fef3c7; color: #d97706; }
    .zone-green { background: #d1fae5; color: #059669; }
    .zone-blue { background: #dbeafe; color: #2563eb; }
    
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Función para obtener el porcentaje de pago según la tabla oficial
def obtener_porcentaje_pago(efectividad):
    """
    Retorna el porcentaje de pago según la tabla de equivalencias oficial.
    
    Rangos:
    - Menos de 80%: 0%
    - 80% a 95%: 71.5% + (efectividad - 80) * 1.5
    - 96% a 99%: incremento de 1% por cada 1%
    - 100%: 100%
    - 101% a 114%: 100% + (efectividad - 100) * 2
    - 115% o más: 130% (límite máximo)
    """
    if efectividad < 80:
        return 0
    elif efectividad >= 115:
        return 130
    elif efectividad == 100:
        return 100
    elif efectividad > 100:
        # Entre 101% y 114%: cada 1% adicional = 2% más de pago
        return 100 + (efectividad - 100) * 2
    elif efectividad >= 96:
        # Entre 95% y 99%: incremento de 1% por cada 1%
        # 96% = 95%, 97% = 96%, 98% = 97%, 99% = 98%
        return efectividad - 1
    else:
        # Entre 80% y 95%: 71.5% + 1.5% por cada 1% adicional
        return 71.5 + (efectividad - 80) * 1.5

# Función para calcular sueldo esquema actual
def calcular_sueldo_actual(sueldo_fijo, sueldo_variable, efectividad):
    variable_ajustado = sueldo_variable * (efectividad / 100)
    return sueldo_fijo + variable_ajustado

# Función para calcular sueldo esquema nuevo
def calcular_sueldo_nuevo(sueldo_fijo, sueldo_variable, efectividad):
    porcentaje_pago = obtener_porcentaje_pago(efectividad)
    return sueldo_fijo + (sueldo_variable * porcentaje_pago / 100)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>📊 Comparador de Esquemas de Comisiones</h1>
    <p>Visualiza cómo el nuevo esquema de compensación puede beneficiarte según tu desempeño</p>
</div>
""", unsafe_allow_html=True)

# Sidebar con parámetros
with st.sidebar:
    st.markdown("### ⚙️ Configuración del Vendedor")
    st.markdown("---")
    
    sueldo_fijo = st.number_input(
        "💵 Sueldo Fijo (S/)", 
        min_value=0, 
        value=3100, 
        step=100,
        help="Tu sueldo base mensual fijo"
    )
    
    sueldo_variable = st.number_input(
        "📈 Sueldo Variable (S/)", 
        min_value=0, 
        value=3000, 
        step=100,
        help="Tu sueldo variable al 100% de cumplimiento"
    )
    
    st.markdown("---")
    
    total_al_100 = sueldo_fijo + sueldo_variable
    
    st.markdown(f"""
    <div class="info-box">
        <strong>📋 Resumen de Compensación</strong><br>
        <small>
        • Sueldo Fijo: <b>S/ {sueldo_fijo:,}</b><br>
        • Sueldo Variable (100%): <b>S/ {sueldo_variable:,}</b><br>
        • <strong>Total al 100%: S/ {total_al_100:,}</strong>
        </small>
    </div>
    """, unsafe_allow_html=True)

# Contenido principal
st.markdown("### 🎯 Simula tu Efectividad de Ventas")

# Inicializar session_state solo si no existe
if 'init' not in st.session_state:
    st.session_state.init = True
    st.session_state.cuota_val = 100000
    st.session_state.venta_val = 100000
    st.session_state.efect_val = 100

# Sección colapsable para inputs detallados
with st.expander("📝 **Editar Cuota y Venta manualmente**", expanded=False):
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        nueva_cuota = st.number_input(
            "📊 Cuota Mensual (S/)",
            min_value=1,
            value=st.session_state.cuota_val,
            step=5000,
            help="Tu meta de ventas mensual"
        )
        if nueva_cuota != st.session_state.cuota_val:
            st.session_state.cuota_val = nueva_cuota
            # Recalcular efectividad
            st.session_state.efect_val = min(max(int((st.session_state.venta_val / nueva_cuota) * 100), 0), 150)
            st.rerun()
    
    with col_input2:
        nueva_venta = st.number_input(
            "💰 Venta Proyectada (S/)",
            min_value=0,
            value=st.session_state.venta_val,
            step=5000,
            help="Tu venta estimada o real del mes"
        )
        if nueva_venta != st.session_state.venta_val:
            st.session_state.venta_val = nueva_venta
            # Recalcular efectividad
            st.session_state.efect_val = min(max(int((nueva_venta / st.session_state.cuota_val) * 100), 0), 150)
            st.rerun()

# Slider para ajustar efectividad rápidamente
st.markdown("##### 🎚️ Ajuste rápido de efectividad")
nueva_efect = st.slider(
    "Desliza para simular diferentes escenarios",
    min_value=0,
    max_value=150,
    value=st.session_state.efect_val,
    step=1,
    format="%d%%",
    help="Mueve el slider para ver cómo cambia tu sueldo"
)

# Si el slider cambió, actualizar venta
if nueva_efect != st.session_state.efect_val:
    st.session_state.efect_val = nueva_efect
    st.session_state.venta_val = int((nueva_efect / 100) * st.session_state.cuota_val)
    st.rerun()

# Obtener valores actuales para mostrar
cuota = st.session_state.cuota_val
venta = st.session_state.venta_val
efectividad = st.session_state.efect_val

# Mostrar valores actualizados en tarjetas compactas
col_c, col_v, col_e = st.columns(3)

with col_c:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); 
                padding: 16px; border-radius: 12px; text-align: center; 
                border: 1px solid #e2e8f0;">
        <div style="font-size: 0.75rem; color: #64748b; font-weight: 500; margin-bottom: 4px;">📊 Cuota Mensual</div>
        <div style="font-size: 1.4rem; font-weight: 700; color: #334155;">S/ {cuota:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col_v:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); 
                padding: 16px; border-radius: 12px; text-align: center; 
                border: 1px solid #e2e8f0;">
        <div style="font-size: 0.75rem; color: #64748b; font-weight: 500; margin-bottom: 4px;">💰 Venta Proyectada</div>
        <div style="font-size: 1.4rem; font-weight: 700; color: #334155;">S/ {venta:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col_e:
    # Color del borde según la zona
    if efectividad < 80:
        border_color = "#fda4af"
        bg_gradient = "linear-gradient(135deg, #fff1f2 0%, #ffe4e6 100%)"
        text_color = "#be123c"
    elif efectividad < 100:
        border_color = "#fde047"
        bg_gradient = "linear-gradient(135deg, #fefce8 0%, #fef9c3 100%)"
        text_color = "#a16207"
    elif efectividad < 115:
        border_color = "#86efac"
        bg_gradient = "linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)"
        text_color = "#15803d"
    else:
        border_color = "#7dd3fc"
        bg_gradient = "linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)"
        text_color = "#0369a1"
    
    st.markdown(f"""
    <div style="background: {bg_gradient}; 
                padding: 16px; border-radius: 12px; text-align: center; 
                border: 2px solid {border_color};">
        <div style="font-size: 0.75rem; color: #64748b; font-weight: 500; margin-bottom: 4px;">📈 % Efectividad</div>
        <div style="font-size: 1.4rem; font-weight: 800; color: {text_color};">{efectividad}%</div>
    </div>
    """, unsafe_allow_html=True)

# Barra visual de progreso con zonas
st.markdown(f"""
<div style="margin: 15px 0 25px 0;">
    <div style="position: relative; padding-top: 40px;">
        <div style="position: absolute; left: {min((efectividad / 150) * 100, 100)}%; transform: translateX(-50%); top: 0; text-align: center;">
            <div style="background: #475569; color: white; padding: 5px 14px; border-radius: 8px; font-size: 0.85rem; font-weight: 700; white-space: nowrap; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">TÚ: {efectividad}%</div>
            <div style="width: 0; height: 0; border-left: 10px solid transparent; border-right: 10px solid transparent; border-top: 10px solid #475569; margin: 0 auto;"></div>
        </div>
        <div style="height: 24px; border-radius: 12px; display: flex; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid #e2e8f0;">
            <div style="background: linear-gradient(180deg, #fecdd3 0%, #fda4af 100%); flex: 80;"></div>
            <div style="background: linear-gradient(180deg, #fef08a 0%, #fde047 100%); flex: 20;"></div>
            <div style="background: linear-gradient(180deg, #bbf7d0 0%, #86efac 100%); flex: 15;"></div>
            <div style="background: linear-gradient(180deg, #bae6fd 0%, #7dd3fc 100%); flex: 35;"></div>
        </div>
        <div style="position: relative; height: 28px; margin-top: 6px;">
            <div style="position: absolute; left: 0%; transform: translateX(-50%); text-align: center;">
                <div style="width: 2px; height: 12px; background: #94a3b8; margin: 0 auto;"></div>
                <div style="font-size: 0.8rem; color: #64748b; font-weight: 600;">0%</div>
            </div>
            <div style="position: absolute; left: 53.33%; transform: translateX(-50%); text-align: center;">
                <div style="width: 2px; height: 12px; background: #be123c; margin: 0 auto;"></div>
                <div style="font-size: 0.8rem; color: #be123c; font-weight: 700;">80%</div>
            </div>
            <div style="position: absolute; left: 66.67%; transform: translateX(-50%); text-align: center;">
                <div style="width: 2px; height: 12px; background: #a16207; margin: 0 auto;"></div>
                <div style="font-size: 0.8rem; color: #a16207; font-weight: 700;">100%</div>
            </div>
            <div style="position: absolute; left: 76.67%; transform: translateX(-50%); text-align: center;">
                <div style="width: 2px; height: 12px; background: #15803d; margin: 0 auto;"></div>
                <div style="font-size: 0.8rem; color: #15803d; font-weight: 700;">115%</div>
            </div>
            <div style="position: absolute; left: 100%; transform: translateX(-50%); text-align: center;">
                <div style="width: 2px; height: 12px; background: #94a3b8; margin: 0 auto;"></div>
                <div style="font-size: 0.8rem; color: #64748b; font-weight: 600;">150%</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Leyenda de zonas
col_z1, col_z2, col_z3, col_z4 = st.columns(4)
with col_z1:
    st.markdown('<div style="display:flex;align-items:center;gap:8px;"><div style="width:18px;height:18px;background:linear-gradient(180deg,#fecdd3,#fda4af);border-radius:5px;border:1px solid #f9a8d4;"></div><span style="font-size:0.8rem;color:#64748b;font-weight:500;">Crítica (&lt;80%)</span></div>', unsafe_allow_html=True)
with col_z2:
    st.markdown('<div style="display:flex;align-items:center;gap:8px;"><div style="width:18px;height:18px;background:linear-gradient(180deg,#fef08a,#fde047);border-radius:5px;border:1px solid #fde047;"></div><span style="font-size:0.8rem;color:#64748b;font-weight:500;">Recuperación (80-&lt;100%)</span></div>', unsafe_allow_html=True)
with col_z3:
    st.markdown('<div style="display:flex;align-items:center;gap:8px;"><div style="width:18px;height:18px;background:linear-gradient(180deg,#bbf7d0,#86efac);border-radius:5px;border:1px solid #86efac;"></div><span style="font-size:0.8rem;color:#64748b;font-weight:500;">Cumplimiento (100-&lt;115%)</span></div>', unsafe_allow_html=True)
with col_z4:
    st.markdown('<div style="display:flex;align-items:center;gap:8px;"><div style="width:18px;height:18px;background:linear-gradient(180deg,#bae6fd,#7dd3fc);border-radius:5px;border:1px solid #7dd3fc;"></div><span style="font-size:0.8rem;color:#64748b;font-weight:500;">Alto Rend. (≥115%)</span></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Indicador de zona y % de pago
col1, col2 = st.columns([2, 1])

with col1:
    if efectividad < 80:
        zona_html = '<span class="zone-indicator zone-red">⚠️ ZONA CRÍTICA - Sin sueldo variable</span>'
        zona_mensaje = "danger-box"
        zona_texto = "⚠️ <strong>Atención:</strong> Por debajo del 80% no recibirás sueldo variable en el nuevo esquema."
    elif efectividad < 100:
        zona_html = '<span class="zone-indicator zone-yellow">📉 ZONA DE RECUPERACIÓN</span>'
        zona_mensaje = "warning-box"
        zona_texto = "💡 <strong>Consejo:</strong> Estás cerca de la meta. Un pequeño esfuerzo adicional mejorará significativamente tu compensación."
    elif efectividad < 115:
        zona_html = '<span class="zone-indicator zone-green">✅ ZONA DE CUMPLIMIENTO</span>'
        zona_mensaje = "success-box"
        zona_texto = "🎉 <strong>¡Excelente!</strong> Estás cumpliendo tu cuota. El nuevo esquema te beneficia más a partir del 100%."
    else:
        zona_html = '<span class="zone-indicator zone-blue">🚀 ZONA DE ALTO RENDIMIENTO</span>'
        zona_mensaje = "info-box"
        zona_texto = "🏆 <strong>¡Sobresaliente!</strong> En el nuevo esquema, tu pago está en el máximo del 130%."
    
    st.markdown(zona_html, unsafe_allow_html=True)

with col2:
    porcentaje_pago = obtener_porcentaje_pago(efectividad)
    st.metric(
        label="📊 % de Pago (Nuevo Esquema)",
        value=f"{porcentaje_pago:.1f}%",
        delta=f"{porcentaje_pago - efectividad:+.1f}% vs efectividad" if efectividad >= 80 else "N/A"
    )

# Cálculos
sueldo_actual = calcular_sueldo_actual(sueldo_fijo, sueldo_variable, efectividad)
sueldo_nuevo = calcular_sueldo_nuevo(sueldo_fijo, sueldo_variable, efectividad)
diferencia = sueldo_nuevo - sueldo_actual

# Mensaje de zona
st.markdown(f'<div class="{zona_mensaje}">{zona_texto}</div>', unsafe_allow_html=True)

# Métricas principales
st.markdown("### 💰 Comparación de Sueldos")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Esquema Actual</div>
        <div class="metric-value actual">S/ {sueldo_actual:,.0f}</div>
        <small style="color: #94a3b8;">Sueldo Fijo + Variable × Efectividad</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Esquema Nuevo</div>
        <div class="metric-value nuevo">S/ {sueldo_nuevo:,.0f}</div>
        <small style="color: #94a3b8;">Sueldo Fijo + Variable × % Tabla</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    clase_diferencia = "diferencia-positiva" if diferencia >= 0 else "diferencia-negativa"
    signo = "+" if diferencia >= 0 else ""
    emoji = "📈" if diferencia >= 0 else "📉"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Diferencia</div>
        <div class="metric-value {clase_diferencia}">{emoji} {signo}S/ {diferencia:,.0f}</div>
        <small style="color: #94a3b8;">{abs(diferencia/sueldo_actual*100):.1f}% {'más' if diferencia >= 0 else 'menos'}</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Gráfico principal de comparación
st.markdown("### 📈 Visualización Comparativa por Nivel de Efectividad")

efectividades = list(range(0, 151, 1))
sueldos_actuales = [calcular_sueldo_actual(sueldo_fijo, sueldo_variable, e) for e in efectividades]
sueldos_nuevos = [calcular_sueldo_nuevo(sueldo_fijo, sueldo_variable, e) for e in efectividades]

fig = go.Figure()

fig.add_vrect(x0=0, x1=80, fillcolor="rgba(254, 205, 211, 0.4)", layer="below", line_width=0,
              annotation_text="Zona Crítica", annotation_position="top left",
              annotation=dict(font_size=10, font_color="#be123c"))

fig.add_vrect(x0=80, x1=100, fillcolor="rgba(254, 240, 138, 0.4)", layer="below", line_width=0,
              annotation_text="Recuperación", annotation_position="top left",
              annotation=dict(font_size=10, font_color="#a16207"))

fig.add_vrect(x0=100, x1=115, fillcolor="rgba(187, 247, 208, 0.4)", layer="below", line_width=0,
              annotation_text="Cumplimiento", annotation_position="top left",
              annotation=dict(font_size=10, font_color="#15803d"))

fig.add_vrect(x0=115, x1=150, fillcolor="rgba(186, 230, 253, 0.4)", layer="below", line_width=0,
              annotation_text="Alto Rend.", annotation_position="top left",
              annotation=dict(font_size=10, font_color="#0369a1"))

fig.add_trace(go.Scatter(
    x=efectividades,
    y=sueldos_actuales,
    name="Esquema Actual",
    line=dict(color="#818cf8", width=3),
    hovertemplate="Efectividad: %{x}%<br>Sueldo Actual: S/ %{y:,.0f}<extra></extra>"
))

fig.add_trace(go.Scatter(
    x=efectividades,
    y=sueldos_nuevos,
    name="Esquema Nuevo",
    line=dict(color="#34d399", width=3),
    hovertemplate="Efectividad: %{x}%<br>Sueldo Nuevo: S/ %{y:,.0f}<extra></extra>"
))

fig.add_trace(go.Scatter(
    x=[efectividad],
    y=[sueldo_actual],
    mode="markers",
    name="Tu posición (Actual)",
    marker=dict(color="#818cf8", size=15, symbol="circle", line=dict(width=2, color="white")),
    hovertemplate=f"Tu Efectividad: {efectividad}%<br>Sueldo Actual: S/ {sueldo_actual:,.0f}<extra></extra>"
))

fig.add_trace(go.Scatter(
    x=[efectividad],
    y=[sueldo_nuevo],
    mode="markers",
    name="Tu posición (Nuevo)",
    marker=dict(color="#34d399", size=15, symbol="diamond", line=dict(width=2, color="white")),
    hovertemplate=f"Tu Efectividad: {efectividad}%<br>Sueldo Nuevo: S/ {sueldo_nuevo:,.0f}<extra></extra>"
))

for x_val, color in [(80, "#e11d48"), (100, "#ca8a04"), (115, "#16a34a")]:
    fig.add_vline(x=x_val, line_dash="dash", line_color=color, line_width=1.5)

fig.update_layout(
    title=dict(
        text="<b>Comparación de Esquemas: ¿Cómo cambia tu sueldo?</b>",
        font=dict(size=18, family="Plus Jakarta Sans")
    ),
    xaxis=dict(
        title="% de Efectividad (Ventas / Cuota × 100)",
        ticksuffix="%",
        dtick=10,
        range=[0, 150],
        gridcolor="rgba(0,0,0,0.05)"
    ),
    yaxis=dict(
        title="Sueldo Total (S/)",
        tickformat=",",
        tickprefix="S/ ",
        gridcolor="rgba(0,0,0,0.05)"
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5
    ),
    hovermode="x unified",
    plot_bgcolor="white",
    paper_bgcolor="white",
    height=500,
    margin=dict(t=100, b=50, l=80, r=50)
)

st.plotly_chart(fig, use_container_width=True)

# Puntos Clave del Nuevo Esquema
st.markdown("### 🔑 Puntos Clave del Nuevo Esquema")

col_k1, col_k2, col_k3, col_k4 = st.columns(4)

with col_k1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #ffe4e6, #fecdd3); padding: 18px; border-radius: 12px; text-align: center; border: 1px solid #fda4af;">
        <div style="font-weight: 700; color: #be123c; font-size: 1.1rem;">&lt;80%</div>
        <div style="font-size: 0.85rem; color: #881337; margin: 6px 0;">→ 0%</div>
        <div style="font-size: 0.75rem; color: #9f1239;">Sin variable</div>
    </div>
    """, unsafe_allow_html=True)

with col_k2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fef9c3, #fef08a); padding: 18px; border-radius: 12px; text-align: center; border: 1px solid #fde047;">
        <div style="font-weight: 700; color: #a16207; font-size: 1.1rem;">80% - 99%</div>
        <div style="font-size: 0.85rem; color: #854d0e; margin: 6px 0;">→ 71.5% - 98%</div>
        <div style="font-size: 0.75rem; color: #a16207;">Recuperación</div>
    </div>
    """, unsafe_allow_html=True)

with col_k3:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #dcfce7, #bbf7d0); padding: 18px; border-radius: 12px; text-align: center; border: 1px solid #86efac;">
        <div style="font-weight: 700; color: #15803d; font-size: 1.1rem;">100% - 114%</div>
        <div style="font-size: 0.85rem; color: #166534; margin: 6px 0;">→ 100% - 128%</div>
        <div style="font-size: 0.75rem; color: #15803d;">Cumplimiento</div>
    </div>
    """, unsafe_allow_html=True)

with col_k4:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #e0f2fe, #bae6fd); padding: 18px; border-radius: 12px; text-align: center; border: 1px solid #7dd3fc;">
        <div style="font-weight: 700; color: #0369a1; font-size: 1.1rem;">≥115%</div>
        <div style="font-size: 0.85rem; color: #075985; margin: 6px 0;">→ 130% (límite)</div>
        <div style="font-size: 0.75rem; color: #0369a1;">Máximo</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Gráfico de barras comparativo
st.markdown("### 📊 Desglose de tu Compensación")

col1, col2 = st.columns(2)

with col1:
    variable_actual = sueldo_variable * (efectividad / 100)
    
    fig_actual = go.Figure(go.Waterfall(
        name="Esquema Actual",
        orientation="v",
        measure=["relative", "relative", "total"],
        x=["Sueldo Fijo", "Sueldo Variable", "TOTAL"],
        y=[sueldo_fijo, variable_actual, 0],
        text=[f"S/ {sueldo_fijo:,}", f"S/ {variable_actual:,.0f}", f"S/ {sueldo_actual:,.0f}"],
        textposition="outside",
        connector={"line": {"color": "#a5b4fc"}},
        increasing={"marker": {"color": "#c7d2fe"}},
        totals={"marker": {"color": "#818cf8"}}
    ))
    
    fig_actual.update_layout(
        title=dict(text=f"<b>Esquema Actual ({efectividad}% efectividad)</b>", font=dict(size=14)),
        showlegend=False,
        height=350,
        yaxis=dict(tickformat=",", tickprefix="S/ ")
    )
    
    st.plotly_chart(fig_actual, use_container_width=True)

with col2:
    if efectividad >= 80:
        porcentaje = obtener_porcentaje_pago(efectividad) / 100
        variable_nuevo = sueldo_variable * porcentaje
        
        fig_nuevo = go.Figure(go.Waterfall(
            name="Esquema Nuevo",
            orientation="v",
            measure=["relative", "relative", "total"],
            x=["Sueldo Fijo", "Sueldo Variable", "TOTAL"],
            y=[sueldo_fijo, variable_nuevo, 0],
            text=[f"S/ {sueldo_fijo:,}", f"S/ {variable_nuevo:,.0f}", f"S/ {sueldo_nuevo:,.0f}"],
            textposition="outside",
            connector={"line": {"color": "#6ee7b7"}},
            increasing={"marker": {"color": "#a7f3d0"}},
            totals={"marker": {"color": "#34d399"}}
        ))
    else:
        fig_nuevo = go.Figure(go.Waterfall(
            name="Esquema Nuevo",
            orientation="v",
            measure=["relative", "total"],
            x=["Sueldo Fijo", "TOTAL"],
            y=[sueldo_fijo, 0],
            text=[f"S/ {sueldo_fijo:,}", f"S/ {sueldo_fijo:,}"],
            textposition="outside",
            connector={"line": {"color": "#6ee7b7"}},
            increasing={"marker": {"color": "#a7f3d0"}},
            totals={"marker": {"color": "#34d399"}}
        ))
    
    fig_nuevo.update_layout(
        title=dict(text=f"<b>Esquema Nuevo ({porcentaje_pago:.0f}% aplicado)</b>", font=dict(size=14)),
        showlegend=False,
        height=350,
        yaxis=dict(tickformat=",", tickprefix="S/ ")
    )
    
    st.plotly_chart(fig_nuevo, use_container_width=True)

# Tabla de Equivalencias Oficial
st.markdown("### 📊 Tabla de Equivalencias: Efectividad → % Pago")

with st.expander("📖 **Ver tabla completa de equivalencias**", expanded=False):
    col_t1, col_t2, col_t3 = st.columns(3)
    
    with col_t1:
        st.markdown("**🔴 Zona Crítica**")
        st.markdown("""
        | Efectividad | % Pago |
        |:-----------:|:------:|
        | < 80% | 0% |
        """)
        
        st.markdown("**🟡 Zona Recuperación (80-95%)**")
        tabla_80_95 = ""
        for e in range(80, 96):
            pago = obtener_porcentaje_pago(e)
            tabla_80_95 += f"| {e}% | {pago:.1f}% |\n"
        st.markdown(f"""
        | Efectividad | % Pago |
        |:-----------:|:------:|
        {tabla_80_95}
        """)
    
    with col_t2:
        st.markdown("**🟡 Zona Recuperación (96-99%)**")
        tabla_96_99 = ""
        for e in range(96, 100):
            pago = obtener_porcentaje_pago(e)
            tabla_96_99 += f"| {e}% | {pago:.1f}% |\n"
        st.markdown(f"""
        | Efectividad | % Pago |
        |:-----------:|:------:|
        {tabla_96_99}
        """)
        
        st.markdown("**🟢 Zona Cumplimiento (100-114%)**")
        tabla_100_114 = ""
        for e in range(100, 115):
            pago = obtener_porcentaje_pago(e)
            tabla_100_114 += f"| {e}% | {pago:.0f}% |\n"
        st.markdown(f"""
        | Efectividad | % Pago |
        |:-----------:|:------:|
        {tabla_100_114}
        """)
    
    with col_t3:
        st.markdown("**🔵 Zona Alto Rendimiento (≥115%)**")
        st.markdown("""
        | Efectividad | % Pago |
        |:-----------:|:------:|
        | 115% | 130% |
        | 116%+ | 130% (límite) |
        """)
        
        st.markdown("---")
        st.markdown("""
        **📌 Fórmulas:**
        - **80-95%:** 71.5% + (Efect-80) × 1.5
        - **96-99%:** Efectividad - 1
        - **100%:** 100%
        - **101-114%:** 100% + (Efect-100) × 2
        - **≥115%:** 130% (tope)
        """)

# Tabla comparativa de escenarios - TODOS los niveles de la escala
st.markdown("### 📋 Tabla de Escenarios Clave")

# Crear lista completa de escenarios según la tabla oficial
escenarios_completos = (
    [59] +  # Ejemplo por debajo del 80%
    list(range(80, 116)) +  # Del 80% al 115% (todos los valores)
    [120, 130, 150]  # Ejemplos por encima del límite
)

datos_escenarios = []

for e in escenarios_completos:
    s_actual = calcular_sueldo_actual(sueldo_fijo, sueldo_variable, e)
    s_nuevo = calcular_sueldo_nuevo(sueldo_fijo, sueldo_variable, e)
    dif = s_nuevo - s_actual
    pago = obtener_porcentaje_pago(e)
    
    # Determinar zona/color
    if e < 80:
        zona = "🔴 Crítica"
    elif e < 100:
        zona = "🟡 Recuperación"
    elif e < 115:
        zona = "🟢 Cumplimiento"
    else:
        zona = "🔵 Alto Rend."
    
    datos_escenarios.append({
        "Zona": zona,
        "Efectividad": f"{e}%",
        "% Pago Tabla": f"{pago:.1f}%" if pago % 1 != 0 else f"{pago:.0f}%",
        "Esquema Actual": f"S/ {s_actual:,.0f}",
        "Esquema Nuevo": f"S/ {s_nuevo:,.0f}",
        "Diferencia": f"{'+'if dif>=0 else ''}S/ {dif:,.0f}",
        "Beneficio": "✅ Nuevo" if dif > 0 else ("⚖️ Igual" if dif == 0 else "📌 Actual")
    })

df_escenarios = pd.DataFrame(datos_escenarios)

# Filtro por zona
zonas_disponibles = ["Todas"] + list(df_escenarios["Zona"].unique())
zona_seleccionada = st.selectbox(
    "🔍 Filtrar por zona:",
    zonas_disponibles,
    index=0
)

if zona_seleccionada != "Todas":
    df_filtrado = df_escenarios[df_escenarios["Zona"] == zona_seleccionada]
else:
    df_filtrado = df_escenarios

# Mostrar con altura fija y scroll
st.dataframe(
    df_filtrado, 
    use_container_width=True, 
    hide_index=True,
    height=400
)

# Mostrar resumen de la tabla
st.caption(f"📊 Mostrando {len(df_filtrado)} de {len(df_escenarios)} escenarios")

# Resumen ejecutivo
st.markdown("---")
st.markdown("### 🎯 Resumen Ejecutivo")

punto_equilibrio = None
for e in range(0, 151):
    s_a = calcular_sueldo_actual(sueldo_fijo, sueldo_variable, e)
    s_n = calcular_sueldo_nuevo(sueldo_fijo, sueldo_variable, e)
    if s_n >= s_a and e >= 80:
        punto_equilibrio = e
        break

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-box">
        <h4 style="margin:0 0 10px 0;">🔑 Puntos Clave del Nuevo Esquema</h4>
        <ul style="margin:0; padding-left: 20px;">
            <li><strong>Por debajo del 80%:</strong> Solo recibes sueldo fijo (0% variable)</li>
            <li><strong>Entre 80% y 95%:</strong> Pago desde 71.5%, incremento de 1.5% por cada 1%</li>
            <li><strong>Entre 96% y 99%:</strong> Incremento de 1% por cada 1%</li>
            <li><strong>Al 100%:</strong> Recibes exactamente el 100% de tu sueldo variable</li>
            <li><strong>Entre 101% y 114%:</strong> Incremento de 2% por cada 1% adicional</li>
            <li><strong>115% o más:</strong> Tu multiplicador es 130% (máximo)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if punto_equilibrio:
        st.markdown(f"""
        <div class="success-box">
            <h4 style="margin:0 0 10px 0;">📍 Tu Punto de Equilibrio</h4>
            <p style="margin:0;">
                A partir del <strong>{punto_equilibrio}% de efectividad</strong>, el nuevo esquema 
                te beneficia más que el actual.
            </p>
            <p style="margin: 10px 0 0 0; font-size: 0.9rem;">
                💡 <em>Si consistentemente superas este umbral, el nuevo esquema es mejor para ti.</em>
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="warning-box">
            <h4 style="margin:0 0 10px 0;">⚠️ Consideración</h4>
            <p style="margin:0;">
                El nuevo esquema premia el alto rendimiento pero tiene mayor riesgo 
                si no alcanzas el 80% de tu cuota.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.85rem; padding: 1rem;">
    <p>💼 Sistema de Comparación de Esquemas de Comisiones | Área Comercial</p>
    <p>Los cálculos son ilustrativos. Consulta con tu supervisor para detalles específicos.</p>
</div>
""", unsafe_allow_html=True)

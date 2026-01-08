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

# CSS personalizado para un diseño profesional
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
    
    .actual { color: #6366f1; }
    .nuevo { color: #10b981; }
    .diferencia-positiva { color: #10b981; }
    .diferencia-negativa { color: #ef4444; }
    
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

# Función para obtener el porcentaje de pago según la tabla
def obtener_porcentaje_pago(efectividad):
    """
    Retorna el porcentaje de pago según la tabla de equivalencias.
    """
    if efectividad < 80:
        return 0
    elif efectividad >= 115:
        return 130
    elif efectividad == 100:
        return 100
    elif efectividad > 100:
        # Entre 100% y 115%: cada 1% de avance = 2% adicional de pago
        return 100 + (efectividad - 100) * 2
    else:
        # Entre 80% y <100%: interpolación según tabla
        # La tabla muestra: 80%→70%, 81%→71.5%, ..., 99%→98.5%, 100%→100%
        return 70 + (efectividad - 80) * 1.5

# Función para calcular sueldo esquema actual
def calcular_sueldo_actual(sueldo_fijo, sueldo_variable, efectividad):
    """
    Esquema Actual: Sueldo Fijo + Sueldo Variable × % Efectividad
    """
    variable_ajustado = sueldo_variable * (efectividad / 100)
    return sueldo_fijo + variable_ajustado

# Función para calcular sueldo esquema nuevo
def calcular_sueldo_nuevo(sueldo_fijo, sueldo_variable, efectividad):
    """
    Esquema Nuevo: Sueldo Fijo + Sueldo Variable × % Pago Tabla
    """
    porcentaje_pago = obtener_porcentaje_pago(efectividad)
    return sueldo_fijo + (sueldo_variable * porcentaje_pago / 100)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>📊 Comparador de Esquemas de Comisiones</h1>
    <p>Visualiza cómo el nuevo esquema de compensación puede beneficiarte según tu desempeño</p>
</div>
""", unsafe_allow_html=True)

# Sidebar con parámetros simplificados
with st.sidebar:
    st.markdown("### ⚙️ Configuración del Vendedor")
    st.markdown("---")
    
    sueldo_fijo = st.number_input(
        "💵 Sueldo Fijo (S/.)", 
        min_value=0, 
        value=3100, 
        step=100,
        help="Tu sueldo base mensual fijo"
    )
    
    sueldo_variable = st.number_input(
        "📈 Sueldo Variable (S/.)", 
        min_value=0, 
        value=3000, 
        step=100,
        help="Tu sueldo variable al 100% de cumplimiento (incluye comisiones, bonos, etc.)"
    )
    
    st.markdown("---")
    
    total_al_100 = sueldo_fijo + sueldo_variable
    
    st.markdown(f"""
    <div class="info-box">
        <strong>📋 Resumen de Compensación</strong><br>
        <small>
        • Sueldo Fijo: <b>S/. {sueldo_fijo:,.0f}</b><br>
        • Sueldo Variable (100%): <b>S/. {sueldo_variable:,.0f}</b><br>
        • <strong>Total al 100%: S/. {total_al_100:,.0f}</strong>
        </small>
    </div>
    """, unsafe_allow_html=True)

# Contenido principal
st.markdown("### 🎯 Simula tu Efectividad de Ventas")

# Campos de Cuota y Venta
col_cuota, col_venta, col_efectividad = st.columns([1, 1, 1])

with col_cuota:
    cuota = st.number_input(
        "📊 Cuota Mensual (S/.)",
        min_value=1,
        value=100000,
        step=5000,
        format="%d",
        help="Tu meta de ventas mensual"
    )

with col_venta:
    venta = st.number_input(
        "💰 Venta Proyectada (S/.)",
        min_value=0,
        value=100000,
        step=5000,
        format="%d",
        help="Tu venta estimada o real del mes"
    )

with col_efectividad:
    # Calcular efectividad automáticamente
    efectividad_calculada = (venta / cuota) * 100 if cuota > 0 else 0
    efectividad = min(max(round(efectividad_calculada), 0), 150)  # Limitar entre 0 y 150
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); 
                padding: 16px; border-radius: 12px; text-align: center; 
                border: 2px solid #0ea5e9; margin-top: 8px;">
        <div style="font-size: 0.8rem; color: #64748b; font-weight: 500;">% de Efectividad</div>
        <div style="font-size: 2rem; font-weight: 800; color: #0284c7;">{efectividad:.0f}%</div>
        <div style="font-size: 0.7rem; color: #94a3b8;">Venta ÷ Cuota × 100</div>
    </div>
    """, unsafe_allow_html=True)

# Barra visual de efectividad con zonas
st.markdown("""
<style>
    .efectividad-bar-container {
        margin: 20px 0 10px 0;
    }
    .efectividad-bar {
        height: 12px;
        border-radius: 6px;
        display: flex;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .zona-critica { background: linear-gradient(90deg, #fecaca, #fca5a5); flex: 80; }
    .zona-recuperacion { background: linear-gradient(90deg, #fde68a, #fcd34d); flex: 20; }
    .zona-cumplimiento { background: linear-gradient(90deg, #6ee7b7, #34d399); flex: 15; }
    .zona-alto { background: linear-gradient(90deg, #93c5fd, #60a5fa); flex: 35; }
    
    .marcas-container {
        position: relative;
        height: 30px;
        margin-top: 4px;
    }
    .marca {
        position: absolute;
        transform: translateX(-50%);
        text-align: center;
    }
    .marca-linea {
        width: 2px;
        height: 8px;
        background: #64748b;
        margin: 0 auto;
    }
    .marca-texto {
        font-size: 0.75rem;
        color: #64748b;
        font-weight: 600;
    }
    .indicador-posicion {
        position: absolute;
        transform: translateX(-50%);
        top: -28px;
    }
    .indicador-flecha {
        width: 0;
        height: 0;
        border-left: 8px solid transparent;
        border-right: 8px solid transparent;
        border-top: 10px solid #1e293b;
        margin: 0 auto;
    }
    .indicador-valor {
        background: #1e293b;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 2px;
    }
</style>
""", unsafe_allow_html=True)

# Calcular posición del indicador (0-150 mapeado a 0-100%)
posicion_indicador = min((efectividad / 150) * 100, 100)

st.markdown(f"""
<div class="efectividad-bar-container">
    <div style="position: relative; padding-top: 35px;">
        <!-- Indicador de posición actual -->
        <div class="indicador-posicion" style="left: {posicion_indicador}%;">
            <div class="indicador-valor">TÚ: {efectividad:.0f}%</div>
            <div class="indicador-flecha"></div>
        </div>
        
        <!-- Barra de zonas -->
        <div class="efectividad-bar">
            <div class="zona-critica"></div>
            <div class="zona-recuperacion"></div>
            <div class="zona-cumplimiento"></div>
            <div class="zona-alto"></div>
        </div>
        
        <!-- Marcas -->
        <div class="marcas-container">
            <div class="marca" style="left: 0%;">
                <div class="marca-linea"></div>
                <div class="marca-texto">0%</div>
            </div>
            <div class="marca" style="left: {(80/150)*100}%;">
                <div class="marca-linea" style="background: #ef4444;"></div>
                <div class="marca-texto" style="color: #ef4444;">80%</div>
            </div>
            <div class="marca" style="left: {(100/150)*100}%;">
                <div class="marca-linea" style="background: #f59e0b;"></div>
                <div class="marca-texto" style="color: #f59e0b;">100%</div>
            </div>
            <div class="marca" style="left: {(115/150)*100}%;">
                <div class="marca-linea" style="background: #10b981;"></div>
                <div class="marca-texto" style="color: #10b981;">115%</div>
            </div>
            <div class="marca" style="left: 100%;">
                <div class="marca-linea"></div>
                <div class="marca-texto">150%</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Leyenda de zonas
col_z1, col_z2, col_z3, col_z4 = st.columns(4)
with col_z1:
    st.markdown('<div style="display:flex;align-items:center;gap:6px;"><div style="width:12px;height:12px;background:#fca5a5;border-radius:3px;"></div><span style="font-size:0.75rem;color:#64748b;">Crítica (&lt;80%)</span></div>', unsafe_allow_html=True)
with col_z2:
    st.markdown('<div style="display:flex;align-items:center;gap:6px;"><div style="width:12px;height:12px;background:#fcd34d;border-radius:3px;"></div><span style="font-size:0.75rem;color:#64748b;">Recuperación (80-&lt;100%)</span></div>', unsafe_allow_html=True)
with col_z3:
    st.markdown('<div style="display:flex;align-items:center;gap:6px;"><div style="width:12px;height:12px;background:#34d399;border-radius:3px;"></div><span style="font-size:0.75rem;color:#64748b;">Cumplimiento (100-&lt;115%)</span></div>', unsafe_allow_html=True)
with col_z4:
    st.markdown('<div style="display:flex;align-items:center;gap:6px;"><div style="width:12px;height:12px;background:#60a5fa;border-radius:3px;"></div><span style="font-size:0.75rem;color:#64748b;">Alto Rend. (≥115%)</span></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Indicador de zona (mensaje)
col1, col2 = st.columns([2, 1])

with col1:
    # Indicador de zona
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
        label="📊 % de Pago Aplicado (Nuevo Esquema)",
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
        <div class="metric-value actual">S/. {sueldo_actual:,.0f}</div>
        <small style="color: #94a3b8;">Sueldo Fijo + Variable × Efectividad</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Esquema Nuevo</div>
        <div class="metric-value nuevo">S/. {sueldo_nuevo:,.0f}</div>
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
        <div class="metric-value {clase_diferencia}">{emoji} {signo}S/. {diferencia:,.0f}</div>
        <small style="color: #94a3b8;">{abs(diferencia/sueldo_actual*100):.1f}% {'más' if diferencia >= 0 else 'menos'}</small>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Gráfico principal de comparación
st.markdown("### 📈 Visualización Comparativa por Nivel de Efectividad")

# Generar datos para el gráfico
efectividades = list(range(0, 151, 1))
sueldos_actuales = [calcular_sueldo_actual(sueldo_fijo, sueldo_variable, e) for e in efectividades]
sueldos_nuevos = [calcular_sueldo_nuevo(sueldo_fijo, sueldo_variable, e) for e in efectividades]

# Crear figura con Plotly
fig = go.Figure()

# Agregar zonas de fondo
fig.add_vrect(x0=0, x1=80, fillcolor="rgba(239, 68, 68, 0.1)", layer="below", line_width=0,
              annotation_text="Zona Crítica<br>(Sin variable)", annotation_position="top left",
              annotation=dict(font_size=10, font_color="#dc2626"))

fig.add_vrect(x0=80, x1=100, fillcolor="rgba(245, 158, 11, 0.1)", layer="below", line_width=0,
              annotation_text="Zona de<br>Recuperación", annotation_position="top left",
              annotation=dict(font_size=10, font_color="#d97706"))

fig.add_vrect(x0=100, x1=115, fillcolor="rgba(16, 185, 129, 0.1)", layer="below", line_width=0,
              annotation_text="Zona de<br>Cumplimiento", annotation_position="top left",
              annotation=dict(font_size=10, font_color="#059669"))

fig.add_vrect(x0=115, x1=150, fillcolor="rgba(59, 130, 246, 0.1)", layer="below", line_width=0,
              annotation_text="Alto<br>Rendimiento", annotation_position="top left",
              annotation=dict(font_size=10, font_color="#2563eb"))

# Líneas de los esquemas
fig.add_trace(go.Scatter(
    x=efectividades,
    y=sueldos_actuales,
    name="Esquema Actual",
    line=dict(color="#6366f1", width=3),
    hovertemplate="Efectividad: %{x}%<br>Sueldo Actual: S/. %{y:,.0f}<extra></extra>"
))

fig.add_trace(go.Scatter(
    x=efectividades,
    y=sueldos_nuevos,
    name="Esquema Nuevo",
    line=dict(color="#10b981", width=3),
    hovertemplate="Efectividad: %{x}%<br>Sueldo Nuevo: S/. %{y:,.0f}<extra></extra>"
))

# Punto actual del vendedor
fig.add_trace(go.Scatter(
    x=[efectividad],
    y=[sueldo_actual],
    mode="markers",
    name="Tu posición (Actual)",
    marker=dict(color="#6366f1", size=15, symbol="circle", line=dict(width=2, color="white")),
    hovertemplate=f"Tu Efectividad: {efectividad}%<br>Sueldo Actual: S/. {sueldo_actual:,.0f}<extra></extra>"
))

fig.add_trace(go.Scatter(
    x=[efectividad],
    y=[sueldo_nuevo],
    mode="markers",
    name="Tu posición (Nuevo)",
    marker=dict(color="#10b981", size=15, symbol="diamond", line=dict(width=2, color="white")),
    hovertemplate=f"Tu Efectividad: {efectividad}%<br>Sueldo Nuevo: S/. {sueldo_nuevo:,.0f}<extra></extra>"
))

# Líneas verticales de referencia
for x_val, label, color in [(80, "80%", "#ef4444"), (100, "100%", "#f59e0b"), (115, "115%", "#10b981")]:
    fig.add_vline(x=x_val, line_dash="dash", line_color=color, line_width=1.5)

# Configuración del layout
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
        title="Sueldo Total (S/.)",
        tickformat=",",
        tickprefix="S/. ",
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
    <div style="background: #fee2e2; padding: 16px; border-radius: 12px; text-align: center;">
        <div style="font-weight: 700; color: #ef4444; font-size: 1.1rem;">&lt;80%</div>
        <div style="font-size: 0.85rem; color: #475569; margin: 4px 0;">→ 0%</div>
        <div style="font-size: 0.75rem; color: #94a3b8;">Sin variable</div>
    </div>
    """, unsafe_allow_html=True)

with col_k2:
    st.markdown("""
    <div style="background: #fef3c7; padding: 16px; border-radius: 12px; text-align: center;">
        <div style="font-weight: 700; color: #f59e0b; font-size: 1.1rem;">80% - &lt;100%</div>
        <div style="font-size: 0.85rem; color: #475569; margin: 4px 0;">→ 70% - 98.5%</div>
        <div style="font-size: 0.75rem; color: #94a3b8;">Recuperación</div>
    </div>
    """, unsafe_allow_html=True)

with col_k3:
    st.markdown("""
    <div style="background: #d1fae5; padding: 16px; border-radius: 12px; text-align: center;">
        <div style="font-weight: 700; color: #10b981; font-size: 1.1rem;">100% - &lt;115%</div>
        <div style="font-size: 0.85rem; color: #475569; margin: 4px 0;">→ 100% - 128%</div>
        <div style="font-size: 0.75rem; color: #94a3b8;">Cumplimiento</div>
    </div>
    """, unsafe_allow_html=True)

with col_k4:
    st.markdown("""
    <div style="background: #dbeafe; padding: 16px; border-radius: 12px; text-align: center;">
        <div style="font-weight: 700; color: #3b82f6; font-size: 1.1rem;">≥115%</div>
        <div style="font-size: 0.85rem; color: #475569; margin: 4px 0;">→ 130%</div>
        <div style="font-size: 0.75rem; color: #94a3b8;">Máximo</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Gráfico de barras comparativo simplificado
st.markdown("### 📊 Desglose de tu Compensación")

col1, col2 = st.columns(2)

with col1:
    # Esquema Actual - Desglose simplificado
    variable_actual = sueldo_variable * (efectividad / 100)
    
    fig_actual = go.Figure(go.Waterfall(
        name="Esquema Actual",
        orientation="v",
        measure=["relative", "relative", "total"],
        x=["Sueldo Fijo", "Sueldo Variable", "TOTAL"],
        y=[sueldo_fijo, variable_actual, 0],
        text=[f"S/. {sueldo_fijo:,.0f}", f"S/. {variable_actual:,.0f}", f"S/. {sueldo_actual:,.0f}"],
        textposition="outside",
        connector={"line": {"color": "#6366f1"}},
        increasing={"marker": {"color": "#818cf8"}},
        totals={"marker": {"color": "#6366f1"}}
    ))
    
    fig_actual.update_layout(
        title=dict(text=f"<b>Esquema Actual ({efectividad}% efectividad)</b>", font=dict(size=14)),
        showlegend=False,
        height=350,
        yaxis=dict(tickformat=",", tickprefix="S/. ")
    )
    
    st.plotly_chart(fig_actual, use_container_width=True)

with col2:
    # Esquema Nuevo - Desglose simplificado
    if efectividad >= 80:
        porcentaje = obtener_porcentaje_pago(efectividad) / 100
        variable_nuevo = sueldo_variable * porcentaje
        
        fig_nuevo = go.Figure(go.Waterfall(
            name="Esquema Nuevo",
            orientation="v",
            measure=["relative", "relative", "total"],
            x=["Sueldo Fijo", "Sueldo Variable", "TOTAL"],
            y=[sueldo_fijo, variable_nuevo, 0],
            text=[f"S/. {sueldo_fijo:,.0f}", f"S/. {variable_nuevo:,.0f}", f"S/. {sueldo_nuevo:,.0f}"],
            textposition="outside",
            connector={"line": {"color": "#10b981"}},
            increasing={"marker": {"color": "#6ee7b7"}},
            totals={"marker": {"color": "#10b981"}}
        ))
    else:
        fig_nuevo = go.Figure(go.Waterfall(
            name="Esquema Nuevo",
            orientation="v",
            measure=["relative", "total"],
            x=["Sueldo Fijo", "TOTAL"],
            y=[sueldo_fijo, 0],
            text=[f"S/. {sueldo_fijo:,.0f}", f"S/. {sueldo_fijo:,.0f}"],
            textposition="outside",
            connector={"line": {"color": "#10b981"}},
            increasing={"marker": {"color": "#6ee7b7"}},
            totals={"marker": {"color": "#10b981"}}
        ))
    
    fig_nuevo.update_layout(
        title=dict(text=f"<b>Esquema Nuevo ({porcentaje_pago:.0f}% aplicado)</b>", font=dict(size=14)),
        showlegend=False,
        height=350,
        yaxis=dict(tickformat=",", tickprefix="S/. ")
    )
    
    st.plotly_chart(fig_nuevo, use_container_width=True)

# Tabla comparativa de escenarios
st.markdown("### 📋 Tabla de Escenarios Clave")

escenarios = [59, 80, 88, 90, 95, 100, 105, 109, 115, 120, 130]
datos_escenarios = []

for e in escenarios:
    s_actual = calcular_sueldo_actual(sueldo_fijo, sueldo_variable, e)
    s_nuevo = calcular_sueldo_nuevo(sueldo_fijo, sueldo_variable, e)
    dif = s_nuevo - s_actual
    pago = obtener_porcentaje_pago(e)
    
    datos_escenarios.append({
        "Efectividad": f"{e}%",
        "% Pago Tabla": f"{pago:.0f}%",
        "Esquema Actual": f"S/. {s_actual:,.0f}",
        "Esquema Nuevo": f"S/. {s_nuevo:,.0f}",
        "Diferencia": f"{'+'if dif>=0 else ''}S/. {dif:,.0f}",
        "Beneficio": "✅ Nuevo" if dif > 0 else ("⚖️ Igual" if dif == 0 else "📌 Actual")
    })

df_escenarios = pd.DataFrame(datos_escenarios)
st.dataframe(df_escenarios, use_container_width=True, hide_index=True)

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
            <li><strong>Por debajo del 80%:</strong> Solo recibes sueldo fijo (no hay variable)</li>
            <li><strong>Entre 80% y &lt;100%:</strong> El % de pago es menor que tu efectividad</li>
            <li><strong>Al 100%:</strong> Recibes exactamente el 100% de tu sueldo variable</li>
            <li><strong>Por encima del 100%:</strong> Ganas más que con el esquema actual</li>
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

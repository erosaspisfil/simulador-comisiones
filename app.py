import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta

# Configuracion de pagina
st.set_page_config(
    page_title="Simulador de Comisiones",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS profesional con tema blanco
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Reset y base */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background-color: #f8fafc;
    }

    /* Ocultar elementos de Streamlit innecesarios */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Header de Streamlit - estilo limpio */
    header[data-testid="stHeader"] {
        background: #ffffff;
        border-bottom: 1px solid #e2e8f0;
        height: 3.5rem;
    }

    /* Sidebar principal */
    [data-testid="stSidebar"] {
        display: block !important;
        min-width: 320px;
        background: #ffffff;
        border-right: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding: 1.5rem 1.25rem;
    }

    [data-testid="stSidebar"] .stMarkdown {
        padding: 0;
    }

    /* Control de sidebar colapsado */
    [data-testid="stSidebarCollapsedControl"] {
        display: flex !important;
    }

    /* Boton de colapsar/expandir sidebar */
    button[data-testid="baseButton-headerNoPadding"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        width: 36px !important;
        height: 36px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: #64748b !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important;
    }

    button[data-testid="baseButton-headerNoPadding"]:hover {
        background: #f8fafc !important;
        border-color: #cbd5e1 !important;
        color: #334155 !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1) !important;
    }

    button[data-testid="baseButton-headerNoPadding"] svg {
        width: 18px !important;
        height: 18px !important;
    }

    /* Boton dentro del sidebar */
    [data-testid="stSidebar"] button[data-testid="baseButton-headerNoPadding"] {
        position: absolute;
        top: 1rem;
        right: 1rem;
        z-index: 100;
    }

    /* Sidebar header */
    .sidebar-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 1.25rem 1.5rem;
        border-radius: 12px;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        position: relative;
    }

    .sidebar-header h2 {
        color: #ffffff;
        font-size: 1.125rem;
        font-weight: 700;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .sidebar-header p {
        color: #94a3b8;
        font-size: 0.8125rem;
        margin: 0.5rem 0 0 0;
        line-height: 1.4;
    }

    /* Input labels mejorados */
    .input-group {
        margin-bottom: 1.25rem;
    }

    .input-label {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.8125rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.025em;
    }

    .input-label .icon {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    }

    .input-label .icon-blue {
        background: #eff6ff;
        color: #2563eb;
    }

    .input-label .icon-green {
        background: #f0fdf4;
        color: #16a34a;
    }

    /* Sidebar inputs */
    [data-testid="stSidebar"] [data-testid="stNumberInput"] > div {
        background: #f8fafc;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
    }

    [data-testid="stSidebar"] [data-testid="stNumberInput"] > div:focus-within {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }

    [data-testid="stSidebar"] [data-testid="stNumberInput"] input {
        font-weight: 600;
        font-size: 1.125rem;
        color: #0f172a;
    }

    /* Summary card mejorada */
    .summary-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.25rem;
        margin-top: 1rem;
    }

    .summary-card-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #e2e8f0;
    }

    .summary-card-header .icon {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1rem;
    }

    .summary-card-header h3 {
        font-size: 0.875rem;
        font-weight: 600;
        color: #374151;
        margin: 0;
    }

    .summary-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
    }

    .summary-row-label {
        font-size: 0.8125rem;
        color: #64748b;
    }

    .summary-row-value {
        font-size: 0.9375rem;
        font-weight: 600;
        color: #334155;
    }

    .summary-total {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        margin: 1rem -1.25rem -1.25rem -1.25rem;
        padding: 1rem 1.25rem;
        border-radius: 0 0 12px 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .summary-total-label {
        font-size: 0.8125rem;
        font-weight: 500;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .summary-total-value {
        font-size: 1.375rem;
        font-weight: 700;
        color: #ffffff;
    }

    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 30px rgba(30, 41, 59, 0.15), 0 2px 6px rgba(0,0,0,0.08);
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 300px;
        height: 100%;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(16, 185, 129, 0.1) 100%);
        border-radius: 0 20px 20px 0;
    }

    .main-header .header-badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        background: rgba(99, 102, 241, 0.2);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #a5b4fc;
        padding: 4px 10px;
        border-radius: 16px;
        font-size: 0.6875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.75rem;
    }

    .main-header h1 {
        color: #ffffff;
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.02em;
        position: relative;
        z-index: 1;
    }

    .main-header p {
        color: #94a3b8;
        font-size: 0.9375rem;
        margin-top: 0.5rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
        max-width: 600px;
    }

    .main-header .header-stats {
        display: flex;
        gap: 2rem;
        margin-top: 1.5rem;
        position: relative;
        z-index: 1;
    }

    .main-header .stat-item {
        display: flex;
        flex-direction: column;
    }

    .main-header .stat-value {
        color: #ffffff;
        font-size: 1.25rem;
        font-weight: 700;
    }

    .main-header .stat-label {
        color: #64748b;
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Cards de metricas */
    .metric-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        text-align: center;
        transition: all 0.2s ease;
    }

    .metric-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-color: #cbd5e1;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
        letter-spacing: -0.025em;
    }

    .metric-label {
        color: #64748b;
        font-size: 0.8125rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .actual { color: #6366f1; }
    .nuevo { color: #10b981; }
    .diferencia-positiva { color: #059669; }
    .diferencia-negativa { color: #dc2626; }

    /* Cajas de informacion */
    .info-box {
        background: #f0f9ff;
        border: 1px solid #bae6fd;
        padding: 1rem 1.25rem;
        border-radius: 10px;
        margin: 1rem 0;
    }

    .warning-box {
        background: #fffbeb;
        border: 1px solid #fde68a;
        padding: 1rem 1.25rem;
        border-radius: 10px;
        margin: 1rem 0;
    }

    .success-box {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        padding: 1rem 1.25rem;
        border-radius: 10px;
        margin: 1rem 0;
    }

    .danger-box {
        background: #fef2f2;
        border: 1px solid #fecaca;
        padding: 1rem 1.25rem;
        border-radius: 10px;
        margin: 1rem 0;
    }

    /* Indicadores de zona */
    .zone-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.875rem;
    }

    .zone-red {
        background: #fef2f2;
        color: #dc2626;
        border: 1px solid #fecaca;
    }
    .zone-yellow {
        background: #fffbeb;
        color: #d97706;
        border: 1px solid #fde68a;
    }
    .zone-green {
        background: #f0fdf4;
        color: #059669;
        border: 1px solid #bbf7d0;
    }
    .zone-blue {
        background: #eff6ff;
        color: #2563eb;
        border: 1px solid #bfdbfe;
    }
    .zone-purple {
        background: #faf5ff;
        color: #7c3aed;
        border: 1px solid #e9d5ff;
    }

    /* Estilos de metrica de Streamlit */
    div[data-testid="stMetricValue"] {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0f172a;
    }

    div[data-testid="stMetricDelta"] {
        font-size: 0.875rem;
    }

    /* Section headers */
    .section-header {
        color: #0f172a;
        font-size: 1.25rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #e2e8f0;
    }

    /* Data card */
    .data-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.25rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }

    .data-card-header {
        font-size: 0.75rem;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.375rem;
    }

    .data-card-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0f172a;
    }

    /* Key points cards */
    .key-card {
        background: #ffffff;
        padding: 1.25rem;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        transition: all 0.2s ease;
    }

    .key-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }

    .key-card-title {
        font-weight: 700;
        font-size: 1.125rem;
        margin-bottom: 0.25rem;
    }

    .key-card-subtitle {
        font-size: 0.875rem;
        margin: 0.375rem 0;
    }

    .key-card-label {
        font-size: 0.75rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Slider styling */
    .stSlider > div > div > div > div {
        background: #6366f1;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
    }

    /* Tables */
    .stDataFrame {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-header {
            padding: 1.5rem;
        }
        .main-header h1 {
            font-size: 1.5rem;
        }
        .metric-value {
            font-size: 1.5rem;
        }
    }

    /* Accesibilidad - focus visible */
    button:focus-visible,
    input:focus-visible,
    select:focus-visible {
        outline: 2px solid #6366f1;
        outline-offset: 2px;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
</style>
""", unsafe_allow_html=True)


# Funcion para obtener el saludo segun la hora de Lima, Peru (GMT-5)
def obtener_saludo():
    """Retorna el saludo e icono apropiado segun la hora en Lima, Peru (GMT-5)."""
    utc_now = datetime.now(timezone.utc)
    lima_offset = timedelta(hours=-5)
    lima_time = utc_now + lima_offset
    hora = lima_time.hour

    if 6 <= hora < 12:
        return "Buenos dias", "☀️"
    elif 12 <= hora < 18:
        return "Buenas tardes", "🌤️"
    else:
        return "Buenas noches", "🌙"


# Funcion para obtener el porcentaje de pago segun la tabla oficial
def obtener_porcentaje_pago(efectividad):
    """
    Retorna el porcentaje de pago segun la tabla de equivalencias oficial.

    Rangos:
    - Menos de 80%: 0%
    - 80% a 95%: 71.5% + (efectividad - 80) * 1.5
    - 96% a 99%: incremento de 1% por cada 1%
    - 100%: 100%
    - 101% a 114%: 100% + (efectividad - 100) * 2
    - 115% a 130%: 130%
    - 131% o mas: igual a la efectividad (sin tope)
    """
    if efectividad < 80:
        return 0
    elif efectividad > 130:
        # A partir de 131%: el pago es igual a la efectividad (sin tope)
        return efectividad
    elif efectividad >= 115:
        # Entre 115% y 130%: pago fijo de 130%
        return 130
    elif efectividad == 100:
        return 100
    elif efectividad > 100:
        # Entre 101% y 114%: cada 1% adicional = 2% mas de pago
        return 100 + (efectividad - 100) * 2
    elif efectividad >= 96:
        # Entre 96% y 99%: incremento de 1% por cada 1%
        return efectividad - 1
    else:
        # Entre 80% y 95%: 71.5% + 1.5% por cada 1% adicional
        return 71.5 + (efectividad - 80) * 1.5


def calcular_sueldo_actual(sueldo_fijo, sueldo_variable, efectividad):
    """Calcula el sueldo con el esquema actual (lineal)."""
    variable_ajustado = sueldo_variable * (efectividad / 100)
    return sueldo_fijo + variable_ajustado


def calcular_sueldo_nuevo(sueldo_fijo, sueldo_variable, efectividad):
    """Calcula el sueldo con el nuevo esquema (por tabla)."""
    porcentaje_pago = obtener_porcentaje_pago(efectividad)
    return sueldo_fijo + (sueldo_variable * porcentaje_pago / 100)


# Header principal
st.markdown("""
<div class="main-header">
    <div class="header-badge">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
        </svg>
        Area Comercial
    </div>
    <h1>Simulador de Comisiones</h1>
    <p>Visualiza y compara tu compensacion entre el esquema actual y el nuevo esquema basado en tu nivel de efectividad de ventas</p>
</div>
""", unsafe_allow_html=True)

# Sidebar con parametros
with st.sidebar:
    # Saludo dinamico basado en hora de Lima
    saludo, icono = obtener_saludo()
    st.markdown(f"""
    <div style="margin-top: 2rem; margin-bottom: 0.5rem;">
        <span style="font-size: 1.25rem; font-weight: 600; color: #334155;">{icono} {saludo}</span>
    </div>
    """, unsafe_allow_html=True)

    # Header del sidebar
    st.markdown("""
    <div class="sidebar-header" style="margin-top: 0.75rem;">
        <h2>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
            Configuracion
        </h2>
        <p>Define tu estructura salarial para simular escenarios</p>
    </div>
    """, unsafe_allow_html=True)

    # Input Sueldo Fijo
    st.markdown("""
    <div class="input-label">
        <div class="icon icon-blue">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
                <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
            </svg>
        </div>
        Sueldo Fijo
    </div>
    """, unsafe_allow_html=True)

    sueldo_fijo = st.number_input(
        "Sueldo Fijo",
        min_value=0,
        value=3100,
        step=100,
        help="Tu sueldo base mensual fijo",
        label_visibility="collapsed"
    )

    # Input Sueldo Variable
    st.markdown("""
    <div class="input-label">
        <div class="icon icon-green">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="12" y1="1" x2="12" y2="23"></line>
                <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
            </svg>
        </div>
        Sueldo Variable
    </div>
    """, unsafe_allow_html=True)

    sueldo_variable = st.number_input(
        "Sueldo Variable",
        min_value=0,
        value=3000,
        step=100,
        help="Tu sueldo variable al 100% de cumplimiento",
        label_visibility="collapsed"
    )

    total_al_100 = sueldo_fijo + sueldo_variable

    # Summary card
    st.markdown(f"""
    <div class="summary-card">
        <div class="summary-card-header">
            <div class="icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                    <line x1="16" y1="13" x2="8" y2="13"></line>
                    <line x1="16" y1="17" x2="8" y2="17"></line>
                </svg>
            </div>
            <h3>Resumen de Compensacion</h3>
        </div>
        <div class="summary-row">
            <span class="summary-row-label">Sueldo Fijo</span>
            <span class="summary-row-value">S/ {sueldo_fijo:,}</span>
        </div>
        <div class="summary-row">
            <span class="summary-row-label">Variable (100%)</span>
            <span class="summary-row-value">S/ {sueldo_variable:,}</span>
        </div>
        <div class="summary-total">
            <span class="summary-total-label">Total al 100%</span>
            <span class="summary-total-value">S/ {total_al_100:,}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Contenido principal
st.markdown('<div class="section-header">Simula tu Efectividad</div>', unsafe_allow_html=True)

# Inicializar session_state
if 'init' not in st.session_state:
    st.session_state.init = True
    st.session_state.cuota_val = 100000
    st.session_state.venta_val = 100000
    st.session_state.efect_val = 100

# Seccion de inputs
with st.expander("Editar Cuota y Venta manualmente", expanded=False):
    col_input1, col_input2 = st.columns(2)

    with col_input1:
        nueva_cuota = st.number_input(
            "Cuota Mensual (S/)",
            min_value=1,
            value=st.session_state.cuota_val,
            step=5000,
            help="Tu meta de ventas mensual"
        )
        if nueva_cuota != st.session_state.cuota_val:
            st.session_state.cuota_val = nueva_cuota
            st.session_state.efect_val = min(max(int((st.session_state.venta_val / nueva_cuota) * 100), 0), 200)
            st.rerun()

    with col_input2:
        nueva_venta = st.number_input(
            "Venta Proyectada (S/)",
            min_value=0,
            value=st.session_state.venta_val,
            step=5000,
            help="Tu venta estimada o real del mes"
        )
        if nueva_venta != st.session_state.venta_val:
            st.session_state.venta_val = nueva_venta
            st.session_state.efect_val = min(max(int((nueva_venta / st.session_state.cuota_val) * 100), 0), 200)
            st.rerun()

# Slider de efectividad
st.markdown("**Ajusta tu porcentaje de efectividad**")
nueva_efect = st.slider(
    "Desliza para simular diferentes escenarios",
    min_value=0,
    max_value=200,
    value=st.session_state.efect_val,
    step=1,
    format="%d%%",
    help="Mueve el slider para ver como cambia tu sueldo",
    label_visibility="collapsed"
)

if nueva_efect != st.session_state.efect_val:
    st.session_state.efect_val = nueva_efect
    st.session_state.venta_val = int((nueva_efect / 100) * st.session_state.cuota_val)
    st.rerun()

# Valores actuales
cuota = st.session_state.cuota_val
venta = st.session_state.venta_val
efectividad = st.session_state.efect_val

# Tarjetas de datos
col_c, col_v, col_e = st.columns(3)

with col_c:
    st.markdown(f"""
    <div class="data-card">
        <div class="data-card-header">Cuota Mensual</div>
        <div class="data-card-value">S/ {cuota:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col_v:
    st.markdown(f"""
    <div class="data-card">
        <div class="data-card-header">Venta Proyectada</div>
        <div class="data-card-value">S/ {venta:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col_e:
    # Color segun zona
    if efectividad < 80:
        border_color = "#fecaca"
        bg_color = "#fef2f2"
        text_color = "#dc2626"
    elif efectividad < 100:
        border_color = "#fde68a"
        bg_color = "#fffbeb"
        text_color = "#d97706"
    elif efectividad < 115:
        border_color = "#bbf7d0"
        bg_color = "#f0fdf4"
        text_color = "#059669"
    elif efectividad <= 130:
        border_color = "#bfdbfe"
        bg_color = "#eff6ff"
        text_color = "#2563eb"
    else:
        border_color = "#e9d5ff"
        bg_color = "#faf5ff"
        text_color = "#7c3aed"

    st.markdown(f"""
    <div class="data-card" style="background: {bg_color}; border-color: {border_color};">
        <div class="data-card-header">% Efectividad</div>
        <div class="data-card-value" style="color: {text_color};">{efectividad}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Barra visual de progreso
st.markdown(f"""
<div style="margin: 0.5rem 0 1.5rem 0;">
    <div style="position: relative; padding-top: 45px;">
        <div style="position: absolute; left: {min((efectividad / 200) * 100, 100)}%; transform: translateX(-50%); top: 0; text-align: center; z-index: 10;">
            <div style="background: #1e293b; color: white; padding: 6px 14px; border-radius: 6px; font-size: 0.8125rem; font-weight: 600; white-space: nowrap; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
                TU: {efectividad}%
            </div>
            <div style="width: 0; height: 0; border-left: 8px solid transparent; border-right: 8px solid transparent; border-top: 8px solid #1e293b; margin: 0 auto;"></div>
        </div>
        <div style="height: 12px; border-radius: 6px; display: flex; overflow: hidden; background: #e2e8f0;">
            <div style="background: #fecaca; flex: 80;"></div>
            <div style="background: #fde68a; flex: 20;"></div>
            <div style="background: #bbf7d0; flex: 15;"></div>
            <div style="background: #bfdbfe; flex: 15;"></div>
            <div style="background: #e9d5ff; flex: 70;"></div>
        </div>
        <div style="position: relative; height: 24px; margin-top: 8px; font-size: 0.75rem; color: #64748b;">
            <div style="position: absolute; left: 0%;">0%</div>
            <div style="position: absolute; left: 40%; transform: translateX(-50%); color: #dc2626; font-weight: 600;">80%</div>
            <div style="position: absolute; left: 50%; transform: translateX(-50%); color: #d97706; font-weight: 600;">100%</div>
            <div style="position: absolute; left: 57.5%; transform: translateX(-50%); color: #059669; font-weight: 600;">115%</div>
            <div style="position: absolute; left: 65%; transform: translateX(-50%); color: #2563eb; font-weight: 600;">130%</div>
            <div style="position: absolute; right: 0;">200%</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Leyenda de zonas
col_z1, col_z2, col_z3, col_z4, col_z5 = st.columns(5)
with col_z1:
    st.markdown('<div style="display:flex;align-items:center;gap:6px;"><div style="width:12px;height:12px;background:#fecaca;border-radius:3px;"></div><span style="font-size:0.75rem;color:#64748b;">Critica (&lt;80%)</span></div>', unsafe_allow_html=True)
with col_z2:
    st.markdown('<div style="display:flex;align-items:center;gap:6px;"><div style="width:12px;height:12px;background:#fde68a;border-radius:3px;"></div><span style="font-size:0.75rem;color:#64748b;">Recuperacion (80-99%)</span></div>', unsafe_allow_html=True)
with col_z3:
    st.markdown('<div style="display:flex;align-items:center;gap:6px;"><div style="width:12px;height:12px;background:#bbf7d0;border-radius:3px;"></div><span style="font-size:0.75rem;color:#64748b;">Cumplimiento (100-115%)</span></div>', unsafe_allow_html=True)
with col_z4:
    st.markdown('<div style="display:flex;align-items:center;gap:6px;"><div style="width:12px;height:12px;background:#bfdbfe;border-radius:3px;"></div><span style="font-size:0.75rem;color:#64748b;">Alto Rend. (+115-130%)</span></div>', unsafe_allow_html=True)
with col_z5:
    st.markdown('<div style="display:flex;align-items:center;gap:6px;"><div style="width:12px;height:12px;background:#e9d5ff;border-radius:3px;"></div><span style="font-size:0.75rem;color:#64748b;">Excepcional (&gt;130%)</span></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Indicador de zona y % de pago
col1, col2 = st.columns([2, 1])

with col1:
    if efectividad < 80:
        zona_html = '<span class="zone-indicator zone-red">ZONA CRITICA - Sin sueldo variable</span>'
        zona_mensaje = "danger-box"
        zona_texto = "<strong>Atencion:</strong> Por debajo del 80% no recibes sueldo variable en el nuevo esquema."
    elif efectividad < 100:
        zona_html = '<span class="zone-indicator zone-yellow">ZONA DE RECUPERACION</span>'
        zona_mensaje = "warning-box"
        zona_texto = "<strong>Consejo:</strong> Estas cerca de la meta. Un esfuerzo adicional mejorara tu compensacion."
    elif efectividad < 115:
        zona_html = '<span class="zone-indicator zone-green">ZONA DE CUMPLIMIENTO</span>'
        zona_mensaje = "success-box"
        zona_texto = "<strong>Excelente:</strong> Estas cumpliendo tu cuota. El nuevo esquema te beneficia a partir del 100%."
    elif efectividad <= 130:
        zona_html = '<span class="zone-indicator zone-blue">ZONA DE ALTO RENDIMIENTO</span>'
        zona_mensaje = "info-box"
        zona_texto = "<strong>Sobresaliente:</strong> En esta zona tu multiplicador es 130%, el maximo de la tabla base."
    else:
        zona_html = '<span class="zone-indicator zone-purple">ZONA EXCEPCIONAL - Sin tope</span>'
        zona_mensaje = "info-box"
        zona_texto = f"<strong>Extraordinario:</strong> Al superar 130%, tu multiplicador es igual a tu efectividad: <b>{efectividad}%</b>."

    st.markdown(zona_html, unsafe_allow_html=True)

with col2:
    porcentaje_pago = obtener_porcentaje_pago(efectividad)
    delta_text = f"{porcentaje_pago - efectividad:+.1f}% vs efectividad" if efectividad >= 80 else "N/A"
    st.metric(
        label="% de Pago (Nuevo Esquema)",
        value=f"{porcentaje_pago:.1f}%",
        delta=delta_text
    )

# Calculos
sueldo_actual = calcular_sueldo_actual(sueldo_fijo, sueldo_variable, efectividad)
sueldo_nuevo = calcular_sueldo_nuevo(sueldo_fijo, sueldo_variable, efectividad)
diferencia = sueldo_nuevo - sueldo_actual

# Mensaje de zona
st.markdown(f'<div class="{zona_mensaje}">{zona_texto}</div>', unsafe_allow_html=True)

# Metricas principales
st.markdown('<div class="section-header">Comparacion de Sueldos</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Esquema Actual</div>
        <div class="metric-value actual">S/ {sueldo_actual:,.0f}</div>
        <div style="color: #94a3b8; font-size: 0.8125rem;">Fijo + Variable x Efectividad</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Esquema Nuevo</div>
        <div class="metric-value nuevo">S/ {sueldo_nuevo:,.0f}</div>
        <div style="color: #94a3b8; font-size: 0.8125rem;">Fijo + Variable x % Tabla</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    clase_diferencia = "diferencia-positiva" if diferencia >= 0 else "diferencia-negativa"
    signo = "+" if diferencia >= 0 else ""
    icon = "arrow_upward" if diferencia >= 0 else "arrow_downward"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Diferencia</div>
        <div class="metric-value {clase_diferencia}">{signo}S/ {diferencia:,.0f}</div>
        <div style="color: #94a3b8; font-size: 0.8125rem;">{abs(diferencia/sueldo_actual*100):.1f}% {'mas' if diferencia >= 0 else 'menos'}</div>
    </div>
    """, unsafe_allow_html=True)

# Grafico principal
st.markdown('<div class="section-header">Visualizacion Comparativa</div>', unsafe_allow_html=True)

efectividades = list(range(0, 201, 1))
sueldos_actuales = [calcular_sueldo_actual(sueldo_fijo, sueldo_variable, e) for e in efectividades]
sueldos_nuevos = [calcular_sueldo_nuevo(sueldo_fijo, sueldo_variable, e) for e in efectividades]

fig = go.Figure()

# Zonas de fondo
fig.add_vrect(x0=0, x1=80, fillcolor="rgba(254, 202, 202, 0.2)", layer="below", line_width=0,
              annotation_text="Critica", annotation_position="top left",
              annotation=dict(font_size=10, font_color="#dc2626"))

fig.add_vrect(x0=80, x1=100, fillcolor="rgba(253, 230, 138, 0.2)", layer="below", line_width=0,
              annotation_text="Recuperacion", annotation_position="top left",
              annotation=dict(font_size=10, font_color="#d97706"))

fig.add_vrect(x0=100, x1=115, fillcolor="rgba(187, 247, 208, 0.2)", layer="below", line_width=0,
              annotation_text="Cumplimiento", annotation_position="top left",
              annotation=dict(font_size=10, font_color="#059669"))

fig.add_vrect(x0=115, x1=130, fillcolor="rgba(191, 219, 254, 0.2)", layer="below", line_width=0,
              annotation_text="Alto Rend.", annotation_position="top left",
              annotation=dict(font_size=10, font_color="#2563eb"))

fig.add_vrect(x0=130, x1=200, fillcolor="rgba(233, 213, 255, 0.2)", layer="below", line_width=0,
              annotation_text="Excepcional", annotation_position="top left",
              annotation=dict(font_size=10, font_color="#7c3aed"))

# Lineas de esquemas
fig.add_trace(go.Scatter(
    x=efectividades,
    y=sueldos_actuales,
    name="Esquema Actual",
    line=dict(color="#6366f1", width=2.5),
    hovertemplate="Efectividad: %{x}%<br>Sueldo Actual: S/ %{y:,.0f}<extra></extra>"
))

fig.add_trace(go.Scatter(
    x=efectividades,
    y=sueldos_nuevos,
    name="Esquema Nuevo",
    line=dict(color="#10b981", width=2.5),
    hovertemplate="Efectividad: %{x}%<br>Sueldo Nuevo: S/ %{y:,.0f}<extra></extra>"
))

# Posicion actual
fig.add_trace(go.Scatter(
    x=[efectividad],
    y=[sueldo_actual],
    mode="markers",
    name="Tu posicion (Actual)",
    marker=dict(color="#6366f1", size=12, symbol="circle", line=dict(width=2, color="white")),
    hovertemplate=f"Tu Efectividad: {efectividad}%<br>Sueldo Actual: S/ {sueldo_actual:,.0f}<extra></extra>"
))

fig.add_trace(go.Scatter(
    x=[efectividad],
    y=[sueldo_nuevo],
    mode="markers",
    name="Tu posicion (Nuevo)",
    marker=dict(color="#10b981", size=12, symbol="diamond", line=dict(width=2, color="white")),
    hovertemplate=f"Tu Efectividad: {efectividad}%<br>Sueldo Nuevo: S/ {sueldo_nuevo:,.0f}<extra></extra>"
))

# Lineas verticales de referencia
for x_val, color in [(80, "#dc2626"), (100, "#d97706"), (115, "#059669"), (130, "#2563eb")]:
    fig.add_vline(x=x_val, line_dash="dash", line_color=color, line_width=1, opacity=0.5)

fig.update_layout(
    title=dict(
        text="<b>Comparacion de Esquemas de Comision</b>",
        font=dict(size=16, family="Inter", color="#0f172a")
    ),
    xaxis=dict(
        title="% de Efectividad",
        ticksuffix="%",
        tickvals=[0, 20, 40, 60, 80, 100, 115, 130, 150, 175, 200],
        range=[0, 200],
        gridcolor="rgba(0,0,0,0.05)",
        zeroline=False
    ),
    yaxis=dict(
        title="Sueldo Total (S/)",
        tickformat=",",
        tickprefix="S/ ",
        gridcolor="rgba(0,0,0,0.05)",
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
        font=dict(size=12)
    ),
    hovermode="x unified",
    plot_bgcolor="white",
    paper_bgcolor="white",
    height=450,
    margin=dict(t=80, b=50, l=80, r=40),
    font=dict(family="Inter")
)

st.plotly_chart(fig, use_container_width=True)

# Puntos clave del nuevo esquema
st.markdown('<div class="section-header">Puntos Clave del Nuevo Esquema</div>', unsafe_allow_html=True)

col_k1, col_k2, col_k3, col_k4, col_k5 = st.columns(5)

with col_k1:
    st.markdown("""
    <div class="key-card" style="border-top: 3px solid #dc2626;">
        <div class="key-card-title" style="color: #dc2626;">&lt;80%</div>
        <div class="key-card-subtitle" style="color: #64748b;">→ 0%</div>
        <div class="key-card-label" style="color: #dc2626;">Sin variable</div>
    </div>
    """, unsafe_allow_html=True)

with col_k2:
    st.markdown("""
    <div class="key-card" style="border-top: 3px solid #d97706;">
        <div class="key-card-title" style="color: #d97706;">80-99%</div>
        <div class="key-card-subtitle" style="color: #64748b;">→ 71.5% - 98%</div>
        <div class="key-card-label" style="color: #d97706;">Recuperacion</div>
    </div>
    """, unsafe_allow_html=True)

with col_k3:
    st.markdown("""
    <div class="key-card" style="border-top: 3px solid #059669;">
        <div class="key-card-title" style="color: #059669;">100-115%</div>
        <div class="key-card-subtitle" style="color: #64748b;">→ 100% - 128%</div>
        <div class="key-card-label" style="color: #059669;">Cumplimiento</div>
    </div>
    """, unsafe_allow_html=True)

with col_k4:
    st.markdown("""
    <div class="key-card" style="border-top: 3px solid #2563eb;">
        <div class="key-card-title" style="color: #2563eb;">+115-130%</div>
        <div class="key-card-subtitle" style="color: #64748b;">→ 130%</div>
        <div class="key-card-label" style="color: #2563eb;">Alto Rend.</div>
    </div>
    """, unsafe_allow_html=True)

with col_k5:
    st.markdown("""
    <div class="key-card" style="border-top: 3px solid #7c3aed;">
        <div class="key-card-title" style="color: #7c3aed;">&gt;130%</div>
        <div class="key-card-subtitle" style="color: #64748b;">→ = Efectividad</div>
        <div class="key-card-label" style="color: #7c3aed;">Sin tope</div>
    </div>
    """, unsafe_allow_html=True)

# Tabla de equivalencias
st.markdown('<div class="section-header">Tabla de Equivalencias</div>', unsafe_allow_html=True)

with st.expander("Ver tabla completa de equivalencias", expanded=False):
    # Estilos para las tablas
    st.markdown("""
    <style>
        .equiv-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 1rem;
            font-size: 0.875rem;
        }
        .equiv-table th {
            background: #f8fafc;
            padding: 0.625rem 0.75rem;
            text-align: center;
            font-weight: 600;
            color: #374151;
            border-bottom: 2px solid #e2e8f0;
        }
        .equiv-table td {
            padding: 0.5rem 0.75rem;
            text-align: center;
            border-bottom: 1px solid #f1f5f9;
            color: #475569;
        }
        .equiv-table tr:hover td {
            background: #f8fafc;
        }
        .zone-title {
            display: flex;
            align-items: center;
            gap: 8px;
            font-weight: 600;
            font-size: 0.9375rem;
            margin-bottom: 0.75rem;
            padding: 0.5rem 0.75rem;
            border-radius: 8px;
        }
        .zone-title-red { background: #fef2f2; color: #dc2626; }
        .zone-title-yellow { background: #fffbeb; color: #d97706; }
        .zone-title-green { background: #f0fdf4; color: #059669; }
        .zone-title-blue { background: #eff6ff; color: #2563eb; }
        .zone-title-purple { background: #faf5ff; color: #7c3aed; }
        .formula-card {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 1rem;
            margin-top: 1rem;
        }
        .formula-card h4 {
            margin: 0 0 0.75rem 0;
            font-size: 0.875rem;
            color: #374151;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .formula-item {
            display: flex;
            justify-content: space-between;
            padding: 0.375rem 0;
            font-size: 0.8125rem;
            border-bottom: 1px dashed #e2e8f0;
        }
        .formula-item:last-child { border-bottom: none; }
        .formula-range { color: #64748b; font-weight: 500; }
        .formula-calc { color: #334155; font-family: 'SF Mono', Monaco, monospace; font-size: 0.75rem; }
    </style>
    """, unsafe_allow_html=True)

    col_t1, col_t2, col_t3 = st.columns(3)

    with col_t1:
        # Zona Critica
        st.markdown('<div class="zone-title zone-title-red">🚫 Zona Critica</div>', unsafe_allow_html=True)
        st.markdown("""
        <table class="equiv-table">
            <thead><tr><th>Efectividad</th><th>% Pago</th></tr></thead>
            <tbody><tr><td>&lt; 80%</td><td><strong>0%</strong></td></tr></tbody>
        </table>
        """, unsafe_allow_html=True)

        # Zona Recuperacion 80-95
        st.markdown('<div class="zone-title zone-title-yellow">📈 Recuperacion (80-95%)</div>', unsafe_allow_html=True)
        rows_80_95 = ""
        for e in range(80, 96):
            pago = obtener_porcentaje_pago(e)
            rows_80_95 += f"<tr><td>{e}%</td><td>{pago:.1f}%</td></tr>"
        st.markdown(f"""
        <table class="equiv-table">
            <thead><tr><th>Efectividad</th><th>% Pago</th></tr></thead>
            <tbody>{rows_80_95}</tbody>
        </table>
        """, unsafe_allow_html=True)

    with col_t2:
        # Zona Recuperacion 96-99
        st.markdown('<div class="zone-title zone-title-yellow">📈 Recuperacion (96-99%)</div>', unsafe_allow_html=True)
        rows_96_99 = ""
        for e in range(96, 100):
            pago = obtener_porcentaje_pago(e)
            rows_96_99 += f"<tr><td>{e}%</td><td>{pago:.1f}%</td></tr>"
        st.markdown(f"""
        <table class="equiv-table">
            <thead><tr><th>Efectividad</th><th>% Pago</th></tr></thead>
            <tbody>{rows_96_99}</tbody>
        </table>
        """, unsafe_allow_html=True)

        # Zona Cumplimiento 100-115
        st.markdown('<div class="zone-title zone-title-green">✅ Cumplimiento (100-115%)</div>', unsafe_allow_html=True)
        rows_100_115 = ""
        for e in range(100, 116):
            pago = obtener_porcentaje_pago(e)
            rows_100_115 += f"<tr><td>{e}%</td><td>{pago:.0f}%</td></tr>"
        st.markdown(f"""
        <table class="equiv-table">
            <thead><tr><th>Efectividad</th><th>% Pago</th></tr></thead>
            <tbody>{rows_100_115}</tbody>
        </table>
        """, unsafe_allow_html=True)

    with col_t3:
        # Zona Alto Rendimiento
        st.markdown('<div class="zone-title zone-title-blue">🚀 Alto Rendimiento (+115-130%)</div>', unsafe_allow_html=True)
        st.markdown("""
        <table class="equiv-table">
            <thead><tr><th>Efectividad</th><th>% Pago</th></tr></thead>
            <tbody>
                <tr><td>116% - 130%</td><td><strong>130%</strong></td></tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

        # Zona Excepcional
        st.markdown('<div class="zone-title zone-title-purple">⭐ Excepcional (&gt;130%)</div>', unsafe_allow_html=True)
        st.markdown("""
        <table class="equiv-table">
            <thead><tr><th>Efectividad</th><th>% Pago</th></tr></thead>
            <tbody>
                <tr><td>131%</td><td>131%</td></tr>
                <tr><td>132%</td><td>132%</td></tr>
                <tr><td>140%</td><td>140%</td></tr>
                <tr><td>150%</td><td>150%</td></tr>
                <tr><td>175%</td><td>175%</td></tr>
                <tr><td>200%</td><td>200%</td></tr>
                <tr><td style="color:#7c3aed;"><em>n%</em></td><td style="color:#7c3aed;"><em>= n%</em></td></tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

        # Formulas
        st.markdown("""
        <div class="formula-card">
            <h4>📐 Formulas de Calculo</h4>
            <div class="formula-item">
                <span class="formula-range">80-95%</span>
                <span class="formula-calc">71.5 + (E-80)×1.5</span>
            </div>
            <div class="formula-item">
                <span class="formula-range">96-99%</span>
                <span class="formula-calc">E - 1</span>
            </div>
            <div class="formula-item">
                <span class="formula-range">100%</span>
                <span class="formula-calc">100%</span>
            </div>
            <div class="formula-item">
                <span class="formula-range">101-115%</span>
                <span class="formula-calc">100 + (E-100)×2</span>
            </div>
            <div class="formula-item">
                <span class="formula-range">116-130%</span>
                <span class="formula-calc">130%</span>
            </div>
            <div class="formula-item">
                <span class="formula-range">&gt;130%</span>
                <span class="formula-calc">= Efectividad</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Tabla de escenarios
st.markdown('<div class="section-header">Tabla de Escenarios</div>', unsafe_allow_html=True)

escenarios_completos = (
    [59] +
    list(range(80, 116)) +
    [120, 130, 131, 132, 133, 134, 135, 140, 150, 175, 200]
)

datos_escenarios = []

for e in escenarios_completos:
    s_actual = calcular_sueldo_actual(sueldo_fijo, sueldo_variable, e)
    s_nuevo = calcular_sueldo_nuevo(sueldo_fijo, sueldo_variable, e)
    dif = s_nuevo - s_actual
    pago = obtener_porcentaje_pago(e)

    if e < 80:
        zona = "Critica"
    elif e < 100:
        zona = "Recuperacion"
    elif e < 115:
        zona = "Cumplimiento"
    elif e <= 130:
        zona = "Alto Rend."
    else:
        zona = "Excepcional"

    datos_escenarios.append({
        "Zona": zona,
        "Efectividad": f"{e}%",
        "% Pago": f"{pago:.1f}%" if pago % 1 != 0 else f"{pago:.0f}%",
        "Esq. Actual": f"S/ {s_actual:,.0f}",
        "Esq. Nuevo": f"S/ {s_nuevo:,.0f}",
        "Diferencia": f"{'+'if dif>=0 else ''}S/ {dif:,.0f}",
        "Beneficio": "Nuevo" if dif > 0 else ("Igual" if dif == 0 else "Actual")
    })

df_escenarios = pd.DataFrame(datos_escenarios)

zonas_disponibles = ["Todas"] + list(df_escenarios["Zona"].unique())
zona_seleccionada = st.selectbox(
    "Filtrar por zona:",
    zonas_disponibles,
    index=0
)

if zona_seleccionada != "Todas":
    df_filtrado = df_escenarios[df_escenarios["Zona"] == zona_seleccionada]
else:
    df_filtrado = df_escenarios

st.dataframe(
    df_filtrado,
    use_container_width=True,
    hide_index=True,
    height=400
)

st.caption(f"Mostrando {len(df_filtrado)} de {len(df_escenarios)} escenarios")

# Resumen ejecutivo
st.markdown('<div class="section-header">Resumen</div>', unsafe_allow_html=True)

punto_equilibrio = None
for e in range(0, 201):
    s_a = calcular_sueldo_actual(sueldo_fijo, sueldo_variable, e)
    s_n = calcular_sueldo_nuevo(sueldo_fijo, sueldo_variable, e)
    if s_n >= s_a and e >= 80:
        punto_equilibrio = e
        break

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-box">
        <h4 style="margin:0 0 12px 0; color: #0369a1;">Puntos Clave</h4>
        <ul style="margin:0; padding-left: 20px; color: #334155; line-height: 1.8;">
            <li><strong>Por debajo del 80%:</strong> Solo sueldo fijo (0% variable)</li>
            <li><strong>Entre 80% y 95%:</strong> Pago desde 71.5%, +1.5% por cada 1%</li>
            <li><strong>Entre 96% y 99%:</strong> +1% por cada 1%</li>
            <li><strong>Al 100%:</strong> Exactamente el 100% de tu variable</li>
            <li><strong>Entre 101% y 115%:</strong> +2% por cada 1% adicional</li>
            <li><strong>Mas de 115% hasta 130%:</strong> Multiplicador fijo de 130%</li>
            <li><strong>Mas de 130%:</strong> Tu multiplicador = tu efectividad</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if punto_equilibrio:
        st.markdown(f"""
        <div class="success-box">
            <h4 style="margin:0 0 12px 0; color: #059669;">Tu Punto de Equilibrio</h4>
            <p style="margin:0; color: #334155;">
                A partir del <strong>{punto_equilibrio}% de efectividad</strong>, el nuevo esquema
                te beneficia mas que el actual.
            </p>
            <p style="margin: 12px 0 0 0; font-size: 0.875rem; color: #64748b;">
                Si consistentemente superas este umbral, el nuevo esquema es mejor para ti.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="warning-box">
            <h4 style="margin:0 0 12px 0; color: #d97706;">Consideracion</h4>
            <p style="margin:0; color: #334155;">
                El nuevo esquema premia el alto rendimiento pero tiene mayor riesgo
                si no alcanzas el 80% de tu cuota.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.8125rem; padding: 1rem 0;">
    <p style="margin: 0;">Simulador de Comisiones | Area Comercial</p>
    <p style="margin: 0.25rem 0 0 0;">Los calculos son ilustrativos. Consulta con tu supervisor para detalles especificos.</p>
</div>
""", unsafe_allow_html=True)

import streamlit as st
import sqlite3
from datetime import date, timedelta

# 1. CONFIGURACIÓN PREMIUM OPTIMIZADA PARA MÓVIL (ESTILO BANCOLOMBIA)
st.set_page_config(page_title="ARYA OS", page_icon="📱", layout="centered")

st.markdown("""
    <style>
    .block-container {
        max-width: 420px !important;
        padding-top: 0px !important; /* Espacio superior eliminado */
        margin-top: 0px !important;
        padding-bottom: 4rem !important; /* Espacio para el menú inferior */
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        margin: 0 auto !important;
        background-color: #FFFFFF;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.05);
        border-radius: 24px;
    }
    div[data-testid="stAppViewBlockContainer"] {
        padding-top: 0px !important;
        margin-top: 0px !important;
    }
    body { background-color: #F6F8FA !important; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    h1 { font-size: 24px !important; font-family: '-apple-system', BlinkMacSystemFont, sans-serif; font-weight: 800; color: #1A1A1A; text-align: center; margin-bottom: 5px !important; }
    h2 { font-size: 18px !important; font-weight: 700; color: #1A1A1A; margin-top: 10px !important; }
    h3 { font-size: 15px !important; font-weight: 700; color: #1A1A1A; margin-top: 15px !important; }
    h4 { font-size: 13px !important; font-weight: 600; margin: 0 !important; }
    p, label, .stMarkdown { font-size: 13px !important; color: #666666; }
    
    .stNumberInput div div input, .stTextInput div div input, .stTextArea div div textarea { padding: 6px 10px !important; font-size: 14px !important; border-radius: 8px !important; }
    
    .stButton>button { background-color: #4A90E2; color: white; border-radius: 10px; width: 100%; font-weight: bold; font-size: 13px !important; padding: 8px !important; border: none; }
    
    /* Mosaico y Tarjetas Ejecutivas */
    .dash-card { background-color: #F8F9FA; padding: 12px; border-radius: 14px; border: 1px solid #EAEAEA; margin-bottom: 10px; }
    
    /* Menú de Navegación Inferior Estacionario */
    .nav-box { display: flex; justify-content: space-around; background-color: #1A1A1A; padding: 10px 0; border-radius: 16px; margin-top: 20px; }
    
    /* Forzar cuadrícula rígida 2x2 en móviles */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        gap: 8px !important;
    }
    [data-testid="stHorizontalBlock"] [data-testid="column"] {
        flex: 1 1 50% !important;
        min-width: 0px !important;
    }
    
    /* Compactación premium para contenedores (tarjetas) en móvil */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        padding: 6px 8px !important;
        margin-bottom: 4px !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stVerticalBlock"] {
        gap: 4px !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] h4 {
        font-size: 11px !important;
        margin-bottom: 2px !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMetricValue"] {
        font-size: 14px !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMetricLabel"] {
        font-size: 9px !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] button {
        padding: 2px 6px !important;
        font-size: 10px !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown, 
    div[data-testid="stVerticalBlockBorderWrapper"] .stMarkdown p,
    div[data-testid="stVerticalBlockBorderWrapper"] label,
    div[data-testid="stVerticalBlockBorderWrapper"] span,
    div[data-testid="stVerticalBlockBorderWrapper"] li {
        font-size: 10px !important;
        margin: 0 !important;
        line-height: 1.2 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. BASE DE DATOS E INFRAESTRUCTURA LOCK-IN
def init_db():
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ingresos (mes_anio TEXT, fuente TEXT, valor INTEGER, PRIMARY KEY (mes_anio, fuente))''')
    c.execute('''CREATE TABLE IF NOT EXISTS mercado_gastos (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, item TEXT, comprado INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS suenos (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT UNIQUE)''')
    c.execute("INSERT OR IGNORE INTO su सपनों (nombre) VALUES ('✈️ Viajar')".replace('su सपनों', 'suenos'))
    c.execute("INSERT OR IGNORE INTO suenos (nombre) VALUES ('📚 Estudiar')")
    c.execute('''CREATE TABLE IF NOT EXISTS pagos_realizados (mes_anio TEXT PRIMARY KEY, estado INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS pendientes (id INTEGER PRIMARY KEY AUTOINCREMENT, bloque TEXT, tarea TEXT, completada INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS despensa (id INTEGER PRIMARY KEY AUTOINCREMENT, producto TEXT, faltante INTEGER DEFAULT 1)''')
    c.execute('''CREATE TABLE IF NOT EXISTS salud_control (fecha TEXT PRIMARY KEY, ejercicio INTEGER DEFAULT 0, nivel_estres TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS agenda (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, bloque TEXT, actividad TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS proyectos_eventos (id INTEGER PRIMARY KEY AUTOINCREMENT, proyecto TEXT, titulo TEXT, fecha TEXT, tipo TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- FUNCIONES DE CALENDARIO, HÁBITOS Y FINANZAS ---
def calcular_racha_ejercicio():
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('SELECT fecha, ejercicio FROM salud_control ORDER BY fecha DESC')
    filas = c.fetchall()
    conn.close()
    
    racha = 0
    hoy = date.today()
    for i in range(30):
        dia_verificar = (hoy - timedelta(days=i)).strftime("%Y-%m-%d")
        ejercicio_dia = 0
        for f, ej in filas:
            if f == dia_verificar:
                ejercicio_dia = ej
                break
        if ejercicio_dia == 1:
            racha += 1
        else:
            if i > 0:
                break
            if i == 0:
                continue
            else:
                break
    return racha

def obtener_historial_ejercicio_emojis():
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('SELECT fecha, ejercicio FROM salud_control ORDER BY fecha DESC LIMIT 7')
    filas = c.fetchall()
    conn.close()
    
    hoy = date.today()
    emojis = []
    for i in range(6, -1, -1):
        dia = hoy - timedelta(days=i)
        dia_str = dia.strftime("%Y-%m-%d")
        hecho = False
        for f, ej in filas:
            if f == dia_str and ej == 1:
                hecho = True
                break
        emojis.append("🟢" if hecho else "⚪")
    return " ".join(emojis)

def obtener_eventos_calendario():
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('SELECT proyecto, titulo, fecha, tipo FROM proyectos_eventos ORDER BY fecha ASC')
    filas = c.fetchall()
    conn.close()
    return filas

def populate_sample_events():
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM proyectos_eventos')
    if c.fetchone()[0] == 0:
        hoy = date.today()
        eventos = [
            ('💼 Alcaldía', 'Entrega de Informe Ejecutivo', (hoy + timedelta(days=2)).strftime("%Y-%m-%d"), 'Hito'),
            ('🌟 PMO Hub', 'Reunión de Alineación Semanal', (hoy + timedelta(days=4)).strftime("%Y-%m-%d"), 'Reunión'),
            ('💼 Alcaldía', 'Comité Técnico Distrital', (hoy + timedelta(days=12)).strftime("%Y-%m-%d"), 'Hito'),
            ('🌟 PMO Hub', 'Cierre Financiero Mensual', (hoy + timedelta(days=20)).strftime("%Y-%m-%d"), 'Entregable'),
            ('💼 Alcaldía', 'Planeación Anual de Inversiones', (hoy + timedelta(days=45)).strftime("%Y-%m-%d"), 'Hito')
        ]
        c.executemany('INSERT INTO proyectos_eventos (proyecto, titulo, fecha, tipo) VALUES (?, ?, ?, ?)', eventos)
        conn.commit()
    conn.close()

def obtener_total_ingresos():
    mes_actual = date.today().strftime("%Y-%m")
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('SELECT SUM(valor) FROM ingresos WHERE mes_anio = ?', (mes_actual,))
    res = c.fetchone()[0]
    conn.close()
    return res if res else (3500000 + 1800000)

populate_sample_events()

def guardar_ingreso(fuente, valor):
    mes_actual = date.today().strftime("%Y-%m")
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO ingresos (mes_anio, fuente, valor) VALUES (?, ?, ?)', (mes_actual, fuente, valor))
    conn.commit()
    conn.close()

def registrar_confirmacion_pago(estado):
    mes_actual = date.today().strftime("%Y-%m")
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO pagos_realizados (mes_anio, estado) VALUES (?, ?)', (mes_actual, estado))
    conn.commit()
    conn.close()

def obtener_estado_pago():
    mes_actual = date.today().strftime("%Y-%m")
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('SELECT estado FROM pagos_realizados WHERE mes_anio = ?', (mes_actual,))
    res = c.fetchone()
    conn.close()
    return res[0] if res else 0

def obtener_suenos():
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute("SELECT nombre FROM su सपनों".replace('su सपनों', 'suenos'))
    lista = [fila[0] for fila in c.fetchall()]
    conn.close()
    return lista

def agregar_pendiente(bloque, tarea):
    if tarea:
        conn = sqlite3.connect('arya.db')
        c = conn.cursor()
        c.execute('INSERT INTO pendientes (bloque, tarea, completada) VALUES (?, ?, 0)', (bloque, tarea))
        conn.commit()
        conn.close()

def obtener_pendientes(bloque):
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('SELECT id, tarea, completada FROM pendientes WHERE bloque = ? AND completada = 0', (bloque,))
    filas = c.fetchall()
    conn.close()
    return filas

def contar_todos_los_pendientes():
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM pendientes WHERE completada = 0')
    count = c.fetchone()[0]
    conn.close()
    return count

def marcar_pendiente_listo(id_tarea):
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('UPDATE pendientes SET completada = 1 WHERE id = ?', (id_tarea,))
    conn.commit()
    conn.close()

def guardar_salud(ejercicio, estres):
    fecha_actual = date.today().strftime("%Y-%m-%d")
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO salud_control (fecha, ejercicio, nivel_estres) VALUES (?, ?, ?)', (fecha_actual, ejercicio, estres))
    conn.commit()
    conn.close()

def obtener_ultimo_estres():
    fecha_actual = date.today().strftime("%Y-%m-%d")
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('SELECT nivel_estres FROM salud_control WHERE fecha = ?', (fecha_actual,))
    res = c.fetchone()
    conn.close()
    return res[0] if res else "Tranquila 🟢"

def guardar_sabiduria(modulo, contenido):
    fecha_actual = date.today().strftime("%Y-%m-%d")
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('INSERT INTO agenda (fecha, bloque, actividad) VALUES (?, ?, ?)', (fecha_actual, modulo, contenido))
    conn.commit()
    conn.close()

# --- MANEJO DE ESTADO DE NAVEGACIÓN ---
if "menu_móvil" not in st.session_state:
    st.session_state.menu_móvil = "🌿 Mi Día"

# 3. INTERFAZ MÓVIL
st.markdown("<h1>📱 ARYA OS</h1>", unsafe_allow_html=True)
ocultar_saldos = st.toggle("👁️ Ocultar saldos de pantalla", value=False)
st.divider()

# ==========================================
# VISTA: 🌿 MI DÍA
# ==========================================
if st.session_state.menu_móvil == "🌿 Mi Día":
    st.write("### ¡Hola, Norma! ✨")
    
    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        hoy_str = date.today().strftime("%Y-%m-%d")
        conn = sqlite3.connect('arya.db')
        c = conn.cursor()
        c.execute('SELECT ejercicio FROM salud_control WHERE fecha = ?', (hoy_str,))
        res_hoy = c.fetchone()
        conn.close()
        ejercicio_hoy = res_hoy[0] if res_hoy else 0
        
        with st.container(border=True):
            st.markdown("<h4>🏃 Hábitos</h4>", unsafe_allow_html=True)
            hizo_ejercicio = st.toggle("¡Entrené!", value=bool(ejercicio_hoy), key="habito_ejercicio")
            if hizo_ejercicio != bool(ejercicio_hoy):
                guardar_salud(1 if hizo_ejercicio else 0, obtener_ultimo_estres())
                st.rerun()
            st.caption(f"Racha: {calcular_racha_ejercicio()} d")

    with row1_col2:
        with st.container(border=True):
            st.markdown("<h4>📅 Agenda</h4>", unsafe_allow_html=True)
            eventos = obtener_eventos_calendario()
            hoy = date.today()
            evs_sem = [ev for ev in eventos if hoy.strftime("%Y-%m-%d") <= ev[2] <= (hoy + timedelta(days=7)).strftime("%Y-%m-%d")]
            if evs_sem:
                st.markdown(f"**Próx:** {evs_sem[0][1][:12]}...")
            else:
                st.caption("Sin hitos")

    row2_col1, row2_col2 = st.columns(2)
    
    with row2_col1:
        total_ing = obtener_total_ingresos()
        saldo_lib = max(0, total_ing - 4050000)
        presupuesto_diario = saldo_lib // 30
        val_disp = f"${presupuesto_diario:,}" if not ocultar_saldos else "$ ***"
        
        with st.container(border=True):
            st.markdown("<h4>💳 Diario</h4>", unsafe_allow_html=True)
            st.metric(label="Disp.", value=val_disp)

    with row2_col2:
        pendientes_totales = contar_todos_los_pendientes()
        with st.container(border=True):
            st.markdown("<h4>📋 Tareas</h4>", unsafe_allow_html=True)
            st.metric(label="Pend.", value=f"{pendientes_totales}")

    st.markdown("---")
    with st.expander("🔍 Ver Detalles del Calendario Completo"):
        tab_sem, tab_mes, tab_an = st.tabs(["Semana", "Mes", "Año"])
        with tab_sem:
            if evs_sem:
                for proj, tit, fec, tipo in evs_sem: st.markdown(f"🔹 **{proj}**: {tit} ({fec})")
            else:
                st.caption("No hay hitos esta semana")
        with tab_mes:
            evs_mes = [ev for ev in eventos if hoy.strftime("%Y-%m-%d") <= ev[2] <= (hoy + timedelta(days=30)).strftime("%Y-%m-%d")]
            for proj, tit, fec, tipo in evs_mes: st.markdown(f"🔹 **{proj}**: {tit} ({fec})")
        with tab_an:
            for proj, tit, fec, tipo in eventos[:5]: st.markdown(f"🔹 **{proj}**: {tit} ({fec})")

# ==========================================
# VISTA:🚀 FINANZAS
# ==========================================
elif st.session_state.menu_móvil == "🚀 Finanzas":
    st.markdown("### 🚀 Finanzas Personales")
    with st.container(border=True):
        st.caption("Contenedor estratégico listo para tus flujos personales.")

# ==========================================
# VISTAS RESTANTES (MANTENIENDO LÓGICA)
# ==========================================
elif st.session_state.menu_móvil == "💰 Fuel":
    st.markdown("### Detalle de Fuel")
    ingreso_t1 = st.number_input("💼 Trabajo 1", min_value=0, value=3500000, step=50000, key="f_t1")
    guardar_ingreso("Trabajo 1", ingreso_t1)
    ingreso_t2 = st.number_input("🚀 Trabajo 2", min_value=0, value=1800000, step=50000, key="f_t2")
    guardar_ingreso("Trabajo 2", ingreso_t2)
    
    total_ingresos = ingreso_t1 + ingreso_t2
    pago_efectuado = obtener_estado_pago()
    if pago_efectuado == 1:
        st.success("✅ Al día con compromisos.")
        if st.button("🔄 Desmarcar"): registrar_confirmacion_pago(0); st.rerun()
    else:
        st.warning("⚠️ Compromisos pendientes.")
        if st.button("🚀 Marcar todo como Pagado"): registrar_confirmacion_pago(1); st.rerun()

elif st.session_state.menu_móvil == "🌱 Core":
    st.markdown("### Control Diario")
    bloque = st.selectbox("Frente:", ["🎓 Maestría", "💼 Alcaldía", "🌟 Voluntarios PMO", "🏡 Personales"])
    nueva_tarea = st.text_input("Nuevo pendiente:", key="c_todo")
    if st.button("➕ Añadir"):
        agregar_pendiente(bloque, nueva_tarea)
        st.rerun()

elif st.session_state.menu_móvil == "✨ Anchor":
    st.markdown("### Mi Ancla de Sabiduría")
    modulo_iglesia = st.selectbox("Módulo:", ["⛪ Palabra", "🙏 Liderazgo"])
    contenido = st.text_area("Revelaciones:")
    if st.button("🔥 Atesorar"):
        if contenido:
            guardar_sabiduria(modulo_iglesia, contenido)
            st.success("Guardado.")

st.divider()

# MENÚ INFERIOR ESTACIONARIO
col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
with col_m1:
    if st.button("🌿 Mi Día"): st.session_state.menu_móvil = "🌿 Mi Día"; st.rerun()
with col_m2:
    if st.button("💰 Fuel"): st.session_state.menu_móvil = "💰 Fuel"; st.rerun()
with col_m3:
    if st.button("🚀 Finanzas"): st.session_state.menu_móvil = "🚀 Finanzas"; st.rerun()
with col_m4:
    if st.button("🌱 Core"): st.session_state.menu_móvil = "🌱 Core"; st.rerun()
with col_m5:
    if st.button("✨ Anchor"): st.session_state.menu_móvil = "✨ Anchor"; st.rerun()
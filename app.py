import streamlit as st
import sqlite3
from datetime import date, timedelta

# 1. CONFIGURACIÓN PREMIUM OPTIMIZADA PARA MÓVIL (ESTILO BANCOLOMBIA)
st.set_page_config(page_title="ARYA OS", page_icon="📱", layout="centered")

st.markdown("""
    <style>
    .block-container {
        max-width: 420px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 5rem !important; /* Espacio para el menú inferior */
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
        margin: 0 auto !important;
        background-color: #FFFFFF;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.05);
        border-radius: 24px;
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
    .circle-menu { display: flex; justify-content: space-around; margin: 15px 0; text-align: center; }
    .circle-item { font-size: 11px; font-weight: 600; color: #1A1A1A; }
    .circle-icon { width: 45px; height: 45px; border-radius: 50%; background-color: #F0F2F6; display: flex; align-items: center; justify-content: center; margin: 0 auto 5px auto; font-size: 18px; }
    
    /* Menú de Navegación Inferior Estacionario */
    .nav-box { display: flex; justify-content: space-around; background-color: #1A1A1A; padding: 10px 0; border-radius: 16px; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 2. BASE DE DATOS E INFRAESTRUCTURA LOCK-IN
def init_db():
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS ingresos (mes_anio TEXT, fuente TEXT, valor INTEGER, PRIMARY KEY (mes_anio, fuente))''')
    c.execute('''CREATE TABLE IF NOT EXISTS mercado_gastos (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, item TEXT, comprado INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS suenos (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT UNIQUE)''')
    c.execute("INSERT OR IGNORE INTO suenos (nombre) VALUES ('✈️ Viajar')")
    c.execute("INSERT OR IGNORE INTO suenos (nombre) VALUES ('📚 Estudiar')")
    c.execute('''CREATE TABLE IF NOT EXISTS pagos_realizados (mes_anio TEXT PRIMARY KEY, estado INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS pendientes (id INTEGER PRIMARY KEY AUTOINCREMENT, bloque TEXT, tarea TEXT, completada INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS despensa (id INTEGER PRIMARY KEY AUTOINCREMENT, producto TEXT, faltante INTEGER DEFAULT 1)''')
    c.execute('''CREATE TABLE IF NOT EXISTS salud_control (fecha TEXT PRIMARY KEY, ejercicio INTEGER DEFAULT 0, nivel_estres TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS agenda (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, bloque TEXT, actividad TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- LÓGICAS COMERCIALES ---
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
    c.execute("SELECT nombre FROM suenos")
    lista = [fila[0] for fila in c.fetchall()]
    conn.close()
    return lista

def guardar_gasto_hormiga(item, valor):
    fecha_actual = date.today().strftime("%Y-%m-%d")
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('INSERT INTO mercado_gastos (fecha, item, comprado) VALUES (?, ?, ?)', (fecha_actual, item, valor))
    conn.commit()
    conn.close()

def obtener_gastos_hormiga_semana():
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    siete_dias_atras = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
    c.execute("SELECT SUM(comprado) FROM mercado_gastos WHERE fecha >= ?", (siete_dias_atras,))
    total = c.fetchone()[0]
    conn.close()
    return total if total else 0

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

def agregar_a_despensa(producto):
    if producto:
        conn = sqlite3.connect('arya.db')
        c = conn.cursor()
        c.execute('INSERT INTO despensa (producto, faltante) VALUES (?, 1)', (producto,))
        conn.commit()
        conn.close()

def obtener_lista_mercado():
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('SELECT id, producto FROM despensa WHERE faltante = 1')
    filas = c.fetchall()
    conn.close()
    return filas

def comprar_producto(id_prod):
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('DELETE FROM despensa WHERE id = ?', (id_prod,))
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
    return res[0] if res else "No registrado ⚪"

def guardar_sabiduria(modulo, contenido):
    fecha_actual = date.today().strftime("%Y-%m-%d")
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('INSERT INTO agenda (fecha, bloque, actividad) VALUES (?, ?, ?)', (fecha_actual, modulo, contenido))
    conn.commit()
    conn.close()

def obtener_ultimo_aprendizaje():
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute("SELECT bloque, actividad FROM agenda WHERE bloque LIKE '%⛪%' OR bloque LIKE '%🙏%' OR ... ORDER BY id DESC LIMIT 1")
    res = c.fetchone()
    conn.close()
    return res if res else ("Ninguno", "Aún no hay registros")

# --- MANEJO DE ESTADO DE NAVEGACIÓN (BOTTOM BAR SIMULATION) ---
if "menu_móvil" not in st.session_state:
    st.session_state.menu_móvil = "⚡ Inicio"

# 3. INTERFAZ MÓVIL EVOLUCIONADA
st.markdown("<h1>📱 ARYA OS</h1>", unsafe_allow_html=True)

# GESTOR DE PRIVACIDAD (Estilo Bancolombia)
ocultar_saldos = st.toggle("👁️ Ocultar saldos de pantalla", value=False)

st.divider()

# ==========================================
# VISTA: INICIO (DASHBOARD COMPACTO)
# ==========================================
if st.session_state.menu_móvil == "⚡ Inicio":
    st.markdown("### Hola, Norma ✨")
    st.caption("Tu vista unificada de control:")
    
    # MOSAICO ACCESOS DIRECTOS (Estilo Círculos de Bancolombia)
    st.markdown("""
    <div class="circle-menu">
        <div class="circle-item"><div class="circle-icon" style="background-color:#FFEAA7;">💼</div>Motores</div>
        <div class="circle-item"><div class="circle-icon" style="background-color:#55E6C1;">🏃</div>Core</div>
        <div class="circle-item"><div class="circle-icon" style="background-color:#D6A2E8;">⚓</div>Anchor</div>
    </div>
    """, unsafe_allow_html=True)
    
    # RESUMEN COMPACTO EJECUTIVO
    estado_pago_actual = obtener_estado_pago()
    alerta_html = "<span style='color: #2ECC71;'>🛡️ Al día</span>" if estado_pago_actual == 1 else "<span style='color: #E74C3C;'>⚠️ Pendiente</span>"
    total_pendientes_hoy = contar_todos_los_pendientes()
    estres_hoy = obtener_ultimo_estres()
    
    val_t1 = "$3.500.000" if not ocultar_saldos else "$ ***"
    val_t2 = "$1.800.000" if not ocultar_saldos else "$ ***"
    
    st.markdown(f"""
    <div class="dash-card">
        <h4>💰 Fuel (Finanzas)</h4>
        <p style='margin:4px 0;'>T1: {val_t1} | T2: {val_t2}</p>
        <p style='margin:4px 0;'>Compromisos fijos: <b>{alerta_html}</b></p>
    </div>
    <div class="dash-card">
        <h4>🌱 Core (Bienestar y Agenda)</h4>
        <p style='margin:4px 0;'>Tareas activas: <b>{total_pendientes_hoy} pendientes</b></p>
        <p style='margin:4px 0;'>Estrés hoy: <b>{estres_hoy}</b></p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# VISTA: FUEL (FINANZAS AL DETALLE)
# ==========================================
elif st.session_state.menu_móvil == "💰 Fuel":
    st.markdown("### Detalle de Fuel")
    
    ingreso_t1 = st.number_input("💼 Trabajo 1", min_value=0, value=3500000, step=50000, key="f_t1")
    guardar_ingreso("Trabajo 1", ingreso_t1)
    ingreso_t2 = st.number_input("🚀 Trabajo 2", min_value=0, value=1800000, step=50000, key="f_t2")
    guardar_ingreso("Trabajo 2", ingreso_t2)
    
    total_ingresos = ingreso_t1 + ingreso_t2
    
    # Control confirmación real de pagos
    pago_efectuado = obtener_estado_pago()
    if pago_efectuado == 1:
        st.success("✅ Estás al día con tus compromisos mensuales.")
        if st.button("🔄 Desmarcar pagos"): registrar_confirmacion_pago(0); st.rerun()
    else:
        st.warning("⚠️ Compromisos fijos pendientes de transferencia.")
        if st.button("🚀 Marcar todo como Pagado"): registrar_confirmacion_pago(1); st.rerun()
        
    if total_ingresos >= 4050000: # Suma base gastos
        saldo_libertad = total_ingresos - 4050000
        txt_saldo = f"${saldo_libertad:,}" if not ocultar_saldos else "$ ***"
        st.markdown(f"<h3 style='text-align:center;'>💸 Saldo Libertad: <span style='color:#4A90E2;'>{txt_saldo}</span></h3>", unsafe_allow_html=True)
        
        with st.expander("✈️ Mi Banco de Sueños"):
            lista_suenos = obtener_suenos()
            if lista_suenos:
                for sueno in lista_suenos:
                    st.caption(f"🎯 {sueno} (Asignado dinámicamente)")

# ==========================================
# VISTA: CORE (GESTIÓN DIARIA)
# ==========================================
elif st.session_state.menu_móvil == "🌱 Core":
    st.markdown("### Control Diario y Escudo")
    hizo_ejercicio = st.checkbox("🏃 ¡Hoy entrené!", key="c_health")
    estado_estres = st.select_slider("⚡ Estrés Mental:", options=["Tranquila 🟢", "Moderada 🟡", "Alerta Estrés 🔴"], value="Tranquila 🟢")
    if st.button("💾 Guardar Estado"):
        guardar_salud(1 if hizo_ejercicio else 0, estado_estres)
        st.toast("Salud registrada.")
        
    st.divider()
    bloque = st.selectbox("Frente Estratégico:", ["🎓 Maestría", "💼 Alcaldía", "🌟 Voluntarios PMO", "🏛️ MIRA", "🏡 Personales"])
    nueva_tarea = st.text_input("Nuevo pendiente:", placeholder="Escribe aquí...", key="c_todo")
    if st.button("➕ Descargar Tarea"):
        agregar_pendiente(bloque, nueva_tarea)
        st.success("¡Mentalmente liberada!")
        st.rerun()
        
    tareas = obtener_pendientes(bloque)
    for id_t, tarea, comp in tareas:
        col_a, col_b = st.columns([4, 1])
        col_a.markdown(f"• {tarea}")
        if col_b.button("✓", key=f"c_done_{id_t}"):
            marcar_pendiente_listo(id_t)
            st.rerun()

# ==========================================
# VISTA: ANCHOR (SABIDURÍA)
# ==========================================
elif st.session_state.menu_móvil == "✨ Anchor":
    st.markdown("### Mi Ancla de Sabiduría")
    modulo_iglesia = st.selectbox("Módulo:", ["Domingo de Palabra ⛪", "Liderazgo 🙏", "Estudios 📖"])
    contenido = st.text_area("Revelaciones:", placeholder="Atesora la palabra...")
    if st.button("🔥 Atesorar"):
        if contenido:
            guardar_sabiduria(modulo_iglesia, contenido)
            st.success("Guardado en tu bitácora eterna.")
            st.rerun()

st.divider()

# MENÚ INFERIOR ESTACIONARIO DE IMPACTO (Estilo Bancolombia App)
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    if st.button("⚡ Inicio"): st.session_state.menu_móvil = "⚡ Inicio"; st.rerun()
with col_m2:
    if st.button("💰 Fuel"): st.session_state.menu_móvil = "💰 Fuel"; st.rerun()
with col_m3:
    if st.button("🌱 Core"): st.session_state.menu_móvil = "🌱 Core"; st.rerun()
with col_m4:
    if st.button("✨ Anchor"): st.session_state.menu_móvil = "✨ Anchor"; st.rerun()

# Despliegue UX Bancolombia
import streamlit as st
import sqlite3
from datetime import date, timedelta

# 1. CONFIGURACIÓN PREMIUM OPTIMIZADA PARA MÓVIL
st.set_page_config(page_title="ARYA OS", page_icon="📱", layout="centered")

st.markdown("""
    <style>
    .block-container {
        max-width: 420px !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
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
    h2 { font-size: 20px !important; font-weight: 700; color: #1A1A1A; }
    h3 { font-size: 16px !important; font-weight: 700; color: #1A1A1A; margin-top: 15px !important; }
    h4 { font-size: 14px !important; font-weight: 600; margin: 0 !important; }
    p, label, .stMarkdown { font-size: 13px !important; color: #666666; }
    
    .stNumberInput div div input { padding: 6px 10px !important; font-size: 14px !important; border-radius: 8px !important; }
    .stTextInput div div input { padding: 6px 10px !important; font-size: 14px !important; border-radius: 8px !important; }
    
    .stButton>button { background-color: #4A90E2; color: white; border-radius: 10px; width: 100%; font-weight: bold; font-size: 14px !important; padding: 10px !important; border: none; }
    </style>
    """, unsafe_allow_html=True)

# 2. ARQUITECTURA DE BASE DE DATOS (CON TABLA DE SUEÑOS PARAMETRIZABLES)
def init_db():
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS compromisos
                 (mes_anio TEXT PRIMARY KEY, arriendo INTEGER DEFAULT 0, servicios INTEGER DEFAULT 0,
                  tarjeta INTEGER DEFAULT 0, diezmo INTEGER DEFAULT 0, mami INTEGER DEFAULT 0, comida INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS ingresos
                 (mes_anio TEXT, fuente TEXT, valor INTEGER, PRIMARY KEY (mes_anio, fuente))''')
    c.execute('''CREATE TABLE IF NOT EXISTS mercado
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, item TEXT, comprado INTEGER DEFAULT 0)''')
    
    # NUEVA TABLA: Parametrizar los sueños de cada usuario
    c.execute('''CREATE TABLE IF NOT EXISTS suenos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT UNIQUE)''')
    
    # Insertar valores por defecto la primera vez para que no aparezca vacío
    c.execute("INSERT OR IGNORE INTO suenos (nombre) VALUES ('✈️ Viajar')")
    c.execute("INSERT OR IGNORE INTO suenos (nombre) VALUES ('📚 Estudiar')")
    
    conn.commit()
    conn.close()

init_db()

# LÓGICAS DE OPERACIÓN
def guardar_ingreso(fuente, valor):
    mes_actual = date.today().strftime("%Y-%m")
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO ingresos (mes_anio, fuente, valor) VALUES (?, ?, ?)', (mes_actual, fuente, valor))
    conn.commit()
    conn.close()

def obtener_ingresos_mes(mes):
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute("SELECT fuente, valor FROM ingresos WHERE mes_anio = ?", (mes,))
    filas = c.fetchall()
    conn.close()
    return {fuente: valor for fuente, valor in filas}

def calcular_comparativa_ingresos():
    mes_actual = date.today().strftime("%Y-%m")
    mes_anterior = (date.today() - timedelta(days=30)).strftime("%Y-%m")
    ingresos_actuales = obtener_ingresos_mes(mes_actual)
    ingresos_anteriores = obtener_ingresos_mes(mes_anterior)
    comparativa = {}
    for fuente, valor_actual in ingresos_actuales.items():
        valor_anterior = ingresos_anteriores.get(fuente, 0)
        comparativa[fuente] = {"actual": valor_actual, "anterior": valor_anterior, "diferencia": valor_actual - valor_anterior}
    return comparativa

def guardar_gasto_hormiga(item, valor):
    fecha_actual = date.today().strftime("%Y-%m-%d")
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute('INSERT INTO mercado (fecha, item, comprado) VALUES (?, ?, ?)', (fecha_actual, item, valor))
    conn.commit()
    conn.close()

def obtener_gastos_hormiga_semana():
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    siete_dias_atras = (date.today() - timedelta(days=7)).strftime("%Y-%m-%d")
    c.execute("SELECT SUM(comprado) FROM mercado WHERE fecha >= ?", (siete_dias_atras,))
    total = c.fetchone()[0]
    conn.close()
    return total if total else 0

# NUEVAS LÓGICAS PARA CONTROL DE SUEÑOS
def obtener_suenos():
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute("SELECT nombre FROM suenos")
    lista = [fila[0] for fila in c.fetchall()]
    conn.close()
    return lista

def agregar_nuevo_sueno(nombre):
    if nombre:
        conn = sqlite3.connect('arya.db')
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO suenos (nombre) VALUES (?)", (nombre,))
        conn.commit()
        conn.close()

def borrar_suenos():
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute("DELETE FROM suenos")
    conn.commit()
    conn.close()

# 3. INTERFAZ EN CUADRO MÓVIL
st.markdown("<h1>📱 ARYA OS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 20px;'>Tu Dinero, Tus Reglas ✨</p>", unsafe_allow_html=True)

# PARAMETRIZACIÓN: Configurar Sueños (Oculto en un acordeón casual)
with st.expander("⚙️ Personalizar mis Tarjetas de Sueños"):
    nuevo_s = st.text_input("Añade un nuevo sueño:", placeholder="Ej. 🚗 Cambiar Carro, 🏠 Casa propia...")
    if st.button("➕ Crear Tarjeta"):
        agregar_nuevo_sueno(nuevo_s)
        st.success(f"¡Tarjeta '{nuevo_s}' creada!")
    
    if st.button("🗑️ Reiniciar todas las tarjetas"):
        borrar_suenos()
        st.info("Tarjetas borradas. Agrega las tuyas.")

st.divider()

# SECCIÓN: INGRESOS
st.markdown("### 💰 Mis Motores (Ingresos)")
col1, col2 = st.columns(2)
with col1:
    ingreso_t1 = st.number_input("💼 Trabajo 1", min_value=0, value=3500000, step=50000)
    guardar_ingreso("Trabajo 1", ingreso_t1)
with col2:
    ingreso_t2 = st.number_input("🚀 Trabajo 2", min_value=0, value=1800000, step=50000)
    guardar_ingreso("Trabajo 2", ingreso_t2)

total_ingresos = ingreso_t1 + ingreso_t2

datos_comp = calcular_comparativa_ingresos()
comp1 = datos_comp.get("Trabajo 1", {"anterior": 0, "diferencia": 0})
comp2 = datos_comp.get("Trabajo 2", {"anterior": 0, "diferencia": 0})

col_c1, col_c2 = st.columns(2)
with col_c1:
    st.metric(label="T1 vs mes anterior", value=f"${ingreso_t1:,}", delta=f"${comp1['diferencia']:,}" if comp1['anterior'] > 0 else "Nuevo")
with col_c2:
    st.metric(label="T2 vs mes anterior", value=f"${ingreso_t2:,}", delta=f"${comp2['diferencia']:,}" if comp2['anterior'] > 0 else "Nuevo")

st.divider()

# SECCIÓN: GASTOS BÁSICOS
st.markdown("### 🛡️ Gastos Básicos (Validación)")
arriendo = st.number_input("🏠 Arriendo de la casa", min_value=0, value=1200000)
servicios = st.number_input("💧 Servicios Públicos", min_value=0, value=350000)
tarjetas = st.number_input("💳 Tarjetas de Crédito", min_value=0, value=450000)
comida = st.number_input("🍏 Mercado General", min_value=0, value=600000)
mami_diezmo = st.number_input("🙏 Mami & Diezmo", min_value=0, value=500000)

total_gastos = arriendo + servicios + tarjetas + comida + mami_diezmo

st.divider()

# SECCIÓN: SALDO Y SUEÑOS PARAMETRIZADOS
lista_suenos = obtener_suenos()

if total_ingresos >= total_gastos:
    saldo_libertad = total_ingresos - total_gastos
    
    st.success("🛡️ Gastos Básicos Asegurados.")
    st.markdown("<h3 style='text-align:center; margin:0;'>💸 Saldo de Libertad</h3>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align:center; color:#4A90E2; margin-top:0;'>$ {saldo_libertad:,}</h2>", unsafe_allow_html=True)
    
    st.markdown("### ✈️ Banco de Sueños")
    
    # Generar Sliders de manera dinámica según los sueños parametrizados
    porcentajes = {}
    if not lista_suenos:
        st.warning("No tienes tarjetas de sueños creadas. Despliega la configuración de arriba ⚙️ para crear una.")
    else:
        for sueno in lista_suenos:
            porcentajes[sueno] = st.slider(f"{sueno} (%)", min_value=0, max_value=100, value=100 // len(lista_suenos))
        
        total_porc = sum(porcentajes.values())
        
        if total_porc > 100:
            st.error(f"⚠️ Te pasaste del 100% disponible. (Llevas el {total_porc}%)")
        elif any(v == 100 for v in porcentajes.values()) and len(lista_suenos) > 1:
            st.warning("⚠️ ¡Repartir es vivir! No le dejes todo a una sola tarjeta. 😉")
        else:
            # Renderizar las tarjetas dinámicas en base a lo que el usuario creó
            columnas = st.columns(len(lista_suenos))
            colores = ["#1A1A1A", "#4A90E2", "#2ECC71", "#9B59B6", "#E67E22"] # Paleta premium cambiante
            
            for i, sueno in enumerate(lista_suenos):
                dinero_asignado = int(saldo_libertad * (porcentajes[sueno] / 100))
                color = colores[i % len(colores)]
                with columnas[i]:
                    st.markdown(f"""
                    <div style='background-color: {color}; padding: 12px; border-radius: 12px; color: white; text-align:center; margin-bottom:10px;'>
                        <h4 style='font-size:12px !important;'>{sueno}</h4>
                        <h3 style='color:white !important; font-size:16px !important; margin:5px 0 0 0 !important;'>${dinero_asignado:,}</h3>
                    </div>
                    """, unsafe_allow_html=True)

st.divider()

# SECCIÓN: GASTO HORMIGA (OPCIÓN B)
st.markdown("### 🐜 Captura Express Diaria")
col_h1, col_h2 = st.columns([1.5, 1])
with col_h1:
    nombre_hormiga = st.text_input("¿Qué compraste?", placeholder="Café, Uber...", key="hormiga_item")
with col_h2:
    valor_hormiga = st.number_input("¿Cuánto?", min_value=0, value=0, step=1000, key="hormiga_valor")

if st.button("⚡ Registrar Gasto Rápido") and valor_hormiga > 0:
    guardar_gasto_hormiga(nombre_hormiga, valor_hormiga)
    st.toast(f"¡{nombre_hormiga} registrado! ☕")

gasto_semanal_acumulado = obtener_gastos_hormiga_semana()
st.info(f"📊 **Control:** Llevas **${gasto_semanal_acumulado:,}** en antojos los últimos 7 días. ¡Control! 😉")
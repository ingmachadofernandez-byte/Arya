import streamlit as st
import sqlite3
from datetime import date

# Configuración de página con estilo limpio/oscuro responsivo
st.set_page_config(page_title="ARYA OS", page_icon="🤖", layout="centered")

# Ocultar menús innecesarios para estética limpia
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stButton>button {width: 100%; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

# 1. CONEXIÓN Y CREACIÓN DE BASE DE DATOS (ARYA.DB)
def init_db():
    try:
        conn = sqlite3.connect('arya.db')
        c = conn.cursor()
        # Tabla para Compromisos del mes
        c.execute('''CREATE TABLE IF NOT EXISTS compromisos 
                     (mes_anio TEXT, arriendo INTEGER DEFAULT 0, servicios INTEGER DEFAULT 0, 
                      tarjeta INTEGER DEFAULT 0, diezmo INTEGER DEFAULT 0, mami INTEGER DEFAULT 0, 
                      PRIMARY KEY(mes_anio))''')
        # Tabla para la lista de mercado
        c.execute('''CREATE TABLE IF NOT EXISTS mercado 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT, comprado INTEGER DEFAULT 0)''')
        # Tabla para Habitos diarios
        c.execute('''CREATE TABLE IF NOT EXISTS habitos_diarios 
                     (fecha DATE PRIMARY KEY, ejercicio INTEGER DEFAULT 0, mercado INTEGER DEFAULT 0, meditacion INTEGER DEFAULT 0)''')
        conn.commit()
        conn.close()
    except Exception as e:
        pass

init_db()

# Lógicas para Hábitos Diarios
def get_habitos_diarios_hoy():
    fecha_hoy = str(date.today())
    try:
        conn = sqlite3.connect('arya.db')
        c = conn.cursor()
        c.execute("SELECT ejercicio, mercado, meditacion FROM habitos_diarios WHERE fecha=?", (fecha_hoy,))
        res = c.fetchone()
        if not res:
            # Inicializar para el día de hoy
            c.execute("INSERT OR IGNORE INTO habitos_diarios (fecha, ejercicio, mercado, meditacion) VALUES (?, 0, 0, 0)", (fecha_hoy,))
            conn.commit()
            conn.close()
            return 0, 0, 0
        conn.close()
        return res[0], res[1], res[2]
    except Exception as e:
        return 0, 0, 0

def update_habito_hoy(campo, valor):
    fecha_hoy = str(date.today())
    try:
        conn = sqlite3.connect('arya.db')
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO habitos_diarios (fecha, ejercicio, mercado, meditacion) VALUES (?, 0, 0, 0)", (fecha_hoy,))
        c.execute(f"UPDATE habitos_diarios SET {campo}=? WHERE fecha=?", (valor, fecha_hoy))
        conn.commit()
        conn.close()
    except Exception as e:
        pass

# Lógicas de consulta para Compromisos (Blindada contra valores None)
def get_compromisos():
    mes_actual = date.today().strftime("%Y-%m")
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute("SELECT arriendo, servicios, tarjeta, diezmo, mami FROM compromisos WHERE mes_anio=?", (mes_actual,))
    res = c.fetchone()
    conn.close()
    
    # Si encuentra el registro, nos aseguramos de convertir cualquier valor en 1 o 0
    if res:
        return [1 if x == 1 else 0 for x in res]
    return [0, 0, 0, 0, 0]

def update_compromiso(campo, valor):
    mes_actual = date.today().strftime("%Y-%m")
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO compromisos (mes_anio) VALUES (?)", (mes_actual,))
    c.execute(f"UPDATE compromisos SET {campo}=? WHERE mes_anio=?", (valor, mes_actual))
    conn.commit()
    conn.close()

# Lógicas para el Mercado
def get_mercado():
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute("SELECT id, item, comprado FROM mercado")
    items = c.fetchall()
    conn.close()
    return items

def add_item_mercado(item):
    if item:
        conn = sqlite3.connect('arya.db')
        c = conn.cursor()
        c.execute("INSERT INTO mercado (item) VALUES (?)", (item,))
        conn.commit()
        conn.close()

def toggle_mercado(item_id, comprado):
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute("UPDATE mercado SET comprado=? WHERE id=?", (1 if comprado else 0, item_id))
    conn.commit()
    conn.close()

def limpiar_mercado():
    conn = sqlite3.connect('arya.db')
    c = conn.cursor()
    c.execute("DELETE FROM mercado")
    conn.commit()
    conn.close()

# 2. INTERFAZ EN UNA SOLA COLUMNA (MOBILE-FIRST)
st.title("🤖 ARYA OS")
st.subheader("Tu Asistente de Paz Mental")

# Saludo empático de ARYA
st.info("👋 Hola Norma. Tranquila, yo me encargo de recordar los pendientes importantes por ti. Enfócate en tu día, que tu mente está a salvo conmigo.")

# --- SECCIÓN: HÁBITOS DE HOY ---
st.markdown("### 🎯 Hábitos de Hoy")
ejercicio, mercado, meditacion = get_habitos_diarios_hoy()

opciones = ["🏃‍♀️ Hice Ejercicio", "🛒 Hice Mercado", "🧘‍♀️ Medité"]
seleccion_default = []
if ejercicio == 1:
    seleccion_default.append("🏃‍♀️ Hice Ejercicio")
if mercado == 1:
    seleccion_default.append("🛒 Hice Mercado")
if meditacion == 1:
    seleccion_default.append("🧘‍♀️ Medité")

# Mostrar las píldoras
seleccionados = st.pills(
    "Selecciona los hábitos completados hoy:",
    options=opciones,
    selection_mode="multi",
    default=seleccion_default,
    label_visibility="collapsed",
    key="habitos_hoy_pills"
)

# Detectar cambios y actualizar
nuevo_ejercicio = 1 if "🏃‍♀️ Hice Ejercicio" in seleccionados else 0
nuevo_mercado = 1 if "🛒 Hice Mercado" in seleccionados else 0
nuevo_meditacion = 1 if "🧘‍♀️ Medité" in seleccionados else 0

# Si hay diferencias, actualizar inmediatamente y recargar
if (nuevo_ejercicio != ejercicio) or (nuevo_mercado != mercado) or (nuevo_meditacion != meditacion):
    if nuevo_ejercicio != ejercicio:
        update_habito_hoy("ejercicio", nuevo_ejercicio)
    if nuevo_mercado != mercado:
        update_habito_hoy("mercado", nuevo_mercado)
    if nuevo_meditacion != meditacion:
        update_habito_hoy("meditacion", nuevo_meditacion)
    st.rerun()

# Caja de Resumen Diario de ARYA
completados_habitos = nuevo_ejercicio + nuevo_mercado + nuevo_meditacion
if completados_habitos == 0:
    resumen_text = "Hola Norma, tu día está comenzando. ¿Qué hábito vamos a dominar hoy? 🌟"
else:
    consejos = []
    if nuevo_ejercicio == 1:
        consejos.append("el ejercicio físico 🏃‍♀️")
    if nuevo_mercado == 1:
        consejos.append("abastecer el hogar con el mercado 🛒")
    if nuevo_meditacion == 1:
        consejos.append("cuidar tu mente con la meditación 🧘‍♀️")
    
    if completados_habitos == 1:
        resumen_text = f"¡Excelente inicio, Norma! Ya completaste {consejos[0]}. ¡Un gran paso para tu bienestar!"
    elif completados_habitos == 2:
        resumen_text = f"¡Sensacional, Norma! Llevas 2 hábitos completados ({' y '.join(consejos)}). ¡Estás muy cerca de lograr un día perfecto!"
    else:
        resumen_text = "¡Día extraordinario, Norma! Completaste el ejercicio, el mercado y la meditación. 👑 ¡Hoy has dominado tu día al 100%!"

st.info(f"🤖 **ARYA:** {resumen_text}")
st.markdown("---")

# --- SECCIÓN 1: COMPROMISOS SAGRADOS ---
st.markdown("### 🚨 Mi Paz Mental (Pagos del Mes)")

comp = get_compromisos()
arriendo_check = comp[0] == 1
servicios_check = comp[1] == 1
tarjeta_check = comp[2] == 1
diezmo_check = comp[3] == 1
mami_check = comp[4] == 1

# Contador de tranquilidad
completados = sum(comp)
st.metric(label="Compromisos Liberados", value=f"{completados} de 5")

# Checkboxes interactivos
if st.checkbox("🏠 Pagar el Arriendo de la casa", value=arriendo_check):
    if not arriendo_check: update_compromiso("arriendo", 1); st.rerun()
else:
    if arriendo_check: update_compromiso("arriendo", 0); st.rerun()

if st.checkbox("⚡ Pagar los Servicios Públicos", value=servicios_check):
    if not servicios_check: update_compromiso("servicios", 1); st.rerun()
else:
    if servicios_check: update_compromiso("servicios", 0); st.rerun()

if st.checkbox("💳 Pagar la Tarjeta de Crédito", value=tarjeta_check):
    if not tarjeta_check: update_compromiso("tarjeta", 1); st.rerun()
else:
    if tarjeta_check: update_compromiso("tarjeta", 0); st.rerun()

if st.checkbox("⛪ Dar el Diezmo de la Iglesia", value=diezmo_check):
    if not diezmo_check: update_compromiso("diezmo", 1); st.rerun()
else:
    if diezmo_check: update_compromiso("diezmo", 0); st.rerun()

if st.checkbox("❤️ Enviarle el dinero a mi Mami", value=mami_check):
    if not mami_check: update_compromiso("mami", 1); st.rerun()
else:
    if mami_check: update_compromiso("mami", 0); st.rerun()

st.markdown("---")

# --- SECCIÓN 2: LISTA DE MERCADO FLASH ---
st.markdown("### 🛒 Mi Lista de Mercado Rápida")

# Formulario para añadir ítem
nuevo_item = st.text_input("¿Qué necesitas comprar hoy?", placeholder="Ej. Huevos, Leche, Café...", label_visibility="collapsed")
if st.button("➕ Agregar al mercado"):
    if nuevo_item:
        add_item_mercado(nuevo_item)
        st.rerun()

# Mostrar ítems actuales del mercado
items_mercado = get_mercado()
if items_mercado:
    for item_id, nombre, comprado in items_mercado:
        check_val = comprado == 1
        if st.checkbox(f"{'✅ (Comprado) ' if check_val else ''}{nombre}", value=check_val, key=f"mercado_{item_id}"):
            if not check_val: toggle_mercado(item_id, True); st.rerun()
        else:
            if check_val: toggle_mercado(item_id, False); st.rerun()
            
    if st.button("🗑️ Vaciar toda la lista"):
        limpiar_mercado()
        st.rerun()
else:
    st.caption("No tienes productos anotados. ARYA guardará aquí lo que recuerdes para que no se te olvide en el supermercado.")
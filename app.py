import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Seguimiento de Obra", layout="centered")

st.title("🏗️ App de Seguimiento de Obra")
st.write("Registre las tareas y descargue el informe en Excel.")

# --- MEMORIA DE LA APP ---
# Esto crea una lista vacía para guardar los datos mientras la web esté abierta
if 'datos_obra' not in st.session_state:
    st.session_state.datos_obra = []

# --- FORMULARIO ---
with st.form("mi_formulario"):
    nombre = st.text_input("Nombre del trabajador:")
    fecha = st.date_input("Fecha del informe:", date.today())
    
    tarea = st.selectbox("Seleccione la tarea realizada:", [
        "Trazado y marcado de cajas, tubos y cuadros", "Ejecución rozas", 
        "Montaje de soportes", "Colocación tubos", "Tendido de cables",
        "Identificación y etiquetado", "Conexionado de cables",
        "Instalación de mecanismos", "Cuadro eléctrico", "Pruebas y verificación"
    ])
    
    estado = st.selectbox("Estado de la tarea:", [
        "Avance 25% aprox.", "Avance 50% aprox.", "Avance 75% aprox.",
        "OK, finalizado sin errores", "Finalizado con errores pendientes",
        "Finalizado y corregido"
    ])
    
    boton_guardar = st.form_submit_button("Añadir a la lista")

# --- LÓGICA DE GUARDADO ---
if boton_guardar:
    if nombre:
        # Añadimos los datos a la "memoria"
        nuevo_registro = {
            "Fecha": fecha,
            "Trabajador": nombre,
            "Tarea": tarea,
            "Estado": estado
        }
        st.session_state.datos_obra.append(nuevo_registro)
        st.success("✅ Registro añadido a la lista temporal.")
    else:
        st.warning("⚠️ Por favor, pon tu nombre.")

# --- MOSTRAR TABLA Y DESCARGAR ---
if st.session_state.datos_obra:
    df = pd.DataFrame(st.session_state.datos_obra)
    st.write("### Registros actuales:")
    st.table(df) # Muestra los datos en pantalla

    # Crear el archivo Excel en memoria
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Informe')
    
    st.download_button(
        label="📥 Descargar Informe Excel",
        data=output.getvalue(),
        file_name=f"informe_obra_{date.today()}.xlsx",
        mime="application/vnd.ms-excel"
    )

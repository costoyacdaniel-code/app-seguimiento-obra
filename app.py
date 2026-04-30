import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Seguimiento de Obra", layout="centered")

# Título de la aplicación
st.title("🏗️ App de Seguimiento de Obra")
st.write("Complete los datos y envíe el informe por email.")

# --- FUNCIÓN PARA ENVIAR EL CORREO ---
def enviar_correo(archivo_excel):
    try:
        # Creamos el mensaje con los datos de los Secrets
        msg = MIMEMultipart()
        msg['From'] = st.secrets["email_usuario"]
        msg['To'] = st.secrets["email_profesora"]
        msg['Subject'] = f"Informe de Obra - {date.today()}"
        
        # Adjuntamos el archivo Excel
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(archivo_excel)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename=informe_{date.today()}.xlsx")
        msg.attach(part)
        
        # Conexión con el servidor de Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(st.secrets["email_usuario"], st.secrets["email_contrasena"])
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return False

# --- GESTIÓN DE DATOS (MEMORIA) ---
if 'datos_obra' not in st.session_state:
    st.session_state.datos_obra = []

# --- FORMULARIO DE ENTRADA ---
with st.form("formulario_obra"):
    nombre_trabajador = st.text_input("Nombre del trabajador:")
    fecha_envio = st.date_input("Fecha del informe:", date.today())
    
    lista_tareas = [
        "Trazado y marcado de cajas, tubos y cuadros",
        "Ejecución rozas en paredes y techos",
        "Montaje de soportes",
        "Colocación tubos y conductos",
        "Tendido de cables",
        "Identificación y etiquetado",
        "Conexionado de cables",
        "Instalación de mecanismos",
        "Cuadro eléctrico",
        "Pruebas y verificación"
    ]
    tarea_seleccionada = st.selectbox("Seleccione la tarea realizada:", lista_tareas)

    lista_estados = [
        "Avance 25% aprox.",
        "Avance 50% aprox.",
        "Avance 75% aprox.",
        "OK, finalizado sin errores",
        "Finalizado con errores pendientes",
        "Finalizado y corregido"
    ]
    estado_seleccionado = st.selectbox("Estado de la tarea:", lista_estados)
    
    submit = st.form_submit_button("Añadir a la lista")

# --- LÓGICA DE GUARDADO ---
if submit:
    if nombre_trabajador:
        st.session_state.datos_obra.append({
            "Fecha": fecha_envio,
            "Trabajador": nombre_trabajador,
            "Tarea": tarea_seleccionada,
            "Estado": estado_seleccionado
        })
        st.success("✅ Registro añadido correctamente.")
    else:
        st.warning("⚠️ Escribe tu nombre antes de guardar.")

# --- TABLA Y BOTONES DE ACCIÓN ---
if st.session_state.datos_obra:
    st.write("### Registros actuales:")
    df = pd.DataFrame(st.session_state.datos_obra)
    st.table(df)

    # Generar el Excel en memoria
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Informe')
    excel_data = output.getvalue()

    # Columnas para los botones finales
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📥 Descargar Informe Excel",
            data=excel_data,
            file_name=f"informe_obra_{date.today()}.xlsx",
            mime="application/vnd.ms-excel"
        )
    
    with col2:
        if st.button("📧 Enviar por Email"):
            with st.spinner("Enviando correo..."):
                if enviar_correo(excel_data):
                    st.success("¡Correo enviado a la profesora!")
                else:
                    st.error("Error al enviar. Revisa tus Secrets y la contraseña de aplicación.")

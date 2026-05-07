import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Seguimiento de Presupuesto", layout="centered")
st.title("💰 Seguimiento de Presupuesto y Albaranes")

# Función para enviar email (usa los mismos Secrets que ya configuraste)
def enviar_correo(archivo_excel):
    try:
        msg = MIMEMultipart()
        msg['From'] = st.secrets["email_usuario"]
        msg['To'] = st.secrets["email_profesora"]
        msg['Subject'] = f"Informe de Presupuesto - {date.today()}"
        
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(archivo_excel)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename=presupuesto_{date.today()}.xlsx")
        msg.attach(part)
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(st.secrets["email_usuario"], st.secrets["email_contrasena"])
        server.send_message(msg)
        server.quit()
        return True
    except:
        return False

# --- MEMORIA DE DATOS ---
if 'datos_presupuesto' not in st.session_state:
    st.session_state.datos_presupuesto = []

# --- FORMULARIO ---
with st.form("form_presupuesto"):
    col_a, col_b = st.columns(2)
    with col_a:
        n_albaran = st.text_input("Número de Albarán:")
        fecha = st.date_input("Fecha:", date.today())
        trabajador = st.text_input("Trabajador:")
    with col_b:
        partida = st.selectbox("Partida del presupuesto:", ["Material Eléctrico", "Mano de Obra Exterior", "Maquinaria", "Otros Gastos"])
        gastos = st.number_input("Gastos de esta partida (€):", min_value=0.0, step=0.01)
    
    comentarios = st.text_area("Comentarios:")
    foto_albaran = st.file_uploader("Subir foto del albarán (Opcional)", type=["jpg", "png", "jpeg"])
    
    if st.form_submit_button("Registrar Gasto"):
        if n_albaran and trabajador:
            st.session_state.datos_presupuesto.append({
                "Albarán": n_albaran, "Fecha": fecha, "Trabajador": trabajador,
                "Partida": partida, "Gasto (€)": gastos, "Comentarios": comentarios,
                "Foto": "Subida" if foto_albaran else "No"
            })
            st.success("✅ Gasto registrado.")

# --- TABLA Y ACCIONES ---
if st.session_state.datos_presupuesto:
    df = pd.DataFrame(st.session_state.datos_presupuesto)
    st.table(df)
    st.metric("Total Gastado acumulado", f"{df['Gasto (€)'].sum()} €")

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    excel_data = output.getvalue()
    
    c1, c2 = st.columns(2)
    with c1:
        st.download_button("📥 Descargar Excel", excel_data, f"presupuesto_{date.today()}.xlsx")
    with c2:
        if st.button("📧 Enviar Informe a Profesora"):
            if enviar_correo(excel_data):
                st.success("¡Email enviado con éxito!")
            else:
                st.error("Error al enviar. Revisa los Secrets.")

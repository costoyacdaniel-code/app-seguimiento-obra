import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Seguimiento de Presupuesto", layout="centered")
st.title("💰 Seguimiento de Presupuesto y Albaranes")
st.write("Introduzca los datos del albarán para el control de gastos.")

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
        # Aquí puedes cambiar las partidas según lo que necesites
        partida = st.selectbox("Partida del presupuesto:", [
            "Material Eléctrico", 
            "Mano de Obra Exterior", 
            "Maquinaria", 
            "Pequeño Material", 
            "Otros Gastos"
        ])
        gastos = st.number_input("Gastos de esta partida (€):", min_value=0.0, step=0.01)
    
    comentarios = st.text_area("Comentarios:")
    
    # NOTA EXTRA: Subida de foto
    foto_albaran = st.file_uploader("Subir foto del albarán (Opcional)", type=["jpg", "png", "jpeg"])
    
    boton_guardar = st.form_submit_button("Registrar Gasto")

# --- LÓGICA DE GUARDADO ---
if boton_guardar:
    if n_albaran and trabajador:
        nuevo_gasto = {
            "Albarán": n_albaran,
            "Fecha": fecha,
            "Trabajador": trabajador,
            "Partida": partida,
            "Gasto (€)": gastos,
            "Comentarios": comentarios,
            "Foto": "Subida" if foto_albaran else "No"
        }
        st.session_state.datos_presupuesto.append(nuevo_gasto)
        st.success("✅ Gasto registrado en la lista.")
    else:
        st.warning("⚠️ El número de albarán y el trabajador son obligatorios.")

# --- MOSTRAR TABLA Y RESUMEN ---
if st.session_state.datos_presupuesto:
    df = pd.DataFrame(st.session_state.datos_presupuesto)
    st.write("### Listado de Gastos")
    st.table(df)
    
    # Cálculo del total para impresionar a la profe
    total = df["Gasto (€)"].sum()
    st.metric("Total Gastado acumulado", f"{total} €")

    # Botón para descargar Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Presupuesto')
    
    st.download_button(
        label="📥 Descargar Excel de Presupuesto",
        data=output.getvalue(),
        file_name=f"presupuesto_{date.today()}.xlsx",
        mime="application/vnd.ms-excel"
    )

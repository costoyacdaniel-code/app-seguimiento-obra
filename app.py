import streamlit as st
import pandas as pd
from datetime import date

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Seguimiento de Obra", layout="centered")

# --- BLOQUE 1: LOGO E INFORMACIÓN ---
st.title("🏗️ App de Seguimiento de Obra")
st.write("Complete los datos para registrar el avance de la jornada.")

# --- BLOQUE 2: FORMULARIO DE ENTRADA ---
nombre_trabajador = st.text_input("Nombre del trabajador:")
fecha_envio = st.date_input("Fecha del informe:", date.today())

lista_tareas = [
    "Trazado y marcado de cajas, tubos y cuadros",
    "Ejecución rozas en paredes y techos",
    "Montaje de soportes",
    "Colocación tubos y conductos",
    "Tendido de cables",
    "Identificación y etiquetado",
    "Conexionado de cables en bornes o regletas",
    "Instalación y conexionado de mecanismos",
    "Fijación de carril DIN y mecanismos en cuadro eléctrico",
    "Cableado interno del cuadro eléctrico",
    "Configuración de equipos domóticos y/o automáticos",
    "Conexionado de sensores/actuadores",
    "Pruebas de continuidad",
    "Pruebas de aislamiento",
    "Verificación de tierras",
    "Programación del automatismo",
    "Pruebas de funcionamiento"
]
tarea_seleccionada = st.selectbox("Seleccione la tarea realizada:", lista_tareas)

lista_estados = [
    "Avance de la tarea en torno al 25% aprox.",
    "Avance de la tarea en torno al 50% aprox.",
    "Avance de la tarea en torno al 75% aprox.",
    "OK, finalizado sin errores",
    "Finalizado, pero con errores pendientes de corregir",
    "Finalizado y corregidos los errores"
]
estado_seleccionado = st.selectbox("Estado de la tarea:", lista_estados)

if st.button("Registrar Tarea"):
    st.success(f"Registrado: {tarea_seleccionada} al {estado_seleccionado} por {nombre_trabajador}")

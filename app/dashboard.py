# app/dashboard.py
import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Dashboard de Viajes de Buses", layout="wide")

# Navegación
page = st.sidebar.radio("Navegación", ["Dashboard", "Definiciones y Lógica"])

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
trip_summary_path = OUTPUT_DIR / "viajes.csv"

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv(trip_summary_path, parse_dates=["inicio", "fin"])
    df['fecha'] = df['inicio'].dt.date
    df['mes'] = df['inicio'].dt.to_period("M").astype(str)
    df['ruta'] = df['origen'] + " → " + df['destino']
    df=df[df['outlier_final']==False]
    return df

trip_summary = load_data()

if page == "Dashboard":
    st.title("🚌 Dashboard de Viajes de Buses")

    # Sidebar - filtros
    st.sidebar.header("Filtros")
    buses = trip_summary['VehicleID'].unique()
    bus_seleccionado = st.sidebar.selectbox("Selecciona un bus", ["Todos"] + list(buses))

    df_filtered = trip_summary.copy()
    if bus_seleccionado != "Todos":
        df_filtered = df_filtered[df_filtered['VehicleID'] == bus_seleccionado]

    # Métricas generales con tarjetas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de viajes", len(df_filtered))
    col2.metric("Horas recorridas", round(df_filtered['duracion_horas'].sum(), 1))
    col3.metric("Horas inactivas", round(df_filtered['stop_duration_horas'].sum(), 1))
    bus_mas_viajes = df_filtered['VehicleID'].value_counts().idxmax()
    col4.metric("Bus más activo", bus_mas_viajes)

    # Gráfico: viajes por día
    st.subheader("🗓️ Viajes por Día")
    viajes_dia = df_filtered.groupby('fecha').size()
    st.bar_chart(viajes_dia)

    # Gráfico: viajes por mes
    st.subheader("📆 Viajes por Mes")
    viajes_mes = df_filtered.groupby('mes').size()
    st.bar_chart(viajes_mes)

    # Gráfico: duración promedio por ruta
    st.subheader("Tiempos Promedio por Ruta (en horas)")
    promedio_ruta = df_filtered.groupby('ruta')['duracion_horas'].mean().sort_values()
    fig = px.bar(
        promedio_ruta,
        orientation='h',
        labels={'value': 'Horas promedio', 'index': 'Ruta'},
        title='Duración promedio por ruta'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Tiempos muertos por bus
    st.subheader("Tiempos Inactivos por Bus (en horas)")
    tiempo_muerto = df_filtered.groupby('VehicleID')['stop_duration_horas'].sum().sort_values()
    fig2 = px.bar(
        tiempo_muerto,
        orientation='h',
        labels={'value': 'Horas inactivas', 'index': 'Bus'},
        title='Total de horas inactivas por bus'
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Número de paradas por bus y por mes
    st.subheader("🚌 Número de Paradas por Bus y por Mes")
    paradas_bus_mes = df_filtered.groupby(['VehicleID', 'mes'])['num_paradas'].sum().reset_index()
    fig3 = px.bar(
        paradas_bus_mes,
        x='mes',
        y='num_paradas',
        color='VehicleID',
        barmode='group',
        title='Número de paradas por bus y mes'
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Correlación entre duración y número de paradas
    st.subheader("🔄 Correlación: Duración vs Número de Paradas")
    fig4 = px.scatter(
        df_filtered,
        x='num_paradas',
        y='duracion_horas',
        color='VehicleID',
        title='Duración del viaje vs número de paradas',
        trendline='ols'
    )
    st.plotly_chart(fig4, use_container_width=True)

    # Destinos con mayor número de paradas
    st.subheader("🌐 Destinos con más Paradas")
    destinos_paradas = df_filtered.groupby('destino')['num_paradas'].sum().sort_values(ascending=False).reset_index()
    fig5 = px.bar(
        destinos_paradas,
        x='destino',
        y='num_paradas',
        title='Cantidad total de paradas por destino'
    )
    st.plotly_chart(fig5, use_container_width=True)

    # Destinos por bus
    st.subheader("🌟 Destinos recorridos por bus")
    destinos_por_bus = df_filtered.groupby('VehicleID')['destino'].unique().reset_index()
    destinos_por_bus['destino'] = destinos_por_bus['destino'].apply(lambda x: ', '.join(x))
    st.dataframe(destinos_por_bus, use_container_width=True)


    # Tabla final
    st.subheader("🔢 Tabla Detalle de Viajes")
    st.dataframe(df_filtered, use_container_width=True)

elif page == "Definiciones y Lógica":
    st.title("Definiciones y Lógica del Cálculo")



    st.markdown("""
    ### 🔍 Origen y Procesamiento de los Datos

    Los datos de este dashboard provienen de los **viajes de buses**. Cada vez que un bus abre sus puertas, se registra una señal con la siguiente información:

    * **ID del bus**
    * **Fecha y hora** del evento
    * **Duración** de la parada
    * **Localización** (latitud y longitud)

    Estos datos crudos son procesados y limpiados para crear una **capa analítica**, la cual es la base de las visualizaciones presentadas.

    ---

    ### ⚖️ Lógica de Agrupación de Viajes

    Un **viaje** se define como el trayecto completo de un bus desde un terminal de origen válido hasta un terminal de destino válido. La lógica de detección se basa en los siguientes criterios:

    * Se utilizan combinaciones de rutas predefinidas como `San Borja → Viña del Mar`, `Viña del Mar → San Borja`, `Pajaritos → Viña del Mar`, entre otras.
    * Se asigna un `trip_id` secuencial a cada viaje completo detectado.

    ---

    ### 🚩 Detección y Eliminación de Outliers

    Para asegurar la precisión del análisis, se identificaron y eliminaron los viajes que se consideraron **valores atípicos (outliers)**. El tratamiento se basó en dos criterios principales:

    1.  **Criterio Experto**: Se establecieron límites lógicos de duración: un viaje no puede durar más de 5 horas (300 minutos) ni menos de 1 hora (60 minutos).
    2.  **Criterio Estadístico (IQR)**: Se aplicó el método del Rango Intercuartílico para identificar valores atípicos de manera estadística, utilizando la siguiente fórmula para los límites:
        * $Límite\ Inferior = Q1 - 1.5 \times IQR$
        * $Límite\ Superior = Q3 + 1.5 \times IQR$

    Los viajes que no cumplieron con estos criterios fueron excluidos del análisis final.

    ---

    ### 📝 Definiciones de Métricas Clave

    Las métricas presentadas en este dashboard se definen de la siguiente manera:

    * **Total de viajes**: El número total de trayectos únicos detectados por bus.
    * **Horas de viaje**: La diferencia de tiempo entre la hora de inicio y la hora de fin de cada viaje.
    * **Horas inactivas**: La suma de todas las duraciones de parada (`Stop_Duration`) registradas dentro de un viaje.
    * **Tiempo promedio por ruta**: La duración promedio de cada viaje para una combinación de origen y destino específica.

    Toda esta información se procesa a partir del archivo `trip_summary.csv`.
    """)
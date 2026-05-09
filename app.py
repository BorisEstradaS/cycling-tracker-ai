import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from utils.db import get_all_rides, get_ride_by_id
from utils.ai_analysis import analyze_ride, compare_rides

st.set_page_config(
    page_title="🚴 CycleTracker Pro",
    page_icon="🚴",
    layout="wide"
)

st.title("🚴 CycleTracker Pro")
st.caption("Análisis de rutas con IA · MongoDB Atlas + Google Gemini")

# Sidebar: lista de rutas
st.sidebar.header("📋 Mis Rutas")
rides = get_all_rides()
ride_names = {str(r["_id"]): r["name"] for r in rides}
selected_id = st.sidebar.selectbox("Selecciona una ruta:", 
                                    options=list(ride_names.keys()),
                                    format_func=lambda x: ride_names[x])

# Cargar ruta completa con trackpoints
ride = get_ride_by_id(selected_id)
stats = ride["stats"]
points = ride["trackpoints"]
df = pd.DataFrame(points)

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("📏 Distancia", f"{stats['distance_km']} km")
col2.metric("⚡ Vel. Promedio", f"{stats['avg_speed_kmh']} km/h")
col3.metric("🏔️ Desnivel", f"{stats['elevation_gain_m']:.0f} m")
col4.metric("❤️ FC Promedio", f"{stats['avg_hr_bpm']} bpm")

tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Mapa", "📈 Gráficos", "🤖 Análisis IA", "📊 Comparar"
])

with tab1:
    m = folium.Map(location=[df["lat"].mean(), df["lon"].mean()], zoom_start=13)
    coords = list(zip(df["lat"], df["lon"]))
    folium.PolyLine(coords, color="#00ff88", weight=3).add_to(m)
    folium.Marker(coords[0], popup="Inicio", 
                  icon=folium.Icon(color="green")).add_to(m)
    folium.Marker(coords[-1], popup="Fin", 
                  icon=folium.Icon(color="red")).add_to(m)
    st_folium(m, width=700, height=450)

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        fig = px.area(df, y="elevation", title="Perfil de Altimetría", 
                      color_discrete_sequence=["#4d9fff"])
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.line(df, y="heart_rate", title="Frecuencia Cardíaca",
                       color_discrete_sequence=["#ff6b35"])
        st.plotly_chart(fig2, use_container_width=True)
    fig3 = px.line(df, y="speed", title="Velocidad a lo largo de la ruta",
                   color_discrete_sequence=["#00ff88"])
    st.plotly_chart(fig3, use_container_width=True)

with tab3:
    if st.button("🤖 Analizar esta ruta con Gemini", type="primary"):
        with st.spinner("Consultando a tu coach de IA..."):
            analysis = analyze_ride(ride)
            st.markdown(analysis)

with tab4:
    if st.button("📊 Comparar todas mis rutas", type="primary"):
        with st.spinner("Analizando progresión..."):
            comparison = compare_rides(rides)
            st.markdown(comparison)
    
    # Tabla comparativa
    df_rides = pd.DataFrame([{
        "Ruta": r["name"],
        "Km": r["stats"]["distance_km"],
        "Vel. avg": r["stats"]["avg_speed_kmh"],
        "Desnivel": r["stats"]["elevation_gain_m"],
        "FC avg": r["stats"]["avg_hr_bpm"]
    } for r in rides])
    st.dataframe(df_rides, use_container_width=True)
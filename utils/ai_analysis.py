import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_ride(ride: dict) -> str:
    stats = ride["stats"]
    prompt = f"""
    Eres un coach de ciclismo experto. Analiza esta ruta ciclista y da feedback detallado:
    
    Ruta: {ride['name']}
    Fecha: {ride['date']}
    Distancia: {stats['distance_km']} km
    Duración: {stats['duration_min']} min
    Velocidad promedio: {stats['avg_speed_kmh']} km/h
    Velocidad máxima: {stats['max_speed_kmh']} km/h
    Desnivel acumulado: {stats['elevation_gain_m']} m
    FC promedio: {stats['avg_hr_bpm']} bpm
    FC máxima: {stats['max_hr_bpm']} bpm
    
    Por favor analiza:
    1. 💪 Rendimiento general y zonas de entrenamiento
    2. 🏔️ Impacto del desnivel en el esfuerzo
    3. ❤️ Análisis de frecuencia cardíaca
    4. 🎯 Recomendaciones para mejorar
    5. 📈 Comparación con métricas ideales para ciclismo
    
    Responde en español con un tono motivador y profesional.
    """
    response = model.generate_content(prompt)
    return response.text

def compare_rides(rides: list) -> str:
    rides_summary = "\n".join([
        f"""- {r['name']}: {r['stats']['distance_km']}km, 
           {r['stats']['avg_speed_kmh']}km/h avg, 
           FC avg {r['stats']['avg_hr_bpm']}bpm"""
        for r in rides
    ])
    prompt = f"""
    Analiza la progresión de estas rutas ciclistas y dame insights sobre la evolución del ciclista:
    
    {rides_summary}
    
    Dame: tendencias, mejoras detectadas, áreas de oportunidad y plan sugerido.
    Responde en español.
    """
    response = model.generate_content(prompt)
    return response.text
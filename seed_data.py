import numpy as np
from datetime import datetime, timedelta
from utils.db import insert_ride

def generate_ride(name, start_lat, start_lon, distance_km, date_str):
    """Simula trackpoints realistas para una ruta ciclista"""
    n_points = int(distance_km * 15)  # ~15 puntos por km
    duration_min = distance_km * 2.5   # ~24 km/h promedio
    
    base_date = datetime.fromisoformat(date_str)
    timestamps = [base_date + timedelta(seconds=i * (duration_min * 60 / n_points))
                  for i in range(n_points)]

    # Simular coordenadas con variación realista
    lats = start_lat + np.cumsum(np.random.normal(0.0002, 0.0005, n_points))
    lons = start_lon + np.cumsum(np.random.normal(0.0003, 0.0005, n_points))
    
    # Altimetría con subidas y bajadas realistas
    base_elev = 150 + np.random.randint(0, 300)
    elevation = base_elev + np.cumsum(np.random.normal(0, 3, n_points))
    elevation = np.clip(elevation, 100, 800)
    
    # Velocidad (kmh) con variación
    speed = np.random.normal(24, 5, n_points)
    speed = np.clip(speed, 5, 55)
    
    # Frecuencia cardíaca
    heart_rate = np.random.normal(145, 12, n_points).astype(int)
    heart_rate = np.clip(heart_rate, 100, 185)
    
    trackpoints = [
        {
            "lat": round(float(lats[i]), 6),
            "lon": round(float(lons[i]), 6),
            "elevation": round(float(elevation[i]), 1),
            "speed": round(float(speed[i]), 1),
            "heart_rate": int(heart_rate[i]),
            "timestamp": timestamps[i].isoformat()
        }
        for i in range(n_points)
    ]
    
    elev_gain = float(np.sum(np.maximum(np.diff(elevation), 0)))
    
    return {
        "name": name,
        "date": base_date,
        "stats": {
            "distance_km": round(distance_km, 1),
            "duration_min": round(duration_min, 1),
            "avg_speed_kmh": round(float(np.mean(speed)), 1),
            "max_speed_kmh": round(float(np.max(speed)), 1),
            "elevation_gain_m": round(elev_gain, 0),
            "avg_hr_bpm": int(np.mean(heart_rate)),
            "max_hr_bpm": int(np.max(heart_rate))
        },
        "trackpoints": trackpoints
    }

# Rutas en Lima, Perú
RIDES = [
    ("Miraflores - La Molina", -12.1219, -77.0281, 42.3, "2024-01-15T07:30:00"),
    ("Costa Verde Loop",        -12.1300, -77.0350, 28.7, "2024-01-22T06:00:00"),
    ("Surco - Pachacámac",      -12.1500, -76.9800, 58.1, "2024-02-03T07:00:00"),
    ("Ciclovía Dominical",      -12.0800, -77.0100, 18.4, "2024-02-11T07:30:00"),
    ("Ate - Chaclacayo",        -12.0200, -76.9200, 67.5, "2024-02-20T06:30:00"),
]

if __name__ == "__main__":
    for name, lat, lon, dist, date in RIDES:
        ride = generate_ride(name, lat, lon, dist, date)
        rid = insert_ride(ride)
        print(f"✅ Insertada: {name} → ID: {rid}")
import pandas as pd
import requests
from geopy.distance import geodesic


df = pd.read_csv("carreras.csv")

# 1 Obtener ubicación del usuario
def obtener_ubicacion():
    url = "http://ip-api.com/json/"
    response = requests.get(url)
    data = response.json()
    
    lat = data['lat']
    lon = data['lon']
    
    return (lat, lon)


# 2 Cargar datos del CSV

def cargar_datos(ruta):
    df = pd.read_csv(ruta)

    df['Latitud'] = (
        df['Latitud']
        .astype(str)
        .str.replace(',', '.')
        .str.strip()
    )

    df['Longitud'] = (
        df['Longitud']
        .astype(str)
        .str.replace(',', '.')
        .str.strip()
    )

    df['Latitud'] = pd.to_numeric(df['Latitud'], errors='coerce')
    df['Longitud'] = pd.to_numeric(df['Longitud'], errors='coerce')

    # Eliminar filas con datos inválidos
    df = df.dropna(subset=['Latitud', 'Longitud'])

    return df


#3 Calcular universidad más cercana

def universidad_mas_cercana(df, ubicacion_usuario,n=4):
    distancias = []

    for _, fila in df.iterrows():
        ubicacion_uni = (fila['Latitud'], fila['Longitud'])
        distancia = geodesic(ubicacion_usuario, ubicacion_uni).km
        distancias.append(distancia)

    df['Distancia_km'] = distancias

    # Ordenar por distancia
    df_ordenado = df.sort_values(by='Distancia_km')

    return df_ordenado.head(n)

#4. Ejecutar programa

def main():
    archivo = "carreras.csv"

    df = cargar_datos(archivo)
    mi_ubicacion = obtener_ubicacion()

    resultados = universidad_mas_cercana(df, mi_ubicacion,5)

    print("Tu ubicación:", mi_ubicacion)
    print("\nUniversidades más cercanas a ti:")

    for i, (_, fila) in enumerate(resultados.iterrows(), start=1):
        print("Carrera:", fila['Nombre de la carrera'])     
        print("Distancia:", round(fila['Distancia_km'], 2), "km\n")

# Ejecutar
if __name__ == "__main__":
    main()
    
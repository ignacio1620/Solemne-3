import streamlit as st
import requests
import matplotlib.pyplot as plt

# URL con filtros para reducir el tamaño de la respuesta
url = 'https://restcountries.com/v3.1/all?fields=name,population,area,flag,currencies,languages,capital'

countries_data = []

# Configurar una sesión con reintentos robustos
session = requests.Session()
retries = requests.adapters.Retry(
    total=5,
    backoff_factor=2,
    status_forcelist=[500, 502, 503, 504]
)
adapter = requests.adapters.HTTPAdapter(max_retries=retries)
session.mount("http://", adapter)
session.mount("https://", adapter)

# Obtener los datos de los países
def obtener_datos_pais(pais):
    for country in countries_data:
        name = country.get('name', {}).get('common', '')
        if name.lower() == pais.lower():
            population = country.get('population', 0)
            area = country.get('area', 0)
            capital = country.get('capital', ['Desconocida'])[0]
            flag = country.get('flags', {}).get('png', '')
            currencies = country.get('currencies', {})
            languages = country.get('languages', {})
            return {
                "name": name,
                "population": population,
                "area": area,
                "capital": capital,
                "flag": flag,
                "currencies": list(currencies.keys()),
                "languages": list(languages.values())
            }
    return None

# Función que carga los datos de los países
def cargar_datos():
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()  # Lanza excepción si ocurre un error con la solicitud HTTP
        return response.json()  # Retorna la respuesta como un objeto JSON
    except requests.exceptions.RequestException as e:
        st.error(f"Error durante la solicitud: {e}")
        return []

# Función para mostrar la página principal
def pagina_principal():
    st.title("Descripción del Proyecto")
    st.write("Este proyecto tiene como objetivo recopilar y analizar información relevante sobre diversos países del mundo, "
             "incluyendo datos sobre su población, idiomas, densidad, área, territorio, etc. A través de una plataforma digital interactiva.")

# Página para visualización de datos
def visualizacion_datos():
    st.title("Visualizaci









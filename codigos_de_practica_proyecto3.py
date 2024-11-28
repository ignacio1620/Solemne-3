import requests
import matplotlib.pyplot as plt
import streamlit as st

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

def obtener_datos_pais(pais):
    """Buscar un país y devolver sus datos relevantes."""
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

# Realiza la solicitud a la API y procesa los datos
try:
    response = session.get(url, timeout=30)
    response.raise_for_status()  # Lanza excepción para errores HTTP
    countries_data = response.json()

    if not countries_data:
        st.error("No hay datos disponibles. Verifica la API.")
        exit()

except requests.exceptions.RequestException as e:
    st.error(f"Error durante la solicitud: {e}")
    countries_data = []

# Aplicación Streamlit
st.title('Información de Países')
st.write('Selecciona un país para obtener información detallada y visualizar gráficos interactivos.')

# Mostrar una lista desplegable para elegir el país
countries_names = [country.get('name', {}).get('common', 'Desconocido') for country in countries_data]
pais_elegido = st.selectbox('Selecciona un país', countries_names)

# Obtener y mostrar la información del país seleccionado
if pais_elegido:
    datos_pais = obtener_datos_pais(pais_elegido)

    if datos_pais:
        st.subheader(f"Datos de {datos_pais['name']}:")
        st.write(f"**Capital**: {datos_pais['capital']}")
        st.write(f"**Población**: {datos_pais['population']}")
        st.write(f"**Área**: {datos_pais['area']} km²")
        st.write(f"**Monedas**: {', '.join(datos_pais['currencies'])}")
        st.write(f"**Idiomas**: {', '.join(datos_pais['languages'])}")

        # Crear las categorías y valores para los gráficos
        categorias = ['Población', 'Área (km²)', 'Idiomas', 'Monedas']
        valores = [datos_pais['population'], datos_pais['area'], len(datos_pais['languages']), len(datos_pais['currencies'])]

        # Opciones de gráficos
        opcion_grafico = st.selectbox("Selecciona el tipo de gráfico", ("Gráfico de Barras", "Gráfico de Pastel", "Gráfico de Líneas"))

        if opcion_grafico == "Gráfico de Barras":
            # Gráfico de Barras
            fig, ax = plt.subplots(figsize=(8, 6))
            barras = ax.bar(categorias, valores, color=['skyblue', 'lightgreen', 'lightcoral', 'gold'])
            for barra in barras:
                yval = barra.get_height()
                ax.text(barra.get_x() + barra.get_width() / 2, yval + 0.02 * yval, int(yval), ha='center', va='bottom')
            ax.set_title(f"Datos de {datos_pais['name']}")
            ax.set_xlabel("Categorías")
            ax.set_ylabel("Valores")
            st.pyplot(fig)

        elif opcion_grafico == "Gráfico de Pastel":
            # Gráfico de Pastel
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(valores, labels=categorias, autopct='%1.1f%%', colors=['skyblue', 'lightgreen', 'lightcoral', 'gold'])
            ax.set_title(f"Distribución de datos de {datos_pais['name']}")
            st.pyplot(fig)

        elif opcion_grafico == "Gráfico de Líneas":
            # Gráfico de Líneas
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.plot(categorias, valores, marker='o', color='b', linestyle='-', linewidth=2, markersize=8)
            ax.set_title(f"Datos de {datos_pais['name']} en gráfico de líneas")
            ax.set_xlabel("Categorías")
            ax.set_ylabel("Valores")
            ax.grid(True)
            st.pyplot(fig)






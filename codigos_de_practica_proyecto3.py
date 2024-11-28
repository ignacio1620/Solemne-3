import streamlit as st
import requests
import pandas as pd

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
    st.title("Visualización de Datos")
    st.write("Aquí se mostrarán datos relevantes sobre diferentes países.")
    # Se pueden incluir tablas o más visualizaciones aquí

# Página de gráficos interactivos
def graficos_interactivos():
    st.title("Gráficos Interactivos")
    st.write("Esta sección permite interactuar con gráficos sobre diversos parámetros de los países.")
    
    # Selección de país
    countries_names = [country.get('name', {}).get('common', 'Desconocido') for country in countries_data]
    pais_elegido = st.selectbox("Selecciona un país", countries_names)
    
    # Verifica si el país fue seleccionado
    if pais_elegido:
        datos_pais = obtener_datos_pais(pais_elegido)

        if datos_pais:
            # Mostrar los datos del país seleccionado
            st.subheader(f"Datos de {datos_pais['name']}")
            st.write(f"Capital: {datos_pais['capital']}")
            st.write(f"Población: {datos_pais['population']}")
            st.write(f"Área: {datos_pais['area']} km²")
            st.write(f"Monedas: {', '.join(datos_pais['currencies'])}")
            st.write(f"Idiomas: {', '.join(datos_pais['languages'])}")
            
            # Datos para el gráfico
            categorias = ['Población', 'Área (km²)', 'Idiomas', 'Monedas']
            valores = [datos_pais['population'], datos_pais['area'], len(datos_pais['languages']), len(datos_pais['currencies'])]
            
            # Selección de tipo de gráfico
            tipo_grafico = st.selectbox("Selecciona el tipo de gráfico", ["Gráfico de Barras", "Gráfico de Pastel", "Gráfico de Líneas"])
            
            if tipo_grafico == "Gráfico de Barras":
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
            
            elif tipo_grafico == "Gráfico de Pastel":
                # Gráfico de Pastel
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.pie(valores, labels=categorias, autopct='%1.1f%%', colors=['skyblue', 'lightgreen', 'lightcoral', 'gold'])
                ax.set_title(f"Distribución de datos de {datos_pais['name']}")
                st.pyplot(fig)
            
            elif tipo_grafico == "Gráfico de Líneas":
                # Gráfico de Líneas
                fig, ax = plt.subplots(figsize=(8, 6))
                ax.plot(categorias, valores, marker='o', color='b', linestyle='-', linewidth=2, markersize=8)
                ax.set_title(f"Datos de {datos_pais['name']} en gráfico de líneas")
                ax.set_xlabel("Categorías")
                ax.set_ylabel("Valores")
                ax.grid(True)
                st.pyplot(fig)

# Función principal que gestiona la navegación
def main():
    # Cargar los datos de los países
    global countries_data
    countries_data = cargar_datos()

    # Verificar si la carga fue exitosa
    if not countries_data:
        st.error("No se pudieron cargar los datos de los países. Intenta nuevamente.")
        return
    
    # Título de la aplicación
    st.title("Aplicación de Análisis de Países del Mundo")
    
    # Barra lateral para navegación
    st.sidebar.title("Navegación")
    pagina = st.sidebar.selectbox("Selecciona una página", ["Página principal", "Visualización de datos", "Gráficos interactivos"])
    
    # Redirigir al contenido correspondiente según la página seleccionada
    if pagina == "Página principal":
        pagina_principal()
    elif pagina == "Visualización de datos":
        visualizacion_datos()
    elif pagina == "Gráficos interactivos":
        graficos_interactivos()

if __name__ == "__main__":
    main()








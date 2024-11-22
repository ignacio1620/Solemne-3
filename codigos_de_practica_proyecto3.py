import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

# URL de la API que proporciona los datos de los países
url = 'https://restcountries.com/v3.1/all'
response = requests.get(url)
countries_data = response.json()

# Convertir los datos obtenidos en un DataFrame
df = pd.DataFrame(countries_data)

# Función para la página principal
def pagina_principal():
    st.title("Descripción del Proyecto")
    st.write(
        "Este proyecto tiene como objetivo recopilar y analizar información relevante sobre diversos países del mundo, "
        "incluyendo datos sobre su población, idiomas, densidad, área, territorio, etc. A través de una plataforma digital interactiva."
    )

# Página para visualización de datos
def visualizacion_datos():
    st.title("Visualización de Datos")
    st.write("Aquí se mostrarán datos relevantes sobre diferentes países.")
    
    # Mostrar un DataFrame con los datos de los países
    st.dataframe(df[['name', 'region', 'population', 'area']])  # Solo columnas relevantes para mostrar

# Página de gráficos interactivos
def graficos_interactivos():
    st.title("Gráficos Interactivos")
    st.write("Esta sección permite interactuar con gráficos sobre diversos parámetros de los países.")
    
    # Generación del gráfico de barras para contar la cantidad de países por región
    conteo_grupos = df.groupby('region')['name'].count()

    fig, ax = plt.subplots(figsize=(10, 5))
    conteo_grupos.plot(kind='bar', ax=ax)
    ax.set_title('Cantidad de países por Región') 
    ax.set_xlabel('Región')  
    ax.set_ylabel('Cantidad de países')
    ax.set_xticklabels(conteo_grupos.index, rotation=45)
    ax.grid(axis='y')

    # Etiquetas encima de las barras
    for i, count in enumerate(conteo_grupos):
        ax.text(i, count + 0.2, str(count), ha='center', va='bottom', fontsize=10)

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

# Función principal que gestiona la navegación
def main():
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


import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Definir la URL de la API y obtener los datos
url = 'https://restcountries.com/v3.1/all'
response = requests.get(url)
countries_data = response.json()

# Convertir los datos a un DataFrame de pandas
df = pd.DataFrame(countries_data)

# Página principal
def pagina_principal():
    st.title("Descripción del Proyecto")
    st.write("""
    Este proyecto tiene como objetivo recopilar y analizar información relevante sobre diversos países del mundo,
    incluyendo datos sobre su población, idiomas, densidad, área, territorio, etc. A través de una plataforma 
    digital interactiva, los usuarios pueden explorar visualizaciones y gráficos interactivos sobre diferentes aspectos 
    de cada país.
    """)

# Página para visualización de datos
def visualizacion_datos():
    st.title("Visualización de Datos")
    st.write("Aquí se mostrarán datos relevantes sobre diferentes países.")
    
    # Muestra los primeros 5 países como ejemplo
    st.write("Ejemplo de los primeros 5 países:")
    st.dataframe(df.head())

    # Mostrar estadísticas generales
    st.write("Estadísticas descriptivas de los datos:")
    st.write(df.describe())

    # Mostrar el conteo de países por región
    conteo_grupos = df.groupby('region')['name'].count().reset_index()
    st.write("Conteo de países por región:")
    st.dataframe(conteo_grupos)

# Página de gráficos interactivos
def graficos_interactivos():
    st.title("Gráficos Interactivos")
    st.write("Esta sección permite interactuar con gráficos sobre diversos parámetros de los países.")
    
    # Crear gráfico de cantidad de países por región
    conteo_grupos = df.groupby('region')['name'].count()

    # Crear un gráfico de barras
    plt.figure(figsize=(10, 5))
    conteo_grupos.plot(kind='bar', color='skyblue')

    plt.title('Cantidad de países por Región')
    plt.xlabel('Región')
    plt.ylabel('Cantidad de países')
    plt.xticks(rotation=45)
    plt.grid(axis='y')

    # Etiquetas de los valores en las barras
    for i, count in enumerate(conteo_grupos):
        plt.text(i, count + 0.2, str(count), ha='center', va='bottom', fontsize=10)

    plt.tight_layout()

    # Mostrar el gráfico en Streamlit
    st.pyplot(plt)

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

# Ejecutar la aplicación
if __name__ == "__main__":
    main()



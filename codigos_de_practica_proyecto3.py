import streamlit as st

# Definimos la página principal
def pagina_principal():
    st.subtitle("Descripción del Proyecto")
    st.write(
        "Este proyecto tiene como objetivo recopilar y analizar información relevante sobre diversos países del mundo, "
        "incluyendo datos sobre su población, idiomas, densidad, área, territorio, etc. A través de una plataforma digital interactiva."
    )

# Página para visualización de datos
def visualizacion_datos():
    st.title("Visualización de Datos")
    st.write("Aquí se mostrarán datos relevantes sobre diferentes países.")
    # Aquí puedes añadir más funcionalidades como tablas, mapas, etc.
    # Ejemplo:
    # st.dataframe(df)  # Si tuvieras un dataframe para mostrar

# Página de gráficos interactivos
def graficos_interactivos():
    st.title("Gráficos Interactivos")
    st.write("Esta sección permite interactuar con gráficos sobre diversos parámetros de los países.")
 import pandas as pd
import matplotlib.pyplot as plt
import requests

url = 'https://restcountries.com/v3.1/all'
response = requests.get(url)
countries_data = response.json()

df = pd.DataFrame(countries_data)

conteo_grupos = df.groupby('region')['name'].count()

plt.figure(figsize=(10, 5))
conteo_grupos.plot(kind='bar')

plt.title('Cantidad de paises por Región') 
plt.xlabel('Región')  
plt.ylabel('Cantidad de paises')
plt.xticks(rotation=45)
plt.grid(axis='y')

for i, count in enumerate(conteo_grupos):
    plt.text(i, count + 0.2, str(count), ha='center', va='bottom', fontsize=10)

plt.tight_layout()

plt.show()

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

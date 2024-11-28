import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Generar datos de ejemplo
np.random.seed(0)
data = pd.DataFrame({
    'x': np.arange(0, 100),
    'y': np.random.randn(100).cumsum()
})

# Título de la aplicación
st.title('Gráficos Interactivos con Streamlit')

# Descripción
st.write('Esta es una aplicación sencilla usando Streamlit. Los gráficos cambian según el botón presionado.')

# Crear un botón para cambiar el gráfico
if st.button('Mostrar gráfico de líneas'):
    st.write("Has presionado el botón: Mostrar gráfico de líneas")
    
    # Gráfico de líneas
    plt.figure(figsize=(10,6))
    plt.plot(data['x'], data['y'], label='Gráfico de Líneas', color='b')
    plt.title('Gráfico de Líneas')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    st.pyplot(plt)

elif st.button('Mostrar gráfico de dispersión'):
    st.write("Has presionado el botón: Mostrar gráfico de dispersión")
    
    # Gráfico de dispersión
    plt.figure(figsize=(10,6))
    sns.scatterplot(x='x', y='y', data=data, color='r')
    plt.title('Gráfico de Dispersión')
    plt.xlabel('X')
    plt.ylabel('Y')
    st.pyplot(plt)

else:
    st.write("Presiona un botón para ver el gráfico")





import streamlit as st
import pandas as pd
import openai
import os
import random

# Configuramos el diseño de la página
st.set_page_config(layout="wide")

# Accedemos a la clave de API de OpenAI a través de una variable de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Agregamos un título al principio
st.title('Thesis Maker')

# Agregamos información de instrucciones
st.write('Suba un archivo .XLSX con las fuentes de su tesis.')

# Pedimos al usuario que suba el archivo Excel
archivo = st.file_uploader('Cargar archivo Excel', type=['xlsx'])

if archivo:
    # Leemos el archivo con pandas
    data = pd.read_excel(archivo)

    # Pedimos al usuario que seleccione las columnas con el autor, título y documento
    columnas = data.columns
    columna_autor = st.selectbox('Selecciona la columna que contiene el autor:', columnas)
    columna_titulo = st.selectbox('Selecciona la columna que contiene el título:', columnas)
    columna_documento = st.selectbox('Selecciona la columna que contiene el documento:', columnas)

    # Agregamos un botón para iniciar la generación
    if st.button('Generar'):
        # Obtenemos los autores, títulos y documentos del archivo
        autores = data[columna_autor].tolist()
        titulos = data[columna_titulo].tolist()
        documentos = data[columna_documento].tolist()

        # Utilizamos la API de GPT-3 para extraer citas de cada documento
        citas_totales = []
        for i, documento in enumerate(documentos):
            prompt_citas = f"Extrae cinco citas textuales del documento titulado '{titulos[i]}' de {autores[i]}. Documento: {documento}. "
            response_citas = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt_citas,
                temperature=0,
                max_tokens=512,
                n=1,
                stop=None
                )
            citas = response_citas.choices[0].text.strip().split("\n")
            citas_totales.extend(citas)

        # Utilizamos la API de OpenAI para generar una nueva síntesis original que elabore un documento original con las citas de los anteriores
        prompt_sintesis_novedosa = "Genera un documento original con las siguientes citas:\n"
        for 
        response_sintesis_novedosa = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_sintesis_novedosa,
            temperature=0.5,
            max_tokens=3024,
            n=1,
            stop=None,
            timeout=60,
        )
        sintesis_novedosa = response_sintesis_novedosa.choices[0].text.strip()

    # Mostramos los resultados en un pop up
        st.write(f'<h2>Síntesis novedosa:</h2><p>{sintesis_novedosa}</p>', unsafe_allow_html=True, target='new')
    else:
        st.write("No se encontraron suficientes citas para generar una síntesis novedosa.")


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

    # Pedimos al usuario que seleccione las columnas con el título y el ensayo
    columnas = data.columns
    columna_titulo = st.selectbox('Selecciona la columna que contiene los títulos:', columnas)
    columna_documento = st.selectbox('Selecciona la columna que contiene los documentos:', columnas)

    # Agregamos un botón para iniciar la generación
    if st.button('Generar'):
        # Obtenemos los títulos y los documentos del archivo
        titulos = data[columna_titulo].tolist()
        documentos = data[columna_documento].tolist()

        # Utilizamos la API de GPT-3 para extraer citas de cada documento
        citas_totales = []
        for i, documento in enumerate(documentos):
            prompt_citas = f"Extrae diez citas textuales del documento titulado '{titulos[i]}'. Documento: {documento}. "
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

        # Generamos una síntesis para cada documento a partir de las citas obtenidas
        sintesis_totales = []
        for i, documento in enumerate(documentos):
            prompt_sintesis = f"Elabora una síntesis e interpretación del documento titulado '{titulos[i]}'. Documento: {documento}. Citas: "
            for cita in citas_totales:
                prompt_sintesis += f"\n- {cita}"
            response_sintesis = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt_sintesis,
                temperature=0,
                max_tokens=1024,
                n=1,
                stop=None,
                timeout=60,
            )
            sintesis = response_sintesis.choices[0].text.strip()
            sintesis_totales.append(sintesis)

        # Utilizamos la API de OpenAI para generar una nueva síntesis original que cite las síntesis anteriores y las citas seleccionadas
        prompt_sintesis_novedosa = "Genera una nueva síntesis original que haga una síntesis de todos los documentos anteriores y cite las siguientes citas: "
        for cita in random.sample(citas_totales, 15):
            prompt_sintesis_novedosa += f"\n- {cita}"
        prompt_sintesis_novedosa += "\nSíntesis anteriores:"
        for sintesis in sintesis_totales:
            prompt_sintesis_novedosa += f"\n- {sintesis}"
        response_sintesis_novedosa = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_sintesis_novedosa,
            temperature=0,
            max_tokens=2048,
            n=1,
            stop=None,
            timeout=60,
        )
        sintesis_novedosa = response_sintesis_novedosa.choices[0].text.strip()

        # Mostramos los resultados en un pop up
        st.write(f'<h2>Síntesis novedosa:</h2><p>{sintesis_novedosa}</p>', unsafe_allow_html=True, target='new')

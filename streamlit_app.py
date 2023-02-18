import streamlit as st
import pandas as pd
import openai
import os

# Configuramos el diseño de la página
st.set_page_config(layout="wide")

# Accedemos a la clave de API de OpenAI a través de una variable de entorno
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Agregamos un título al principio
st.title('Thesis Maker')

# Agregamos información de instrucciones
st.write('Suba un archivo .XLSX con las fuentes de sum tesis.')

# Pedimos al usuario que suba el archivo Excel
archivo = st.file_uploader('Cargar archivo Excel', type=['xlsx'])

if archivo:
    # Leemos el archivo con pandas
    data = pd.read_excel(archivo)

    # Pedimos al usuario que seleccione las columnas con el título y el ensayo
    columnas = data.columns
    columna_titulo = st.selectbox('Selecciona la columna que contiene los títulos:', columnas)
    columna_ensayo = st.selectbox('Selecciona la columna que contiene los ensayos:', columnas)

    # Agregamos un botón para iniciar la generación
    if st.button('Generar'):
        # Obtenemos los títulos y los ensayos del archivo
        titulos = data[columna_titulo].tolist()
        ensayos = data[columna_ensayo].tolist()

        # Utilizamos la API de GPT-3 para extraer citas de cada documento
        resultados = []
        for i, ensayo in enumerate(ensayos):
            prompt = f"Extrae diez citas texuales del documento titulado '{titulos[i]}'. "
            prompt += f"Documento: {doocumento}. "
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                temperature=0,
                max_tokens=512,
                n=1,
                stop=None
                
            )
            interpretación = response.choices[0].text.strip()

            # Agregamos una síntesis elaborada a partir de las citas
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Elabora una síntesis e interpretación del documento titulado '{titulos[i]}'. Documento: {documento}",
                temperature=0,
                max_tokens=1024,
                n=1,
                stop=None,
                timeout=60,
            )
            sugerencias = response.choices[0].text.strip()

            # Agregamos las citas y la sínesis a la tabla
            resultados.append({
                'Ensayo': titulos[i],
                'Citas': citas,
                'Síntesis e interpretación': síntesis,
            })

        # Mostramos los resultados en una tabla en un pop up
        if len(resultados) > 0:
            tabla_resultados = pd.DataFrame(resultados)
            tabla_html = tabla_resultados.to_html(index=False)
            st.write(f'<h2>Resultados:</h2>{tabla_html}', unsafe_allow_html=True, target='new')
        else:
            st.write("No se encontraron resultados")

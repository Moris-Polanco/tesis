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
        resultados = []
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
            citas = response_citas.choices[0].text.strip()

            # Agregamos una síntesis elaborada a partir de las citas
            prompt_sintesis = f"Elabora una síntesis e interpretación del documento titulado '{titulos[i]}'. Documento: {documento}. Citas: {citas}"
            response_sintesis = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt_sintesis,
                temperature=0,
                max_tokens=1024,
                n=1,
                stop=None,
                timeout=60,
            )
            síntesis = response_sintesis.choices[0].text.strip()

            # Generamos una interpretación novedosa a partir de las citas y la síntesis
            combinacion = list(zip(citas.split("\n"), síntesis.split("\n")))
            prompt_interpretacion = f"Genera una interpretación novedosa del documento titulado '{titulos[i]}'. Documento: {documento}. Citas y síntesis: {combinacion}"
            response_interpretacion = openai.Completion.create(
                engine="text-davinci-003",
                                prompt=prompt_interpretacion,
                temperature=0,
                max_tokens=1024,
                n=1,
                stop=None,
                timeout=60,
            )
            interpretacion = response_interpretacion.choices[0].text.strip()

            # Agregamos las citas, la síntesis y la interpretación a la tabla
            resultados.append({
                'Ensayo': titulos[i],
                'Citas': citas,
                'Síntesis e interpretación': síntesis,
                'Interpretación novedosa': interpretacion
            })

        # Mostramos los resultados en una tabla en un pop up
        if len(resultados) > 0:
            tabla_resultados = pd.DataFrame(resultados)
            tabla_html = tabla_resultados.to_html(index=False)
            st.write(f'<h2>Resultados:</h2>{tabla_html}', unsafe_allow_html=True, target='new')
        else:
            st.write("No se encontraron resultados")

               

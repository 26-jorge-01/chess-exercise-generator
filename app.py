import streamlit as st
import pandas as pd
from io import BytesIO
import requests

# Función para cargar una partición desde una URL de Google Drive
@st.cache_data
def load_partition_from_url(google_drive_url):
    try:
        # Descargar el archivo desde la URL
        response = requests.get(google_drive_url)
        response.raise_for_status()  # Verificar que la descarga sea exitosa
        file_bytes = BytesIO(response.content)
        
        # Leer el archivo Parquet
        return pd.read_parquet(file_bytes)
    except Exception as e:
        st.error(f"Error al cargar la partición desde Google Drive: {e}")
        return None

# Función para generar enlaces en Streamlit
def generar_enlace(row):
    url = row['GameUrl']  # Asegúrate de que esta columna exista en tu base de datos
    return f"[Haz clic aquí]({url})"

# Configuración de la app
st.title("Generador de Ejercicios de Ajedrez")
st.write("""
Bienvenid@ al **Generador de Ejercicios de Ajedrez**. 
Esta herramienta utiliza datos provenientes de diversas categorías tácticas y estratégicas extraidas de la base pública de Puzzles de Lichess, para mejorar tus habilidades ajedrecísticas. Sigue los pasos a continuación para filtrar y ver los ejercicios.
""")

# Diccionario con enlaces de Google Drive (simulación de estructura jerárquica)
google_drive_urls = {
    "Openings": {
        "Discovered Attack": "https://drive.google.com/uc?id=1tCnjgBpPjQTsFDeG8wSskXYlbD-1WKaP&export=download",
        "Double Attack": "https://drive.google.com/uc?id=1a7r_jMddhbs-rWUrzHTmDVebC_sfy0LV&export=download",
        "Double Check": "https://drive.google.com/uc?id=1vh_ul7Qn8zMaZuIk3ggezsNFOzqOjEjs&export=download",
        "Fork": "https://drive.google.com/uc?id=17H4WkxkmVEj3CRqKxh8VpNBuoKchjc8U&export=download",
        "Intermezzo": "https://drive.google.com/uc?id=1VApleivs7WYhc0Ci1yXxFFzBeFSIV_kI&export=download",
        "Mate in 1": "https://drive.google.com/uc?id=1b2Oz4ZVFJQHHOsR8yOjNsW3xIhNp1GQ0&export=download",
        "Mate in 2": "https://drive.google.com/uc?id=1CAhF3HQIEEFhvWYdY5kwWTP_Vm9ewMIf&export=download",
        "Mate in 3": "https://drive.google.com/uc?id=1n33a_capxmgUMNaWibo59dKO2323WB9Y&export=download",
        "Pin": "https://drive.google.com/uc?id=1SDpsKHvZQzVmNoQR6qJxmOS3d58v3p9w&export=download",
        "Skewer": "https://drive.google.com/uc?id=1Bh7ND_Rhxy_EwPAA8XSwX-w29MbHE_G5&export=download",
        "Smothered Mate": "https://drive.google.com/uc?id=1_bDvBgo2xF1hI6k9Fn_PvD7Z67iq4j_J&export=download",
        "X Ray Attack": "https://drive.google.com/uc?id=1xn5ZqhCKUvOwhr_yhCq5DKf5DEWv6vZB&export=download",
        "Others": "https://drive.google.com/uc?id=1XPWGz09OulCI_U10p7XieOptnMg3UnwN&export=download",
    },
    "Midgame": {
        "Discovered Attack": "https://drive.google.com/uc?id=17Yktvz4jiBamdQw-21dC-AuLSNYdoWCl&export=download",
        "Double Attack": "https://drive.google.com/uc?id=1aUxvWc54Xyx9TdHsyPtDYcMmxfENfkuV&export=download",
        "Double Check": "https://drive.google.com/uc?id=12yWH1ajAw26t_E-Sac6nMeC_zExEVH9K&export=download",
        "Fork": "https://drive.google.com/uc?id=1pkQtsfK3H8234dY2FNEkb8EwPZpPkXUc&export=download",
        "Intermezzo": "https://drive.google.com/uc?id=1ICmfeLPqNSaJSaVpeo4xz3qg2qBZ3u6R&export=download",
        "Mate in 1": "https://drive.google.com/uc?id=1F0GzWLR7XQzzHVY_WH-8RaKal-xRcRWv&export=download",
        "Mate in 2": "https://drive.google.com/uc?id=1dE3K9cpQp3YlG04sExOx4thYAwUPdoQ3&export=download",
        "Mate in 3": "https://drive.google.com/uc?id=1ZEvJWtxXEZTsv1CVsVgQBclbvpRCjs5L&export=download",
        "Pin": "https://drive.google.com/uc?id=16rNkGaT6Aex1QSNGI2K-3GEWxCTQE5WT&export=download",
        "Skewer": "https://drive.google.com/uc?id=1cF1Eay5Yf5bhX3yCqfG9EhEE3DXie7MB&export=download",
        "Smothered Mate": "https://drive.google.com/uc?id=1hvr-gkE3L0Y06QseVytgULlMZCCNm1Er&export=download",
        "X Ray Attack": "https://drive.google.com/uc?id=1QDwp1KE5eQKNHEji00mmS7b_9BuJcGyA&export=download",
        "Others": "https://drive.google.com/uc?id=1fMJhApMsRS5CWs5smMhxk295Ysnt8znf&export=download",
    },
    "Endgame": {
        "Discovered Attack": "https://drive.google.com/uc?id=11LE59zmggaqoVNeXKfUS6bKmJp-w3q0L&export=download",
        "Double Attack": "https://drive.google.com/uc?id=1VKRTOI6KJrWYzpOFAoc_Lumbwhh5tYA0&export=download",
        "Double Check": "https://drive.google.com/uc?id=19EBK1HUlRaPSguhjUEtM0Pv7IJZoOOKS&export=download",
        "Fork": "https://drive.google.com/uc?id=18l4R9ki0249DR0sBDVcMewH-U_VikY20&export=download",
        "Intermezzo": "https://drive.google.com/uc?id=1f0Jl8XUbrToGPGG_GJOXiqxf-vDhtmDX&export=download",
        "Mate in 1": "https://drive.google.com/uc?id=1lZxTRwP7mPt_FkmIsyYdydRWsu02DeBZ&export=download",
        "Mate in 2": "https://drive.google.com/uc?id=1uQD9b15vSYn5cunYkA8vthhIyHgUlarn&export=download",
        "Mate in 3": "https://drive.google.com/uc?id=12rIyu1EYW1TsB-QFMcDTprvgJYSTTaFy&export=download",
        "Pin": "https://drive.google.com/uc?id=1veNDmXd2kjcoXMgztEztJ_tZ0pP2KzjD&export=download",
        "Skewer": "https://drive.google.com/uc?id=1L3h0di3XnzBgLcgumdANl-qbgj4s5yV0&export=download",
        "Smothered Mate": "https://drive.google.com/uc?id=1cyiI-G9aZYjbYc4iH44To1tx-a_BWJ2J&export=download",
        "X Ray Attack": "https://drive.google.com/uc?id=1PTc4AWg_y0liAlAMaLp7g6pVtW38tcEb&export=download",
        "Others": "https://drive.google.com/uc?id=1VuH3Ob-H_KIe_BRcH4YqvRfIBxTcSVPm&export=download",
    },
    "General Moments": {
        "Discovered Attack": "https://drive.google.com/uc?id=1-vG9uJxWmrkuEOg4-s3d8hD8psT-KKdD&export=download",
        "Double Attack": "https://drive.google.com/uc?id=1mYdUPjSdjzYZ1nlwyu5itGftiE-Xp0YU&export=download",
        "Double Check": "https://drive.google.com/uc?id=1Xow1bUtxY6pH-1q80ai537ZZ44yGZZzO&export=download",
        "Fork": "https://drive.google.com/uc?id=1KGW0s6FicnZigvKRrtivIt20mQN4waB7&export=download",
        "Intermezzo": "https://drive.google.com/uc?id=1hTG2T6EiG8JhPt2yVbccXIQ9A98W_ZXp&export=download",
        "Mate in 1": "https://drive.google.com/uc?id=1KrtvqJkoXh8NeK0X4OUrYesRJMF0t1v4&export=download",
        "Mate in 2": "https://drive.google.com/uc?id=1VlfYNXLNfA-YcsvQJ2euebSqSGbwbdkn&export=download",
        "Mate in 3": "https://drive.google.com/uc?id=1-IR6z9d6lbaTD0q4bT_rLu26jGUvihTi&export=download",
        "Pin": "https://drive.google.com/uc?id=1ZEJyBMZh4_9bv3pYFwwZtaU8XTGSbb3f&export=download",
        "Skewer": "https://drive.google.com/uc?id=1I7FG7xueCBjYClTY8TBp0e2d3tYmG7RA&export=download",
        "Smothered Mate": "https://drive.google.com/uc?id=1WzM-sjP8Op8mY0-S12xOTQp4T_T7a1P5&export=download",
        "X Ray Attack": "https://drive.google.com/uc?id=16mzHouKcyiGJBctY6BmU7Te9Y78XOQLW&export=download",
        "Others": "https://drive.google.com/uc?id=1I9YMoq4jpevkB0QseR_94X-4acucZkUq&export=download",
    }
}

# Campo para seleccionar categoría
st.header("1. Filtrar por categoría")
categoria_seleccionada = st.selectbox(
    "Selecciona una categoría:",
    [""] + list(google_drive_urls.keys()),
    help="Selecciona una categoría amplia como Openings, Midgame, Endgame, etc."
)

if categoria_seleccionada:
    # Campo para seleccionar subcategoría dentro de la categoría seleccionada
    subcategoria_seleccionada = st.selectbox(
        "Selecciona una subcategoría:",
        [""] + list(google_drive_urls[categoria_seleccionada].keys()),
        help="Selecciona una subcategoría dentro de la categoría."
    )
    
    if subcategoria_seleccionada:
        # Obtener el enlace de Google Drive correspondiente a la subcategoría seleccionada
        google_drive_url = google_drive_urls[categoria_seleccionada].get(subcategoria_seleccionada)

        # Cargar la partición correspondiente
        data_filtrada = load_partition_from_url(google_drive_url)

        if data_filtrada is not None:
            st.success(f"Se cargaron {len(data_filtrada)} registros para la subcategoría: {subcategoria_seleccionada}")
            
            # Campo para seleccionar rango de Elo
            st.header("2. Filtrar por rango de Elo (Rating)")
            min_rating = int(data_filtrada['Rating'].min())
            max_rating = int(data_filtrada['Rating'].max())
            rango_elo = st.slider(
                "Selecciona el rango de Elo:",
                min_value=min_rating,
                max_value=max_rating,
                value=(min_rating, max_rating),
                step=100,
                help="Ajusta el rango de Elo para encontrar ejercicios adecuados a tu nivel."
            )

            # Aplicar el filtro de rango de Elo
            data_filtrada = data_filtrada[
                (data_filtrada['Rating'] >= rango_elo[0]) & (data_filtrada['Rating'] <= rango_elo[1])
            ]

            # Implementar paginación
            st.header("3. Resultados filtrados")
            if not data_filtrada.empty:
                registros_por_pagina = 10
                total_paginas = (len(data_filtrada) - 1) // registros_por_pagina + 1
                pagina_actual = st.number_input(
                    "Página:",
                    min_value=1,
                    max_value=total_paginas,
                    value=1,
                    step=1,
                    help="Navega entre las páginas para ver los registros."
                )

                # Filtrar registros para la página actual
                inicio = (pagina_actual - 1) * registros_por_pagina
                fin = inicio + registros_por_pagina
                data_paginada = data_filtrada.iloc[inicio:fin]

                # Mostrar resultados en formato Markdown con paginación clara
                st.markdown(f"**Página {pagina_actual} de {total_paginas}**")
                for idx, row in data_paginada.iterrows():
                    st.markdown(f"""
                    **Ejercicio {idx + 1}**  
                    - **FEN**: `{row['FEN']}`  
                    - **ID del Ejercicio**: `{row['PuzzleId']}`  
                    - **Rating (Elo)**: `{row['Rating']}`  
                    - **Enlace**: {row['GameUrl']}  
                    ---
                    """)
            else:
                st.warning("No se encontraron registros con los filtros seleccionados.")
        else:
            st.error("Error al cargar la partición de la subcategoría seleccionada.")
else:
    st.info("Por favor, selecciona una categoría para continuar.")

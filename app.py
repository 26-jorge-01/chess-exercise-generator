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
Bienvenido al **Generador de Ejercicios de Ajedrez**.  
Esta herramienta utiliza datos provenientes de la base pública de puzzles de [Lichess](https://database.lichess.org/#puzzles), que contiene ejercicios tácticos y estratégicos extraídos de partidas reales.

---

### **Instrucciones de uso**:
1. Selecciona una categoría amplia (`Tactics`, `Strategy`, `Finals`, etc.).
2. Ajusta el rango de Elo (`Rating`) para obtener ejercicios adecuados para cierto nivel.
3. (Opcional) Filtra por temas específicos dentro del rango seleccionado (puedes elegir hasta 3 temas).
4. Navega por los resultados, paginados de 10 en 10.
5. Haz clic en el enlace para analizar o resolver cada ejercicio directamente en Lichess.

---

¡Explora, filtra y mejora tus habilidades!
""")

# Diccionario con URLs de las particiones por categoría
google_drive_urls = {
    "Tactics": "https://drive.google.com/uc?id=1WlWELH7opgwAEjCoZBtLEWCaGMMMy0B_&export=download",
    "Strategy <= 1800": "https://drive.google.com/uc?id=1KJ-lHjLsPfs7lApm9FQtWjGy2pR2k2PY&export=download",
    "Strategy > 1800": "https://drive.google.com/uc?id=13r-plkpAh5rNC57vceV-MsvbRQ-X4nc1&export=download",
    "Finals <= 1800": "https://drive.google.com/uc?id=1H8fjrURBNvlLQ-HyF6H3PoAlhlhPB4jm&export=download",
    "Finals > 1800": "https://drive.google.com/uc?id=1okARnELgLUXo4wATyclqRUWY59uDhg1M&export=download",
    "Attacks": "https://drive.google.com/uc?id=1NauotKPIGMBYmpN9VNciw5iasNYV3MwI&export=download",
    "Mate Patterns": "https://drive.google.com/uc?id=1jjMwGMvGh8MlmoFRib_QZWQtZ-87Cocf&export=download",
    "Other": "https://drive.google.com/uc?id=1GhE9OBH1aWIV19mWLpOwkd97_FU8rhPU&export=download"
}

# Campo para seleccionar categoría
st.header("1. Filtrar por categoría")
categoria_seleccionada = st.selectbox(
    "Selecciona una categoría:",
    [""] + list(google_drive_urls.keys()),
    help="Selecciona una categoría amplia como Tactics, Strategy, Finals, etc."
)

if categoria_seleccionada:
    # Obtener la URL de la categoría seleccionada
    google_drive_url = google_drive_urls.get(categoria_seleccionada)

    # Cargar solo la partición correspondiente
    data_filtrada = load_partition_from_url(google_drive_url)

    if data_filtrada is not None:
        st.success(f"Se cargaron {len(data_filtrada)} registros para la categoría: {categoria_seleccionada}")

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

        # Actualizar dinámicamente los temas según el rango de Elo seleccionado
        temas_filtrados = (
            data_filtrada['Themes']
            .str.split('\n')
            .explode()
            .unique()
        )
        temas_filtrados = sorted(temas_filtrados)

        # Campo para seleccionar hasta 3 temas
        st.header("3. Filtrar por tema (opcional)")
        temas_seleccionados = st.multiselect(
            "Selecciona hasta 3 temas:",
            temas_filtrados,
            default=[],
            help="Selecciona hasta 3 temas específicos dentro del rango de Elo seleccionado."
        )

        # Aplicar el filtro de temas si se seleccionan
        if temas_seleccionados:
            data_filtrada = data_filtrada[
                data_filtrada['Themes'].apply(lambda x: any(tema in x for tema in temas_seleccionados))
            ]

        # Implementar paginación
        st.header("4. Resultados filtrados")
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
        st.error("Error al cargar la partición de la categoría seleccionada.")
else:
    st.info("Por favor, selecciona una categoría para continuar.")

# 🎯 Generador de Ejercicios de Ajedrez
## 📌 Descripción
El Generador de Ejercicios de Ajedrez es una herramienta diseñada para apoyar a profesores de ajedrez en la preparación de clases, permitiéndoles generar ejercicios basados en temas específicos y niveles de habilidad de sus estudiantes.

Este proyecto toma como base los puzzles públicos de Lichess ([ver base de datos](https://database.lichess.org/#puzzles)), realiza una clasificación detallada y permite filtrar los ejercicios según categorías tácticas y estratégicas, así como por nivel de Elo.

## 🚀 Funcionalidades
* Filtrado por categoría y subcategoría: Los ejercicios se organizan en diferentes momentos de la partida y temáticas específicas.
* Filtrado por nivel de Elo: Se pueden seleccionar ejercicios adecuados para distintos niveles de habilidad.
* Visualización de resultados: Se muestra el FEN, el rating del ejercicio y un enlace directo a Lichess para ver la solución.
## 🏗️ Estructura del Proyecto
* 📘 asignacion.ipynb → Notebook donde se realizó la clasificación y partición de los ejercicios.
* 🎮 app.py → Aplicación principal desarrollada en Streamlit.
* 📦 requirements.txt → Lista de dependencias necesarias para ejecutar el proyecto.
* 📂 Base de Datos → Los datos están almacenados en formato Parquet en una carpeta de Google Drive, accesibles solo para lectura.
## 🛠️ Instalación y Ejecución
* 🔹 Requisitos Previos
  * Python 3.8 o superior
  * Dependencias indicadas en requirements.txt
* 🔹 Instalación
  1. Clona el repositorio:
    ```
    git clone https://github.com/26-jorge-01/chess-exercise-generator.git
    cd chess-exercise-generator
    ```
  2. Instala las dependencias:
    ```
    pip install -r requirements.txt
    ```
* 🔹 Ejecución
  
  Ejecuta la aplicación con Streamlit:
  ```
  streamlit run app.py
  ```

## 🖼️ Vista Previa
![chess-exercise-generator](https://github.com/user-attachments/assets/51258dfd-8705-4e22-b730-18cc0f0e6f59)

## 🔗 Enlace a la app
[Generador de Ejercicios de Ajedrez](https://chess-exercise-generator-p99a2zfbpncbxkdfkyawwa.streamlit.app/)

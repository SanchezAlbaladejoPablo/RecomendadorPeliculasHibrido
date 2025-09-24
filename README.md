# 🎬 Sistema de Recomendación Híbrido

[![Python](https://img.shields.io/badge/Python-3.9-blue.svg)](https://python.org)  
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-green.svg)](https://fastapi.tiangolo.com)  
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25.0-red.svg)](https://streamlit.io)  
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.1.1-orange.svg)](https://scikit-learn.org)  
[![Surprise](https://img.shields.io/badge/Surprise-1.1.1-purple.svg)](http://surpriselib.com)

Un sistema de recomendación híbrido completo que combina filtrado colaborativo y filtrado basado en contenido para proporcionar recomendaciones de películas personalizadas y precisas.

## 🎯 Descripción del Proyecto

Este proyecto implementa un sistema de recomendación híbrido profesional utilizando el dataset MovieLens 1M, que contiene 1 millón de calificaciones de 6,040 usuarios sobre 3,900 películas. El sistema combina dos enfoques principales:

- **Filtrado Colaborativo**: Utiliza Singular Value Decomposition (SVD) para encontrar patrones en las preferencias de usuarios similares  
- **Filtrado por Contenido**: Analiza las características de las películas usando TF-IDF para encontrar similitudes basadas en títulos y géneros  
- **Sistema Híbrido**: Combina ambos enfoques con ponderación 70% colaborativo / 30% contenido para obtener mejores recomendaciones  

## ✨ Características Principales

### 🔧 Tecnologías Utilizadas

- **Backend**: FastAPI con endpoints RESTful  
- **Frontend**: Streamlit con interfaz interactiva  
- **Machine Learning**: scikit-learn, Surprise  
- **Análisis de Datos**: pandas, numpy  
- **Visualización**: plotly, matplotlib, seaborn  
- **MLOps**: DVC para versionado de datos y modelos  
- **Control de Versiones**: Git  

### 🚀 Funcionalidades

1. **Recomendaciones Personalizadas**: Obtén recomendaciones híbridas para cualquier usuario  
2. **Películas Similares**: Encuentra películas similares basadas en contenido  
3. **Películas Populares**: Explora las películas más populares del dataset  
4. **Análisis de Datos**: Visualizaciones interactivas del dataset  
5. **API RESTful**: Endpoints completos para integración  
6. **Dashboard Interactivo**: Interfaz web intuitiva  

## 📊 Métricas y Evaluación

### Modelo de Filtrado Colaborativo (SVD)
- **RMSE**: 0.8729  
- **Dataset**: 80% entrenamiento / 20% prueba  
- **Parámetros**: Configuración por defecto optimizada  

### Modelo de Contenido (TF-IDF)
- **Vectorización**: TF-IDF con stop words en inglés  
- **Similitud**: Coseno entre vectores de características  
- **Características**: Títulos y géneros de películas  

## 🏗️ Estructura del Proyecto

RecommenderSystem/
├── data/
│ └── ml-1m/
├── notebooks/
│ └── eda.ipynb
├── src/
│ ├── recommend.py
│ └── utils.py
├── app/
│ ├── api.py
│ └── streamlit_app.py
├── models/
│ ├── svd_model.pkl
│ ├── tfidf_vectorizer.pkl
│ ├── cosine_sim_matrix.pkl
│ └── movies_with_soup.pkl
├── train.py
├── requirements.txt
├── dvc.yaml
└── README.md

markdown
Copiar código

## 🚀 Instalación y Configuración

### Prerrequisitos

- **Python 3.9** (recomendado usar conda)  
- Conda (Anaconda o Miniconda)  
- DVC (opcional, para versionado)  
- Git  

### Instalación usando Conda (recomendado en Windows)

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd RecommenderSystem
Crear entorno conda

bash
Copiar código
conda create -n recomendador python=3.9
conda activate recomendador
Instalar scikit-surprise precompilado y resto de dependencias

bash
Copiar código
# Instalar scikit-surprise desde conda-forge
conda install -c conda-forge scikit-surprise

# Instalar el resto de librerías
pip install -r requirements.txt
Descargar y preparar datos

bash
Copiar código
# Los datos ya están incluidos en data/ml-1m/
# Si necesitas reentrenar los modelos:
python train.py
🎮 Uso
1. Ejecutar la API
bash
Copiar código
cd app
python api.py
La API estará disponible en http://localhost:8000

2. Ejecutar el Dashboard
bash
Copiar código
cd app
streamlit run streamlit_app.py
El dashboard estará disponible en http://localhost:8501

3. Endpoints de la API
Recomendaciones para Usuario
pgsql
Copiar código
GET /recommend/user/{user_id}?n=10
Películas Similares
bash
Copiar código
GET /recommend/movie/{movie_id}?n=10
Películas Populares
bash
Copiar código
GET /recommend/popular?n=10
Información de Película
bash
Copiar código
GET /movies/{movie_id}
Calificaciones de Usuario
bash
Copiar código
GET /users/{user_id}/ratings?limit=20
📈 Análisis de Datos
1,000,209 calificaciones de 6,040 usuarios únicos

3,706 películas únicas en el dataset

Calificación promedio: 3.58/5.0

Géneros más populares: Drama, Comedy, Action

Distribución de calificaciones: Sesgada hacia calificaciones altas

🔄 MLOps y Versionado
DVC Pipeline
bash
Copiar código
# Reproducir pipeline completo
dvc repro

# Ver estado del pipeline
dvc status

# Ver DAG del pipeline
dvc dag
Versionado de Modelos
Modelos versionados con DVC

Pipeline reproducible definido en dvc.yaml

Datos y modelos trackeados automáticamente

🌐 Despliegue
Despliegue Local
API: python app/api.py

Dashboard: streamlit run app/streamlit_app.py

Despliegue en Producción
Frontend: Streamlit Cloud, Heroku, u otra plataforma compatible

Backend: FastAPI en Heroku, Railway, o servicios cloud similares

Datos: Los modelos pueden almacenarse en S3, GCS, o almacenamiento cloud

🧪 Testing
Pruebas de la API
bash
Copiar código
curl http://localhost:8000/
curl http://localhost:8000/recommend/user/1
curl http://localhost:8000/recommend/popular
Pruebas del Dashboard
Navegar a http://localhost:8501

Probar cada página del dashboard

Verificar que las recomendaciones se generen correctamente

📝 Casos de Uso
E-commerce de Entretenimiento: Recomendar películas a usuarios según su historial

Plataforma de Streaming: Sugerir contenido similar al que está viendo el usuario

Sistema de Reseñas: Proporcionar recomendaciones contextuales y análisis de tendencias

🤝 Contribución
Fork el proyecto

Crea una rama para tu feature (git checkout -b feature/AmazingFeature)

Commit tus cambios (git commit -m 'Add some AmazingFeature')

Push a la rama (git push origin feature/AmazingFeature)

Abre un Pull Request

📄 Licencia
Licencia MIT. Ver LICENSE para más detalles.

👥 Autores
Desarrollador Principal - Sistema de Recomendación Híbrido

🙏 Agradecimientos
GroupLens Research por el dataset MovieLens 1M

Surprise Library por las herramientas de filtrado colaborativo

Streamlit por la plataforma de dashboard interactivo

FastAPI por el framework de API moderno y rápido

📞 Soporte
Si tienes preguntas o necesitas ayuda:

Revisa la documentación en este README

Busca en los issues existentes

Crea un nuevo issue con detalles del problema

¡Gracias por usar el Sistema de Recomendación Híbrido! 🎬✨
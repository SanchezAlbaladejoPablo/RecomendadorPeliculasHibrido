
# 🎬 Sistema de Recomendación Híbrido

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.117.1-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.50.0-red.svg)](https://streamlit.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.7.2-orange.svg)](https://scikit-learn.org)
[![Surprise](https://img.shields.io/badge/Surprise-1.1.4-purple.svg)](http://surpriselib.com)

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

```
RecommenderSystem/
├── data/                    # Datos del proyecto
│   └── ml-1m/              # Dataset MovieLens 1M
├── notebooks/              # Jupyter notebooks para EDA
│   └── eda.ipynb          # Análisis exploratorio de datos
├── src/                    # Código fuente
│   ├── recommend.py       # Funciones de recomendación
│   └── utils.py          # Utilidades
├── app/                    # Aplicaciones
│   ├── api.py            # API FastAPI
│   └── streamlit_app.py  # Dashboard Streamlit
├── models/                 # Modelos entrenados
│   ├── svd_model.pkl
│   ├── tfidf_vectorizer.pkl
│   ├── cosine_sim_matrix.pkl
│   └── movies_with_soup.pkl
├── train.py               # Script de entrenamiento
├── requirements.txt       # Dependencias
├── dvc.yaml              # Pipeline DVC
└── README.md             # Documentación
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.11+
- Git
- DVC (opcional, para versionado)

### Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd RecommenderSystem
```

2. **Crear entorno Conda**
```bash
conda create -n recomendador python=3.11 -y
conda activate recomendador
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

   *Nota: Si encuentras problemas con alguna dependencia, intenta instalarla directamente con `conda install <paquete>` antes de usar `pip`.*

4. **Descargar y preparar datos**

Los datos del dataset MovieLens 1M ya están incluidos en la carpeta `data/ml-1m/`.

Si necesitas reentrenar los modelos (por ejemplo, después de modificar `train.py` o actualizar los datos), ejecuta:
```bash
python train.py
```

## 🎮 Uso

### 1. Ejecutar la API

```bash
cd app
python api.py
```

La API estará disponible en `http://localhost:8000`

### 2. Ejecutar el Dashboard

```bash
cd app
streamlit run streamlit_app.py
```

El dashboard estará disponible en `http://localhost:8501`

### 3. Endpoints de la API

#### Recomendaciones para Usuario
```
GET /recommend/user/{user_id}?n=10
```

#### Películas Similares
```
GET /recommend/movie/{movie_id}?n=10
```

#### Películas Populares
```
GET /recommend/popular?n=10
```

#### Información de Película
```
GET /movies/{movie_id}
```

#### Calificaciones de Usuario
```
GET /users/{user_id}/ratings?limit=20
```

## 📈 Análisis de Datos

El sistema incluye análisis exploratorio completo:

- **1,000,209 calificaciones** de 6,040 usuarios únicos
- **3,706 películas** únicas en el dataset
- **Calificación promedio**: 3.58/5.0
- **Géneros más populares**: Drama, Comedy, Action
- **Distribución de calificaciones**: Sesgada hacia calificaciones altas

## 🔄 MLOps y Versionado

### DVC Pipeline

El proyecto utiliza DVC para versionado de datos y modelos:

```bash
# Reproducir pipeline completo
dvc repro

# Ver estado del pipeline
dvc status

# Ver DAG del pipeline
dvc dag
```

### Versionado de Modelos

- Modelos versionados con DVC
- Pipeline reproducible definido en `dvc.yaml`
- Datos y modelos trackeados automáticamente

## 🌐 Despliegue

### Despliegue Local

1. **API**: `python app/api.py`
2. **Dashboard**: `streamlit run app/streamlit_app.py`

### Despliegue en Producción

El sistema está diseñado para despliegue en:

- **Frontend**: Streamlit Cloud, Heroku, o cualquier plataforma que soporte Python
- **Backend**: FastAPI en Heroku, Railway, o servicios cloud similares
- **Datos**: Los modelos pueden almacenarse en S3, GCS, o almacenamiento cloud

### URLs de Demostración

- **Dashboard**: [https://8501-igd9ms7mjyno8e9kav59t-05b3820d.manusvm.computer](https://8501-igd9ms7mjyno8e9kav59t-05b3820d.manusvm.computer)
- **API**: [https://8000-igd9ms7mjyno8e9kav59t-05b3820d.manusvm.computer](https://8000-igd9ms7mjyno8e9kav59t-05b3820d.manusvm.computer)

## 🧪 Testing

### Pruebas de la API

```bash
# Probar endpoint básico
curl http://localhost:8000/

# Probar recomendaciones para usuario
curl http://localhost:8000/recommend/user/1

# Probar películas populares
curl http://localhost:8000/recommend/popular
```

### Pruebas del Dashboard

1. Navegar a `http://localhost:8501`
2. Probar cada página del dashboard
3. Verificar que las recomendaciones se generen correctamente

## 📝 Casos de Uso

### 1. E-commerce de Entretenimiento
- Recomendar películas a usuarios basándose en su historial
- Aumentar engagement y tiempo en plataforma
- Personalizar experiencia de usuario

### 2. Plataforma de Streaming
- Sugerir contenido similar al que está viendo el usuario
- Descubrir nuevas películas basadas en preferencias
- Mejorar retención de usuarios

### 3. Sistema de Reseñas
- Ayudar a usuarios a encontrar películas que les gusten
- Proporcionar recomendaciones contextuales
- Análisis de tendencias de popularidad

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👥 Autores

- **Desarrollador Principal** - Sistema de Recomendación Híbrido

## 🙏 Agradecimientos

- **GroupLens Research** por el dataset MovieLens 1M
- **Surprise Library** por las herramientas de filtrado colaborativo
- **Streamlit** por la plataforma de dashboard interactivo
- **FastAPI** por el framework de API moderno y rápido

## 📞 Soporte

Si tienes preguntas o necesitas ayuda:

1. Revisa la documentación en este README
2. Busca en los issues existentes
3. Crea un nuevo issue con detalles del problema

---

**¡Gracias por usar el Sistema de Recomendación Híbrido!** 🎬✨


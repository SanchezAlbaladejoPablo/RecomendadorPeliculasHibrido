# Diseño de la Nueva Arquitectura del Flujo de Interacción

## 1. Introducción
El objetivo es mejorar la experiencia del usuario en el sistema de recomendación de películas, ofreciendo dos vías claras de interacción: explorar el sistema con un perfil de usuario existente aleatorio o crear un perfil rápido personalizado. Esto se logrará mediante la modificación de la interfaz de usuario en `streamlit_app.py` y la adición de nuevos endpoints en `api.py` para soportar las nuevas funcionalidades.

## 2. Cambios en `streamlit_app.py`

### 2.1. Página de Inicio (Home Page)
- Se modificará la página de inicio actual para incluir el texto introductorio y los dos botones principales.
- **Texto Introductorio**: "Este sistema recomienda películas en base a lo que ya has visto y lo que valoras. Solo necesitamos unas pistas de tus gustos para empezar."
- **Botón 1**: "🎲 Elegir Usuario Aleatorio"
- **Botón 2**: "⭐ Crear tu perfil rápido"

### 2.2. Flujo "Elegir Usuario Aleatorio"
- Al pulsar el botón "🎲 Elegir Usuario Aleatorio":
    - Se realizará una llamada a un nuevo endpoint de la API (`/random_user_ratings`).
    - Se mostrará un resumen de las valoraciones reales del usuario seleccionado (5-10 películas con sus ratings).
    - Se llamará al endpoint existente `/recommend/user/{user_id}` para obtener recomendaciones.
    - Las recomendaciones se mostrarán en una tabla con ID, título, géneros y una columna opcional "Razón".

### 2.3. Flujo "Crear tu perfil rápido"
- Al pulsar el botón "⭐ Crear tu perfil rápido":
    - Se realizará una llamada a un nuevo endpoint de la API (`/popular_movies_for_rating`) para obtener 5-10 títulos populares al azar.
    - Se presentará una interfaz donde el usuario pueda valorar estas películas (1 a 5 estrellas o slider).
    - Al finalizar las valoraciones, se enviarán a un nuevo endpoint de la API (`/recommend/custom_profile`).
    - El sistema generará recomendaciones personalizadas basadas en estas valoraciones y las mostrará en una tabla, similar al flujo de usuario aleatorio, con una explicación clara.

### 2.4. Componente de Visualización de Resultados
- Se creará o adaptará una función para mostrar las recomendaciones en una lista o tabla simple:
    - Formato: "🎬 The Lord of the Rings — Aventura, Fantasía"
    - Mensaje explicativo: "Estas recomendaciones se generaron a partir de tus valoraciones iniciales usando un modelo híbrido entrenado con 1 millón de calificaciones reales."

## 3. Cambios en `api.py`

### 3.1. Nuevo Endpoint: `/random_user_ratings`
- **Método**: GET
- **Descripción**: Selecciona un `user_id` aleatorio del dataset y devuelve sus últimas 5-10 valoraciones, junto con la información de las películas.
- **Salida**: JSON con `user_id`, `ratings` (lista de diccionarios con `movie_id`, `title`, `genres`, `rating`).

### 3.2. Nuevo Endpoint: `/popular_movies_for_rating`
- **Método**: GET
- **Descripción**: Devuelve una lista de 5-10 películas populares al azar para que el usuario las valore.
- **Salida**: JSON con `movies` (lista de diccionarios con `movie_id`, `title`, `genres`).

### 3.3. Nuevo Endpoint: `/recommend/custom_profile`
- **Método**: POST
- **Descripción**: Recibe un conjunto de valoraciones de películas de un perfil ficticio y genera recomendaciones personalizadas.
- **Entrada**: JSON con `ratings` (lista de diccionarios con `movie_id`, `rating`).
- **Salida**: JSON con `recommendations` (lista de diccionarios con `movie_id`, `title`, `genres`).

## 4. Modificaciones en `src/recommend.py` (si es necesario)
- Se podría necesitar una función auxiliar para `get_hybrid_recommendations` que acepte un DataFrame de ratings en lugar de un `user_id` para el perfil personalizado.

## 5. Resumen de la Interacción

```mermaid
graph TD
    A[Usuario Inicia Aplicación] --> B{Página de Inicio}
    B --> C[Botón: Elegir Usuario Aleatorio]
    B --> D[Botón: Crear tu perfil rápido]

    C --> E[API: /random_user_ratings]
    E --> F[Mostrar Valoraciones del Usuario Aleatorio]
    F --> G[API: /recommend/user/{user_id}]
    G --> H[Mostrar Recomendaciones (Tabla)]

    D --> I[API: /popular_movies_for_rating]
    I --> J[Mostrar Películas para Valorar]
    J --> K[Usuario Valora Películas]
    K --> L[API: /recommend/custom_profile (POST)]
    L --> H

    H --> M[Mensaje Explicativo]
```

Este diseño permitirá una interacción más dinámica y clara para el usuario, demostrando las capacidades del sistema de recomendación de manera efectiva.

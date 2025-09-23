
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Recomendación Híbrido",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL base de la API
API_BASE_URL = "http://localhost:8000"

# Título principal
st.title("🎬 Sistema de Recomendación Híbrido")
st.markdown("---")

# Sidebar para navegación
st.sidebar.title("Navegación")
page = st.sidebar.selectbox(
    "Selecciona una página:",
    ["Inicio", "Recomendaciones por Usuario", "Películas Similares", "Películas Populares", "Análisis de Datos"]
)

def make_api_request(endpoint):
    """Función auxiliar para hacer peticiones a la API"""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error en la API: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("No se puede conectar a la API. Asegúrate de que esté ejecutándose en http://localhost:8000")
        return None
    except Exception as e:
        st.error(f"Error inesperado: {str(e)}")
        return None

def display_movies(movies, title="Películas"):
    """Función auxiliar para mostrar películas en formato de tarjetas"""
    st.subheader(title)
    
    if not movies:
        st.warning("No se encontraron películas.")
        return
    
    # Crear columnas para mostrar las películas
    cols = st.columns(2)
    
    for i, movie in enumerate(movies):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"""
                <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin: 10px 0; background-color: #f9f9f9;">
                    <h4 style="color: #1f77b4; margin: 0 0 10px 0;">{movie['title']}</h4>
                    <p style="margin: 5px 0;"><strong>ID:</strong> {movie['movie_id']}</p>
                    <p style="margin: 5px 0;"><strong>Géneros:</strong> {movie['genres']}</p>
                </div>
                """, unsafe_allow_html=True)

# Página de Inicio
if page == "Inicio":
    st.header("Bienvenido al Sistema de Recomendación Híbrido")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Características del Sistema
        
        - **Filtrado Colaborativo**: Utiliza SVD para encontrar patrones en las preferencias de usuarios similares
        - **Filtrado por Contenido**: Analiza las características de las películas usando TF-IDF
        - **Sistema Híbrido**: Combina ambos enfoques para mejores recomendaciones
        - **Dataset**: MovieLens 1M con 1 millón de calificaciones
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 Cómo usar la aplicación
        
        1. **Recomendaciones por Usuario**: Ingresa un ID de usuario para obtener recomendaciones personalizadas
        2. **Películas Similares**: Busca películas similares a una película específica
        3. **Películas Populares**: Explora las películas más populares del dataset
        4. **Análisis de Datos**: Visualiza estadísticas del dataset
        """)
    
    # Verificar conexión con la API
    st.markdown("### 🔗 Estado de la API")
    api_status = make_api_request("/")
    if api_status:
        st.success("✅ API conectada correctamente")
        st.json(api_status)
    else:
        st.error("❌ No se puede conectar a la API")

# Página de Recomendaciones por Usuario
elif page == "Recomendaciones por Usuario":
    st.header("🎯 Recomendaciones Personalizadas")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        user_id = st.number_input("ID del Usuario", min_value=1, max_value=6040, value=1, step=1)
        num_recommendations = st.slider("Número de recomendaciones", min_value=5, max_value=20, value=10)
        
        if st.button("Obtener Recomendaciones", type="primary"):
            with st.spinner("Generando recomendaciones..."):
                recommendations = make_api_request(f"/recommend/user/{user_id}?n={num_recommendations}")
                
                if recommendations:
                    st.session_state.user_recommendations = recommendations
    
    with col2:
        if 'user_recommendations' in st.session_state:
            recommendations = st.session_state.user_recommendations
            st.success(f"Recomendaciones para el Usuario {recommendations['user_id']}")
            display_movies(recommendations['recommendations'], "Películas Recomendadas")
            
            # Mostrar calificaciones del usuario
            st.markdown("### 📊 Historial de Calificaciones del Usuario")
            user_ratings = make_api_request(f"/users/{user_id}/ratings?limit=10")
            if user_ratings:
                ratings_df = pd.DataFrame(user_ratings['ratings'])
                st.dataframe(ratings_df[['title', 'genres', 'rating']], use_container_width=True)

# Página de Películas Similares
elif page == "Películas Similares":
    st.header("🔍 Encuentra Películas Similares")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        movie_id = st.number_input("ID de la Película", min_value=1, max_value=3952, value=1, step=1)
        num_similar = st.slider("Número de películas similares", min_value=5, max_value=15, value=10)
        
        # Mostrar información de la película seleccionada
        if st.button("Buscar Información de la Película"):
            movie_info = make_api_request(f"/movies/{movie_id}")
            if movie_info:
                st.session_state.selected_movie = movie_info
        
        if 'selected_movie' in st.session_state:
            movie = st.session_state.selected_movie
            st.markdown(f"""
            **Película Seleccionada:**
            - **Título**: {movie['title']}
            - **Géneros**: {movie['genres']}
            """)
        
        if st.button("Encontrar Películas Similares", type="primary"):
            with st.spinner("Buscando películas similares..."):
                similar_movies = make_api_request(f"/recommend/movie/{movie_id}?n={num_similar}")
                
                if similar_movies:
                    st.session_state.similar_movies = similar_movies
    
    with col2:
        if 'similar_movies' in st.session_state:
            similar_movies = st.session_state.similar_movies
            st.success(f"Películas similares a la película ID {similar_movies['movie_id']}")
            display_movies(similar_movies['similar_movies'], "Películas Similares")

# Página de Películas Populares
elif page == "Películas Populares":
    st.header("🏆 Películas Más Populares")
    
    num_popular = st.slider("Número de películas populares", min_value=5, max_value=20, value=10)
    
    if st.button("Obtener Películas Populares", type="primary"):
        with st.spinner("Cargando películas populares..."):
            popular_movies = make_api_request(f"/recommend/popular?n={num_popular}")
            
            if popular_movies:
                st.session_state.popular_movies = popular_movies
    
    if 'popular_movies' in st.session_state:
        popular_movies = st.session_state.popular_movies
        display_movies(popular_movies['popular_movies'], "Películas Más Populares")

# Página de Análisis de Datos
elif page == "Análisis de Datos":
    st.header("📊 Análisis del Dataset MovieLens 1M")
    
    # Cargar datos localmente para análisis
    try:
        # Intentar cargar los datos desde el directorio local
        data_path = '../data/ml-1m/'
        
        # Cargar ratings
        rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
        ratings = pd.read_csv(os.path.join(data_path, 'ratings.dat'), 
                             sep='::', header=None, names=rnames, engine='python')
        
        # Cargar movies
        mnames = ['movie_id', 'title', 'genres']
        movies = pd.read_csv(os.path.join(data_path, 'movies.dat'), 
                            sep='::', header=None, names=mnames, engine='python', encoding='latin-1')
        
        # Estadísticas básicas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Calificaciones", f"{len(ratings):,}")
        
        with col2:
            st.metric("Total de Usuarios", f"{ratings['user_id'].nunique():,}")
        
        with col3:
            st.metric("Total de Películas", f"{ratings['movie_id'].nunique():,}")
        
        with col4:
            st.metric("Calificación Promedio", f"{ratings['rating'].mean():.2f}")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribución de calificaciones
            rating_counts = ratings['rating'].value_counts().sort_index()
            fig_ratings = px.bar(
                x=rating_counts.index, 
                y=rating_counts.values,
                title="Distribución de Calificaciones",
                labels={'x': 'Calificación', 'y': 'Número de Calificaciones'}
            )
            st.plotly_chart(fig_ratings, use_container_width=True)
        
        with col2:
            # Top 10 géneros más populares
            all_genres = []
            for genres in movies['genres']:
                all_genres.extend(genres.split('|'))
            
            genre_counts = pd.Series(all_genres).value_counts().head(10)
            fig_genres = px.bar(
                x=genre_counts.values,
                y=genre_counts.index,
                orientation='h',
                title="Top 10 Géneros Más Populares",
                labels={'x': 'Número de Películas', 'y': 'Género'}
            )
            st.plotly_chart(fig_genres, use_container_width=True)
        
        # Actividad de usuarios
        st.subheader("📈 Análisis de Actividad de Usuarios")
        user_activity = ratings.groupby('user_id')['rating'].count().sort_values(ascending=False)
        
        fig_activity = px.histogram(
            x=user_activity.values,
            nbins=50,
            title="Distribución de Actividad de Usuarios",
            labels={'x': 'Número de Calificaciones por Usuario', 'y': 'Número de Usuarios'}
        )
        st.plotly_chart(fig_activity, use_container_width=True)
        
        # Top películas más calificadas
        st.subheader("🎬 Top 10 Películas Más Calificadas")
        movie_ratings = ratings.groupby('movie_id').agg({
            'rating': ['count', 'mean']
        }).round(2)
        movie_ratings.columns = ['num_ratings', 'avg_rating']
        movie_ratings = movie_ratings.merge(movies, on='movie_id')
        top_movies = movie_ratings.nlargest(10, 'num_ratings')
        
        st.dataframe(
            top_movies[['title', 'genres', 'num_ratings', 'avg_rating']],
            use_container_width=True
        )
        
    except Exception as e:
        st.error(f"Error cargando los datos para análisis: {str(e)}")
        st.info("Asegúrate de que los archivos de datos estén en la ruta correcta.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Sistema de Recomendación Híbrido - MovieLens 1M Dataset</p>
    <p>Desarrollado con Streamlit, FastAPI, scikit-learn y Surprise</p>
</div>
""", unsafe_allow_html=True)


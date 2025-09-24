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
    initial_sidebar_state="collapsed"
)

# URL base de la API
API_BASE_URL = "http://localhost:8000"

# Título principal
st.title("🎬 Sistema de Recomendación Híbrido")
st.markdown("---")

def make_api_request(endpoint, method='GET', data=None):
    """Función auxiliar para hacer peticiones a la API"""
    try:
        if method == 'GET':
            response = requests.get(f"{API_BASE_URL}{endpoint}")
        elif method == 'POST':
            response = requests.post(f"{API_BASE_URL}{endpoint}", json=data)
        else:
            st.error(f"Método HTTP no soportado: {method}")
            return None

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error en la API: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("No se puede conectar a la API. Asegúrate de que esté ejecutándose en http://localhost:8000")
        return None
    except Exception as e:
        st.error(f"Error inesperado: {str(e)}")
        return None

def display_movies_table(movies, title="Películas", reason_col=False):
    """Función auxiliar para mostrar películas en formato de tabla con ID, título, géneros y opcionalmente razón"""
    st.subheader(title)
    
    if not movies:
        st.warning("No se encontraron películas.")
        return
    
    # Crear una lista de películas con formato mejorado
    for i, movie in enumerate(movies, 1):
        with st.container():
            st.markdown(f"""
            <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 16px; margin: 8px 0; background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <span style="background: #1f77b4; color: white; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: bold; margin-right: 12px;">{i}</span>
                    <h4 style="color: #1f77b4; margin: 0; font-size: 18px;">🎬 {movie['title']}</h4>
                </div>
                <p style="margin: 4px 0; color: #666; font-size: 14px;"><strong>Géneros:</strong> {movie['genres']}</p>
                {f'<p style="margin: 4px 0; color: #28a745; font-size: 13px; font-style: italic;"><strong>Razón:</strong> {movie.get("reason", "")}</p>' if reason_col and movie.get("reason") else ''}
            </div>
            """, unsafe_allow_html=True)

# --- Nueva Página de Inicio --- #

# Inicializar session_state para controlar la vista
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'home'

if st.session_state.current_view == 'home':
    # Texto introductorio con mejor diseño
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; margin: 20px 0; text-align: center; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
        <h2 style="margin: 0 0 15px 0; font-size: 28px;">¡Bienvenido al Sistema de Recomendación!</h2>
        <p style="margin: 0; font-size: 18px; opacity: 0.9;">Este sistema recomienda películas en base a lo que ya has visto y lo que valoras. Solo necesitamos unas pistas de tus gustos para empezar.</p>
    </div>
    """, unsafe_allow_html=True)

    # Botones principales con diseño mejorado
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 12px; border: 2px solid #e9ecef; text-align: center; margin-bottom: 20px;">
            <h3 style="color: #495057; margin: 0 0 10px 0;">🎲 Opción 1</h3>
            <p style="color: #6c757d; margin: 0 0 15px 0; font-size: 14px;">Explora el sistema con un perfil de usuario real del dataset MovieLens</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎲 Elegir Usuario Aleatorio", use_container_width=True, type="primary"):
            st.session_state.current_view = 'random_user_flow'
            st.session_state.current_view = 'random_user_flow'

    with col2:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 20px; border-radius: 12px; border: 2px solid #e9ecef; text-align: center; margin-bottom: 20px;">
            <h3 style="color: #495057; margin: 0 0 10px 0;">⭐ Opción 2</h3>
            <p style="color: #6c757d; margin: 0 0 15px 0; font-size: 14px;">Crea tu propio perfil valorando algunas películas populares</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⭐ Crear tu perfil rápido", use_container_width=True, type="secondary"):
            st.session_state.current_view = 'custom_profile_flow'
            st.session_state.current_view = 'random_user_flow'

    # Estado de la API con diseño mejorado
    st.markdown("---")
    st.markdown("### 🔗 Estado de la API")
    api_status = make_api_request("/")
    if api_status:
        st.success("✅ API conectada correctamente")
        with st.expander("Ver detalles de la API"):
            st.json(api_status)
    else:
        st.error("❌ No se puede conectar a la API")

elif st.session_state.current_view == 'random_user_flow':
    st.header("🎲 Explorar como un usuario real del dataset")
    
    if st.button("⬅️ Volver al Inicio"):
        st.session_state.current_view = 'home'
        st.session_state.current_view = 'random_user_flow'

    if 'random_user_data' not in st.session_state:
        with st.spinner("Seleccionando un usuario aleatorio y sus valoraciones..."):
            random_user_data = make_api_request("/random_user_ratings")
            if random_user_data:
                st.session_state.random_user_data = random_user_data
            else:
                st.error("No se pudo cargar la información del usuario aleatorio.")
                st.session_state.current_view = 'home'
                st.session_state.current_view = 'random_user_flow'

    if 'random_user_data' in st.session_state:
        user_id = st.session_state.random_user_data['user_id']
        user_ratings = st.session_state.random_user_data['ratings']

        # Mostrar información del usuario con diseño mejorado
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%); padding: 25px; border-radius: 12px; margin: 20px 0; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
            <h3 style="margin: 0 0 15px 0; font-size: 24px;">👤 Usuario Aleatorio #{user_id}</h3>
            <p style="margin: 0; font-size: 16px; opacity: 0.9;">Este usuario valoró las siguientes películas del dataset MovieLens:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar valoraciones del usuario en formato de tarjetas
        cols = st.columns(2)
        for i, rating in enumerate(user_ratings):
            with cols[i % 2]:
                stars = "⭐" * int(rating['rating'])
                st.markdown(f"""
                <div style="border: 1px solid #e0e0e0; border-radius: 8px; padding: 12px; margin: 4px 0; background: #f8f9fa;">
                    <h5 style="margin: 0 0 5px 0; color: #495057;">{rating['title']}</h5>
                    <p style="margin: 0; color: #6c757d; font-size: 12px;">{rating['genres']}</p>
                    <p style="margin: 5px 0 0 0; font-size: 16px;">{stars} ({rating['rating']}/5)</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("🎯 Recomendaciones para este usuario")
        with st.spinner("Generando recomendaciones..."):
            recommendations = make_api_request(f"/recommend/user/{user_id}?n=10")
            if recommendations:
                # Añadir una columna de razón para la explicación
                for rec in recommendations['recommendations']:
                    rec['reason'] = "Usuarios con gustos similares también valoraron esta película positivamente."
                display_movies_table(recommendations['recommendations'], "Películas Recomendadas", reason_col=True)
                st.markdown("""
                <div style="background: linear-gradient(135deg,                <div style="background: linear-gradient(135deg, #00b894 0%, #00a085 100%); padding: 20px; border-radius: 12px; margin: 20px 0; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                    <h4 style="margin: 0 0 10px 0;">💡 ¿Cómo funciona?</h4>
                    <p style="margin: 0; opacity: 0.9;">Estas recomendaciones se generaron a partir de las valoraciones del usuario usando un modelo híbrido entrenado con 1 millón de calificaciones reales del dataset MovieLens.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("No se pudieron generar recomendaciones para este usuario.")

elif st.session_state.current_view == 'custom_profile_flow':
    st.header("⭐ Crear tu perfil rápido")
    
    if st.button("⬅️ Volver al Inicio"):
        st.session_state.current_view = 'home'
        st.session_state.current_view = 'random_user_flow'

    if 'movies_to_rate' not in st.session_state:
        with st.spinner("Cargando películas populares para valorar..."):
            response = make_api_request("/popular_movies_for_rating?n=10")
            if response and response["movies"]:
                st.session_state.movies_to_rate = response["movies"]
                st.session_state.user_custom_ratings = {movie["movie_id"]: 0 for movie in response["movies"]}
            else:
                st.error("No se pudieron cargar películas para valorar.")
                st.session_state.current_view = 'home'
                st.session_state.current_view = 'random_user_flow'

    if 'movies_to_rate' in st.session_state:
        st.subheader("Valora estas películas (1-5 estrellas)")
        st.markdown("Por favor, valora algunas películas para que podamos entender tus gustos y ofrecerte las mejores recomendaciones.")
        
        all_rated = True
        for movie in st.session_state.movies_to_rate:
            movie_id = movie["movie_id"]
            current_rating = st.session_state.user_custom_ratings.get(movie_id, 0)
            
            new_rating = st.slider(
                f"**{movie['title']}** ({movie['genres']})",
                min_value=0, max_value=5, value=current_rating, step=1,
                key=f"rating_{movie_id}"
            )
            if new_rating == 0:
                all_rated = False
            st.session_state.user_custom_ratings[movie_id] = new_rating

        if st.button("Obtener Recomendaciones Personalizadas", type="primary", disabled=not all_rated):
            with st.spinner("Generando recomendaciones personalizadas..."):
                # Filtrar películas no valoradas (rating 0)
                valid_ratings = [
                    {"movie_id": mid, "rating": rating}
                    for mid, rating in st.session_state.user_custom_ratings.items()
                    if rating > 0
                ]
                
                if not valid_ratings:
                    st.warning("Por favor, valora al menos una película para obtener recomendaciones.")
                else:
                    recommendations_response = make_api_request(
                        "/recommend/custom_profile",
                        method='POST',
                        data={"ratings": valid_ratings}
                    )
                    
                    if recommendations_response:
                        st.session_state.custom_profile_recommendations = recommendations_response["recommendations"]
                        st.session_state.current_view = 'display_custom_recommendations'
                        st.session_state.current_view = 'random_user_flow'
                    else:
                        st.error("No se pudieron generar recomendaciones personalizadas.")

elif st.session_state.current_view == 'display_custom_recommendations':
    st.header("✨ Tus Recomendaciones Personalizadas")
    
    if st.button("⬅️ Volver a Valorar Películas"):
        st.session_state.current_view = 'custom_profile_flow'
        st.session_state.current_view = 'random_user_flow'

    if 'custom_profile_recommendations' in st.session_state:
        display_movies_table(st.session_state.custom_profile_recommendations, "Películas Recomendadas")
        st.markdown("""
        <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin: 10px 0; background-color: #f9f9f9;">
            <p style="margin: 5px 0;">Estas recomendaciones se generaron a partir de tus valoraciones iniciales usando un modelo híbrido entrenado con 1 millón de calificaciones reales.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No hay recomendaciones para mostrar. Por favor, valora algunas películas.")
        if st.button("Volver a la página de valoración"):
            st.session_state.current_view = 'custom_profile_flow'
            st.session_state.current_view = 'random_user_flow'

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>Sistema de Recomendación Híbrido - MovieLens 1M Dataset</p>
    <p>Desarrollado con Streamlit, FastAPI, scikit-learn y Surprise</p>
</div>
""", unsafe_allow_html=True)

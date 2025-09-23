
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import pickle
import os
import sys

# Añadir el directorio src al path para importar las funciones
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from recommend import load_data, get_hybrid_recommendations, get_content_recommendations, get_popular_recommendations

app = FastAPI(title="Sistema de Recomendación Híbrido", version="1.0.0")

# Configurar CORS para permitir acceso desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables globales para almacenar los modelos y datos
svd_model = None
tfidf_vectorizer = None
cosine_sim_matrix = None
movies = None
ratings = None

@app.on_event("startup")
async def load_models():
    global svd_model, tfidf_vectorizer, cosine_sim_matrix, movies, ratings
    
    # Cargar datos
    data_path = '../data/ml-1m/'
    movies_path = os.path.join(data_path, 'movies.dat')
    ratings_path = os.path.join(data_path, 'ratings.dat')
    ratings, movies = load_data(movies_path, ratings_path)
    
    # Cargar modelos
    models_path = '../models/'
    
    with open(os.path.join(models_path, 'svd_model.pkl'), 'rb') as f:
        svd_model = pickle.load(f)
    
    with open(os.path.join(models_path, 'tfidf_vectorizer.pkl'), 'rb') as f:
        tfidf_vectorizer = pickle.load(f)
    
    with open(os.path.join(models_path, 'cosine_sim_matrix.pkl'), 'rb') as f:
        cosine_sim_matrix = pickle.load(f)
    
    print("Modelos y datos cargados exitosamente")

@app.get("/")
async def root():
    return {"message": "Sistema de Recomendación Híbrido API"}

@app.get("/recommend/user/{user_id}")
async def recommend_for_user(user_id: int, n: int = 10):
    """
    Obtener recomendaciones híbridas para un usuario específico
    """
    if svd_model is None or movies is None or ratings is None:
        raise HTTPException(status_code=500, detail="Modelos no cargados")
    
    # Verificar si el usuario existe
    if user_id not in ratings['user_id'].values:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    try:
        recommendations = get_hybrid_recommendations(
            user_id, svd_model, movies, cosine_sim_matrix, ratings, n=n
        )
        
        result = []
        for _, row in recommendations.iterrows():
            result.append({
                "movie_id": int(row['movie_id']),
                "title": row['title'],
                "genres": row['genres']
            })
        
        return {
            "user_id": user_id,
            "recommendations": result,
            "count": len(result)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando recomendaciones: {str(e)}")

@app.get("/recommend/movie/{movie_id}")
async def recommend_similar_movies(movie_id: int, n: int = 10):
    """
    Obtener películas similares basadas en contenido
    """
    if cosine_sim_matrix is None or movies is None:
        raise HTTPException(status_code=500, detail="Modelos no cargados")
    
    # Verificar si la película existe
    if movie_id not in movies['movie_id'].values:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    try:
        recommendations = get_content_recommendations(
            movie_id, movies, cosine_sim_matrix, n=n
        )
        
        result = []
        for _, row in recommendations.iterrows():
            result.append({
                "movie_id": int(row['movie_id']),
                "title": row['title'],
                "genres": row['genres']
            })
        
        return {
            "movie_id": movie_id,
            "similar_movies": result,
            "count": len(result)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando recomendaciones: {str(e)}")

@app.get("/recommend/popular")
async def get_popular_movies(n: int = 10):
    """
    Obtener las películas más populares
    """
    if movies is None or ratings is None:
        raise HTTPException(status_code=500, detail="Datos no cargados")
    
    try:
        popular_movies = get_popular_recommendations(ratings, movies, n=n)
        
        result = []
        for _, row in popular_movies.iterrows():
            result.append({
                "movie_id": int(row['movie_id']),
                "title": row['title'],
                "genres": row['genres']
            })
        
        return {
            "popular_movies": result,
            "count": len(result)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo películas populares: {str(e)}")

@app.get("/movies/{movie_id}")
async def get_movie_info(movie_id: int):
    """
    Obtener información de una película específica
    """
    if movies is None:
        raise HTTPException(status_code=500, detail="Datos no cargados")
    
    movie = movies[movies['movie_id'] == movie_id]
    if movie.empty:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    movie_row = movie.iloc[0]
    return {
        "movie_id": int(movie_row['movie_id']),
        "title": movie_row['title'],
        "genres": movie_row['genres']
    }

@app.get("/users/{user_id}/ratings")
async def get_user_ratings(user_id: int, limit: int = 20):
    """
    Obtener las calificaciones de un usuario
    """
    if ratings is None or movies is None:
        raise HTTPException(status_code=500, detail="Datos no cargados")
    
    user_ratings = ratings[ratings['user_id'] == user_id].merge(
        movies, on='movie_id'
    ).sort_values('timestamp', ascending=False).head(limit)
    
    if user_ratings.empty:
        raise HTTPException(status_code=404, detail="Usuario no encontrado o sin calificaciones")
    
    result = []
    for _, row in user_ratings.iterrows():
        result.append({
            "movie_id": int(row['movie_id']),
            "title": row['title'],
            "genres": row['genres'],
            "rating": float(row['rating']),
            "timestamp": int(row['timestamp'])
        })
    
    return {
        "user_id": user_id,
        "ratings": result,
        "count": len(result)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


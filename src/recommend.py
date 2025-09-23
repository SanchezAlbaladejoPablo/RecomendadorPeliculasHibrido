
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pickle
import os

# Cargar datos
def load_data(movies_path, ratings_path):
    rnames = ["user_id", "movie_id", "rating", "timestamp"]
    mnames = ["movie_id", "title", "genres"]
    ratings = pd.read_csv(ratings_path, sep="::", header=None, names=rnames, engine="python")
    movies = pd.read_csv(movies_path, sep="::", header=None, names=mnames, engine="python", encoding="latin-1")
    return ratings, movies

# Modelo de popularidad (Baseline)
def get_popular_recommendations(ratings, movies, n=10):
    movie_popularity = ratings.groupby("movie_id")["rating"].count().sort_values(ascending=False)
    popular_movie_ids = movie_popularity.head(n).index
    return movies[movies["movie_id"].isin(popular_movie_ids)]

# Filtrado Colaborativo (SVD)
def train_svd_model(ratings):
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(ratings[["user_id", "movie_id", "rating"]], reader)
    trainset, testset = train_test_split(data, test_size=0.2, random_state=42)
    model = SVD(random_state=42)
    model.fit(trainset)
    predictions = model.test(testset)
    rmse = accuracy.rmse(predictions)
    return model, rmse

# Recomendador de Contenido (TF-IDF)
def train_content_model(movies):
    movies["soup"] = movies["title"] + " " + movies["genres"]
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(movies["soup"])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return tfidf, cosine_sim

def get_content_recommendations(movie_id, movies, cosine_sim, n=10):
    idx = movies[movies["movie_id"] == movie_id].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n+1]
    movie_indices = [i[0] for i in sim_scores]
    return movies.iloc[movie_indices]

# Recomendador Híbrido
def get_hybrid_recommendations(user_id, svd_model, movies, cosine_sim, ratings, weight_cf=0.7, weight_content=0.3, n=10):
    all_movie_ids = movies["movie_id"].unique()
    rated_movie_ids = ratings[ratings["user_id"] == user_id]["movie_id"].tolist()
    unrated_movie_ids = [mid for mid in all_movie_ids if mid not in rated_movie_ids]

    svd_preds = []
    for movie_id in unrated_movie_ids:
        svd_preds.append((movie_id, svd_model.predict(user_id, movie_id).est))
    svd_preds.sort(key=lambda x: x[1], reverse=True)
    top_svd_movies = svd_preds[:n]

    if rated_movie_ids:
        last_rated_movie_id = ratings[ratings["user_id"] == user_id].sort_values(by="timestamp", ascending=False)["movie_id"].iloc[0]
        content_recs = get_content_recommendations(last_rated_movie_id, movies, cosine_sim, n=n)
        content_movie_ids = content_recs["movie_id"].tolist()
    else:
        content_movie_ids = []

    hybrid_scores = {}
    for movie_id, score in top_svd_movies:
        hybrid_scores[movie_id] = score * weight_cf

    for movie_id in content_movie_ids:
        if movie_id in hybrid_scores:
            hybrid_scores[movie_id] += weight_content * 5
        else:
            hybrid_scores[movie_id] = weight_content * 5

    sorted_hybrid_recs = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)
    top_hybrid_movie_ids = [movie_id for movie_id, score in sorted_hybrid_recs[:n]]
    return movies[movies["movie_id"].isin(top_hybrid_movie_ids)]


if __name__ == "__main__":
    data_path = '../data/ml-1m/'
    movies_path = os.path.join(data_path, "movies.dat")
    ratings_path = os.path.join(data_path, "ratings.dat")

    ratings, movies = load_data(movies_path, ratings_path)

    print("\nTop 10 películas más populares:")
    popular_movies = get_popular_recommendations(ratings, movies, n=10)
    print(popular_movies[["title", "genres"]])

    print("\nEntrenando modelo SVD...")
    svd_model, svd_rmse = train_svd_model(ratings)
    print(f"RMSE del modelo SVD: {svd_rmse:.4f}")
    with open("../models/svd_model.pkl", "wb") as f:
        pickle.dump(svd_model, f)
    print("Modelo SVD guardado en models/svd_model.pkl")

    print("\nEntrenando recomendador de contenido...")
    tfidf_vectorizer, cosine_sim_matrix = train_content_model(movies)
    with open("../models/tfidf_vectorizer.pkl", "wb") as f:
        pickle.dump(tfidf_vectorizer, f)
    with open("../models/cosine_sim_matrix.pkl", "wb") as f:
        pickle.dump(cosine_sim_matrix, f)
    print("Vectorizador TF-IDF y matriz de similitud de coseno guardados en models/")

    toy_story_id = 1
    print(f"\nRecomendaciones de contenido para la película ID {toy_story_id} (Toy Story (1995)): ")
    content_recs = get_content_recommendations(toy_story_id, movies, cosine_sim_matrix, n=5)
    print(content_recs[["title", "genres"]])

    print("\nGenerando recomendaciones híbridas para el usuario 1...")
    user_id_example = 1
    hybrid_recs = get_hybrid_recommendations(user_id_example, svd_model, movies, cosine_sim_matrix, ratings, n=10)
    print(hybrid_recs[["title", "genres"]])

    print("\nComponentes del modelo híbrido (SVD, TF-IDF, Cosine Sim) guardados.")



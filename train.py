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
    return tfidf, cosine_sim, movies # Return movies with soup column


if __name__ == "__main__":
    data_path = "./data/ml-1m/"
    movies_path = os.path.join(data_path, "movies.dat")
    ratings_path = os.path.join(data_path, "ratings.dat")

    ratings, movies = load_data(movies_path, ratings_path)

    # Entrenar modelo SVD
    print("\nEntrenando modelo SVD...")
    svd_model, svd_rmse = train_svd_model(ratings)
    print(f"RMSE del modelo SVD: {svd_rmse:.4f}")
    with open("./models/svd_model.pkl", "wb") as f:
        pickle.dump(svd_model, f)
    print("Modelo SVD guardado en models/svd_model.pkl")

    # Entrenar recomendador de contenido
    print("\nEntrenando recomendador de contenido...")
    tfidf_vectorizer, cosine_sim_matrix, movies_with_soup = train_content_model(movies)
    with open("./models/tfidf_vectorizer.pkl", "wb") as f:
        pickle.dump(tfidf_vectorizer, f)
    with open("./models/cosine_sim_matrix.pkl", "wb") as f:
        pickle.dump(cosine_sim_matrix, f)
    with open("./models/movies_with_soup.pkl", "wb") as f:
        pickle.dump(movies_with_soup, f)
    print("Vectorizador TF-IDF, matriz de similitud de coseno y películas con columna soup guardados en models/")



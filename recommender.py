# app/services/recommender.py

import os
import joblib
import pandas as pd
import requests
from sklearn.metrics.pairwise import cosine_similarity
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../../"))
ARTIFACT_DIR = os.path.join(BACKEND_ROOT, "artifacts")


class ContentRecommender:

    def __init__(self):
        self.movies = joblib.load(os.path.join(ARTIFACT_DIR, "movies.pkl"))
        self.vectorizer = joblib.load(os.path.join(ARTIFACT_DIR, "tfidf.pkl"))
        self.tfidf_matrix = joblib.load(os.path.join(ARTIFACT_DIR, "tfidf_matrix.pkl"))

    def fetch_poster(self, title):
        if not TMDB_API_KEY:
            return None
        url = "https://api.themoviedb.org/3/search/movie"
        params = {"api_key": TMDB_API_KEY, "query": title}
        try:
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            if data.get("results"):
                poster_path = data["results"][0].get("poster_path")
                if poster_path:
                    return f"https://image.tmdb.org/t/p/w500{poster_path}"
        except Exception:
            pass
        return None

    def get_genres(self):
        genres = set()
        for g in self.movies.get("genres", pd.Series(dtype=str)).fillna(""):
            for genre in str(g).split():
                if genre:
                    genres.add(genre.strip().title())
        return sorted(genres)

    def recommend(self, query: str, top_n: int = 10):
        if not query:
            return []

        query = query.strip()

        # Free-text query: transform the raw input directly (no exact title match needed)
        query_vector = self.vectorizer.transform([query.lower()])
        similarity_scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        top_indices = similarity_scores.argsort()[-top_n:][::-1]

        results = []
        for idx in top_indices:
            movie_data = self.movies.iloc[idx]
            title = movie_data.get("title", "")
            encoded = quote_plus(title)

            imdb_rating = movie_data.get("imdb_rating", None)
            if not imdb_rating or str(imdb_rating) == "nan":
                imdb_rating = "N/A"

            results.append({
                "title": title,
                "overview": movie_data.get("overview", ""),
                "genres": movie_data.get("genres", ""),
                "imdb_rating": str(imdb_rating),
                "poster_url": self.fetch_poster(title),
                "wikipedia_url": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                "watch_links": {
                    "netflix": f"https://www.netflix.com/search?q={encoded}",
                    "prime": f"https://www.primevideo.com/search?k={encoded}",
                    "jiostar": f"https://www.jiocinema.com/search/{encoded}"
                }
            })

        return results

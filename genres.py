from fastapi import APIRouter
import joblib
import os

router = APIRouter(prefix="/genres", tags=["Genres"])

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS = os.path.join(BASE_DIR, "../../artifacts")
movies = joblib.load(os.path.join(ARTIFACTS, "movies.pkl"))


@router.get("/")
def all_genres():
    genres = set()
    for g in movies["genres"].fillna(""):
        for genre in str(g).split():
            if genre:
                genres.add(genre.strip().title())
    return sorted(genres)


@router.get("/{genre_name}")
def genre_movies(genre_name: str):
    data = movies[movies["genres"].str.contains(genre_name, case=False, na=False)]
    return data[["title", "genres"]].head(30).to_dict("records")

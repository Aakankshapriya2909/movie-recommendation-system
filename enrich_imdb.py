"""
enrich_imdb.py  —  Run ONCE after training to add IMDb ratings to movies.pkl

Usage:
    cd backend
    python -m app.scripts.enrich_imdb

Requires: OMDB_API_KEY in .env  (free key at https://www.omdbapi.com/apikey.aspx)
"""

import os
import time
import joblib
import requests
from dotenv import load_dotenv

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
APP_DIR     = os.path.dirname(SCRIPT_DIR)
BACKEND_DIR = os.path.dirname(APP_DIR)
ARTIFACTS_DIR = os.path.join(BACKEND_DIR, "artifacts")
MOVIES_PATH = os.path.join(ARTIFACTS_DIR, "movies.pkl")


def fetch_imdb_rating(title: str):
    try:
        r = requests.get(
            "http://www.omdbapi.com/",
            params={"apikey": OMDB_API_KEY, "t": title},
            timeout=5,
        )
        data = r.json()
        if data.get("Response") == "True":
            return data.get("imdbRating")
    except Exception:
        pass
    return None


if __name__ == "__main__":
    if not OMDB_API_KEY:
        print("OMDB_API_KEY not set in .env")
        exit(1)

    df = joblib.load(MOVIES_PATH)
    ratings = []

    for i, title in enumerate(df["title"]):
        rating = fetch_imdb_rating(title)
        ratings.append(rating)
        print(f"[{i+1}/{len(df)}] {title} -> {rating}")
        time.sleep(0.3)

    df["imdb_rating"] = ratings
    joblib.dump(df, MOVIES_PATH)
    print("Saved updated movies.pkl with IMDb ratings.")

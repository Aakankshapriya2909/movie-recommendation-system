print("ML ENGINE")

import os
import re
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# -----------------------------
# CONFIG
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../"))

DATA_PATH = os.path.join(BACKEND_ROOT, "data", "movies.csv")
ARTIFACT_DIR = os.path.join(BACKEND_ROOT, "artifacts")

os.makedirs(ARTIFACT_DIR, exist_ok=True)

# -----------------------------
# TEXT PREPROCESSING
# -----------------------------
def preprocess_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text

# -----------------------------
# LOAD DATA
# -----------------------------
def load_dataset(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    selected_features = [
        "genres",
        "keywords",
        "overview",
        "tagline",
        "original_title",
        "title",
        "cast",
        "director"
    ]

    for feature in selected_features:
        if feature not in df.columns:
            df[feature] = ""
        df[feature] = df[feature].fillna("").astype(str)

    df["combined_features"] = (
        df["genres"] + " " +
        df["keywords"] + " " +
        df["overview"] + " " +
        df["tagline"] + " " +
        df["original_title"] + " " +
        df["title"] + " " +
        df["cast"] + " " +
        df["director"]
    )

    df["combined_features"] = df["combined_features"].apply(preprocess_text)
    df = df.reset_index(drop=True)

    return df

# -----------------------------
# TRAIN MODEL
# -----------------------------
def train_content_model(df: pd.DataFrame):
    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(df["combined_features"])
    return vectorizer, tfidf_matrix

# -----------------------------
# SAVE ARTIFACTS
# -----------------------------
def save_artifacts(df, vectorizer, tfidf_matrix):
    joblib.dump(df, os.path.join(ARTIFACT_DIR, "movies.pkl"))
    joblib.dump(vectorizer, os.path.join(ARTIFACT_DIR, "tfidf.pkl"))
    joblib.dump(tfidf_matrix, os.path.join(ARTIFACT_DIR, "tfidf_matrix.pkl"))
    print("✅ Artifacts saved successfully.")

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    print("🚀 Training Content-Based Recommender")

    df = load_dataset(DATA_PATH)
    vectorizer, tfidf_matrix = train_content_model(df)
    save_artifacts(df, vectorizer, tfidf_matrix)

    print("🎯 Training completed.")
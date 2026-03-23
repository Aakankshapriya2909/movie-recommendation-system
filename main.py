from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.genres import router as genres_router
from app.api.library import router as library_router
from app.api.schemas import RecommendationResponse
from app.services.recommender import ContentRecommender

app = FastAPI(title="Movie Recommender API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(genres_router)
app.include_router(library_router)

# Load recommender once at startup
recommender = ContentRecommender()


@app.get("/")
def root():
    return {"message": "Movie Recommender API is running"}


@app.get("/recommend", response_model=RecommendationResponse)
def recommend(query: str, top_n: int = 10):
    result = recommender.recommend(query, top_n)
    return {
        "query": query,
        "results": result,
        "message": None
    }

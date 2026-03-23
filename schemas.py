from pydantic import BaseModel
from typing import List, Optional, Dict


class Movie(BaseModel):
    title: str
    overview: Optional[str] = ""
    genres: Optional[str] = ""
    imdb_rating: Optional[str] = "N/A"
    poster_url: Optional[str] = None
    wikipedia_url: Optional[str] = None
    watch_links: Optional[Dict[str, str]] = {}


class RecommendationResponse(BaseModel):
    query: str
    results: List[Movie]
    message: Optional[str] = None

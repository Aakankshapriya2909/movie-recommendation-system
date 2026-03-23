from fastapi import APIRouter

router = APIRouter(prefix="/library", tags=["Library"])

# In-memory library store per user
library: dict = {}


@router.post("/add")
def add_movie(username: str, movie: str):
    library.setdefault(username, [])
    if movie not in library[username]:
        library[username].append(movie)
        return {"message": "Movie added to library"}
    return {"message": "Already in library"}


@router.delete("/remove")
def remove_movie(username: str, movie: str):
    if username in library and movie in library[username]:
        library[username].remove(movie)
    return {"message": "Removed"}


@router.get("/{username}")
def get_library(username: str):
    return library.get(username, [])

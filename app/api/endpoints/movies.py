from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud.movie import get_movie, get_trending_movies, get_popular_movies, search_movies_db
from app.schemas.movie import Movie

router = APIRouter()

@router.get("/trending", response_model=List[Movie])
def trending_movies(db: Session = Depends(get_db)):
    return get_trending_movies(db)

@router.get("/popular", response_model=List[Movie])
def popular_movies(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return get_popular_movies(db, skip=skip, limit=limit)

@router.get("/search", response_model=List[Movie])
def search_movies(query: str, db: Session = Depends(get_db)):
    return search_movies_db(db, query=query)

@router.get("/{movie_id}", response_model=Movie)
def movie_details(movie_id: int, db: Session = Depends(get_db)):
    db_movie = get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie
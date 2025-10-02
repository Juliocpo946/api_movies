import os
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import httpx
from datetime import timedelta
import asyncio

# Importaciones locales
import crud
import models
import schemas
import auth
from database import SessionLocal, engine, get_db

# --- Configuración Inicial ---
# Crea las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "c36bfcf4ed331318874f906b8aa56964")
TMDB_BASE_URL = os.getenv("TMDB_BASE_URL", "https://api.themoviedb.org/3")
app = FastAPI(title="Movie Night API", description="API para la aplicación Movie Night")

# --- Endpoints ---

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Movie Night API!"}

@app.get("/movies/trending", response_model=List[schemas.Movie], tags=["Movies"])
def get_trending_movies(db: Session = Depends(get_db)):
    """
    Devuelve las 10 películas más populares. Ideal para el carrusel de tendencias.
    """
    return crud.get_trending_movies(db)

@app.get("/movies/popular", response_model=List[schemas.Movie], tags=["Movies"])
def get_popular_movies(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """
    Devuelve una lista paginada de películas populares. Ideal para el grid principal con scroll.
    """
    return crud.get_popular_movies(db, skip=skip, limit=limit)

@app.get("/movies/search", response_model=List[schemas.Movie], tags=["Movies"])
def search_movies(query: str, db: Session = Depends(get_db)):
    # La búsqueda se hace directamente en la API de TMDB para obtener resultados actualizados
    # y luego se guardan/actualizan en la BD local.
    # (Esta parte se puede implementar si se desea, por ahora busca en la BD local)
    return crud.search_movies_db(db, query=query)


@app.get("/movies/{movie_id}", response_model=schemas.Movie, tags=["Movies"])
def get_movie_details(movie_id: int, db: Session = Depends(get_db)):
    db_movie = crud.get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

# --- Endpoints de Usuario, Favoritos y Calificaciones (sin cambios) ---

@app.post("/users/register", response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(user.password)
    return crud.create_user(db=db, user=user, hashed_password=hashed_password)

@app.post("/users/login", response_model=schemas.Token, tags=["Users"])
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id, "username": user.username}

@app.get("/users/{user_id}/favorites", response_model=List[schemas.Movie], tags=["Favorites"])
def get_user_favorites(user_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user's favorites")
    return crud.get_user_favorites(db, user_id=user_id)

@app.post("/users/{user_id}/favorites", status_code=status.HTTP_201_CREATED, tags=["Favorites"])
def add_favorite(user_id: int, favorite: schemas.FavoriteCreate, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.add_favorite(db, user_id=user_id, movie_id=favorite.movie_id)

@app.delete("/users/{user_id}/favorites/{movie_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Favorites"])
def remove_favorite(user_id: int, movie_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    crud.remove_favorite(db, user_id=user_id, movie_id=movie_id)
    return {"ok": True}

@app.get("/users/{user_id}/ratings", response_model=List[schemas.Rating], tags=["Ratings"])
def get_user_ratings(user_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.get_user_ratings(db, user_id=user_id)

@app.post("/users/{user_id}/ratings", response_model=schemas.Rating, tags=["Ratings"])
def add_or_update_rating(user_id: int, rating: schemas.RatingCreate, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.add_or_update_rating(db, user_id=user_id, movie_id=rating.movie_id, score=rating.score)

@app.delete("/users/{user_id}/ratings/{movie_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Ratings"])
def delete_rating(user_id: int, movie_id: int, current_user: schemas.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    crud.delete_rating(db, user_id=user_id, movie_id=movie_id)
    return {"ok": True}


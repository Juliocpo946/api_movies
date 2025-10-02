from sqlalchemy.orm import Session
from sqlalchemy import desc

import models
import schemas
from auth import get_password_hash

# --- CRUD para Usuarios ---
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(
        username=user.username, 
        email=user.email, 
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- CRUD para Películas ---
def get_movie(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

def create_or_update_movie(db: Session, movie_data: dict):
    movie_id = movie_data.get('id')
    db_movie = get_movie(db, movie_id)
    
    # Validar y crear el objeto Pydantic
    movie_schema = schemas.MovieCreate(
        id=movie_data.get('id'),
        title=movie_data.get('title'),
        overview=movie_data.get('overview'),
        poster_path=movie_data.get('poster_path'),
        backdrop_path=movie_data.get('backdrop_path'),
        release_date=movie_data.get('release_date'),
        vote_average=movie_data.get('vote_average'),
        vote_count=movie_data.get('vote_count'),
        popularity=movie_data.get('popularity')
    )

    if db_movie:
        # Actualizar película existente
        for key, value in movie_schema.dict().items():
            setattr(db_movie, key, value)
    else:
        # Crear nueva película
        db_movie = models.Movie(**movie_schema.dict())
        db.add(db_movie)
    
    db.commit()
    db.refresh(db_movie)
    return db_movie

def get_trending_movies(db: Session):
    """Obtiene las 10 películas con mayor popularidad."""
    return db.query(models.Movie).order_by(desc(models.Movie.popularity)).limit(10).all()

def get_popular_movies(db: Session, skip: int = 0, limit: int = 20):
    """Obtiene una lista paginada de películas, ordenadas por popularidad."""
    return db.query(models.Movie).order_by(desc(models.Movie.popularity)).offset(skip).limit(limit).all()

def search_movies_db(db: Session, query: str):
    """Busca películas en la base de datos local cuyo título contenga el query."""
    return db.query(models.Movie).filter(models.Movie.title.ilike(f"%{query}%")).all()


# --- CRUD para Favoritos ---
def get_user_favorites(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return []
    return [fav.movie for fav in user.favorites]

def add_favorite(db: Session, user_id: int, movie_id: int):
    db_movie = get_movie(db, movie_id)
    if not db_movie:
        raise ValueError(f"Movie with id {movie_id} not found")
    db_favorite = db.query(models.Favorite).filter_by(user_id=user_id, movie_id=movie_id).first()
    if db_favorite:
        return db_favorite

    db_favorite = models.Favorite(user_id=user_id, movie_id=movie_id)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

def remove_favorite(db: Session, user_id: int, movie_id: int):
    db_favorite = db.query(models.Favorite).filter_by(user_id=user_id, movie_id=movie_id).first()
    if db_favorite:
        db.delete(db_favorite)
        db.commit()
    return

# --- CRUD para Calificaciones ---
def get_user_ratings(db: Session, user_id: int):
    return db.query(models.Rating).filter(models.Rating.user_id == user_id).all()

def add_or_update_rating(db: Session, user_id: int, movie_id: int, score: float):
    db_rating = db.query(models.Rating).filter_by(user_id=user_id, movie_id=movie_id).first()
    if db_rating:
        db_rating.score = score
    else:
        db_rating = models.Rating(user_id=user_id, movie_id=movie_id, score=score)
        db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def delete_rating(db: Session, user_id: int, movie_id: int):
    db_rating = db.query(models.Rating).filter_by(user_id=user_id, movie_id=movie_id).first()
    if db_rating:
        db.delete(db_rating)
        db.commit()
    return


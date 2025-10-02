from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.models import Movie
from app.schemas.movie import MovieCreate

def get_movie(db: Session, movie_id: int):
    return db.query(Movie).filter(Movie.id == movie_id).first()

def create_or_update_movie(db: Session, movie_data: dict):
    movie_id = movie_data.get('id')
    db_movie = get_movie(db, movie_id)
    movie_schema = MovieCreate(
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
        for key, value in movie_schema.dict().items():
            setattr(db_movie, key, value)
    else:
        db_movie = Movie(**movie_schema.dict())
        db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def get_trending_movies(db: Session):
    return db.query(Movie).order_by(desc(Movie.popularity)).limit(10).all()

def get_popular_movies(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Movie).order_by(desc(Movie.popularity)).offset(skip).limit(limit).all()

def search_movies_db(db: Session, query: str):
    return db.query(Movie).filter(Movie.title.ilike(f"%{query}%")).all()
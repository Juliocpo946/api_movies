from sqlalchemy.orm import Session
from app.db.models import User, Favorite
from app.crud.movie import get_movie

def get_user_favorites(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    return [fav.movie for fav in user.favorites] if user else []

def add_favorite(db: Session, user_id: int, movie_id: int):
    db_movie = get_movie(db, movie_id)
    if not db_movie:
        raise ValueError(f"Movie with id {movie_id} not found")
    db_favorite = db.query(Favorite).filter_by(user_id=user_id, movie_id=movie_id).first()
    if db_favorite:
        return db_favorite
    db_favorite = Favorite(user_id=user_id, movie_id=movie_id)
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite

def remove_favorite(db: Session, user_id: int, movie_id: int):
    db_favorite = db.query(Favorite).filter_by(user_id=user_id, movie_id=movie_id).first()
    if db_favorite:
        db.delete(db_favorite)
        db.commit()
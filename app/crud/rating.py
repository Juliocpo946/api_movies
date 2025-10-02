from sqlalchemy.orm import Session
from app.db.models import Rating

def get_user_ratings(db: Session, user_id: int):
    return db.query(Rating).filter(Rating.user_id == user_id).all()

def add_or_update_rating(db: Session, user_id: int, movie_id: int, score: float):
    db_rating = db.query(Rating).filter_by(user_id=user_id, movie_id=movie_id).first()
    if db_rating:
        db_rating.score = score
    else:
        db_rating = Rating(user_id=user_id, movie_id=movie_id, score=score)
        db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def delete_rating(db: Session, user_id: int, movie_id: int):
    db_rating = db.query(Rating).filter_by(user_id=user_id, movie_id=movie_id).first()
    if db_rating:
        db.delete(db_rating)
        db.commit()
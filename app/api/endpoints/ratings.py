from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.deps import get_current_user
from app.crud.rating import get_user_ratings, add_or_update_rating, delete_rating
from app.schemas.rating import Rating, RatingCreate
from app.schemas.user import User

router = APIRouter()

@router.get("/{user_id}/ratings", response_model=List[Rating])
def user_ratings(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return get_user_ratings(db, user_id=user_id)

@router.post("/{user_id}/ratings", response_model=Rating)
def create_or_update_rating(user_id: int, rating: RatingCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return add_or_update_rating(db, user_id=user_id, movie_id=rating.movie_id, score=rating.score)

@router.delete("/{user_id}/ratings/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_rating(user_id: int, movie_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    delete_rating(db, user_id=user_id, movie_id=movie_id)
    return {"ok": True}
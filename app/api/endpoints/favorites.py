from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.deps import get_current_user
from app.crud.favorite import get_user_favorites, add_favorite, remove_favorite
from app.schemas.movie import Movie
from app.schemas.favorite import FavoriteCreate
from app.schemas.user import User

router = APIRouter()

@router.get("/{user_id}/favorites", response_model=List[Movie])
def user_favorites(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user's favorites")
    return get_user_favorites(db, user_id=user_id)

@router.post("/{user_id}/favorites", status_code=status.HTTP_201_CREATED)
def create_favorite(user_id: int, favorite: FavoriteCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return add_favorite(db, user_id=user_id, movie_id=favorite.movie_id)

@router.delete("/{user_id}/favorites/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_favorite(user_id: int, movie_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    remove_favorite(db, user_id=user_id, movie_id=movie_id)
    return {"ok": True}
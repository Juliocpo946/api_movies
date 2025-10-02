from pydantic import BaseModel, ConfigDict
from app.schemas.movie import Movie

class FavoriteBase(BaseModel):
    user_id: int
    movie_id: int

class FavoriteCreate(BaseModel):
    movie_id: int

class Favorite(FavoriteBase):
    id: int
    movie: Movie
    model_config = ConfigDict(from_attributes=True)
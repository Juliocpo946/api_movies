from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# --- Esquemas para Películas ---
class MovieBase(BaseModel):
    id: int
    title: str
    overview: Optional[str] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    release_date: Optional[str] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None
    popularity: Optional[float] = None

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    model_config = ConfigDict(from_attributes=True) # <-- CAMBIO CLAVE: orm_mode a from_attributes con ConfigDict

# --- Esquemas para Usuarios ---
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True) # <-- CAMBIO CLAVE

# --- Esquemas para Favoritos ---
class FavoriteBase(BaseModel):
    user_id: int
    movie_id: int

class FavoriteCreate(BaseModel):
    movie_id: int

class Favorite(FavoriteBase):
    id: int
    movie: Movie

    model_config = ConfigDict(from_attributes=True) # <-- CAMBIO CLAVE

# --- Esquemas para Calificaciones ---
class RatingBase(BaseModel):
    score: float

class RatingCreate(RatingBase):
    movie_id: int

class Rating(RatingBase):
    id: int
    movie_id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True) # <-- CAMBIO CLAVE


# --- Esquemas para Autenticación ---
class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str

class TokenData(BaseModel):
    username: Optional[str] = None


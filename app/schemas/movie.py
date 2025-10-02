from pydantic import BaseModel, ConfigDict
from typing import Optional

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
    model_config = ConfigDict(from_attributes=True)
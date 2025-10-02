from pydantic import BaseModel, ConfigDict

class RatingBase(BaseModel):
    score: float

class RatingCreate(RatingBase):
    movie_id: int

class Rating(RatingBase):
    id: int
    movie_id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)
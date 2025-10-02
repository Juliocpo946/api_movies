from fastapi import FastAPI
from app.db.database import engine
from app.db import models
from app.api.endpoints import auth, movies, favorites, ratings

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movie Night API", description="API para la aplicación Movie Night")

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Movie Night API!"}

app.include_router(auth.router, prefix="/users", tags=["Users"])
app.include_router(movies.router, prefix="/movies", tags=["Movies"])
app.include_router(favorites.router, prefix="/users", tags=["Favorites"])
app.include_router(ratings.router, prefix="/users", tags=["Ratings"])
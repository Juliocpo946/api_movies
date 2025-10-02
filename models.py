from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# --- Tabla de Asociación para la relación muchos a muchos ---
movie_category_association = Table(
    'movie_category_association', Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('movie_categories.id'), primary_key=True)
)

# --- Modelo de Película ---
class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    overview = Column(String)
    poster_path = Column(String, nullable=True)
    backdrop_path = Column(String, nullable=True)
    release_date = Column(String, nullable=True)
    vote_average = Column(Float, nullable=True)
    vote_count = Column(Integer, nullable=True)
    popularity = Column(Float, nullable=True)

    # Relaciones
    ratings = relationship("Rating", back_populates="movie")
    favorited_by = relationship("Favorite", back_populates="movie")
    categories = relationship("MovieCategory", secondary=movie_category_association, back_populates="movies")

# --- Modelo de Categoría de Película ---
class MovieCategory(Base):
    __tablename__ = "movie_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True) # "popular", "top_rated", etc.

    movies = relationship("Movie", secondary=movie_category_association, back_populates="categories")


# --- Modelo de Usuario ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # Relaciones
    favorites = relationship("Favorite", back_populates="user")
    ratings = relationship("Rating", back_populates="user")

# --- Modelo de Favorito ---
class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))

    # Relaciones
    user = relationship("User", back_populates="favorites")
    movie = relationship("Movie", back_populates="favorited_by")


# --- Modelo de Calificación ---
class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    score = Column(Float)

    # Relaciones
    user = relationship("User", back_populates="ratings")
    movie = relationship("Movie", back_populates="ratings")


import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Boolean, Text, BigInteger
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SQLITE_PATH = BASE_DIR / "database" / "recommendation.db"

# Load environment variables from the project root so imports work from any cwd.
load_dotenv(BASE_DIR / ".env")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


def _build_database_url() -> str:
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    return f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def _create_engine():
    database_url = _build_database_url()

    try:
        candidate_engine = create_engine(database_url, pool_pre_ping=True)
        with candidate_engine.connect():
            pass
        return candidate_engine
    except OperationalError as exc:
        fallback_url = f"sqlite:///{DEFAULT_SQLITE_PATH.as_posix()}"
        print(
            "PostgreSQL is unavailable, falling back to local SQLite database "
            f"at {DEFAULT_SQLITE_PATH}. Original error: {exc}"
        )
        return create_engine(
            fallback_url,
            connect_args={"check_same_thread": False},
        )


engine = _create_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- SCHEMA DEFINITIONS ---

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    gender = Column(String)

class Movie(Base):
    __tablename__ = "movies"
    movie_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    genre = Column(String)
    release_year = Column(Integer)
    runtime_min = Column(Integer)
    overview = Column(Text)
    poster_url = Column(Text)
    trailer_url = Column(Text)
    language = Column(String)
    country = Column(String)
    director = Column(String)
    cast = Column(Text)
    tmdb_id = Column(String)
    omdb_id = Column(String)
    average_rating = Column(Float)
    rating_count = Column(Integer)
    popularity = Column(Float)

class Rating(Base):
    __tablename__ = "ratings"
    rating_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    movie_id = Column(Integer, ForeignKey("movies.movie_id"))
    rating = Column(Float)
    timestamp = Column(BigInteger)

class Recommendation(Base):
    __tablename__ = "recommendations"
    recommendation_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    movie_id = Column(Integer, ForeignKey("movies.movie_id"))
    score = Column(Float)
    provider = Column(String)
    prompt = Column(Text)

class Feedback(Base):
    __tablename__ = "feedback"
    feedback_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    movie_id = Column(Integer, ForeignKey("movies.movie_id"))
    liked = Column(Boolean)
    comment = Column(Text)

class UserEvent(Base):
    __tablename__ = "user_events"
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    event_type = Column(String)
    payload = Column(Text)

def init_db():
    """Creates all tables in the database."""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")
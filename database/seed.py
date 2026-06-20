from __future__ import annotations

import os
import sys

import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_connection import Feedback, Movie, Rating, Recommendation, SessionLocal, User, init_db
from services.preprocess import download_and_extract_data, load_and_clean_data

def seed_database():
    """Populates PostgreSQL with the processed MovieLens data."""
    init_db()
    db = SessionLocal()
    
    print("Loading data for seeding...")
    download_and_extract_data()
    users_df, movies_df, ratings_df = load_and_clean_data()
    
    # Check if data already exists to avoid duplication
    if db.query(User).first():
        print("Database already seeded. Skipping.")
        db.close()
        return

    print("Inserting Users...")
    user_records = users_df.to_dict(orient='records')
    db.bulk_insert_mappings(User, user_records)
    
    print("Inserting Movies...")
    movies_df = movies_df.rename(columns={'movieId': 'movie_id', 'genres': 'genre'})
    if 'release_year' not in movies_df.columns:
        movies_df['release_year'] = movies_df['title'].str.extract(r'\((\d{4})\)').astype(float)
    movie_records = movies_df[['movie_id', 'title', 'genre']].to_dict(orient='records')
    db.bulk_insert_mappings(Movie, movie_records)
    
    print("Inserting Ratings (This might take a moment)...")
    ratings_df = ratings_df.rename(columns={'userId': 'user_id', 'movieId': 'movie_id'})
    rating_records = ratings_df[['user_id', 'movie_id', 'rating', 'timestamp']].to_dict(orient='records')
    db.bulk_insert_mappings(Rating, rating_records)

    if not db.query(Recommendation).first():
        db.bulk_insert_mappings(Recommendation, [])
    if not db.query(Feedback).first():
        db.bulk_insert_mappings(Feedback, [])
    
    db.commit()
    db.close()
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
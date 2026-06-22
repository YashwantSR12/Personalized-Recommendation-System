import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# Ensure Python can find the database module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_connection import engine

EDA_DIR = os.path.join("outputs", "eda")

def run_eda():
    """Fetches data from PostgreSQL and generates EDA visualizations."""
    print("Fetching data from PostgreSQL...")
    
    # Using Pandas to read directly from our SQL tables
    ratings_df = pd.read_sql("SELECT * FROM ratings", engine)
    movies_df = pd.read_sql("SELECT * FROM movies", engine)
    
    # Merge datasets for comprehensive analysis
    df = pd.merge(ratings_df, movies_df, on='movie_id')
    
    print("Generating Visualizations...")
    
    # 1. Rating Distribution
    plt.figure(figsize=(10, 6))
    df['rating'].value_counts().sort_index().plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Distribution of Movie Ratings')
    plt.xlabel('Rating')
    plt.ylabel('Count')
    plt.grid(axis='y', alpha=0.75)
    plt.savefig(os.path.join(EDA_DIR, "rating_distribution.png"))
    plt.close()

    # 2. Top 10 Most Rated Movies (Popularity)
    plt.figure(figsize=(12, 6))
    top_movies = df['title'].value_counts().head(10)
    top_movies.plot(kind='barh', color='coral', edgecolor='black')
    plt.title('Top 10 Most Rated Movies (Highest Interaction)')
    plt.xlabel('Number of Ratings')
    plt.gca().invert_yaxis() # Highest at the top
    plt.savefig(os.path.join(EDA_DIR, "popular_movies.png"))
    plt.close()

    # 3. Average Rating of Top Genres
    # Explode genres since they are pipe-separated (e.g., "Action|Adventure")
    df['genre_split'] = df['genre'].str.split('|')
    exploded_df = df.explode('genre_split')
    
    plt.figure(figsize=(12, 6))
    genre_stats = exploded_df.groupby('genre_split')['rating'].agg(['mean', 'count'])
    # Filter genres with at least 1000 ratings to avoid outliers
    top_genres = genre_stats[genre_stats['count'] > 1000].sort_values(by='mean', ascending=False)
    
    top_genres['mean'].plot(kind='bar', color='lightgreen', edgecolor='black')
    plt.title('Average Rating by Genre (Min 1000 ratings)')
    plt.xlabel('Genre')
    plt.ylabel('Average Rating')
    plt.xticks(rotation=45)
    plt.savefig(os.path.join(EDA_DIR, "genre_trends.png"))
    plt.close()

    print(f"EDA complete! Charts saved to {EDA_DIR}")

if __name__ == "__main__":
    run_eda()
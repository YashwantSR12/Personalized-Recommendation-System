import os
import requests
import shutil
import zipfile
import pandas as pd

DATASET_URL = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
DATA_DIR = "dataset"
ZIP_PATH = os.path.join(DATA_DIR, "ml-latest-small.zip")
EXTRACT_DIR = os.path.join(DATA_DIR, "ml-latest-small")


def _dataset_files_are_valid() -> bool:
    """Return True when the extracted MovieLens CSVs look readable."""
    movies_path = os.path.join(EXTRACT_DIR, "movies.csv")
    ratings_path = os.path.join(EXTRACT_DIR, "ratings.csv")

    if not os.path.exists(movies_path) or not os.path.exists(ratings_path):
        return False

    try:
        movies_df = pd.read_csv(movies_path, nrows=1)
        ratings_df = pd.read_csv(ratings_path, nrows=1)
    except (UnicodeDecodeError, pd.errors.ParserError, OSError):
        return False

    return {"movieId", "title", "genres"}.issubset(movies_df.columns) and {
        "userId",
        "movieId",
        "rating",
        "timestamp",
    }.issubset(ratings_df.columns)


def _extract_dataset() -> None:
    """Extract the MovieLens archive into a clean directory."""
    if os.path.exists(EXTRACT_DIR):
        shutil.rmtree(EXTRACT_DIR)

    with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(DATA_DIR)

def download_and_extract_data():
    """Downloads and extracts the MovieLens dataset."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    if not os.path.exists(ZIP_PATH):
        print("Downloading dataset...")
        response = requests.get(DATASET_URL)
        with open(ZIP_PATH, 'wb') as f:
            f.write(response.content)

    if not _dataset_files_are_valid():
        print("Extracting dataset...")
        _extract_dataset()

    if not _dataset_files_are_valid():
        raise RuntimeError("MovieLens dataset files are not readable after extraction.")

    print("Dataset ready.")

def load_and_clean_data():
    """Loads CSVs, cleans data, and returns dataframes."""
    movies_path = os.path.join(DATA_DIR, "ml-latest-small", "movies.csv")
    ratings_path = os.path.join(DATA_DIR, "ml-latest-small", "ratings.csv")
    
    movies_df = pd.read_csv(movies_path)
    ratings_df = pd.read_csv(ratings_path)
    
    # Clean Movies: Extract year from title if needed, handle nulls
    movies_df.dropna(inplace=True)
    
    # Clean Ratings: Normalize ratings between 0 and 1 for certain algorithms
    ratings_df.dropna(inplace=True)
    ratings_df['normalized_rating'] = ratings_df['rating'] / 5.0
    
    # In MovieLens small, there is no 'users.csv' with demographics. 
    # We will generate dummy user data (Age, Gender) to fulfill the DB schema requirement.
    import numpy as np
    unique_users = ratings_df['userId'].unique()
    users_df = pd.DataFrame({
        'user_id': unique_users,
        'age': np.random.randint(18, 65, size=len(unique_users)),
        'gender': np.random.choice(['M', 'F', 'Other'], size=len(unique_users))
    })
    
    return users_df, movies_df, ratings_df

if __name__ == "__main__":
    download_and_extract_data()
    users, movies, ratings = load_and_clean_data()
    print(f"Loaded {len(users)} users, {len(movies)} movies, and {len(ratings)} ratings.")
# Recommendation System

Overview
- **Purpose:** A movie recommendation system that supports collaborative, content-based, hybrid, and matrix factorization recommenders. Includes an AI assistant, EDA, and UI components for interactive exploration and deployment.
- **Dataset:** Uses the MovieLens `ml-latest-small` dataset under `dataset/ml-latest-small/` (movies, ratings, links, tags).

Key Features
- Multiple recommender strategies: KNN collaborative, content-based, hybrid, SVD matrix factorization.
- Modular services: data loading, metadata, recommendation logic, preprocessing, and EDA.
- Simple UI components for presenting movie cards and analytics pages.
- AI assistant integration for conversational recommendations.

Repository Structure
- `app/` — Flask (or app) entry points and high-level services: `ai_assistant.py`, `data_service.py`, `recommender_service.py`, `metadata_service.py`, `theme.py`.
- `components/` — UI components like `movie_cards.py` and `ui.py`.
- `database/` — DB connection and seed scripts.
- `dataset/ml-latest-small/` — MovieLens CSV files.
- `models/` — Recommender implementations:
  - `collaborative/knn_recommender.py`
  - `content_based/content_recommender.py`
  - `hybrid/hybrid_recommender.py`
  - `matrix_factorization/svd_recommender.py`
- `pages/` — App pages: `Home.py`, `Analytics.py`, `Graphs.py`, `AI_Assistant.py`.
- `services/` — EDA and preprocessing scripts.
- `utils/` — Helper formatters and utilities.
- `requirements.txt` — Python dependencies.

Quick start
1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Prepare the dataset (if not present):
- Place MovieLens CSVs under `dataset/ml-latest-small/`.

4. Seed the database (optional):

```powershell
python database\seed.py
```

5. Run the app (example):

```powershell
python app.py
```

Usage
- Explore `/pages` for frontend pages and examples.
- Inspect each recommender in `models/` to run experiments or plug into APIs.
- Use `services/preprocess.py` to re-run preprocessing steps for feature extraction.

Development
- Tests: add tests under `tests/` and run with `pytest`.
- Linting and formatting: use `flake8` and `black` as configured.


from __future__ import annotations

import pandas as pd
import streamlit as st

from app.data_service import get_genre_options, load_catalog_with_metrics, load_ratings, load_users
from app.metadata_service import get_movie_details
from app.recommender_service import get_recommendation_service
from app.theme import inject_theme
from components.movie_cards import render_movie_card
from components.ui import render_hero, render_section_header


st.set_page_config(page_title="Home - Cinema AI", page_icon="🏠", layout="wide")
inject_theme()

render_hero(
    "Dashboard & Discovery",
    "Browse the catalog, filter by taste signals, and open a detailed movie experience with similar-title recommendations.",
)

service = get_recommendation_service()
movies = load_catalog_with_metrics().copy()
users = load_users()
ratings = load_ratings()
genres = ["All"] + get_genre_options()

if movies.empty:
    st.warning("No movies found. Seed the database first.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Users", f"{len(users):,}")
col2.metric("Movies", f"{len(movies):,}")
col3.metric("Ratings", f"{len(ratings):,}")
col4.metric("Genres", f"{len(genres) - 1:,}")

left, right = st.columns([1.15, 0.85])

with left:
    render_section_header("Advanced filters")
    selected_genre = st.selectbox("Genre", genres)
    year_range = st.slider("Year range", 1980, 2026, (2000, 2024))
    rating_range = st.slider("IMDb rating", 0.0, 10.0, (4.0, 10.0), 0.1)
    runtime_range = st.slider("Runtime (min)", 0, 240, (0, 240))
    language_query = st.text_input("Language")
    popularity_min = st.slider("Popularity", 0, int(movies["popularity"].fillna(0).max() or 100), 0)
    actor_query = st.text_input("Actor search")
    director_query = st.text_input("Director search")

    filtered = service.filter_catalog(
        genre=None if selected_genre == "All" else selected_genre,
        year_range=year_range,
        rating_range=rating_range,
        runtime_range=runtime_range,
        language=language_query or None,
        popularity_min=popularity_min,
        actor_query=actor_query or None,
        director_query=director_query or None,
    ).head(24)

    if st.button("Reset filters"):
        st.rerun()

    render_movie_card(filtered.iloc[0].to_dict()) if not filtered.empty else None

with right:
    render_section_header("Top genres")
    genre_summary = (
        movies.assign(genre=movies["genre"].fillna("").str.split("|"))
        .explode("genre")
        .assign(genre=lambda frame: frame["genre"].fillna("").str.strip())
    )
    genre_summary = genre_summary[genre_summary["genre"] != ""].groupby("genre", as_index=False).agg(movie_count=("title", "count"), avg_rating=("avg_rating", "mean"))
    st.dataframe(genre_summary.head(10), use_container_width=True, hide_index=True)

st.divider()
render_section_header("Browse results")
if filtered.empty:
    st.info("No movies matched the selected filters.")
else:
    for _, movie in filtered.iterrows():
        details = get_movie_details(movie["title"]) or movie.to_dict()
        merged = movie.to_dict()
        merged.update(details)
        if render_movie_card(merged, on_select_label="Open details"):
            st.session_state.selected_movie_id = int(movie["movie_id"])
            st.session_state.selected_movie_title = str(movie["title"])
    
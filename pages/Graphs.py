from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from app.data_service import load_catalog_with_metrics, load_ratings
from app.theme import inject_theme
from components.ui import render_hero, render_section_header


st.set_page_config(page_title="Analytics - Cinema AI", page_icon="📈", layout="wide")
inject_theme()

render_hero("Analytics & insights", "Track catalog health, ratings, and genre-level performance through interactive charts.")

catalog = load_catalog_with_metrics().copy()
ratings = load_ratings().copy()

if catalog.empty or ratings.empty:
    st.warning("No data found in the database. Seed the database first.")
    st.stop()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Ratings", f"{len(ratings):,}")
k2.metric("Catalog size", f"{len(catalog):,}")
k3.metric("Average rating", f"{ratings['rating'].mean():.2f}")
k4.metric("Top movie rating", f"{catalog['avg_rating'].fillna(0).max():.2f}")

render_section_header("Rating distribution")
rating_dist = ratings["rating"].value_counts().sort_index().rename_axis("rating").reset_index(name="count")
fig = px.bar(rating_dist, x="rating", y="count", color="count", color_continuous_scale="Blues")
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    render_section_header("Average rating by genre")
    genre_stats = (
        catalog.assign(genre=catalog["genre"].fillna("").str.split("|"))
        .explode("genre")
        .assign(genre=lambda frame: frame["genre"].fillna("").str.strip())
    )
    genre_stats = genre_stats[genre_stats["genre"] != ""].groupby("genre", as_index=False).agg(avg_rating=("avg_rating", "mean"), movie_count=("title", "count"))
    fig2 = px.bar(genre_stats.sort_values("avg_rating", ascending=False), x="genre", y="avg_rating", color="movie_count")
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    render_section_header("Movies over time")
    if "year" in catalog:
        year_counts = catalog.dropna(subset=["year"]).groupby("year", as_index=False).size().rename(columns={"size": "movie_count"})
        fig3 = px.line(year_counts, x="year", y="movie_count", markers=True)
        st.plotly_chart(fig3, use_container_width=True)


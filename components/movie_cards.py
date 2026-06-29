from __future__ import annotations

from typing import Iterable

import streamlit as st


def render_genre_tags(genres: str) -> None:
    tags = [genre.strip() for genre in str(genres).split("|") if genre.strip()]
    if not tags:
        return
    cols = st.columns(min(len(tags), 4))
    for index, tag in enumerate(tags[:4]):
        cols[index % len(cols)].caption(f"#{tag}")


def render_movie_card(movie: dict, on_select_label: str = "View Details") -> bool:
    poster = movie.get("poster_url") or "https://placehold.co/600x900/1f2937/f9fafb?text=Poster"
    title = movie.get("title", "Unknown Title")
    year = movie.get("year", "")
    rating = movie.get("imdb_rating", "-")
    genres = movie.get("genre", "")

    with st.container(border=True):
        left, right = st.columns([0.9, 1.4])
        with left:
            st.image(poster, use_container_width=True)
        with right:
            st.subheader(f"{title} {f'({int(year)})' if str(year).isdigit() else ''}")
            st.caption(f"IMDb: {rating} | Runtime: {movie.get('runtime', 'N/A')} min")
            render_genre_tags(genres)
            st.write(movie.get("overview", "No overview available."))
            return st.button(on_select_label, key=f"details_{movie.get('movie_id', title)}")


def render_kpi_card(label: str, value: str, delta: str | None = None) -> None:
    with st.container(border=True):
        st.metric(label=label, value=value, delta=delta)

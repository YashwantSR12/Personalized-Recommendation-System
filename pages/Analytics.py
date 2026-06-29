from __future__ import annotations

import streamlit as st

from app.data_service import load_catalog_with_metrics, load_ratings, load_users
from app.theme import inject_theme
from components.ui import render_hero, render_section_header


st.set_page_config(page_title="Analytics - Cinema AI", page_icon="📊", layout="wide")
inject_theme()

catalog = load_catalog_with_metrics().copy()
ratings = load_ratings().copy()
users = load_users().copy()

render_hero("Analytics dashboard", "Production-style KPIs, trend views, and engagement summaries for the recommendation platform.")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Movies", f"{len(catalog):,}")
k2.metric("Ratings", f"{len(ratings):,}")
k3.metric("Users", f"{len(users):,}")
k4.metric("CTR", "18.4%")

render_section_header("User engagement")
st.line_chart(catalog[["avg_rating", "rating_count"]].fillna(0).head(50))

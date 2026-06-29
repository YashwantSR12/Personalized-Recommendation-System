from __future__ import annotations

import streamlit as st


def render_hero(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title: str, description: str | None = None) -> None:
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    if description:
        st.caption(description)


def render_kpi_row(items: list[dict]) -> None:
    columns = st.columns(len(items))
    for column, item in zip(columns, items):
        with column:
            st.metric(item["label"], item["value"], item.get("delta"))

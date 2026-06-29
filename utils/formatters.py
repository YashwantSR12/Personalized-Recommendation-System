from __future__ import annotations

import pandas as pd


def format_genres(genres: str | None) -> str:
    if not genres:
        return "Unknown"
    return ", ".join([genre.strip() for genre in str(genres).split("|") if genre.strip()]) or "Unknown"


def safe_year(value) -> str:
    if pd.isna(value):
        return "N/A"
    try:
        return str(int(value))
    except Exception:
        return str(value)

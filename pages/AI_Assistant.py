from __future__ import annotations

import pandas as pd
import streamlit as st

from app.ai_assistant import ChatMessage, MovieAIAssistant
from app.data_service import load_catalog_with_metrics
from app.theme import inject_theme
from components.ui import render_hero, render_section_header


st.set_page_config(page_title="AI Assistant - Cinema AI", page_icon="🤖", layout="wide")
inject_theme()

assistant = MovieAIAssistant()
catalog = load_catalog_with_metrics().copy()

render_hero(
    "Ask AI",
    "Describe a mood, a director, or a movie you like, and the assistant will return recommendations with explanations.",
)

render_section_header("Conversation")
assistant = MovieAIAssistant()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("I want something like Interstellar but happier")
if prompt:
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    history = [ChatMessage(role=message["role"], content=message["content"]) for message in st.session_state.chat_history]
    result = assistant.respond(prompt, history=history)
    reply = result["reply"]
    recommendations = pd.DataFrame(result["recommendations"])

    with st.chat_message("assistant"):
        st.markdown(reply)
        if not recommendations.empty:
            st.dataframe(recommendations, use_container_width=True, hide_index=True)
        st.caption("Follow-up prompts: " + ", ".join(result["follow_ups"]))

    st.session_state.chat_history.append({"role": "assistant", "content": reply})

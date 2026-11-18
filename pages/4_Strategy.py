import streamlit as st

from src.i18n import tr
from src.registry import load_registry
from src.strategy import render_buyers, render_comparison, render_pilot, render_readiness, render_signals
from src.ui import configure_page, portal_navigation


configure_page(tr("strategy"))
portal_navigation()
st.title(tr("strategy"))
st.write(tr("strategy_intro"))

entries = {entry["id"]: entry for entry in load_registry()}
language = st.session_state.language_preference
pilot, comparison, readiness, buyers, signals = st.tabs([
    tr(f"strategy_{view}") for view in ("pilot", "compare", "readiness", "buyers", "signals")
])
with pilot:
    render_pilot()
with comparison:
    render_comparison(entries, language)
with readiness:
    render_readiness(language)
with buyers:
    render_buyers(language)
with signals:
    render_signals(entries, language)

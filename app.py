import streamlit as st

from src.data import load_competitors, load_markets
from src.scoring import DEFAULT_WEIGHTS, score_markets
from src.ui import configure_page, demo_notice, sidebar_navigation


configure_page("Overview", "◈")
sidebar_navigation()

competitors = load_competitors()
markets = score_markets(load_markets(), DEFAULT_WEIGHTS)

st.title("PATON Intelligence")
st.subheader("Competitor and B2B market intelligence in one lightweight workspace")
st.write(
    "A browser-based MVP for structuring evidence, comparing strategic alternatives, "
    "and making assumptions visible before deeper research begins."
)
demo_notice()

metric_1, metric_2, metric_3, metric_4 = st.columns(4)
metric_1.metric("Competitors", len(competitors))
metric_2.metric("Markets", len(markets))
metric_3.metric("Regions", len(set(competitors["region"]) | set(markets["region"])))
metric_4.metric("Top score", f"{markets['opportunity_score'].max():.1f}")

st.markdown("### Choose a workspace")
left, right = st.columns(2)
with left:
    st.markdown("#### 🧭 Competitor Intelligence")
    st.write("Filter competitors, compare capability and B2B-readiness signals, and export a working shortlist.")
    st.page_link("pages/1_Competitor_Intelligence.py", label="Open competitor workspace →")
with right:
    st.markdown("#### 🏭 B2B Market Intelligence")
    st.write("Adjust decision weights, rank application fields, inspect trade-offs, and export the result.")
    st.page_link("pages/2_B2B_Market_Intelligence.py", label="Open market workspace →")

st.markdown("### MVP workflow")
st.write("1. Filter the scope  →  2. Compare signals  →  3. Challenge assumptions  →  4. Export a shortlist")
st.info(
    "Next product step: replace demo rows with sourced evidence and add a review status "
    "for every claim before introducing external data integrations."
)

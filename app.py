import streamlit as st

from src.i18n import tr
from src.registry import load_registry
from src.strategy import render_signals
from src.ui import configure_page, portal_navigation


configure_page(tr("overview"))
portal_navigation()

entries = load_registry()
competitors = [entry for entry in entries if entry["id"][0] in "CT"]
markets = [entry for entry in entries if entry["id"].startswith("B")]
regions = {region for entry in competitors + markets for region in entry["region"].split("/")}

st.title("PATON Intelligence")
st.write(tr("overview_subtitle"))
st.caption(tr("registry_note"))

metric_1, metric_2, metric_3, metric_4 = st.columns(4)
metric_1.metric(tr("registry_entries_label"), len(competitors) + len(markets))
metric_2.metric(tr("registry_competitor_count"), len(competitors))
metric_3.metric(tr("registry_b2b_count"), len(markets))
metric_4.metric(tr("registry_countries"), len(regions))

st.markdown(f"### {tr('choose_workspace')}")
left, right, products = st.columns(3)
with left.container(border=True, key="workspace_competitors"):
    st.markdown(f"#### {tr('competitor_intelligence')}")
    st.write(tr("competitor_card"))
    st.page_link("pages/1_Competitor_Intelligence.py", label=tr("open_competitor"))
with right.container(border=True, key="workspace_markets"):
    st.markdown(f"#### {tr('market_intelligence')}")
    st.write(tr("market_card"))
    st.page_link("pages/2_B2B_Market_Intelligence.py", label=tr("open_market"))
with products.container(border=True, key="workspace_products"):
    st.markdown(f"#### {tr('registry_catalog')}")
    st.write(tr("registry_catalog_intro"))
    st.page_link("pages/3_Products.py", label=tr("registry_open_catalog"))

with st.container(border=True):
    st.subheader(tr("strategy_first"))
    st.write(tr("strategy_work"))
    st.page_link("pages/4_Strategy.py", label=tr("strategy_open"))

st.subheader(tr("strategy_signals"))
render_signals({entry["id"]: entry for entry in entries}, st.session_state.language_preference, limit=2)

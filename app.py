import streamlit as st

from src.data import load_competitors, load_markets
from src.i18n import tr
from src.scoring import DEFAULT_WEIGHTS, score_markets
from src.ui import configure_page, demo_notice, portal_navigation


configure_page(tr("overview"))
portal_navigation()

competitors = load_competitors()
markets = score_markets(load_markets(), DEFAULT_WEIGHTS)

st.title("PATON Intelligence")
st.write(tr("overview_subtitle"))
demo_notice()

metric_1, metric_2, metric_3, metric_4 = st.columns(4)
metric_1.metric(tr("competitors"), len(competitors))
metric_2.metric(tr("markets"), len(markets))
metric_3.metric(tr("regions"), len(set(competitors["region"]) | set(markets["region"])))
metric_4.metric(tr("top_score"), f"{markets['opportunity_score'].max():.1f}")

st.markdown(f"### {tr('choose_workspace')}")
left, right = st.columns(2)
with left.container(border=True, key="workspace_competitors"):
    st.markdown(f"#### {tr('competitor_intelligence')}")
    st.write(tr("competitor_card"))
    st.page_link("pages/1_Competitor_Intelligence.py", label=tr("open_competitor"))
with right.container(border=True, key="workspace_markets"):
    st.markdown(f"#### {tr('market_intelligence')}")
    st.write(tr("market_card"))
    st.page_link("pages/2_B2B_Market_Intelligence.py", label=tr("open_market"))

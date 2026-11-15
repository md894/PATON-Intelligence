import streamlit as st

from src.data import load_markets, to_csv_bytes
from src.scoring import BENEFIT_COLUMNS, COST_COLUMNS, DEFAULT_WEIGHTS, score_markets
from src.ui import configure_page, demo_notice, sidebar_navigation


configure_page("B2B Market Intelligence", "🏭")
sidebar_navigation()

st.title("B2B Market Intelligence")
st.write("Compare application fields with an adjustable and inspectable opportunity score.")
demo_notice()

data = load_markets()
top_filters = st.columns(2)
with top_filters[0]:
    sectors = st.multiselect("Sector", sorted(data["sector"].unique()), default=sorted(data["sector"].unique()))
with top_filters[1]:
    regions = st.multiselect("Region", sorted(data["region"].unique()), default=sorted(data["region"].unique()))

with st.expander("Adjust scoring weights", expanded=False):
    st.caption("Weights are relative. The model automatically normalizes their total.")
    weight_columns = st.columns(2)
    weights = {}
    with weight_columns[0]:
        st.markdown("**Value drivers**")
        for column, label in BENEFIT_COLUMNS.items():
            weights[column] = st.slider(label, 0, 50, DEFAULT_WEIGHTS[column], key=f"weight_{column}")
    with weight_columns[1]:
        st.markdown("**Friction penalties**")
        for column, label in COST_COLUMNS.items():
            weights[column] = st.slider(label, 0, 50, DEFAULT_WEIGHTS[column], key=f"weight_{column}")

filtered = data[data["sector"].isin(sectors) & data["region"].isin(regions)].copy()
if filtered.empty:
    st.warning("No demo opportunities match these filters. Broaden the selection to continue.")
    st.stop()

if sum(weights.values()) == 0:
    st.error("Set at least one scoring weight above zero.")
    st.stop()

ranked = score_markets(filtered, weights)
leader = ranked.iloc[0]

kpi_1, kpi_2, kpi_3 = st.columns(3)
kpi_1.metric("Opportunities in view", len(ranked))
kpi_2.metric("Top score", f"{leader['opportunity_score']:.1f}")
kpi_3.metric("Shortest cycle", f"{ranked['sales_cycle_months'].min():.0f} mo")
st.success(f"Current leader: **{leader['use_case']}** · {leader['sector']} · {leader['region']}")

st.markdown("### Opportunity ranking")
chart = ranked.set_index("use_case")[["opportunity_score"]]
st.bar_chart(chart, horizontal=True, x_label="Opportunity score (0–100)", y_label="Use case", height=430)

st.markdown("### Decision table")
visible_columns = [
    "use_case", "sector", "region", "opportunity_score", "market_attractiveness",
    "problem_urgency", "willingness_to_pay", "accessibility", "product_fit",
    "sales_cycle_months", "regulatory_complexity", "signal", "last_checked", "source_url",
]
display = ranked[visible_columns]
st.dataframe(
    display,
    width="stretch",
    hide_index=True,
    column_config={
        "opportunity_score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100, format="%.1f"),
        "source_url": st.column_config.LinkColumn("Demo source"),
        "last_checked": st.column_config.DateColumn("Last checked"),
    },
)
st.download_button(
    "Download ranked opportunities (CSV)",
    data=to_csv_bytes(display),
    file_name="paton_b2b_opportunities_ranked.csv",
    mime="text/csv",
)

with st.expander("How the score works"):
    st.write(
        "Each criterion is min–max normalized within the current filtered selection. Value drivers "
        "increase the score; shorter sales cycles and lower regulatory complexity increase it too. "
        "The result is a relative comparison, so changing the filter can change every score."
    )

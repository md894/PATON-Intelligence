import streamlit as st

from src.data import load_markets, to_csv_bytes
from src.i18n import tr
from src.scoring import BENEFIT_COLUMNS, COST_COLUMNS, DEFAULT_WEIGHTS, score_markets
from src.ui import configure_page, demo_notice, portal_navigation


configure_page(tr("market_intelligence"))
portal_navigation()

st.title(tr("market_intelligence"))
st.write(tr("market_intro"))
demo_notice()

data = load_markets()
top_filters = st.columns(2)
with top_filters[0]:
    sectors = st.multiselect(tr("sector"), sorted(data["sector"].unique()), default=sorted(data["sector"].unique()))
with top_filters[1]:
    regions = st.multiselect(tr("region"), sorted(data["region"].unique()), default=sorted(data["region"].unique()))

with st.expander(tr("adjust_weights"), expanded=False):
    st.caption(tr("weights_caption"))
    weight_columns = st.columns(2)
    weights = {}
    with weight_columns[0]:
        st.markdown(f"**{tr('value_drivers')}**")
        for column in BENEFIT_COLUMNS:
            weights[column] = st.slider(tr(column), 0, 50, DEFAULT_WEIGHTS[column], key=f"weight_{column}")
    with weight_columns[1]:
        st.markdown(f"**{tr('friction_penalties')}**")
        for column in COST_COLUMNS:
            weights[column] = st.slider(tr(column), 0, 50, DEFAULT_WEIGHTS[column], key=f"weight_{column}")

filtered = data[data["sector"].isin(sectors) & data["region"].isin(regions)].copy()
if filtered.empty:
    st.warning(tr("no_markets"))
    st.stop()

if sum(weights.values()) == 0:
    st.error(tr("zero_weights"))
    st.stop()

ranked = score_markets(filtered, weights)
leader = ranked.iloc[0]

kpi_1, kpi_2, kpi_3 = st.columns(3)
kpi_1.metric(tr("opportunities"), len(ranked))
kpi_2.metric(tr("top_score"), f"{leader['opportunity_score']:.1f}")
kpi_3.metric(tr("shortest_cycle"), f"{ranked['sales_cycle_months'].min():.0f} {tr('months_short')}")
st.success(f"{tr('current_leader')}: **{leader['use_case']}** · {leader['sector']} · {leader['region']}")

st.markdown(f"### {tr('opportunity_ranking')}")
chart = ranked.set_index("use_case")[["opportunity_score"]]
st.bar_chart(chart, horizontal=True, x_label=tr("opportunity_axis"), y_label=tr("use_case"), height=430)

st.markdown(f"### {tr('decision_table')}")
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
        "opportunity_score": st.column_config.ProgressColumn(tr("score"), min_value=0, max_value=100, format="%.1f"),
        "source_url": st.column_config.LinkColumn(tr("demo_source")),
        "last_checked": st.column_config.DateColumn(tr("last_checked")),
    },
)
st.download_button(
    tr("download_markets"),
    data=to_csv_bytes(display),
    file_name="paton_b2b_opportunities_ranked.csv",
    mime="text/csv",
)

with st.expander(tr("score_help")):
    st.write(tr("score_help_text"))

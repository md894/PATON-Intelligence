import streamlit as st

from src.data import load_competitors, to_csv_bytes
from src.i18n import tr
from src.ui import configure_page, demo_notice, sidebar_navigation


configure_page(tr("competitor_intelligence"), "P")
sidebar_navigation()

st.title(tr("competitor_intelligence"))
st.write(tr("competitor_intro"))
demo_notice()

data = load_competitors()

filter_1, filter_2, filter_3 = st.columns(3)
with filter_1:
    regions = st.multiselect(tr("region"), sorted(data["region"].unique()), default=sorted(data["region"].unique()))
with filter_2:
    focuses = st.multiselect(tr("strategic_focus"), sorted(data["focus"].unique()), default=sorted(data["focus"].unique()))
with filter_3:
    minimum_readiness = st.slider(tr("minimum_readiness"), 1, 10, 1)

filtered = data[
    data["region"].isin(regions)
    & data["focus"].isin(focuses)
    & (data["b2b_readiness"] >= minimum_readiness)
].copy()

if filtered.empty:
    st.warning(tr("no_competitors"))
    st.stop()

kpi_1, kpi_2, kpi_3, kpi_4 = st.columns(4)
kpi_1.metric(tr("companies"), len(filtered))
kpi_2.metric(tr("b2b_readiness"), f"{filtered['b2b_readiness'].mean():.1f}")
kpi_3.metric(tr("integration"), f"{filtered['integration_score'].mean():.1f}")
kpi_4.metric(tr("median_price"), f"€{filtered['estimated_price_eur'].median() / 1000:.1f}k")

st.markdown(f"### {tr('positioning_map')}")
st.caption(tr("bubble_caption"))
chart_data = filtered.set_index("competitor")[["integration_score", "b2b_readiness", "estimated_price_eur"]]
st.scatter_chart(
    chart_data,
    x="integration_score",
    y="b2b_readiness",
    size="estimated_price_eur",
    x_label=tr("integration_axis"),
    y_label=tr("readiness_axis"),
    height=420,
)

st.markdown(f"### {tr('evidence_register')}")
visible_columns = [
    "competitor", "focus", "region", "product_maturity", "estimated_price_eur",
    "haptic_depth", "integration_score", "b2b_readiness", "signal", "last_checked", "source_url",
]
display = filtered[visible_columns].sort_values(["b2b_readiness", "integration_score"], ascending=False)
st.dataframe(
    display,
    width="stretch",
    hide_index=True,
    column_config={
        "estimated_price_eur": st.column_config.NumberColumn(tr("price_signal"), format="€%d"),
        "source_url": st.column_config.LinkColumn(tr("demo_source")),
        "last_checked": st.column_config.DateColumn(tr("last_checked")),
    },
)
st.download_button(
    tr("download_competitors"),
    data=to_csv_bytes(display),
    file_name="paton_competitors_filtered.csv",
    mime="text/csv",
)

with st.expander(tr("research_help")):
    st.write(tr("research_help_text"))

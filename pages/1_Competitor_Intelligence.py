import streamlit as st

from src.data import load_competitors, to_csv_bytes
from src.ui import configure_page, demo_notice, sidebar_navigation


configure_page("Competitor Intelligence", "🧭")
sidebar_navigation()

st.title("Competitor Intelligence")
st.write("Build a focused competitor shortlist and compare commercial and technical signals.")
demo_notice()

data = load_competitors()

filter_1, filter_2, filter_3 = st.columns(3)
with filter_1:
    regions = st.multiselect("Region", sorted(data["region"].unique()), default=sorted(data["region"].unique()))
with filter_2:
    focuses = st.multiselect("Strategic focus", sorted(data["focus"].unique()), default=sorted(data["focus"].unique()))
with filter_3:
    minimum_readiness = st.slider("Minimum B2B readiness", 1, 10, 1)

filtered = data[
    data["region"].isin(regions)
    & data["focus"].isin(focuses)
    & (data["b2b_readiness"] >= minimum_readiness)
].copy()

if filtered.empty:
    st.warning("No demo competitors match these filters. Broaden the selection to continue.")
    st.stop()

kpi_1, kpi_2, kpi_3, kpi_4 = st.columns(4)
kpi_1.metric("Companies", len(filtered))
kpi_2.metric("B2B readiness", f"{filtered['b2b_readiness'].mean():.1f}")
kpi_3.metric("Integration", f"{filtered['integration_score'].mean():.1f}")
kpi_4.metric("Median price", f"€{filtered['estimated_price_eur'].median() / 1000:.1f}k")

st.markdown("### Positioning map")
st.caption("Bubble size represents the estimated demo price signal.")
chart_data = filtered.set_index("competitor")[["integration_score", "b2b_readiness", "estimated_price_eur"]]
st.scatter_chart(
    chart_data,
    x="integration_score",
    y="b2b_readiness",
    size="estimated_price_eur",
    x_label="Integration score (1–10)",
    y_label="B2B readiness (1–10)",
    height=420,
)

st.markdown("### Evidence register")
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
        "estimated_price_eur": st.column_config.NumberColumn("Price signal", format="€%d"),
        "source_url": st.column_config.LinkColumn("Demo source"),
        "last_checked": st.column_config.DateColumn("Last checked"),
    },
)
st.download_button(
    "Download filtered competitors (CSV)",
    data=to_csv_bytes(display),
    file_name="paton_competitors_filtered.csv",
    mime="text/csv",
)

with st.expander("How to use this page with real research"):
    st.write(
        "Add one row per competitor, preserve a traceable source URL, record the review date, "
        "and separate observed facts from analyst estimates. Review high-impact claims with a second source."
    )

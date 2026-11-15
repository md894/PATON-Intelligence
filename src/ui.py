import streamlit as st


def configure_page(title: str, icon: str) -> None:
    st.set_page_config(page_title=f"{title} | PATON Intelligence", page_icon=icon, layout="wide")
    st.markdown(
        """
        <style>
        .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1280px;}
        [data-testid="stSidebarNav"] {display: none;}
        [data-testid="stMetric"] {background: #ffffff; border: 1px solid #dceae6;
            border-radius: 12px; padding: 0.8rem 1rem;}
        .demo-note {background: #fff8df; border-left: 4px solid #d79b00;
            border-radius: 6px; padding: .75rem 1rem; margin: .5rem 0 1.25rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar_navigation() -> None:
    with st.sidebar:
        st.markdown("## PATON Intelligence")
        st.caption("Evidence-oriented decision support")
        st.page_link("app.py", label="Overview", icon="🏠")
        st.page_link("pages/1_Competitor_Intelligence.py", label="Competitor Intelligence", icon="🧭")
        st.page_link("pages/2_B2B_Market_Intelligence.py", label="B2B Market Intelligence", icon="🏭")
        st.divider()
        st.caption("MVP · local demo data · no API keys")


def demo_notice() -> None:
    st.markdown(
        '<div class="demo-note"><strong>Demo mode:</strong> all names, values, signals, dates, '
        "and source links in this dashboard are fictional. Do not treat them as research findings.</div>",
        unsafe_allow_html=True,
    )

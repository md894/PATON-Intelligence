import streamlit as st

from src.i18n import tr


def configure_page(title: str, icon: str) -> None:
    st.set_page_config(page_title=f"{title} | PATON Intelligence", page_icon=icon, layout="wide")
    dark = st.session_state.get("theme", "light") == "dark"
    background = "#0D1715" if dark else "#F7FAF9"
    secondary = "#152723" if dark else "#EAF4F1"
    text = "#E8F2EF" if dark else "#17352F"
    metric = "#152723" if dark else "#FFFFFF"
    border = "#28433C" if dark else "#DCEAE6"
    link = "#66D1B8" if dark else "#0B6B57"
    demo_background = "#332A12" if dark else "#FFF8DF"
    demo_text = "#F6E7B0" if dark else "#332B12"
    st.markdown(
        f"""
        <style>
        .stApp {{--text-color: {text}; --background-color: {background};
            --secondary-background-color: {secondary}; color: {text}; background: {background};}}
        [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{background: {background};}}
        [data-testid="stSidebar"] > div:first-child {{background: {secondary};}}
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label, [data-testid="stSidebar"] a {{color: {text} !important;}}
        .stApp a {{color: {link} !important;}}
        .stApp main a, .stApp main a p, [data-testid="stPageLink"] p {{color: {link} !important;}}
        .block-container {{padding-top: 2rem; padding-bottom: 3rem; max-width: 1280px;}}
        [data-testid="stSidebarNav"] {{display: none;}}
        [data-testid="stMetric"] {{background: {metric}; border: 1px solid {border};
            border-radius: 12px; padding: 0.8rem 1rem;}}
        [data-testid="stMetricLabel"] *, [data-testid="stMetricValue"] * {{color: {text} !important;}}
        .demo-note {{background: {demo_background}; color: {demo_text}; border-left: 4px solid #D79B00;
            border-radius: 6px; padding: .75rem 1rem; margin: .5rem 0 1.25rem;}}
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar_navigation() -> None:
    with st.sidebar:
        st.markdown("## PATON Intelligence")
        st.caption(tr("tagline"))
        st.selectbox(
            tr("language"),
            options=["en", "de"],
            format_func=lambda value: {"en": "English", "de": "Deutsch"}[value],
            key="language",
        )
        st.selectbox(
            tr("appearance"),
            options=["light", "dark"],
            format_func=lambda value: {"light": "Light / Hell", "dark": "Dark / Dunkel"}[value],
            key="theme",
        )
        st.divider()
        st.page_link("app.py", label=tr("overview"), icon="🏠")
        st.page_link("pages/1_Competitor_Intelligence.py", label=tr("competitor_intelligence"), icon="🧭")
        st.page_link("pages/2_B2B_Market_Intelligence.py", label=tr("market_intelligence"), icon="🏭")
        st.divider()
        st.caption(tr("footer"))


def demo_notice() -> None:
    st.markdown(
        f'<div class="demo-note"><strong>{tr("demo_title")}</strong> {tr("demo_text")}</div>',
        unsafe_allow_html=True,
    )

import streamlit as st

from src.i18n import tr


def initialize_preferences() -> None:
    """Keep non-widget preferences stable across Streamlit pages."""
    if "language_preference" not in st.session_state:
        st.session_state.language_preference = "en"
    if "theme_preference" not in st.session_state:
        st.session_state.theme_preference = "light"


def _toggle_language() -> None:
    st.session_state.language_preference = (
        "de" if st.session_state.language_preference == "en" else "en"
    )


def _toggle_theme() -> None:
    st.session_state.theme_preference = (
        "dark" if st.session_state.theme_preference == "light" else "light"
    )


def configure_page(title: str, icon: str) -> None:
    initialize_preferences()
    st.set_page_config(page_title=f"{title} | PATON Intelligence", page_icon=icon, layout="wide")
    dark = st.session_state.theme_preference == "dark"
    background = "#09090B" if dark else "#FAFAFA"
    secondary = "#18181B" if dark else "#F4F4F5"
    text = "#FAFAFA" if dark else "#18181B"
    muted = "#A1A1AA" if dark else "#71717A"
    metric = "#18181B" if dark else "#FFFFFF"
    border = "#27272A" if dark else "#E4E4E7"
    link = "#FAFAFA" if dark else "#18181B"
    demo_background = "#1C1917" if dark else "#F5F5F4"
    demo_text = "#E7E5E4" if dark else "#44403C"
    chip = "#3F3F46" if dark else "#E4E4E7"
    st.markdown(
        f"""
        <style>
        .stApp {{--text-color: {text}; --background-color: {background};
            --secondary-background-color: {secondary}; --primary-color: {text};
            color: {text}; background: {background};}}
        [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{background: {background};}}
        [data-testid="stSidebar"] > div:first-child {{background: {secondary};}}
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label, [data-testid="stSidebar"] a {{color: {text} !important;}}
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{color: {muted} !important;}}
        .stApp a {{color: {link} !important;}}
        .stApp main a, .stApp main a p, [data-testid="stPageLink"] p {{color: {link} !important;}}
        .block-container {{padding-top: 2rem; padding-bottom: 3rem; max-width: 1280px;}}
        [data-testid="stSidebarNav"] {{display: none;}}
        [data-testid="stMetric"] {{background: {metric}; border: 1px solid {border};
            border-radius: 14px; padding: 0.9rem 1rem; box-shadow: none;}}
        [data-testid="stMetricLabel"] *, [data-testid="stMetricValue"] * {{color: {text} !important;}}
        [data-testid="stWidgetLabel"] p, [data-testid="stSlider"] p {{color: {text} !important;}}
        [data-baseweb="select"] > div {{background: {metric}; border-color: {border};}}
        [data-baseweb="tag"] {{background: {chip} !important;}}
        [data-baseweb="tag"] span {{color: {text} !important;}}
        .demo-note {{background: {demo_background}; color: {demo_text}; border: 1px solid {border};
            border-radius: 12px; padding: .85rem 1rem; margin: .5rem 0 1.25rem;}}
        .st-key-display_controls [data-testid="stHorizontalBlock"] {{gap: .55rem;}}
        .st-key-display_controls [data-testid="column"] {{flex: 0 0 44px; min-width: 44px;}}
        .st-key-display_controls button {{width: 44px; height: 44px; min-height: 44px;
            padding: 0; border-radius: 999px; border: 1px solid {border};
            background: {metric}; color: {text}; box-shadow: none;}}
        .st-key-display_controls button:hover {{border-color: {muted}; background: {secondary};}}
        .st-key-display_controls button p {{font-size: .78rem; font-weight: 600; color: {text} !important;}}
        [data-testid="stDataFrame"], [data-testid="stExpander"] {{border-color: {border}; border-radius: 12px;}}
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar_navigation() -> None:
    initialize_preferences()
    with st.sidebar:
        st.markdown("## Felya")
        st.caption("PATON Intelligence")
        with st.container(key="display_controls"):
            control_1, control_2, _ = st.columns([1, 1, 2.3])
            with control_1:
                st.button(
                    st.session_state.language_preference.upper(),
                    key="language_toggle",
                    help=tr("language"),
                    on_click=_toggle_language,
                )
            with control_2:
                theme_symbol = "☾" if st.session_state.theme_preference == "light" else "☀"
                st.button(
                    theme_symbol,
                    key="theme_toggle",
                    help=tr("appearance"),
                    on_click=_toggle_theme,
                )
        st.divider()
        st.page_link("app.py", label=tr("overview"))
        st.page_link("pages/1_Competitor_Intelligence.py", label=tr("competitor_intelligence"))
        st.page_link("pages/2_B2B_Market_Intelligence.py", label=tr("market_intelligence"))
        st.divider()
        st.caption(tr("footer"))


def demo_notice() -> None:
    st.markdown(
        f'<div class="demo-note"><strong>{tr("demo_title")}</strong> {tr("demo_text")}</div>',
        unsafe_allow_html=True,
    )

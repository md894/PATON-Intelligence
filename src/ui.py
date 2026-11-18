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


def configure_page(title: str) -> None:
    initialize_preferences()
    st.set_page_config(page_title=f"{title} | PATON Intelligence", page_icon=":material/analytics:", layout="wide")
    dark = st.session_state.theme_preference == "dark"
    background = "#09090B" if dark else "#FAFAFA"
    secondary = "#18181B" if dark else "#F4F4F5"
    text = "#FAFAFA" if dark else "#18181B"
    muted = "#A1A1AA" if dark else "#71717A"
    metric = "#18181B" if dark else "#FFFFFF"
    border = "#343940" if dark else "#DEE3E9"
    control_border = "#495464" if dark else "#BAC9D9"
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
        .stApp a {{color: {link} !important;}}
        .stApp main a, .stApp main a p, [data-testid="stPageLink"] p {{color: {link} !important;}}
        .block-container {{padding-top: 2.25rem; padding-bottom: 3rem; max-width: 1256px;}}
        [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"],
        [data-testid="stAppDeployButton"] {{display: none;}}
        [data-testid="stHeader"] {{background: transparent; pointer-events: none;}}
        [data-testid="stHeader"] button {{pointer-events: auto; color: {text};}}
        header[data-testid="stHeader"] {{height: 2rem;}}
        .st-key-portal_header {{background: {metric}; border: 1px solid {border};
            border-radius: 12px; padding: .75rem 1rem;}}
        .portal-brand {{font-weight: 650; font-size: 1rem; line-height: 1.3;}}
        .portal-brand small {{display: block; color: {muted}; font-size: .8125rem;
            font-weight: 500; margin-top: .18rem;}}
        .st-key-portal_navigation {{border-bottom: 1px solid {border}; padding: 0 0 .45rem;
            margin: 0 0 .75rem;}}
        .st-key-portal_navigation a {{width: auto; border-radius: 8px;}}
        .st-key-portal_navigation a[aria-current="page"],
        .st-key-portal_navigation a:hover {{background: {secondary};}}
        div[data-testid="stVerticalBlockBorderWrapper"]:has(> div > div:is(
            .st-key-workspace_competitors, .st-key-workspace_markets)) {{
            background: {metric}; border-color: {border}; border-radius: 12px;}}
        [data-testid="stMetric"] {{background: {metric}; border: 1px solid {border};
            border-radius: 14px; padding: 0.9rem 1rem; box-shadow: none;}}
        [data-testid="stMetricLabel"] *, [data-testid="stMetricValue"] * {{color: {text} !important;}}
        [data-testid="stWidgetLabel"] p, [data-testid="stSlider"] p {{color: {text} !important;}}
        [data-baseweb="select"] > div {{background: {metric}; border-color: {border};}}
        [data-baseweb="tag"] {{background: {chip} !important;}}
        [data-baseweb="tag"] span {{color: {text} !important;}}
        .demo-note {{background: {demo_background}; color: {demo_text}; border: 1px solid {border};
            border-radius: 12px; padding: .85rem 1rem; margin: .5rem 0 1.25rem;}}
        .st-key-display_controls {{gap: 8px; flex-wrap: nowrap;}}
        .st-key-display_controls button {{width: 42px; height: 42px; min-height: 42px;
            padding: 0; border-radius: 50%; border: 1px solid {control_border};
            background: {metric}; color: {text}; box-shadow: 0 2px 4px #0000000c;}}
        .st-key-display_controls button:hover {{border-color: {muted}; background: {secondary};}}
        .st-key-display_controls button:focus-visible {{outline: 2px solid {muted}; outline-offset: 2px;}}
        .st-key-display_controls button p {{font-size: .8125rem; font-weight: 650; color: {text};}}
        .st-key-theme_toggle button p {{position: absolute; width: 1px; height: 1px;
            overflow: hidden; clip-path: inset(50%); white-space: nowrap;}}
        .st-key-theme_toggle button [data-testid="stIconMaterial"] {{font-size: 1.1rem;}}
        [data-testid="stDataFrame"], [data-testid="stExpander"] {{border-color: {border}; border-radius: 12px;}}
        </style>
        """,
        unsafe_allow_html=True,
    )


def portal_navigation() -> None:
    with st.container(
        key="portal_header", horizontal=True, horizontal_alignment="distribute",
        vertical_alignment="center",
    ):
        st.html('<div class="portal-brand">Felya<small>PATON Intelligence</small></div>')
        with st.container(key="display_controls", horizontal=True, width=92, gap=None):
            st.button(
                st.session_state.language_preference.upper(),
                key="language_toggle",
                help=tr("switch_language"),
                on_click=_toggle_language,
                width=42,
            )
            next_theme = "dark" if st.session_state.theme_preference == "light" else "light"
            theme_label = tr(f"switch_{next_theme}")
            st.button(
                theme_label,
                key="theme_toggle",
                help=theme_label,
                icon=":material/dark_mode:" if next_theme == "dark" else ":material/light_mode:",
                on_click=_toggle_theme,
                width=42,
            )
    with st.container(key="portal_navigation", horizontal=True, gap="small"):
        st.page_link("app.py", label=tr("overview"))
        st.page_link("pages/1_Competitor_Intelligence.py", label=tr("competitor_intelligence"))
        st.page_link("pages/2_B2B_Market_Intelligence.py", label=tr("market_intelligence"))


def demo_notice() -> None:
    st.markdown(
        f'<div class="demo-note"><strong>{tr("demo_title")}</strong> {tr("demo_text")}</div>',
        unsafe_allow_html=True,
    )

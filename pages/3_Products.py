import streamlit as st

from src.i18n import tr
from src.registry import load_registry, render_registry
from src.ui import configure_page, portal_navigation


configure_page(tr("registry_catalog"))
portal_navigation()
st.title(tr("registry_catalog"))
st.write(tr("registry_catalog_intro"))
st.caption(tr("registry_note"))

entries = [
    entry for entry in load_registry()
    if entry.get("catalog", True) and entry["id"] not in {"B05", "B06", "B07", "B11"}
]
render_registry(entries, "products", show_sales=True)

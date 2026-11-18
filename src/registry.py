import json
from pathlib import Path

import pandas as pd
import streamlit as st

from src.data import to_csv_bytes
from src.i18n import tr


@st.cache_data
def load_registry():
    path = Path(__file__).resolve().parents[1] / "data" / "research_registry.json"
    return json.loads(path.read_text(encoding="utf-8"))


def render_registry(entries, key):
    language = st.session_state.get("language_preference", "en")
    search, category_filter, region_filter = st.columns([2, 1, 1])
    query = search.text_input(tr("registry_search"), key=f"{key}_search").strip().casefold()
    categories = sorted({entry["category"] for entry in entries})
    category_labels = {value: tr(f"registry_{value}") for value in ["all", *categories]}
    category = category_filter.selectbox(
        tr("registry_category"), list(category_labels),
        format_func=category_labels.__getitem__, key=f"{key}_category",
    )
    regions = sorted({region for entry in entries for region in entry["region"].split("/")})
    region_labels = {"all": tr("registry_all"), **{value: value for value in regions}}
    region = region_filter.selectbox(
        tr("region"), list(region_labels), format_func=region_labels.__getitem__,
        key=f"{key}_region",
    )
    filtered = [
        entry for entry in entries
        if (category == "all" or entry["category"] == category)
        and (region == "all" or region in entry["region"].split("/"))
        and all(word in " ".join(entry.get(field, "") for field in (
            "id", "organization", "product", "region", "en", "de", "search_aliases"
        )).casefold() for word in query.split())
    ]
    st.caption(f"{len(filtered)} / {len(entries)} {tr('registry_entries')}")
    if not filtered:
        st.info(tr("registry_empty"))
        return

    table = pd.DataFrame([
        {
            "id": entry["id"],
            "organization": entry["organization"],
            "product": entry["product"],
            "region": entry["region"],
            "category": tr(f"registry_{entry['category']}"),
            "stage": tr(f"registry_{entry['stage']}"),
            "evidence": entry[language],
            "relevance": entry[f"relevance_{language}"],
            "source": entry["sources"][0]["url"],
            "additional_sources": " | ".join(source["url"] for source in entry["sources"][1:]),
        }
        for entry in filtered
    ])
    visible = ["product", "organization", "region", "category", "stage", "source"]
    labels = {column: tr(f"registry_{column}") for column in table.columns}
    st.dataframe(
        table[visible], hide_index=True, width="stretch", column_config={
            **{column: labels[column] for column in visible},
            "source": st.column_config.LinkColumn(labels["source"], display_text=tr("registry_open_source")),
        },
    )

    options = {entry["id"]: entry for entry in filtered}
    selected = st.selectbox(
        tr("registry_details"), list(options),
        format_func=lambda entry_id: f"{options[entry_id]['product']} · {options[entry_id]['organization']}",
        key=f"{key}_details",
    )
    entry = options[selected]
    stage_label = tr(f"registry_{entry['stage']}")
    with st.container(border=True):
        st.subheader(entry["product"])
        st.caption(f"{entry['organization']} · {entry['region']} · {stage_label}")
        st.markdown(f"**{tr('registry_evidence')}**")
        st.write(entry[language])
        st.markdown(f"**{tr('registry_relevance')}**")
        st.write(entry[f"relevance_{language}"])
        for index, source in enumerate(entry["sources"]):
            source_label = tr("registry_open_source" if index == 0 else "registry_additional_sources")
            st.markdown(f"[{source_label}]({source['url']})")

    st.download_button(
        tr("registry_export"), to_csv_bytes(table.rename(columns=labels)),
        file_name=f"paton_{key}.csv", mime="text/csv", key=f"{key}_export",
    )


def render_research_view(entries, key):
    labels = {value: tr(f"registry_{value}") for value in ("research_view", "demo_view")}
    view = st.radio(
        tr("registry_view"), list(labels),
        format_func=labels.__getitem__, horizontal=True, key=f"{key}_view",
    )
    if view == "research_view":
        st.caption(tr("registry_note"))
        render_registry(entries, key)
        st.stop()

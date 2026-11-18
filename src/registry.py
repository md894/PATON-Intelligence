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


@st.cache_data
def load_availability():
    path = Path(__file__).resolve().parents[1] / "data" / "product_availability.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _sales_status(entry, availability):
    fallback = "research" if entry["stage"] == "research" else "unknown"
    return availability.get(entry["id"], {}).get("status", fallback)


def _sales_year(record):
    if "year" not in record:
        return tr("registry_sales_no_year")
    if record["basis"] == "by":
        return tr("registry_sales_by").format(year=record["year"])
    return str(record["year"])


def _remember_sales_filter(widget_key, preference_key):
    st.session_state[preference_key] = st.session_state[widget_key]


def render_registry(entries, key, *, show_sales=False):
    language = st.session_state.get("language_preference", "en")
    availability = load_availability() if show_sales else {}
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
    sales_filter = "all"
    if show_sales:
        st.caption(tr("registry_sales_note"))
        statuses = ("order", "inquiry", "preorder", "research", "open", "unknown")
        status_labels = {"all": tr("registry_all")}
        status_labels.update({status: tr(f"registry_sales_status_{status}") for status in statuses})
        widget_key = f"{key}_sales_filter"
        preference_key = f"{key}_sales_preference"
        sales_filter = st.selectbox(
            tr("registry_availability"), list(status_labels),
            index=list(status_labels).index(st.session_state.get(preference_key, "all")),
            format_func=status_labels.__getitem__, key=widget_key,
            on_change=_remember_sales_filter, args=(widget_key, preference_key),
        )
    filtered = [
        entry for entry in entries
        if (category == "all" or entry["category"] == category)
        and (region == "all" or region in entry["region"].split("/"))
        and (sales_filter == "all" or _sales_status(entry, availability) == sales_filter)
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
    if show_sales:
        records = [availability.get(entry["id"], {}) for entry in filtered]
        table["availability"] = [status_labels[_sales_status(entry, availability)] for entry in filtered]
        table["sales_year"] = [_sales_year(record) for record in records]
        table["sales_source"] = [record.get("source") for record in records]
        visible = ["product", "organization", "availability", "sales_year", "region", "category", "sales_source"]
    labels = {column: tr(f"registry_{column}") for column in table.columns}
    source_column = "sales_source" if show_sales else "source"
    st.dataframe(
        table[visible], hide_index=True, width="stretch", column_config={
            **{column: labels[column] for column in visible},
            source_column: st.column_config.LinkColumn(labels[source_column], display_text=tr("registry_open_source")),
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
        if show_sales:
            record = availability.get(selected, {})
            status = status_labels[_sales_status(entry, availability)]
            st.markdown(f"**{tr('registry_availability')}** · {status}")
            if record.get("year"):
                st.write(f"{tr('registry_sales_year')} · {_sales_year(record)}")
            if record:
                st.write(record[language])
                st.markdown(f"[{tr('registry_sales_open_source')}]({record['source']})")
                if record.get("additional_source"):
                    st.markdown(f"[{tr('registry_additional_sources')}]({record['additional_source']})")
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

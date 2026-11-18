import pandas as pd
import streamlit as st

from src.data import to_csv_bytes
from src.i18n import tr
from src.strategy_data import BUYERS, READINESS, SIGNALS, TASKS


def _save_draft(key):
    st.session_state.setdefault("strategy_draft_values", {})[key] = st.session_state[key]


def _draft_widget(key):
    drafts = st.session_state.get("strategy_draft_values", {})
    if key in drafts and key not in st.session_state:
        st.session_state[key] = drafts[key]
    return {"key": key, "on_change": _save_draft, "args": (key,)}


def render_pilot():
    st.subheader(tr("strategy_first"))
    st.write(tr("strategy_work"))
    with st.expander(tr("strategy_protocol"), expanded=True):
        st.write(tr("strategy_protocol_body"))
        st.markdown("[ORCA Teleop](https://github.com/orcahand/orca_teleop)")
    st.caption(tr("strategy_draft"))
    tolerance = st.number_input(tr("strategy_tolerance"), min_value=0.0, value=None, **_draft_widget("pilot_tolerance"))
    records = []
    invalid = False
    for column, method, label in zip(
        st.columns(2), ("paton", "orca_camera"), ("PATON", tr("strategy_baseline"))
    ):
        with column.container(border=True):
            st.markdown(f"**{label}**")
            setup = st.number_input(tr("strategy_setup"), min_value=0.0, value=None, **_draft_widget(f"pilot_{method}_setup"))
            trials = st.number_input(tr("strategy_attempts"), min_value=1, value=None, step=1, **_draft_widget(f"pilot_{method}_trials"))
            successes = st.number_input(tr("strategy_successes"), min_value=0, value=None, step=1, **_draft_widget(f"pilot_{method}_successes"))
            spread = st.number_input(tr("strategy_spread"), min_value=0.0, value=None, **_draft_widget(f"pilot_{method}_spread"))
        if all(value is None for value in (setup, trials, successes, spread)):
            continue
        if not tolerance or trials is None or successes is None or successes > trials or (spread is not None and trials < 2):
            invalid = True
            continue
        records.append({
            "method": label, "tolerance_deg": tolerance, "setup_minutes": setup,
            "trials": trials, "successful_trials": successes, "success_rate_pct": round(100 * successes / trials, 1),
            "repeatability_stddev_deg": spread,
        })
    if invalid:
        st.warning(tr("strategy_invalid"))
    if records:
        results = pd.DataFrame(records)
        st.dataframe(results, hide_index=True, width="stretch", column_config={
            "success_rate_pct": st.column_config.NumberColumn(tr("strategy_rate"), format="%.1f%%"),
            "setup_minutes": tr("strategy_setup"), "trials": tr("strategy_attempts"),
            "successful_trials": tr("strategy_successes"), "method": tr("strategy_method"),
            "tolerance_deg": tr("strategy_tolerance"), "repeatability_stddev_deg": tr("strategy_spread"),
        })
        if not invalid:
            st.download_button(tr("strategy_export"), to_csv_bytes(results), "orca-pilot.csv", "text/csv")
    elif not invalid:
        st.info(tr("strategy_empty"))


def render_comparison(entries, language):
    index = int(language == "de")
    labels = {key: task["title"][index] for key, task in TASKS.items()}
    selected = st.selectbox(tr("strategy_task"), list(labels), format_func=labels.__getitem__, key="strategy_task")
    task = TASKS[selected]
    st.write(task["question"][index])
    rows = [
        {
            tr("registry_product"): entries[entry_id]["product"],
            tr("strategy_claim"): entries[entry_id][language],
            tr("strategy_gap"): entries[entry_id][f"relevance_{language}"],
            tr("registry_source"): entries[entry_id]["sources"][0]["url"],
        }
        for entry_id in task["entries"]
    ]
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True, column_config={
        tr("registry_source"): st.column_config.LinkColumn(display_text=tr("registry_open_source")),
    })


def render_readiness(language):
    index = int(language == "de")
    labels = {stage: tr(f"strategy_readiness_{stage}") for stage in ("none", "demo", "measured")}
    records = []
    st.caption(tr("strategy_review_draft"))
    for key, english, german, public_status, verify_en, verify_de in READINESS:
        name = (english, german)[index]
        with st.container(border=True):
            st.subheader(name)
            st.caption(tr(public_status))
            st.markdown(f"**{tr('strategy_measure')}**")
            st.write((verify_en, verify_de)[index])
            stage = st.selectbox(
                tr("strategy_status"), list(labels), format_func=labels.__getitem__,
                **_draft_widget(f"strategy_readiness_{key}"),
            )
        records.append({"capability_id": key, "capability": name, "review_stage": stage})
    st.markdown("[FELYA LABS](https://www.felyalabs.com/)")
    st.download_button(tr("strategy_readiness_export"), to_csv_bytes(pd.DataFrame(records)), "paton-readiness.csv", "text/csv")


def render_buyers(language):
    index = int(language == "de")
    labels = {stage: tr(f"strategy_demand_{stage}") for stage in ("none", "interview", "trial", "paid")}
    records = []
    st.caption(tr("strategy_review_draft"))
    for key, profile in BUYERS.items():
        name, user, budget, alternative, value = [item[index] for item in profile]
        with st.container(border=True):
            st.subheader(name)
            st.caption(tr("strategy_hypothesis"))
            for label, text in zip(("user", "budget", "alternative", "value"), (user, budget, alternative, value)):
                st.markdown(f"**{tr(f'strategy_{label}')}** — {text}")
            stage = st.selectbox(
                tr("strategy_demand"), list(labels), format_func=labels.__getitem__,
                **_draft_widget(f"strategy_buyer_{key}"),
            )
        records.append({"segment_id": key, "segment": name, "demand_stage": stage})
    st.download_button(tr("strategy_buyer_export"), to_csv_bytes(pd.DataFrame(records)), "buyer-validation.csv", "text/csv")


def render_signals(entries, language, *, limit=None):
    st.caption(tr("strategy_signals_note"))
    index = int(language == "de")
    for entry_id, date, impact in SIGNALS[:limit]:
        entry = entries[entry_id]
        with st.container(border=True):
            st.markdown(f"**{entry['organization']} · {entry['product']}**")
            st.caption(" · ".join(part for part in (date, tr("strategy_reviewed")) if part))
            st.write(entry[language])
            st.markdown(f"**{tr('strategy_impact')}** — {impact[index]}")
            st.markdown(f"[{tr('registry_open_source')}]({entry['sources'][0]['url']})")

from collections.abc import Mapping

import pandas as pd


BENEFIT_COLUMNS = {
    "market_attractiveness": "Market attractiveness",
    "problem_urgency": "Problem urgency",
    "willingness_to_pay": "Willingness to pay",
    "accessibility": "Customer accessibility",
    "product_fit": "Product fit",
}

COST_COLUMNS = {
    "sales_cycle_months": "Sales cycle",
    "regulatory_complexity": "Regulatory complexity",
}

DEFAULT_WEIGHTS = {
    "market_attractiveness": 20,
    "problem_urgency": 20,
    "willingness_to_pay": 15,
    "accessibility": 10,
    "product_fit": 25,
    "sales_cycle_months": 5,
    "regulatory_complexity": 5,
}


def _min_max(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="raise").astype(float)
    spread = numeric.max() - numeric.min()
    if spread == 0:
        return pd.Series(0.5, index=series.index, dtype=float)
    return (numeric - numeric.min()) / spread


def score_markets(frame: pd.DataFrame, weights: Mapping[str, float]) -> pd.DataFrame:
    """Return a copy with a transparent 0-100 weighted opportunity score.

    Benefit criteria increase the score. Cost criteria (sales cycle and
    regulatory complexity) are inverted so that lower values score higher.
    """
    required = set(BENEFIT_COLUMNS) | set(COST_COLUMNS)
    missing_columns = required.difference(frame.columns)
    missing_weights = required.difference(weights)
    if missing_columns:
        raise ValueError(f"Missing scoring columns: {sorted(missing_columns)}")
    if missing_weights:
        raise ValueError(f"Missing scoring weights: {sorted(missing_weights)}")

    total_weight = sum(float(weights[column]) for column in required)
    if total_weight <= 0:
        raise ValueError("At least one scoring weight must be greater than zero.")

    result = frame.copy()
    score = pd.Series(0.0, index=result.index)
    for column in BENEFIT_COLUMNS:
        score += _min_max(result[column]) * float(weights[column])
    for column in COST_COLUMNS:
        score += (1 - _min_max(result[column])) * float(weights[column])

    result["opportunity_score"] = (score / total_weight * 100).round(1)
    return result.sort_values("opportunity_score", ascending=False).reset_index(drop=True)

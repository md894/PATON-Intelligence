from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def load_competitors() -> pd.DataFrame:
    """Load the bundled competitor demonstration dataset."""
    return pd.read_csv(DATA_DIR / "competitors_demo.csv", parse_dates=["last_checked"])


def load_markets() -> pd.DataFrame:
    """Load the bundled B2B market demonstration dataset."""
    return pd.read_csv(DATA_DIR / "markets_demo.csv", parse_dates=["last_checked"])


def to_csv_bytes(frame: pd.DataFrame) -> bytes:
    """Create an Excel-friendly UTF-8 CSV without writing to disk."""
    return frame.to_csv(index=False).encode("utf-8-sig")

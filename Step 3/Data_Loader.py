"""
Loads FastF1 sessions, exports raw laps, converts lap-time strings to seconds, 
builds stint-level features (lap index, average pace, delta), and saves a 
processed CSV with a dynamic filename.
"""
import numpy as np
import pandas as pd
import fastf1 as f1
from pathlib import Path

# Block: Project paths
DATA_RAW       = Path("data/raw")
CACHE_DIR      = Path("data/cache")
DATA_PROCESSED = Path("data/processed")

# Enable FastF1 on-disk cache (speeds up repeated loads)
f1.Cache.enable_cache(str(CACHE_DIR))

# Function: Session loader (Download & load a FastF1 session, return laps + session, and save raw laps as CSV)
def load_session(year: int, gp: str, sess: str):
    session = f1.get_session(year, gp, sess)
    session.load()
    laps = session.laps.copy()
    out  = DATA_RAW / f"{gp}_{year}_{sess}_laps.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    laps.to_csv(out, index=False)
    return laps, session


# Block: Time conversions
# Function: Convert a time string like '0 days 00:01:38.693000' to seconds
def convert_to_seconds(time_str):
    # Treat missing values up front
    if pd.isna(time_str):
        return np.nan
    try:
        # Expected shape: "0 days 00:01:38.693000"
        # Split into days and the HH:MM:SS.uuuuuu part
        days, time = str(time_str).split(" days ")

        # Split time into hours, minutes, seconds.decimals
        h, m, s = time.split(":")

        # Compute total seconds
        # 1 day = 86400 s, 1 hour = 3600 s, 1 minute = 60 s
        return int(days) * 86400 + int(h) * 3600 + int(m) * 60 + float(s)

    except (ValueError, AttributeError):
        # Any parsing issue falls back to NaN
        return np.nan

# Function: Convert seconds to a 'M:SS.mmm' string
def convert_to_minutes(seconds):
    if pd.isna(seconds):
        return np.nan
    minutes = int(seconds // 60)
    rem     = float(seconds % 60)
    return f"{minutes}:{rem:06.3f}"

# Function: Feature engineering (Build lap-level features and save a processed CSV)
def prepare_lap_features(
    input_file: str | Path,
    output_dir: str | Path = "data/processed",
    year: int | None = None,
    gp: str | None   = None,
    sess: str | None = None,
):
    # Load raw laps
    df = pd.read_csv(input_file)

    # Core numeric features (seconds)
    df["LapTimeSeconds"] = df["LapTime"].apply(convert_to_seconds)

    # Lap index (per Driver, Stint)
    df["LapInStint"] = df.groupby(["Driver", "Stint"]).cumcount() + 1

    # Average pace (seconds) per (Driver, Stint)
    df["StintAvgPaceSeconds"] = df.groupby(["Driver", "Stint"])["LapTimeSeconds"].transform("mean")

    # Average pace string (m:ss.mmm) per (Driver, Stint)
    df["StintAvgPace"] = df["StintAvgPaceSeconds"].apply(convert_to_minutes)

    # Delta vs stint average (in seconds)
    df["DeltaToStintAvgSeconds"] = df["LapTimeSeconds"] - df["StintAvgPaceSeconds"]

    # Persist results (dynamic name if metadata is provided)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = (
        out_dir / f"{gp}_{year}_{sess}_processed.csv"
        if (year and gp and sess)
        else out_dir / "processed_laps.csv"
    )

    df.to_csv(out_file, index=False)
    return df, out_file

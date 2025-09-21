"""
Loads lap-time data, converts mm:ss to seconds, cleans invalid rows, 
computes per-driver averages and worst laps, finds the overall 
fastest lap, and adds a delta column vs. the session best.
"""
import pandas as pd
import numpy as np

# FUNCTION: convert 'minutes:seconds' format to total seconds
def convert_to_seconds(time_str):
    try:
        minutes, seconds = time_str.split(":")
        return int(minutes) * 60 + float(seconds)
    except Exception:
        return np.nan
 
# Load CSV data
# Check "sample2.csv" file 
df = pd.read_csv("sample2.csv", sep=";") 

# Converting lap times from minutes to seconds to enable calculations
df["LapTimeSeconds"] = df["LapTime"].apply(convert_to_seconds)

# Drop rows with invalid/missing lap times to avoid contaminating stats
df = df.dropna(subset=["LapTimeSeconds"])

# Quick sanity check: preview the transformed table
print(pd.concat([df.head(10), df.tail(10)]))

# Per-driver mean lap time (in seconds)
average = df.groupby("Driver").agg(AverageLapTime=("LapTimeSeconds", "mean"))
print(average)

# Global best lap: time, driver, and lap number
best_time = df["LapTimeSeconds"].min()                    # Fastest lap time overall
best_driver = df[df["LapTimeSeconds"] == best_time]["Driver"].values[0]   # Corresponding driver
best_lap = df[df["LapTimeSeconds"] == best_time]["Lap"].values[0]         # Corresponding lap number
print(f"The overall best time is by {best_driver}: {best_time:.3f}s on lap {best_lap}")

# Per-driver worst (slowest) lap time
worst_time_per_driver = df.groupby("Driver").agg(WorstLapTime=("LapTimeSeconds", "max"))
print(worst_time_per_driver)

# Add a delta column: gap to the session's best lap
df["Delta"] = df["LapTimeSeconds"] - best_time
print(df.head())

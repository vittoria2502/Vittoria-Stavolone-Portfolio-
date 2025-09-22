"""
This script builds three Plotly visualizations for race analysis: stint pace (lap vs time, colored by compound), 
tyre degradation (lap-in-stint vs time with OLS trendline), and fuel burn (mean lap time vs lap number with linear fit), 
filtered by driver.
"""
import numpy as np
import pandas as pd
import plotly.express as px

# Color legend for different tyre compounds
TYRE_COLORS = {
    "SOFT": "red",
    "MEDIUM": "yellow",
    "HARD": "grey",
    "INTERMEDIATE": "green",
    "WET": "blue",
}

# Function: Scatter plot – LapNumber vs LapTimeSeconds (colored by tyre compound)
def stint_pace(df: pd.DataFrame, driver: str | None = None):
    # Filter laps only for the selected driver
    df = df[df.Driver.isin([driver])]
    fig = px.scatter(
        df,
        x="LapNumber",               # x-axis: race lap index
        y="LapTimeSeconds",          # y-axis: lap time (seconds)
        color="Compound",
        color_discrete_map=TYRE_COLORS,
        hover_data=[
            "Stint",                 # shows stint index on hover
            "TyreLife",              # shows tyre age on hover
        ],
        title=f"Stint Pace – {driver}",
    )
    return fig

# Function: Scatter plot – LapInStint vs LapTimeSeconds (with regression trendline)
def tire_degradation(df: pd.DataFrame, driver: str | None = None):
    # Filter laps only for the selected driver
    df = df[df.Driver.isin([driver])]
    fig = px.scatter(
        df,
        x="LapInStint",              # x-axis: race lap index in that stint
        y="LapTimeSeconds",          # y-axis: lap time (seconds)
        color="Compound",
        trendline="ols",             # fit a regression line
        color_discrete_map=TYRE_COLORS,
        facet_col="Driver",          # one subplot per driver
        # Detailed info on hover
        hover_data=[
            "Stint",
            "TyreLife",
            "LapNumber",
        ],
        title=f"Tire Degradation – {driver}",
    )
    return fig


# Function: Scatter plot – LapNumber vs FuelCorrectedLapTime (with regression trendline)
def fuel_burn(df: pd.DataFrame, driver: str | None = None, initial_fuel: float = 100.0):
    # Filter laps only for the selected driver
    df = df[df.Driver.isin([driver])]

    # Note: cars start with 103.5 kg but only 100 kg are burned during the race
    total_fuel = 103.5  

    # Total number of laps completed in the session
    total_laps = df["LapNumber"].max()

    # Average fuel consumption per lap (kg/lap), normalized on the usable fuel (100 kg)
    fuel_per_lap = initial_fuel / total_laps

    # Block: Estimate the effect of fuel weight on lap time:
    # each kg of fuel burned reduces lap time by ~0.03 s (reference: Barcelona GP)
    # check "https://www.reddit.com/r/F1Technical/comments/1eebmbz/what_difference_in_pace_would_15_kg_make/#:~:text=The%20rule%20of%20thumb%20is,seconds%20over%20the%20whole%20race."
    # (LapNumber - 1) ensures that at Lap 1 the correction is zero, since no fuel has been burned yet
    df["FuelWeightEffect"] = ((df["LapNumber"] - 1) * fuel_per_lap) * 0.03
    
    # Compute fuel-corrected lap time by removing the benefit from fuel burn
    df["FuelCorrectedLapTime"] = df["LapTimeSeconds"] - df["FuelWeightEffect"]
    fig = px.scatter(
        df,
        x="LapNumber",
        y="FuelCorrectedLapTime",
        color="Driver",
        trendline="ols",  # adds an OLS regression line to highlight residual performance trends
        title=f"Fuel Burn - {driver}"
    )
    return fig

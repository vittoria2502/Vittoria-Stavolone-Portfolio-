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

# Function: # Scatter plot – LapInStint vs LapTimeSeconds (with regression trendline)
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

# Function: Scatter plot – LapNumber vs LapTimeSeconds (with regression line)
def fuel_burn(df: pd.DataFrame, driver: str | None = None):
    # Filter laps only for the selected driver
    df = df[df.Driver.isin([driver])]

    # Compute mean laptime (group by lap number)
    grouped = df.groupby("LapNumber")["LapTimeSeconds"].mean().reset_index()

    # Linear regression on the aggregated data (least squares fit):
    # np.polyfit(x, y, 1) estimates a straight line y = m*x + b that best fits
    # the relation between lap number (x) and mean lap time (y).
    # m = (slope)  -> how much lap time changes per additional lap
    # b = (intercept) -> baseline lap time when LapNumber = 0 (line’s intercept).
    m, b = np.polyfit(grouped.LapNumber, grouped.LapTimeSeconds, 1)

    # Predicted values from the linear model for each lap:
    # Create a new column "Fit" = m*LapNumber + b so that the DataFrame contains:
    # – actual measurements (LapTimeSeconds)
    # – estimated trend from the regression (Fit)
    # This allows comparison, plotting both real vs. fitted, or analyzing residuals.
    grouped["Fit"] = m * grouped.LapNumber + b  # regression fit

    fig = px.scatter(
        grouped,
        x="LapNumber",               # x-axis: race lap index
        y="LapTimeSeconds",          # y-axis: lap time (seconds)
        trendline="ols",             # fit a regression line
        title=f"Fuel-Burn – {driver}",
    )
    return fig

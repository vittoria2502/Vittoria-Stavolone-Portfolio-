import streamlit as st
import pandas as pd
from pathlib import Path
from data_loader import load_session, prepare_lap_features
from plotting_prototypes import stint_pace, tire_degradation, fuel_burn

# Block: Cache get_prepared's output to avoid re-downloading, for 1 hour
@st.cache_data(show_spinner="Loading session…", ttl=3600)
def get_prepared(year: int, gp: str, sess: str):
    laps, _ = load_session(year, gp, sess)         # load a FastF1 session
    tmp = Path(f"data/raw/{gp}_{year}_{sess}_laps.csv")   # ensure dynamic name
    tmp.parent.mkdir(parents=True, exist_ok=True)
    laps.to_csv(tmp, index=False)                   # persist raw laps to CSV
    df, _ = prepare_lap_features(tmp, "data/processed", year=year, gp=gp, sess=sess)
    return df                                       # return the processed DataFrame

# Block: Manual cache invalidation (Refresh button)
if st.button("Refresh"):
    get_prepared.clear()

# Block: App header
st.title("Test Streamlit App")
st.write("If you see this message, Streamlit is running correctly")
st.title("Pit-Wall Lite – Demo")

# Block: Controls (session selectors)
year = st.selectbox("Year", [2025, 2024], index=0)
gp = st.text_input("GP name", "Bahrain")
session_type = st.selectbox("Session", ["R", "Q", "FP1", "FP2", "FP3"], index=0)

# Block: Load session (download + process)
if st.button("Load session"):
    with st.spinner("Loading and processing…"):
        # Use the cached pipeline; also store df for plotting tabs
        df = get_prepared(year, gp, session_type)
        st.session_state["data"] = df
        st.success("Data loaded successfully!")
        st.dataframe(df)   # quick preview table

# Block: Load data: re-open the already processed CSV for this Year/GP/Session ---
if st.button("Load data"):
    processed_path = Path(f"data/processed/{gp}_{year}_{session_type}_processed.csv")
    if processed_path.exists():
        df = pd.read_csv(processed_path)
        st.session_state["data"] = df
        st.success(f"Loaded: {processed_path.name}")
    else:
        st.error("File not found. Press 'Load session' first for this GP/Session.")

# Block: Tabs: show visuals only if we have data in memory
if "data" in st.session_state:
    df = st.session_state["data"]
    tab1, tab2, tab3 = st.tabs(["Stint pace", "Tyre degradation", "Fuel burn"])

    with tab1:
        # Single-driver render pace by compound
        drv = st.selectbox("Driver", sorted(df.Driver.unique()), key="p_drv")
        st.plotly_chart(stint_pace(df, drv), use_container_width=True)

    with tab2:
        # Single-driver degradation view
        drv = st.selectbox("Driver", sorted(df.Driver.unique()), key="d_drv")
        st.plotly_chart(tire_degradation(df, drv), use_container_width=True)

    with tab3:
        # Single-driver fuel-burn trend
        drv = st.selectbox("Driver", sorted(df.Driver.unique()), key="f_drv")
        st.plotly_chart(fuel_burn(df, drv), use_container_width=True)

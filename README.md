# Formula 1 

Welcome to the official repository of my Formula 1 project, a full immersion into motorsport data analysis and race strategy simulation. Over the course of 4 themed steps, I progressively built my technical skills and delivered structured outputs, merging my passion for Formula 1 with scientific programming.


## 🔸 Step 1: Setup and Foundations

In this first step, I set up the entire environment:

- Installed Python, Git, WSL (Ubuntu), Jupyter Lab, VS Code.
- Created the folder structure for the sprint.
- Learned Python Libraries basics (**NumPy, Pandas, Matplotlib, Seaborn**)

Deliverables:

- Python scripts using Data Analysis libraries 


## 🔸 Step 2: FastF1 and Telemetry Analysis

In this step I worked with real Formula 1 data using the FastF1 Python library:

- Downloaded and cached 3 sessions from the 2025 season
- Parsed telemetry data (Speed, Throttle, Brake, Gear, LapTime)
- Generated plots such as **Speed vs Distance, Throttle vs Brake, Gear vs Distance**
- Exported clean CSVs 

Deliverables:

- Python scripts for lap comparison and telemetry analysis
- Export of sessions and data as CSV


## 🔸 Step 3: Data Pipelines and Streamlit Dashboards

In this step I focused on building reusable code and interactive visualizations:

- Modularized data loading (e.g. 'data_loader.py', 'plotting_prototypes.py')
- Built Streamlit apps for:
  * Delta vs Leader per driver
  * **Stint pace** per driver
  * **Tyre degradation** per driver
  * **Fuel burn** per driver
- Centralized data/cache/processed folders

Deliverables:

- **Streamlit app** with tabs for each analysis
- Local dashboards with real race data


## 🔸 Step 4: Strategy Simulation with Monte Carlo

In the last step I implemented a Monte Carlo simulator to analyze the duration of a race with different strategies and interferences (pit-stop and SC):

- Defined tyre model using degradation function: **$lap time = base + a \sqrt{laps} + b \cdot laps$**
- Simulated race outcomes with randomized Safety Car events
- Compared strategies like Soft-Medium vs Soft-Hard vs Medium-Hard
- Compared strategies like Soft-Medium vs Soft-Medium with SC 

Deliverables:

- Notebook 'Race_Strategy_Monte_Carlo_Analysis.ipynb'
- Race time analysis with plots


## 🏁 Final Goal

This project is a training sprint towards **motorsport engineering**, combining:

- Python for data science
- Git/GitHub for version control
- FastF1 for telemetry parsing
- Matplotlib/Seaborn/Plotly for visualization
- Streamlit for dashboards
- Simulation for race strategy 

Every line of code, chart, and strategy contributes to building a solid foundation for F1 race data and vehicle performance analysis. 

> Built by Vittoria Stavolone – Mathematician 



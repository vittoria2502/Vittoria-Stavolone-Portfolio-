"""
This script compares Leclerc vs. Verstappen in Bahrain qualifying: loads fastest laps, 
computes delta-time along distance, and plots both the gap trace and speed traces with 
team colors.
"""
from matplotlib import pyplot as plt
import fastf1
import fastf1.plotting
from fastf1 import utils

fastf1.Cache.enable_cache('cache')

# Configure FastF1 plotting
fastf1.plotting.setup_mpl(mpl_timedelta_support=True, misc_mpl_mods=False, color_scheme='fastf1')

# Load qualifying session
# 'Q' = Qualifying
session = fastf1.get_session(2025, 'Bahrain', 'Q')
session.load()

# Block: Extract fastest laps and telemetry for Leclerc and Verstappen
fast_leclerc = session.laps.pick_driver("LEC").pick_fastest()
leclerc_car_data = fast_leclerc.get_car_data().add_distance()

fast_verstappen = session.laps.pick_driver("VER").pick_fastest()
verstappen_car_data = fast_verstappen.get_car_data().add_distance()

# Block: Team colors for plot styling
fer_color = fastf1.plotting.get_team_color(fast_leclerc['Team'], session=session)  # Ferrari
rbr_color = fastf1.plotting.get_team_color(fast_verstappen['Team'], session=session)  # Red Bull

# Delta time calculation
delta_time, ref_tel, compare_tel = utils.delta_time(fast_leclerc, fast_verstappen)

# Block: Plot telemetry — Delta and Distance vs Speed comparison
fig, ax = plt.subplots(2, 1, figsize=(18, 16))  # 2 rows, 1 column

# 1) Delta line (gap vs distance)
ax[0].plot(ref_tel['Distance'], delta_time, color=rbr_color, label="Delta to LEC")
ax[0].set_xlabel("Distance (m)")
ax[0].set_ylabel("Delta (s)")
ax[0].set_title("Delta Verstappen vs Leclerc Bahrain GP - Qualifying")
for x, lab in zip(corner_positions, corner_labels):
    ax[0].axvline(x=x, color="white", linestyle="--", alpha=0.5)
    ax[0].text(x, 0.02, lab, color="lime", ha="left", va="center", transform=ax[0].get_xaxis_transform())
ax[0].axhline(y=0, color="white", linestyle="--", alpha=0.5)

# 2) Speed traces comparison
# Leclerc speed telemetry
ax[1].plot(leclerc_car_data["Distance"], leclerc_car_data["Speed"], color=fer_color, label="LEC")
# Verstappen speed telemetry
ax[1].plot(verstappen_car_data["Distance"], verstappen_car_data["Speed"], color=rbr_color, label="VER")
ax[1].set_xlabel("Distance (m)")
ax[1].set_ylabel("Speed (Km/h)")
ax[1].set_title("Fastest lap Verstappen vs Leclerc Bahrain GP - Qualifying")
for x, lab in zip(corner_positions, corner_labels):
    ax[1].axvline(x=x, color="white", linestyle="--", alpha=0.5)
    ax[1].text(x, 0.02, lab, color="lime", ha="left", va="center", transform=ax[1].get_xaxis_transform())
ax[1].legend()

# Layout & export
plt.subplots_adjust(hspace=0.4)
plt.savefig("Fastest_Lap_Telemetry_Comparison.png", dpi=300)
plt.show()

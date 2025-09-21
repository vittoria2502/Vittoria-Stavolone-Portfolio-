"""
This script loads Bahrain qualifying, extracts Leclerc’s fastest-lap telemetry, 
and plots three views: distance vs speed, distance vs throttle/brake, 
and distance vs gear.
"""
from matplotlib import pyplot as plt
import fastf1 
import fastf1.plotting

fastf1.Cache.enable_cache('cache')

# Configure FastF1 plotting
fastf1.plotting.setup_mpl(misc_mpl_mods=False, color_scheme="fastf1")

# Load qualifying session
# 'Q' = Qualifying session type
session = fastf1.get_session(2025, "Bahrain", "Q")
session.load()

# Block: Extract Leclerc's fastest lap telemetry
fast_leclerc = session.laps.pick_driver("LEC").pick_fastest()
leclerc_car_data = fast_leclerc.get_car_data().add_distance()

# Plot Telemetry
fig, ax = plt.subplots(3, 1, figsize=(22, 20))

# 1) Distance vs Speed
ax[0].plot(leclerc_car_data["Distance"], leclerc_car_data["Speed"])
ax[0].set_xlabel("Distance (m)")
ax[0].set_ylabel("Speed (km/h)")
ax[0].set_title("LEC fastest lap Bahrain GP – Qualifying")

# 2) Distance vs Throttle/Brake
ax[1].plot(leclerc_car_data["Distance"], leclerc_car_data["Throttle"], label="Throttle", color="green")
ax[1].plot(leclerc_car_data["Distance"], leclerc_car_data["Brake"], label="Brake", color="red")
ax[1].set_xlabel("Distance (m)")
ax[1].set_ylabel("Throttle/Brake (%)")
ax[1].set_title("LEC fastest lap (Distance vs Throttle/Brake) Bahrain GP – Qualifying")
ax[1].legend()

# 3) Distance vs Gear
ax[2].plot(leclerc_car_data["Distance"], leclerc_car_data["nGear"])
ax[2].set_xlabel("Distance (m)")
ax[2].set_ylabel("Gear")
ax[2].set_title("LEC fastest lap (Distance vs Gear) Bahrain GP – Qualifying")

# Layout & export
plt.tight_layout()
plt.savefig("Fastest_Lap_Analysis2.png", dpi=300)
plt.show()

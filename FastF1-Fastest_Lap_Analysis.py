import fastf1

fastf1.Cache.enable_cache('cache')

# Load race sessions
# 'R' = Race session type
session_bah = fastf1.get_session(2025, 'Bahrain', 'R')
session_bah.load()
session_mon = fastf1.get_session(2025, 'Monaco', 'R')
session_mon.load()
session_sil = fastf1.get_session(2025, 'Silverstone', 'R')
session_sil.load()

# Block: Extract fastest lap for Leclerc in Bahrain GP
laps_bah = session_bah.laps                        # full lap data for Bahrain
leclerc_laps_bah = laps_bah.pick_driver("LEC")     # filter only Leclerc’s laps
fastest_bah = leclerc_laps_bah.pick_fastest()      # fastest lap of that driver
print("Bahrain Race – LEC fastest lap:\n", fastest_bah)
laps_bah.to_csv("bahrain_2025_laps.csv", index=False)  # save all laps to CSV

# Block: Extract fastest lap for Leclerc in Monaco GP
laps_mon = session_mon.laps
leclerc_laps_mon = laps_mon.pick_driver("LEC")
fastest_mon = leclerc_laps_mon.pick_fastest()
print("Monaco Race – LEC fastest lap:\n", fastest_mon)
laps_mon.to_csv("monaco_2025_laps.csv", index=False)

# Block: Extract fastest lap for Leclerc in Silverstone GP
laps_sil = session_sil.laps
leclerc_laps_sil = laps_sil.pick_driver("LEC")
fastest_sil = leclerc_laps_sil.pick_fastest()
print("Silverstone Race – LEC fastest lap:\n", fastest_sil)
laps_sil.to_csv("silverstone_2025_laps.csv", index=False)






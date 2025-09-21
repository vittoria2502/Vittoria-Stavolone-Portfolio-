import numpy as np 
m = np.array([])  # array for average sector times
t = np.array([])  # array for lap times

# Laps × sectors matrix (each row is a lap, each column a sector)
sectors = np.array([
    [22.1, 30.2, 27.8],  # Lap 1: sector times
    [22.0, 30.3, 27.7],  # Lap 2
    [21.9, 30.1, 27.9],  # Lap 3
    [21.8, 30.4, 27.5],  # Lap 4
    [22.2, 30.0, 27.6],  # Lap 5
])

# Block: compute per-sector averages across all laps and print them
for i in range(sectors.shape[1]):  # iterate over columns (i.e., sectors)
    sector_avg = sectors[0:5, i].mean()  # compute average time for this sector across all laps
    m = np.append(m, sector_avg)  # append result to the sector-average array
    print(f"The average time for sector {i+1} is {sector_avg:.2f} s")  # report sector mean

# Block: compute per-lap total times (sum of 3 sectors) and print them
for j in range(sectors.shape[0]):  # iterate over rows (i.e., laps)
    lap_time = sectors[j, 0:3].sum()  # compute total lap time as the sum of its 3 sectors
    t = np.append(t, lap_time)  # append result to the lap-time array
    print(f"The time for lap {j+1} is {lap_time:.2f} s")  # report lap time

# Setup: find fastest lap time; prepare arrays for baseline means and influential sectors
minimum = min(t)  # minimum lap time (fastest lap)
weak_sector_means = np.array([])  # mean sector times excluding fastest lap
best_sector_vector = np.array([])  # index(es) of most influential sector(s) in fastest lap

# Block: locate the fastest lap
for k in range(len(t)):
    if t[k] == minimum:  # check if current lap is the fastest
        print(f"The fastest lap is lap {k+1} with per-sector times: {sectors[k]} s")
        min_lap_times = sectors[k]  # store sector times for the fastest lap
        # Remove the fastest lap from the matrix (to compute averages over the weak laps)
        sectors_with_no_fastest = np.delete(sectors, k, axis=0)

# Block: compute per-sector means on the update matrix without fastest lap
for s in range(sectors_with_no_fastest.shape[1]):  # iterate over columns
    mean_val = sectors_with_no_fastest[:, s].mean()  # mean of each sector across remaining laps
    weak_sector_means = np.append(weak_sector_means, mean_val)  # store the sector mean

# Block: delta = min_lap_times – weak_sector_means (compute delta vs. baseline)
delta = min_lap_times - weak_sector_means
m = delta.min()  # the minimum (i.e., max improvement)

# Block: find sector indices where the minimum delta occurs (key contributors)
for a in range(len(delta)):
    if delta[a] == m:  # check if this sector matches the minimum delta
        best_sector_vector = np.append(best_sector_vector, a + 1)  # append best sector/s index/es
print(f"In the best lap, i.e., lap {k+1}, the most influential sector/s is/are {best_sector_vector}.")

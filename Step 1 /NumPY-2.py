import numpy as np

# FUNCTION: search for laps with speed > average speed
def laps_above_average(speed_vector):
    avg = speed_vector.mean()
    above = speed_vector >= avg
    below = speed_vector < avg
    print(f"The average speed is {avg:.4f} km/h.")
    for i, x in enumerate(speed_vector, start=1):
        if x > avg:
            print(f"Lap {i}: speed = {x} km/h – above the average speed.")
        else:
            print(f"Lap {i}: speed = {x} km/h – below the average speed.")

    # return a formatted summary string with two groups of speeds: above/below average
    return (
        f"Speeds greater than or equal to the average: {speed_vector[above]} km/h.\n"
        f"Speeds below the average: {speed_vector[below]} km/h"
    )

# FUNCTION: comparison between successive lap speeds
def analyze_speed(speed_vector):
    deltas = []           # list to store lap-to-lap speed differences
    currnt_run = 0        # current run length of consecutive increases
    max_run = 0           # maximum length of a strictly increasing run
    start = 0             # starting index of the current run

    for i in range(len(speed_vector) - 1):
        diff = np.round(speed_vector[i+1] - speed_vector[i], 3)  # lap-to-lap difference
        deltas.append(diff)

        if diff > 0:  # speed increased
            if currnt_run == 0:  # start of a new run
                start = i
            currnt_run += 1
            if currnt_run > max_run:  # update maximum run
                max_run = currnt_run
                subsequence = speed_vector[start:start+currnt_run+1]
        else:  # no increase so reset the counter
            currnt_run = 0

    # returns: list of deltas, max length of increasing subsequence, and the subsequence itself
    return (deltas, max_run, subsequence)

# Array generation
np.random.seed(42) # ensures reproducibility of the random generation
speeds = np.random.normal(loc=318, scale=3, size=20)  # 20 random speeds ~ N(318, 3^2)
rounded_speeds = np.round(speeds, 2)  # round to 2 decimals

print(f"Simulated lap speeds: {rounded_speeds} km/h")

# Print laps above/below the average
print(laps_above_average(rounded_speeds))

# Boolean array for speeds > average speed
avg_speed = rounded_speeds.mean()
bool_array = rounded_speeds > avg_speed
print(f"Boolean array for speeds above average: {bool_array}")

# Print lap-to-lap deltas and the longest strictly increasing subsequence
print(f"Lap-to-lap speed deltas: {analyze_speed(rounded_speeds)[0]} km/h")
print(f"Longest increasing subsequence length = {analyze_speed(rounded_speeds)[1]}, " f"subsequence = {analyze_speed(rounded_speeds)[2]} km/h")

      

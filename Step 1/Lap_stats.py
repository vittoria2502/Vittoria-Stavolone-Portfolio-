import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid") # pleasant-looking style

# Load the CSV file
# Check "sample.csv" file
df = pd.read_csv("sample.csv") 
df.head()

# Note: The function convert_to_seconds, along with the creation of the
# "LapTimeSeconds" and "DeltaTime" columns, and the calculation of the
# best lap time, were already introduced earlier in the Pandas_Telemetry file.
def convert_to_seconds(time_str):
    try:
        minutes, seconds = time_str.split(":")
        return int(minutes) * 60 + float(seconds)
    except:
        return np.nan

df["LapTimeSeconds"] = df["LapTime"].apply(convert_to_seconds)
best_time = df["LapTimeSeconds"].min()
df["DeltaTime"] = df["LapTimeSeconds"] - best_time
print(df.head(10))

# Plot 1
plt.figure(figsize=(8,4))
plt.barh(df["Driver"], df["DeltaTime"], color="skyblue") # bar chart (barh = 90-degree rotated bar plot)
plt.xlabel("Delta Time (s)")
plt.ylabel("Drivers")
plt.title("Delta vs Leader Lap 20 Bahrain GP 2023")
plt.tight_layout() # prevents data from overlapping with labels
plt.grid(True)
plt.savefig("delta_bars.png", dpi=150)
plt.show()

# Plot 2
plt.figure(figsize=(6,4))
sns.scatterplot(data=df, x="Speed", y="LapTimeSeconds", hue="Driver", s=100) # scatter plot
plt.gca().invert_yaxis() # invert y-axis so faster lap times appear higher
plt.xlabel("Speed (km/h)")
plt.ylabel("Lap Time (s)")
plt.legend(bbox_to_anchor=(1, 1)) # move legend to the upper right outside the plot
plt.tight_layout() # prevents points from overlapping with labels
plt.grid(True)
plt.savefig("scatter_plot.png", dpi=150)
plt.show()

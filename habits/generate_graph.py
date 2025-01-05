import matplotlib.pyplot as plt
import pandas as pd
import july

dates_and_data = pd.read_csv("2025.csv", sep=",", header=None).to_numpy()

dates = dates_and_data[:, 0]
data = dates_and_data[:, 1]

july.heatmap(dates, data, title="Habit tracker", cmap="github")
plt.savefig("habits2025.png")

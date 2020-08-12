import os
import sys
import numpy as np
from mpl_toolkits import mplot3d
from gather_data import parse_results
import numpy as np
import matplotlib.pyplot as plt
import random

base_result_folder = "results"
result_folders = ["cpu_results", "gpu_results",
                  "wata-orz_results"]



dictionary = parse_results(base_result_folder, result_folders)
fig, ax = plt.subplots()

results = {}
for name in result_folders:
    results[name] = {"terminals": [], "time": []}
for value in dictionary.values():
    for name in result_folders:
        results[name]["terminals"].append(int(value["terminals"]))
        time = value[name]
        if time == 'over 30s':
            time = 40.0
        results[name]["time"].append(float(time)+0.0001)


for (name, color, marker) in zip(result_folders, ['red', 'green', 'blue'], [".", "+", "x"]):
    ax.scatter(results[name]["terminals"], results[name]["time"], c=color, s=100, label=name,
               alpha=0.5, edgecolors='none', marker=marker)


plt.axhline(30.0, color="orange", linestyle="dashed", alpha=0.2, label="30s border")
ax.legend()
ax.grid(True)
ax.set_yscale('log')
plt.xlabel("Terminals")
plt.ylabel("Time")
plt.show()

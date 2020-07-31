import os
import sys
import numpy as np
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

folder_gpu_results = 'all/results'
folder_cpu_results = 'all/cpp_results'
folder_wata_orz_results = 'all/wata-orz_results'
max_time_in_ms = 1000
results = []
current_result = []


def parse_results(result_folder):
    results = []
    current_result = []
    for file_name in os.listdir(result_folder):
        with open(result_folder + '/' + file_name, 'r') as f:
            file_results = []
            current_result = []
            for line in f.readlines():
                if line[0] == '-':
                    if len(current_result) > 0 and current_result[7] < max_time_in_ms:
                        file_results.append(current_result)
                        current_result = []
                    continue
                if 'Correct' in line:
                    continue
                if 'us' in line:
                    current_result.append(float(line.split(' ')[0])/1000)
                else:
                    current_result.append(float(line.split(' ')[0]))
            results = results + file_results
    results = np.array(results)
    return results[np.argsort(results[:, 7])]


def parse_wata_results(result_folder):
    results = []
    current_result = []
    for file_name in os.listdir(result_folder):
        with open(result_folder + '/' + file_name, 'r') as f:
            file_results = []
            current_result = []
            for line in f.readlines():
                if line[0] == '-':
                    if len(current_result) > 0 and current_result[2] < max_time_in_ms/1000:
                        current_result[2] = current_result[2]*1000
                        file_results.append(current_result)
                        current_result = []
                    continue
                if '.stp' in line or '.grp' in line:
                    continue
                current_result.append(float(line.split(' ')[0]))
            results = results + file_results
    results = np.array(results)
    return results[np.argsort(results[:, 2])]


results_gpu = parse_results(folder_gpu_results)
results_cpu = parse_results(folder_cpu_results)
results_wata_orz = parse_wata_results(folder_wata_orz_results)


def create_figure(results, x_index, y_index, z_index, ax, title, color, label):
    x_data = results[:, x_index]
    y_data = results[:, y_index]
    z_data = results[:, z_index]
    ax.scatter3D(x_data, y_data, z_data, c=color, label=label)
    ax.set_xlabel('nodes')
    ax.set_ylabel('terminals')
    ax.set_zlabel("time in ms")
    ax.set_title(title)
    ax.legend()


def create_figure_all():
    plt.figure()
    ax = plt.axes(projection='3d')
    create_figure(results_gpu, 0, 1, 7, ax,
                  "time for everything", "black", "GPU")
    create_figure(results_cpu, 0, 1, 7, ax,
                  "time for everything", "green", "CPU")
    create_figure(results_wata_orz, 0, 1, 2, ax,
                  "time for everything", "blue", "Wata-Orz")


def create_figure_first_phase():
    plt.figure()
    ax = plt.axes(projection='3d')
    create_figure(results_gpu, 0, 1, 5, ax,
                  "time for first phase", "red", "GPU")
    create_figure(results_cpu, 0, 1, 5, ax,
                  "time for first phase", "green", "CPU")


def create_figure_second_phase():
    plt.figure()
    ax = plt.axes(projection='3d')
    create_figure(results_gpu, 0, 1, 6, ax,
                  "time for second phase", "red", "GPU")
    create_figure(results_cpu, 0, 1, 6, ax,
                  "time for second phase", "green", "CPU")


def create_figure_distances():
    plt.figure()
    ax = plt.axes(projection='3d')
    create_figure(results_gpu, 0, 1, 3, ax,
                  "time for distances", "red", "GPU")
    create_figure(results_cpu, 0, 1, 3, ax,
                  "time for distances", "green", "CPU")


def create_figure_copy():
    plt.figure()
    ax = plt.axes(projection='3d')
    create_figure(results_gpu, 0, 1, 4, ax, "time for copy", "black", "black")


create_figure_all()
create_figure_copy()
create_figure_distances()
create_figure_first_phase()
create_figure_second_phase()
plt.show()

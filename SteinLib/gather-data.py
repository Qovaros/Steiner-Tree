import os
import sys
import numpy as np
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

result_folder = 'all/results'
results = []
current_result = []

for file_name in os.listdir(result_folder):
    with open(result_folder + '/' + file_name, 'r') as f:
        file_results = []
        current_result = []
        for line in f.readlines():
            if line[0] == '-':
                file_results.append(current_result)
                current_result = []
                continue
            if 'Correct' in line:
                continue
            if 'us' in line:
                current_result.append(float(line.split(' ')[0])/1000)
            else:
                current_result.append(float(line.split(' ')[0]))
        results = results + file_results[1:]
results = np.array(results)
results = results[np.argsort(results[:, 7])]
np.set_printoptions(suppress=True, threshold=sys.maxsize)
# for array in results:
# print(array)
print(results)

def create_figure(x_index, y_index, z_index, title):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    x_data = results[:, x_index]
    y_data = results[:, y_index]
    z_data = results[:, z_index]
    ax.scatter3D(x_data, y_data, z_data, c=z_data)
    ax.set_xlabel('nodes')
    ax.set_ylabel('terminals')
    ax.set_zlabel("time in ms")
    ax.set_title(title)

def create_figure_all():
    create_figure(0,1,7,"time for everything")

def create_figure_first_phase():
    create_figure(0,1,5,"time for first phase")

def create_figure_second_phase():
    create_figure(0,1,6,"time for second phase")

def create_figure_distances():
    create_figure(0,1,3,"time for distances")

def create_figure_copy():
    create_figure(0,1,4,"time for copy")

create_figure_all()
create_figure_copy()
create_figure_distances()
create_figure_first_phase()
create_figure_second_phase()
plt.show()

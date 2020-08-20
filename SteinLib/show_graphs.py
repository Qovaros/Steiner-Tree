import os
import sys
import numpy as np
from mpl_toolkits import mplot3d
from gather_data import parse_results
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import random

import matplotlib.cm as cm
from scipy.ndimage.filters import gaussian_filter

# matplotlib.use("pgf")
# matplotlib.rcParams.update({
#     "pgf.texsystem": "pdflatex",
#     'font.family': 'serif',
#     'text.usetex': True,
#     'pgf.rcfonts': False,
# })

base_result_folder = sys.argv[1]
data_folders = ["cpu_results", "gpu_results",
                  "wata-orz_results", "gpu_results_with_preprocessing", "wata-orz_results_with_preprocessing"]
result_folders = ["cpu_results", "gpu_results",
                  "wata-orz_results"]
result_folders_gpu_better = ["gpu_results",
                  "wata-orz_results"]

result_folders_gpu_better_2 = ["gpu_results_with_preprocessing",
                  "wata-orz_results_with_preprocessing"]
terminals_number = {
    "0-5 terminals": [0,5],
    "6-10 terminals": [6,10],
    "11-15 terminals": [11,15],
    "16-20 terminals": [16,20]
}

dataset_names = {
    "Sparse with random weight": ["P6Z", "B","C", "D"],
    "Grid graph with holes": ["DIW", "DMXA", "GAP", "MSM", "TAQ", "LIN"],
    "Sparse with incidence weights": ["I080", "I160", "I320", "I640"],
    "Other": ["P4E", "P4Z", "P6E", "PUC", "SP", "ES10FST"]
}

name_mapping = {
    "cpu_results": "Dreyfus-Wagner on CPU",
    "gpu_results": "Dreyfus-Wagner on GPU",
    "wata-orz_results": "Pruning EMV on CPU"
}


dictionary = parse_results(base_result_folder, data_folders)


def show_graph_all():
    fig, ax = plt.subplots(figsize=(10,10))
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
        ax.scatter(results[name]["terminals"], results[name]["time"], c=color, s=100, label=name_mapping[name],
                   alpha=0.5, edgecolors='none', marker=marker)
    plt.axhline(30.0, color="orange", linestyle="dashed", alpha=0.2, label="30s border")
    ax.legend(loc=2, prop={'size': 15})
    ax.grid(True)
    ax.set_yscale('log')
    plt.xlabel("Terminals")
    plt.ylabel("Time")

# def show_graph_gpu_better():
#     fig, ax = plt.subplots(figsize=(10,10))
#     results = {}
#     for name in result_folders:
#         results[name] = {"terminals": [], "time": []}
#     for value in dictionary.values():
#         for name in result_folders_gpu_better:
#             time = value[name]
#             if time == 'over 30s':
#                 time = 40.0
#             if value["gpu_results"] != 'over 30s' and (value["wata-orz_results"] == 'over 30s' or float(value["gpu_results"]) < float(value["wata-orz_results"])):
#                 results[name]["terminals"].append(int(value["terminals"]))
#                 results[name]["time"].append(float(time)+0.0001)

#     for (name, color, marker) in zip(result_folders_gpu_better, ['red', 'blue'], ["+", "x"]):
#         ax.scatter(results[name]["terminals"], results[name]["time"], c=color, s=100, label=name_mapping[name],
#                    alpha=0.5, edgecolors='none', marker=marker)
#     plt.axhline(30.0, color="orange", linestyle="dashed", alpha=0.2, label="30s border")
#     ax.legend(loc=2, prop={'size': 15})
#     ax.grid(True)
#     ax.set_yscale('log')
#     plt.xlabel("Terminals")
#     plt.ylabel("Time")

def show_graph_gpu_better2():
    fig, ax = plt.subplots(figsize=(10,10))
    results = {}
    for name in terminals_number.keys():
        results[name] = {"gpu_results": [], "wata-orz_results": []}
    for value in dictionary.values():
        for name in result_folders_gpu_better:
            time = value[name]
            if time == 'over 30s':
                time = 40.0
            for (terminal_limit_name, terminal_limit) in terminals_number.items():
                if int(value['terminals']) >= terminal_limit[0] and int(value['terminals']) <= terminal_limit[1]:
                    results[terminal_limit_name][name].append(float(time)+0.0001)

    for (name, color, marker) in zip(terminals_number.keys(), ['red', 'blue', "green", "purple"], ["1", "2", "3", "4"]):
        ax.scatter(results[name]["gpu_results"], results[name]["wata-orz_results"], c=color, s=100, label=name,
                   alpha=0.5, edgecolors='none', marker=marker)
    plt.axhline(30.0, color="orange", linestyle="dashed",
                alpha=0.2, label="30s border")
    ax.legend(loc=2, prop={'size': 15})
    plt.axvline(30.0, color="orange", linestyle="dashed",
                alpha=0.2, label="30s border")
    ax.grid(True)
    plt.plot([0,60], [0, 60], color="grey", linestyle="dashed", alpha=0.2)
    ax.set_xlim(0.00005, 60.0)
    ax.set_ylim(0.00005, 60.0)
    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.xlabel("Dreyfus-Wagner on GPU duration")
    plt.ylabel("Pruning EMV on CPU duration")

def show_graph_gpu_better3():
    fig, ax = plt.subplots(figsize=(10,10))
    results = {}
    for name in dataset_names.keys():
        results[name] = {"gpu_results": [], "wata-orz_results": []}
    for value in dictionary.values():
        for name in result_folders_gpu_better:
            time = value[name]
            if time == 'over 30s':
                time = 40.0
            for (dataset_name, dataset_content) in dataset_names.items():
                if value["name"] in dataset_content:
                    results[dataset_name][name].append(float(time)+0.0001)
    for (name, color, marker) in zip(dataset_names.keys(), ['red', 'blue', "green", "purple"], ["1", "2", "3", "4"]):
        ax.scatter(results[name]["gpu_results"], results[name]["wata-orz_results"], c=color, s=100, label=name,
                   alpha=0.5, edgecolors='none', marker=marker)
    plt.axhline(30.0, color="orange", linestyle="dashed",
                alpha=0.2, label="30s border")
    ax.legend(loc=2, prop={'size': 15})
    plt.axvline(30.0, color="orange", linestyle="dashed",
                alpha=0.2, label="30s border")
    ax.grid(True)
    plt.plot([0,60], [0, 60], color="grey", linestyle="dashed", alpha=0.2)
    ax.set_xlim(0.00005, 60.0)
    ax.set_ylim(0.00005, 60.0)
    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.xlabel("Dreyfus-Wagner on GPU duration")
    plt.ylabel("Pruning EMV on CPU duration")

def show_graph_gpu_better4():
    fig, ax = plt.subplots(figsize=(10,10))
    results = {}
    for name in terminals_number.keys():
        results[name] = {"gpu_results_with_preprocessing": [], "wata-orz_results_with_preprocessing": []}
    for value in dictionary.values():
        for name in result_folders_gpu_better_2:
            time = value[name]
            if time == 'over 30s':
                time = 40.0
            for (terminal_limit_name, terminal_limit) in terminals_number.items():
                if int(value['terminals']) >= terminal_limit[0] and int(value['terminals']) <= terminal_limit[1]:
                    results[terminal_limit_name][name].append(float(time)+0.0001)

    for (name, color, marker) in zip(terminals_number.keys(), ['red', 'blue', "green", "purple"], ["1", "2", "3", "4"]):
        ax.scatter(results[name]["gpu_results_with_preprocessing"], results[name]["wata-orz_results_with_preprocessing"], c=color, s=100, label=name,
                   alpha=0.5, edgecolors='none', marker=marker)
    plt.axhline(30.0, color="orange", linestyle="dashed",
                alpha=0.2, label="30s border")
    ax.legend(loc=2, prop={'size': 15})
    plt.axvline(30.0, color="orange", linestyle="dashed",
                alpha=0.2, label="30s border")
    ax.grid(True)
    plt.plot([0,60], [0, 60], color="grey", linestyle="dashed", alpha=0.2)
    ax.set_xlim(0.00005, 60.0)
    ax.set_ylim(0.00005, 60.0)
    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.xlabel("Dreyfus-Wagner on GPU with pre-processing duration")
    plt.ylabel("Pruning EMV on CPU with pre-processing duration")

def show_graph_gpu_better5():
    fig, ax = plt.subplots(figsize=(10,10))
    results = {}
    for name in dataset_names.keys():
        results[name] = {"gpu_results_with_preprocessing": [], "wata-orz_results_with_preprocessing": []}
    for value in dictionary.values():
        for name in result_folders_gpu_better_2:
            time = value[name]
            if time == 'over 30s':
                time = 40.0
            for (dataset_name, dataset_content) in dataset_names.items():
                if value["name"] in dataset_content:
                    results[dataset_name][name].append(float(time)+0.0001)
    for (name, color, marker) in zip(dataset_names.keys(), ['red', 'blue', "green", "purple"], ["1", "2", "3", "4"]):
        ax.scatter(results[name]["gpu_results_with_preprocessing"], results[name]["wata-orz_results_with_preprocessing"], c=color, s=100, label=name,
                   alpha=0.5, edgecolors='none', marker=marker)
    plt.axhline(30.0, color="orange", linestyle="dashed",
                alpha=0.2, label="30s border")
    ax.legend(loc=2, prop={'size': 15})
    plt.axvline(30.0, color="orange", linestyle="dashed",
                alpha=0.2, label="30s border")
    ax.grid(True)
    plt.plot([0,60], [0, 60], color="grey", linestyle="dashed", alpha=0.2)
    ax.set_xlim(0.00005, 60.0)
    ax.set_ylim(0.00005, 60.0)
    ax.set_yscale('log')
    ax.set_xscale('log')
    plt.xlabel("Dreyfus-Wagner on GPU with pre-processing duration")
    plt.ylabel("Pruning EMV on CPU with pre-processing duration")

show_graph_all()
# show_graph_gpu_better()
# plt.savefig('all.pgf', bbox_inches='tight')
show_graph_gpu_better2()
# plt.savefig('gpu_vs_pruning_sizes.pgf', bbox_inches='tight')
show_graph_gpu_better3()
# plt.savefig('gpu_vs_pruning_types.pgf', bbox_inches='tight')
show_graph_gpu_better4()
# plt.savefig('gpu_vs_pruning_preprocessing_sizes.pgf', bbox_inches='tight')
show_graph_gpu_better5()
# plt.savefig('gpu_vs_pruning_preprocessing_types.pgf', bbox_inches='tight')
plt.show()

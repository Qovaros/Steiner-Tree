import os
import sys
import numpy as np
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from gather_data import parse_results

base_result_folder = "results"
result_folders = ["cpu_results", "gpu_results", "gpu_results_with_preprocessing",
                  "wata-orz_results", "wata-orz_results_with_preprocessing"]
output_file = "summary.csv"
output_file_gpu = "gpu_better.csv"
output_file_gpu_preprocessing = "gpu_better_preprocessing.csv"
output_file_gpu_vs_cpu = "gpu_vs_cpu.csv"
output_file_gpu_summary = "gpu_vs_wata_summary.csv"
output_file_gpu_summary_preprocessing = "gpu_vs_wata_preprocessing_summary.csv"
dataset_names = {
    "Sparse with random weight": ["P6Z", "B","C", "D"],
    "Grid graph with holes": ["DIW", "DMXA", "GAP", "MSM", "TAQ", "LIN"],
    "Sparse with incidence weights": ["I080", "I160", "I320", "I640"],
    "Complete with euclidian weights": ["P4E"],
    "Complete with random weights": ["P4Z"],
    "Sparse with euclidian weights": ["P6E"],
    "Sparse constructed graphs": ["PUC"],
    "Sparse artificially constructed graphs": ["SP"],
    "FST-preprocessed rectilinear L1 weights": ["ES10FST"],
}
result_folders_gpu_better = ["gpu_results",
                  "wata-orz_results"]

dictionary = parse_results(base_result_folder, result_folders)

def write_table_to_csv_file():
    with open(base_result_folder + '/' + output_file, 'w') as f:
        f.write("test,nodes,edges,terminals")
        for result_folder in result_folders:
            f.write(','+result_folder)
        f.write('\n')
        for (key, value) in dictionary.items():
            f.write(key+','+value["nodes"]+','+value["edges"]+','+value["terminals"])
            for result_folder in result_folders:
                f.write(',' + value[result_folder])
            f.write('\n')

def write_gpu_better_table_to_csv_file():
    with open(base_result_folder + '/' + output_file_gpu, 'w') as f:
        f.write("test,nodes,edges,terminals,gpu_results,cpu_results,wata-orz_results,wata-orz_results_with_preprocessing\n")
        for (key, value) in dictionary.items():
            if value['wata-orz_results'] == 'over 30s' or (value["gpu_results"] != 'over 30s' and value['wata-orz_results'] > value["gpu_results"]):
                f.write(key+','+value["nodes"]+','+value["edges"]+','+value["terminals"]+','+value["gpu_results"]+','+value['cpu_results']+','+value['wata-orz_results']+','+value["wata-orz_results_with_preprocessing"]+'\n')

def write_gpu_with_preprocessing_better_table_to_csv_file():
    with open(base_result_folder + '/' + output_file_gpu_preprocessing, 'w') as f:
        f.write("test,nodes,edges,terminals,gpu_results,gpu_results_with_preprocessing,wata-orz_results,wata-orz_results_with_preprocessing\n")
        for (key, value) in dictionary.items():
            if value['wata-orz_results'] == 'over 30s' or (value["gpu_results_with_preprocessing"] != 'over 30s' and value['wata-orz_results_with_preprocessing'] > value["gpu_results_with_preprocessing"]):
                f.write(key+','+value["nodes"]+','+value["edges"]+','+value["terminals"]+','+value["gpu_results"]+','+value['gpu_results_with_preprocessing']+','+value['wata-orz_results']+','+value["wata-orz_results_with_preprocessing"]+'\n')

def write_speed_up_table_to_csv_file():
    with open(base_result_folder + '/' + output_file_gpu_vs_cpu, 'w') as f:
        f.write("test,nodes,edges,terminals,gpu_results,cpu_results,speed_up\n")
        for (key, value) in dictionary.items():
            if value['cpu_results'] == 'over 30s':
                f.write(key+','+value["nodes"]+','+value["edges"]+','+value["terminals"]+','+value["gpu_results"]+','+value['cpu_results']+',a lot\n')
            else:
                f.write(key+','+value["nodes"]+','+value["edges"]+','+value["terminals"]+','+value["gpu_results"]+','+value['cpu_results']+','+str((float(value['cpu_results'])+0.00001)/(float(value['gpu_results'])+0.00001))+'\n')

def write_gpu_faster_summary():
    fig, ax = plt.subplots(figsize=(10,10))
    results = {}
    for name in dataset_names.keys():
        results[name] = {"gpu_results": 0, "wata-orz_results": 0, "all": 0}
    for value in dictionary.values():
        time_gpu = value["gpu_results"]
        time_wata = value["wata-orz_results"]
        if time_gpu == 'over 30s':
            time_gpu = 40.0
        else:
            time_gpu = float(time_gpu)
        if time_wata == 'over 30s':
            time_wata = 40.0
        else:
            time_wata = float(time_wata)
        for (dataset_name, dataset_content) in dataset_names.items():
            if value["name"] in dataset_content:
                results[dataset_name]["all"] = results[dataset_name]["all"] + 1
                if time_gpu < time_wata:
                    results[dataset_name]["gpu_results"] = results[dataset_name]["gpu_results"] + 1 
                elif time_gpu > time_wata:
                    results[dataset_name]["wata-orz_results"] = results[dataset_name]["wata-orz_results"] + 1 
    with open(base_result_folder + '/' + output_file_gpu_summary, 'w') as f:
        f.write("type,gpu better,wata_orz better,all\n")
        for (key, value) in results.items():
            f.write(key+','+str(value["gpu_results"])+','+str(value["wata-orz_results"])+','+str(value["all"])+'\n')

def write_gpu_faster_summary_with_preprocessing():
    fig, ax = plt.subplots(figsize=(10,10))
    results = {}
    for name in dataset_names.keys():
        results[name] = {"gpu_results_with_preprocessing": 0, "wata-orz_results_with_preprocessing": 0, "all": 0}
    for value in dictionary.values():
        time_gpu = value["gpu_results_with_preprocessing"]
        time_wata = value["wata-orz_results_with_preprocessing"]
        if time_gpu == 'over 30s':
            time_gpu = 40.0
        else:
            time_gpu = float(time_gpu)
        if time_wata == 'over 30s':
            time_wata = 40.0
        else:
            time_wata = float(time_wata)
        for (dataset_name, dataset_content) in dataset_names.items():
            if value["name"] in dataset_content:
                results[dataset_name]["all"] = results[dataset_name]["all"] + 1
                if time_gpu < time_wata:
                    results[dataset_name]["gpu_results_with_preprocessing"] = results[dataset_name]["gpu_results_with_preprocessing"] + 1 
                elif time_gpu > time_wata:
                    results[dataset_name]["wata-orz_results_with_preprocessing"] = results[dataset_name]["wata-orz_results_with_preprocessing"] + 1 
    with open(base_result_folder + '/' + output_file_gpu_summary_preprocessing, 'w') as f:
        f.write("type,gpu better,wata_orz better,all\n")
        for (key, value) in results.items():
            f.write(key+','+str(value["gpu_results_with_preprocessing"])+','+str(value["wata-orz_results_with_preprocessing"])+','+str(value["all"])+'\n')

write_table_to_csv_file()
write_gpu_better_table_to_csv_file()
write_gpu_with_preprocessing_better_table_to_csv_file()
write_gpu_faster_summary()
write_gpu_faster_summary_with_preprocessing()
write_speed_up_table_to_csv_file()
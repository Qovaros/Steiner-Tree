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
            if value['wata-orz_results'] == 'over 30s' or (value["gpu_results_with_preprocessing"] != 'over 30s' and value['wata-orz_results'] > value["gpu_results_with_preprocessing"]):
                f.write(key+','+value["nodes"]+','+value["edges"]+','+value["terminals"]+','+value["gpu_results"]+','+value['gpu_results_with_preprocessing']+','+value['wata-orz_results']+','+value["wata-orz_results_with_preprocessing"]+'\n')

def write_speed_up_table_to_csv_file():
    with open(base_result_folder + '/' + output_file_gpu_vs_cpu, 'w') as f:
        f.write("test,nodes,edges,terminals,gpu_results,cpu_results,speed_up\n")
        for (key, value) in dictionary.items():
            if value['cpu_results'] == 'over 30s':
                f.write(key+','+value["nodes"]+','+value["edges"]+','+value["terminals"]+','+value["gpu_results"]+','+value['cpu_results']+',a lot\n')
            else:
                f.write(key+','+value["nodes"]+','+value["edges"]+','+value["terminals"]+','+value["gpu_results"]+','+value['cpu_results']+','+str((float(value['cpu_results'])+0.00001)/(float(value['gpu_results'])+0.00001))+'\n')

write_table_to_csv_file()
write_gpu_better_table_to_csv_file()
write_gpu_with_preprocessing_better_table_to_csv_file()
write_speed_up_table_to_csv_file()
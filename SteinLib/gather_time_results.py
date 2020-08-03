import os
import sys
import numpy as np
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

base_result_folder = "results"
result_folders = ["cpu_results", "gpu_results",
                  "wata-orz_results", "wata-orz_results_with_preprocessing"]
output_file = "summary.csv"
output_file_gpu = "gpu_better.csv"
output_file_gpu_vs_cpu = "gpu_vs_cpu.csv"

dictionary = {}

def parse_result(result_folder):
    solution_key = result_folder[len(base_result_folder)+1:]
    for file_name in sorted(os.listdir(result_folder)):
        with open(result_folder + '/' + file_name, 'r') as f:
            firstLine = f.readline().split('\n')[0].split(',')
            name = firstLine.index('name')
            nodes = firstLine.index('nodes')
            edges = firstLine.index('edges')
            terminals = firstLine.index('terminals')
            time = firstLine.index('time')
            for line in [l.split('\n')[0].split(',') for l in f.readlines()]:
                if line[name] not in dictionary:
                    dictionary[line[name]] = {"nodes": line[nodes], "edges": line[edges], "terminals": line[terminals]}
                if len(line) == len(firstLine):
                    dictionary[line[name]][solution_key] = line[time]
                else:
                    dictionary[line[name]][solution_key] = "over 30s"


def parse_results():
    for result_folder in result_folders:
        parse_result(base_result_folder + '/' + result_folder)

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

def write_speed_up_table_to_csv_file():
    with open(base_result_folder + '/' + output_file_gpu_vs_cpu, 'w') as f:
        f.write("test,nodes,edges,terminals,gpu_results,cpu_results,speed_up\n")
        for (key, value) in dictionary.items():
            if value['cpu_results'] == 'over 30s':
                f.write(key+','+value["nodes"]+','+value["edges"]+','+value["terminals"]+','+value["gpu_results"]+','+value['cpu_results']+',a lot\n')
            else:
                f.write(key+','+value["nodes"]+','+value["edges"]+','+value["terminals"]+','+value["gpu_results"]+','+value['cpu_results']+','+str((float(value['cpu_results'])+0.00001)/(float(value['gpu_results'])+0.00001))+'\n')

parse_results()
write_table_to_csv_file()
write_gpu_better_table_to_csv_file()
write_speed_up_table_to_csv_file()
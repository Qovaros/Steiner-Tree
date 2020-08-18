import os

def parse_result(base_result_folder, result_folder, dictionary):
    solution_key = result_folder
    for file_name in sorted(os.listdir(base_result_folder + '/' + result_folder)):
        with open(base_result_folder + '/' + result_folder + '/' + file_name, 'r') as f:
            firstLine = f.readline().split('\n')[0].split(',')
            name = firstLine.index('name')
            nodes = firstLine.index('nodes')
            edges = firstLine.index('edges')
            terminals = firstLine.index('terminals')
            time = firstLine.index('time')
            for line in [l.split('\n')[0].split(',') for l in f.readlines()]:
                if line[name] not in dictionary:
                    dictionary[line[name]] = {"name": file_name[:-4], "nodes": int(line[nodes]), "edges": int(line[edges]), "terminals": int(line[terminals])}
                if len(line) == len(firstLine):
                    dictionary[line[name]][solution_key] = line[time]
                else:
                    dictionary[line[name]][solution_key] = "over 30s"


def parse_results(base_result_folder, result_folders):
    dictionary = {}
    for result_folder in result_folders:
        parse_result(base_result_folder, result_folder, dictionary)
    return dictionary
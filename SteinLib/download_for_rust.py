import requests
import tarfile
import os
import urllib
from bs4 import BeautifulSoup
import requests

test_url = 'http://steinlib.zib.de/download/{}.tgz'
solution_url = 'http://steinlib.zib.de/showset.php?{}'
target_path = 'test.tar.gz'
test_folder_name = 'test/'
test_names = []
# test_names = ['B', 'C', 'D', 'E', 'SP', 'PUC', 'I080', 'I160', 'I320', 'I640', 'P4Z', 'P6E', 'P6Z', 'DIW', 'DMXA', 'GAP', 'MSM', 'TAQ', 'LIN', 'ES10FST', 'ES20FST']
max_terminal_number = 20
max_node_number = 1500

def get_solutions(url):
    html = requests.get(url).text
    table_rows = BeautifulSoup(html, "lxml").find("table").find_all("tr")

    solutions = []
    for tr in table_rows:
        for td in tr.find_all("td", attrs={"bgcolor": "#FFFF00"}):
            if td.getText() == '----\xa0':
                solutions.append(0)
            else:
                solutions.append(int(td.getText()))

    return solutions


def download_tests(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(target_path, 'wb') as f:
            f.write(response.raw.read())

    tar = tarfile.open(target_path, "r:gz")
    tar.extractall()
    tar.close()
    os.remove(target_path)


def delete_bigger_tests(name, solutions):
    if not os.path.exists(test_folder_name + name):
        os.makedirs(test_folder_name + name)

    filtered_files = [file for file in os.listdir(name) if file.endswith(".crd") or file.endswith(".grp") ]
    for file in filtered_files:
	    os.remove(os.path.join(name, file))
    
    for file_name, solution in zip(sorted(os.listdir(name)), solutions):
        print(file_name, solution)
        edges, terminals, nodes = [], [], 0
        with open(name + '/' + file_name, 'r') as f:
            for line in f.readlines():
                line = line.split()
                if len(line) > 0:
                    if line[0] == 'Nodes':
                        nodes = line[1]
                    if line[0] == 'E':
                        edges.append(line[1:4])
                    if line[0] == 'T':
                        terminals.append(line[1])
        if len(terminals) > max_terminal_number or int(nodes) > max_node_number:
            os.remove(name + '/' + file_name)

def download_dataset(name):
    solutions = get_solutions(solution_url.format(name))
    download_tests(test_url.format(name))
    delete_bigger_tests(name, solutions)


for name in test_names:
    download_dataset(name)

download_tests("http://steinlib.zib.de/download/P4E/P4E.tgz")
solutions = get_solutions("http://steinlib.zib.de/showset.php?P4E")
delete_bigger_tests("P4E", solutions)


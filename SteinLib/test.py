import os
import sys
import subprocess

program_name = sys.argv[1]
test_folder = sys.argv[2]
result_folder = sys.argv[3]

for directory in os.listdir(test_folder):
    os.system('echo name,nodes,edges,terminals,distances time, copy time, dreyfus-wagner time,time,result >> ' + result_folder + '/' + directory + '.csv ')
    for f in sorted(os.listdir(test_folder + '/' + directory)):
        print(f)
        os.system("echo -n " + f.split(".")[0] + ', >> ' + result_folder + '/' + directory + '.csv ')
        result = os.system("timeout 31s " + program_name + ' < ' + test_folder + '/' + directory + '/' + f + ' >> ' + result_folder + '/' + directory + '.csv')
        if result != 0:
            os.system('echo n/a,n/a,n/a,over 30s,n/a >> ' + result_folder + '/' + directory + '.csv ')

import os
import sys
import subprocess

program_name = sys.argv[1]
test_folder = 'test_preprocessing/'

for directory in os.listdir(test_folder):
    os.system('echo name,nodes,edges,terminals,distances time, copy time, dreyfus-wagner time,time,result >> results/' + directory + '.csv ')
    for f in sorted(os.listdir(test_folder + directory)):
        print(f)
        os.system("echo -n " + f.split(".")[0] + ', >> results/' + directory + '.csv ')
        result = os.system("timeout 31s " + program_name + ' < ' + test_folder + directory + '/' + f + ' >> results/' + directory + '.csv')
        if result != 0:
            os.system('echo n/a,n/a,n/a,over 30s,n/a >> results/' + directory + '.csv ')

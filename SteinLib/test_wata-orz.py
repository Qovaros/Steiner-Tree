import os
import sys
import subprocess

program_name = sys.argv[1]
test_folder = 'for_rust/'
destination_folder = 'test_preprocessing/'

if 'withoutPreprocessing' in program_name:
    for directory in os.listdir(test_folder):
        os.system('echo name,nodes,edges,terminals,time >> results/' + directory + '.csv ')
        for f in sorted(os.listdir(test_folder + directory)):
            print(f)
            os.system("echo -n " + f.split(".")[0] + ', >> results/' + directory + '.csv ')
            result = os.system("timeout 31s " + program_name + ' < ' + test_folder + directory + '/' + f + ' >> results/' + directory + '.csv ' + f)
            if result != 0:
                os.system('echo over 30s >> results/' + directory + '.csv ')

if 'withPreprocessing' in program_name:
    for directory in os.listdir(test_folder):
        os.system('echo name,nodes,edges,terminals,nodes\\\',edges\\\',terminals\\\',time,result >> results/' + directory + '.csv ')
        for f in sorted(os.listdir(test_folder + directory)):
            print(f)
            os.system("echo -n " + f.split(".")[0] + ', >> results/' + directory + '.csv ')
            result = os.system("timeout 30s " + program_name + ' < ' + test_folder + directory + '/' + f + ' >> results/' + directory + '.csv ' + f)
            if result != 0:
                os.system('echo over 30s,n/a >> results/' + directory + '.csv ')

if 'generateReduced' in program_name:
    for directory in os.listdir(test_folder):
        os.makedirs(destination_folder+directory)
        for f in sorted(os.listdir(test_folder+directory)):
            os.system(program_name + " < " + test_folder+directory+'/'+f+ " > " + destination_folder + directory + '/' + f)
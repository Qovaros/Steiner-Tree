import os
import sys

program_name = sys.argv[1]
test_folder = 'test/'

for directory in os.listdir(test_folder):
    for f in os.listdir(test_folder + directory):
        print(f)
        os.system(program_name + ' < ' + test_folder + directory + '/' + f)

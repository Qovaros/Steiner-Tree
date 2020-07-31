import os
import sys

program_name = sys.argv[1]
test_folder = 'for_rust/'

for directory in os.listdir(test_folder):
    for f in sorted(os.listdir(test_folder + directory)):
        print(f)
        os.system('echo - >> results/' + directory + '.out ')
        os.system("echo " + f + ' >> results/' + directory + '.out ')
        os.system(program_name + ' < ' + test_folder + directory + '/' + f + ' >> results/' + directory + '.out ' + f)
 
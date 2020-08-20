# Steiner-Tree
## Workflow:
### To run implementations of Dreyfus-Wagner:
  * Download test datasets by using `make test-dowload`
  * Test either GPU or CPU solution by running:
    * `make test-gpu`
    * `make test-cpu`
  * Results can be found in `results/program_results`

## Makefile commands:
### Compiling gpu program:
  * `make gpu`, `make gpu-release` - release
  * `make gpu-debug` - debug

### Compiling cpu program:
  * `make cpu`

### Testing:
  * `make test-download` - download dataset from SteinLib
  * `make test-gpu` - test gpu solution
  * `make test-cpu` - test cpu solution

### Cleaning:
  * `make clean` - clean after compilation process
  * `make clean-test` - clean all tests

### Showing results:
  * `make show-graphs` - shows graphs displaying results that can be found in `results/program_results`
  * `make generate-result-tables` - generates .csv tables based on results that can be found in `results/program_results`
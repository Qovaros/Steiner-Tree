CUDA_INSTALL_PATH ?= /usr/local/cuda
CC=g++
NV=$(CUDA_INSTALL_PATH)/bin/nvcc
LD=$(CUDA_INSTALL_PATH)/bin/nvcc
CCFLAGS=-Isrc -I$(CUDA_INSTALL_PATH)/include -std=c++14 -Wall
NVFLAGS=-Isrc -std=c++14 $(NVARCH) --compiler-options -Wall --resource-usage
NVFLAGSDEP=-Isrc -std=c++14 $(NVARCH)
LDFLAGS=$(NVARCH) -lcuda
gpu-debug : CCFLAGS += -g
gpu-release : CCFLAGS += -O3 -DNDEBUG
gpu-release : LDFLAGS += -O3
BASE_DIR=Dreyfus-Wagner
RESULTS_DIR=results/new
SRC_DIR:=$(BASE_DIR)/src
INT_DIR:=$(BASE_DIR)/build
INT_DIR_DEBUG:=$(INT_DIR)/debug
INT_DIR_RELEASE:=$(INT_DIR)/release
OUT_DIR=$(BASE_DIR)/bin
GPU_OUT_DIR=$(OUT_DIR)/gpu
CPU_OUT_DIR=$(OUT_DIR)/cpu
TEST_DIR=test
TARGET_DEBUG=programd
TARGET_RELEASE=program

SOURCES := $(shell find $(SRC_DIR) -name *.cpp)
CUSOURCES := $(shell find $(SRC_DIR) -name *.cu)
SRCDIRS := $(shell find $(SRC_DIR) -type d)

DIRS_DEBUG = $(SRCDIRS:$(SRC_DIR)%=$(INT_DIR_DEBUG)%)
DIRS_RELEASE = $(SRCDIRS:$(SRC_DIR)%=$(INT_DIR_RELEASE)%)

OBJS_DEBUG = $(SOURCES:$(SRC_DIR)/%.cpp=$(INT_DIR_DEBUG)/%.o)
OBJS_RELEASE = $(SOURCES:$(SRC_DIR)/%.cpp=$(INT_DIR_RELEASE)/%.o)
CUOBJS_DEBUG = $(CUSOURCES:$(SRC_DIR)/%.cu=$(INT_DIR_DEBUG)/%.cu.o)
CUOBJS_RELEASE = $(CUSOURCES:$(SRC_DIR)/%.cu=$(INT_DIR_RELEASE)/%.cu.o)
DEPS_DEBUG = $(SOURCES:$(SRC_DIR)/%.cpp=$(INT_DIR_DEBUG)/%.d)
DEPS_RELEASE = $(SOURCES:$(SRC_DIR)/%.cpp=$(INT_DIR_RELEASE)/%.d)
CUDEPS_DEBUG = $(CUSOURCES:$(SRC_DIR)/%.cu=$(INT_DIR_DEBUG)/%.cud)
CUDEPS_RELEASE = $(CUSOURCES:$(SRC_DIR)/%.cu=$(INT_DIR_RELEASE)/%.cud)


show-graphs:
	@mkdir -p $(RESULTS_DIR)/results
	python3 SteinLib/show_graphs.py results/program_results

generate-result-tables:
	@mkdir -p $(RESULTS_DIR)/summaries
	python3 SteinLib/generate_time_result_tables.py results/program_results $(RESULTS_DIR)/summaries

gpu: gpu-release

gpu-debug: $(GPU_OUT_DIR)/$(TARGET_DEBUG)

gpu-release: $(GPU_OUT_DIR)/$(TARGET_RELEASE)

cpu: $(CPU_OUT_DIR)/$(TARGET_RELEASE)

test-cpu: $(CPU_OUT_DIR)/$(TARGET_RELEASE)
	rm -rf $(RESULTS_DIR)/program_results/cpu_results
	@mkdir -p $(RESULTS_DIR)/program_results/cpu_results
	python3 SteinLib/test.py $(BASE_DIR)/bin/cpu/program $(TEST_DIR) $(RESULTS_DIR)/program_results/cpu_results

test-gpu: $(GPU_OUT_DIR)/$(TARGET_RELEASE)
	rm -rf $(RESULTS_DIR)/program_results/gpu_results
	@mkdir -p $(RESULTS_DIR)/program_results/gpu_results
	python3 SteinLib/test.py $(BASE_DIR)/bin/gpu/program $(TEST_DIR) $(RESULTS_DIR)/program_results/gpu_results

test-download:
	python3 SteinLib/download.py

$(CPU_OUT_DIR)/$(TARGET_RELEASE) : Dreyfus-Wagner/cpp/dreyfus-wagner.cpp | $(CPU_OUT_DIR)
	echo $^
	echo $(CCFLAGS)
	echo $@
	$(CC) $^ $(CCFLAGS) -o $@

$(GPU_OUT_DIR)/$(TARGET_DEBUG) : $(OBJS_DEBUG) $(CUOBJS_DEBUG) | $(DIRS_DEBUG) $(GPU_OUT_DIR)
	$(LD) $^ $(LDFLAGS) -o $@

$(GPU_OUT_DIR)/$(TARGET_RELEASE) : $(OBJS_RELEASE) $(CUOBJS_RELEASE) | $(DIRS_RELEASE) $(GPU_OUT_DIR)
	$(LD) $^ $(LDFLAGS) -o $@

$(INT_DIR_DEBUG)/%.o : $(SRC_DIR)/%.cpp $(INT_DIR_DEBUG)/%.d | $(DIRS_DEBUG)
	$(CC) $< $(CCFLAGS) -c -o $@

$(INT_DIR_RELEASE)/%.o : $(SRC_DIR)/%.cpp $(INT_DIR_RELEASE)/%.d | $(DIRS_RELEASE)
	$(CC) $< $(CCFLAGS) -c -o $@

$(INT_DIR_DEBUG)/%.cu.o : $(SRC_DIR)/%.cu $(INT_DIR_DEBUG)/%.cud | $(DIRS_DEBUG)
	$(NV) $< $(NVFLAGS) -c -o $@

$(INT_DIR_RELEASE)/%.cu.o : $(SRC_DIR)/%.cu $(INT_DIR_RELEASE)/%.cud | $(DIRS_RELEASE)
	$(NV) $< $(NVFLAGS) -c -o $@

$(INT_DIR_DEBUG)/%.d : $(SRC_DIR)/%.cpp | $(DIRS_DEBUG)
	@$(CC) $(CCFLAGS) $< -MM -MP |\
		sed 's=\($(*F)\)\.o[ :]*=$(@D)/\1.o $@ : =g;'\
		> $@

$(INT_DIR_RELEASE)/%.d : $(SRC_DIR)/%.cpp | $(DIRS_RELEASE)
	@$(CC) $(CCFLAGS) $< -MM -MP |\
		sed 's=\($(*F)\)\.o[ :]*=$(@D)/\1.o $@ : =g;'\
		> $@

$(INT_DIR_DEBUG)/%.cud : $(SRC_DIR)/%.cu | $(DIRS_DEBUG)
	@$(NV) $(NVFLAGSDEP) $< -M |\
		sed 's=\($(*F)\)\.o[ :]*=$(@D)/\1.o $@ : =g;'\
		> $@

$(INT_DIR_RELEASE)/%.cud : $(SRC_DIR)/%.cu | $(DIRS_RELEASE)
	@$(NV) $(NVFLAGSDEP) $< -M |\
		sed 's=\($(*F)\)\.o[ :]*=$(@D)/\1.o $@ : =g;'\
		> $@

$(DIRS_DEBUG) $(DIRS_RELEASE) $(GPU_OUT_DIR) $(CPU_OUT_DIR) $(TEST_DIR) $(RESULTS_DIR):
	@mkdir -p $@

clean:
	@rm -rf $(INT_DIR_DEBUG)
	@rm -rf $(INT_DIR_RELEASE)
	@rm -rf $(INT_DIR)
	@rm -rf $(OUT_DIR)
	@rm -rf $(TEST_DIR)
	@rm -rf $(RESULTS_DIR)

clean-test:
	@rm -rf $(TEST_DIR)

.PHONY: all debug release clean
.SECONDARY: $(OBJS_DEBUG) $(OBJS_RELEASE) $(CUOBJS_DEBUG) $(CUOBJS_RELEASE) $(DEPS_DEBUG) $(DEPS_RELEASE) $(CUDEPS_DEBUG) $(CUDEPS_RELEASE)

-include $(DEPS) $(CUDEPS)


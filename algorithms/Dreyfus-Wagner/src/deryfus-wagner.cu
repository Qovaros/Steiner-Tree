#include "common.h"
#include "dreyfus-wagner.h"
#include <chrono>
#include <iostream>
#include <stdint.h>
#include <vector>
// #include <curand.h>
// #include <curand_kernel.h>
// #include <cuda.h>

// #define gpuErrchk(ans) { gpuAssert((ans), __FILE__, __LINE__); }

// inline void gpuAssert(cudaError_t code, const char *file, int line, bool
// abort = true) {
//     if (code != cudaSuccess) {
//         fprintf(stderr, "GPUassert: %s %s %d\n", cudaGetErrorString(code),
//         file, line); if (abort) exit(code);
//     }
// }

static int hostTable[(int)1e8];
static const int INF = 1e9;
static const int BLOCK_NUMBER = 10;

static __global__ void dreyfusWagnerFirstStep(const int *distances,
                                              int *dynamicTable,
                                              const int nodes, const int mask) {
    int nodeIndex = blockDim.x * blockIdx.x + threadIdx.x, tmp;
    if (nodeIndex >= nodes)
        return;

    for (int subMask = (mask - 1) & mask; subMask;
         subMask = (subMask - 1) & mask) {
        tmp = dynamicTable[subMask * nodes + nodeIndex] +
              dynamicTable[(mask ^ subMask) * nodes + nodeIndex];
        dynamicTable[mask * nodes + nodeIndex] =
            tmp < dynamicTable[mask * nodes + nodeIndex]
                ? tmp
                : dynamicTable[mask * nodes + nodeIndex];
    }
}

static __global__ void dreyfusWagnerSecondStep(const int *distances,
                                               int *dynamicTable,
                                               const int nodes,
                                               const int mask) {
    int nodeIndex = blockDim.x * blockIdx.x + threadIdx.x, tmp;
    if (nodeIndex >= nodes)
        return;

    for (int node2 = 0; node2 < nodes; node2++) {
        tmp = dynamicTable[mask * nodes + node2] +
              distances[nodeIndex * nodes + node2];
        dynamicTable[mask * nodes + nodeIndex] =
            tmp < dynamicTable[mask * nodes + nodeIndex]
                ? tmp
                : dynamicTable[mask * nodes + nodeIndex];
    }
}

static int *
copyDistancesToDevice(const std::vector<std::vector<int>> &distances) {
    for (int i = 0; i < distances.size(); i++) {
        for (int j = 0; j < distances.size(); j++) {
            hostTable[i * distances.size() + j] = distances[i][j];
        }
    }

    int *cudaDistances;
    cudaMalloc(&cudaDistances,
               distances.size() * distances.size() * sizeof(int));

    cudaMemcpy(cudaDistances, hostTable,
               distances.size() * distances.size() * sizeof(int),
               cudaMemcpyHostToDevice);

    return cudaDistances;
}

static __global__ void fillDynamicTable(const int *distances, int *dynamicTable,
                                        const int nodes, const int mask) {
    int nodeIndex = blockDim.x * blockIdx.x + threadIdx.x, tmp;
    if (nodeIndex >= nodes)
        return;

    for (int node2 = 0; node2 < nodes; node2++) {
        tmp = dynamicTable[mask * nodes + node2] +
              distances[nodeIndex * nodes + node2];
        dynamicTable[mask * nodes + nodeIndex] =
            tmp < dynamicTable[mask * nodes + nodeIndex]
                ? tmp
                : dynamicTable[mask * nodes + nodeIndex];
    }
}

static int *
copyDynamicTableToDevice(const std::vector<std::vector<int>> &distances,
                         const std::vector<int> &terminals,
                         const int &fullMask) {
    for (int i = 0; i < (fullMask + 1); i++) {
        for (int j = 0; j < distances.size(); j++) {
            hostTable[i * distances.size() + j] = INF;
        }
    }
    for (int i = 0; i < terminals.size() - 1; i++) {
        hostTable[(1 << i) * distances.size() + terminals[i]] = 0;
    }

    int *cudaDynamicTable;
    cudaMalloc(&cudaDynamicTable,
               (fullMask + 1) * distances.size() * sizeof(int));

    cudaMemcpy(cudaDynamicTable, hostTable,
               (fullMask + 1) * distances.size() * sizeof(int),
               cudaMemcpyHostToDevice);

    return cudaDynamicTable;
}

DreyfusWagnerStatistics
dreyfusWagner(std::vector<std::vector<int>> &distances,
              const std::vector<std::vector<std::pair<int, int>>> &graph,
              const std::vector<int> &terminals) {
    cudaFree(NULL);
    DreyfusWagnerStatistics statistics = {0, 0, 0, 0, 0};
    if (terminals.size() <= 1) {
        return statistics;
    }
    const int fullMask = (1 << (terminals.size() - 1)) - 1;
    int block_size = distances.size() / BLOCK_NUMBER + 1;

    auto beforeFloydWarshall = std::chrono::steady_clock::now();
    compouteDistances(distances, graph);
    auto afterFloydWarshall = std::chrono::steady_clock::now();
    statistics.distancesDuration =
        std::chrono::duration_cast<std::chrono::milliseconds>(
            afterFloydWarshall - beforeFloydWarshall)
            .count();

    auto beforeCopy = std::chrono::steady_clock::now();
    int *cudaDistances = copyDistancesToDevice(distances);
    int *cudaDynamicTable =
        copyDynamicTableToDevice(distances, terminals, fullMask);
    auto afterCopy = std::chrono::steady_clock::now();
    statistics.copyDuration =
        std::chrono::duration_cast<std::chrono::milliseconds>(afterCopy -
                                                              beforeCopy)
            .count();
    for (int mask = 1; mask <= fullMask; mask++) {
        dreyfusWagnerFirstStep<<<BLOCK_NUMBER, block_size>>>(
            cudaDistances, cudaDynamicTable, distances.size(), mask);
        dreyfusWagnerSecondStep<<<BLOCK_NUMBER, block_size>>>(
            cudaDistances, cudaDynamicTable, distances.size(), mask);
    }
    auto end = std::chrono::steady_clock::now();
    statistics.dreyfusWagnerDuration =
        std::chrono::duration_cast<std::chrono::milliseconds>(end - afterCopy)
            .count();
    statistics.everythingDuration =
        std::chrono::duration_cast<std::chrono::milliseconds>(
            end - beforeFloydWarshall)
            .count();
    cudaMemcpy(&statistics.result,
               cudaDynamicTable +
                   (fullMask * distances.size() + terminals.back()),
               1 * sizeof(int), cudaMemcpyDeviceToHost);

    cudaFree(cudaDistances);
    cudaFree(cudaDynamicTable);

    return statistics;
}

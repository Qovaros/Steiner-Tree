#include "common.h"
#include "dreyfus-wagner.h"
#include <chrono>
#include <iostream>
#include <stdint.h>
#include <vector>

static int hostTable[(int)1e8];
static const int INF = 1e9;
static const int MAX_THREADS = 1024;

static __global__ void dreyfusWagnerFirstStep(const int *distances,
                                              int *dynamicTable, int *masks,
                                              const int nodes,
                                              const int masksStart,
                                              const int masksEnd) {
    int maskIndex = threadIdx.x, nodeIndex = blockIdx.x, tmp;
    if (maskIndex >= masksEnd - masksStart)
        return;
    int mask = masks[masksStart + maskIndex];
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
                                               int *dynamicTable, int *masks,
                                               const int nodes,
                                               const int masksStart,
                                               const int masksEnd) {
    int maskIndex = threadIdx.x, nodeIndex = blockIdx.x, tmp;
    if (maskIndex >= masksEnd - masksStart)
        return;
    int mask = masks[masksStart + maskIndex];
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

static int *copyMasksToDevice(const int &terminals, const int &fullMask,
                              std::vector<int> &masksBeginings) {
    std::vector<std::vector<int>> masks(terminals);

    for (int mask = 1; mask <= fullMask; mask++) {
        masks[__builtin_popcount(mask) - 1].push_back(mask);
    }

    int *cudaMasksTable;
    cudaMalloc(&cudaMasksTable, (fullMask + 1) * sizeof(int));
    for (int i = 0, j = 0; i < masks.size(); j += masks[i].size(), i++) {
        masksBeginings.push_back(j);
        cudaMemcpy(cudaMasksTable + j, &masks[i][0],
                   masks[i].size() * sizeof(int), cudaMemcpyHostToDevice);
    }
    masksBeginings.push_back(
        masksBeginings[masksBeginings.size() - 1] +
        masks[masks.size() - 1].size()); // could be just +1

    return cudaMasksTable;
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
    std::vector<int> masksBeginings;

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
    int *cudaMasksTable =
        copyMasksToDevice(terminals.size() - 1, fullMask, masksBeginings);
    auto afterCopy = std::chrono::steady_clock::now();
    statistics.copyDuration =
        std::chrono::duration_cast<std::chrono::milliseconds>(afterCopy -
                                                              beforeCopy)
            .count();
    for (int maskSize = 1; maskSize < masksBeginings.size(); maskSize++) {
        for (int i = 0, block_size;
             i < masksBeginings[maskSize] - masksBeginings[maskSize - 1];
             i += MAX_THREADS) {
            block_size = std::min(
                (masksBeginings[maskSize] - masksBeginings[maskSize - 1] - i),
                MAX_THREADS);
            dreyfusWagnerFirstStep<<<distances.size(), block_size>>>(
                cudaDistances, cudaDynamicTable, cudaMasksTable,
                distances.size(), masksBeginings[maskSize - 1] + i,
                masksBeginings[maskSize] + i);
            dreyfusWagnerSecondStep<<<distances.size(), block_size>>>(
                cudaDistances, cudaDynamicTable, cudaMasksTable,
                distances.size(), masksBeginings[maskSize - 1] + i,
                masksBeginings[maskSize] + i);
        }
    }
    cudaMemcpy(&statistics.result,
               cudaDynamicTable +
                   (fullMask * distances.size() + terminals.back()),
               1 * sizeof(int), cudaMemcpyDeviceToHost);
    auto end = std::chrono::steady_clock::now();
    statistics.dreyfusWagnerDuration =
        std::chrono::duration_cast<std::chrono::milliseconds>(end - afterCopy)
            .count();
    statistics.everythingDuration =
        std::chrono::duration_cast<std::chrono::milliseconds>(
            end - beforeFloydWarshall)
            .count();
    cudaFree(cudaDistances);
    cudaFree(cudaDynamicTable);
    cudaFree(cudaMasksTable);
    return statistics;
}

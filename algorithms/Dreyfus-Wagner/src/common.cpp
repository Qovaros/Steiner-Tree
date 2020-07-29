#ifndef COMMON_CPP
#define COMMON_CPP

#include "common.h"
#include <fstream>
#include <iostream>
#include <vector>

static int INF = 1e9;

void floydWarshall(std::vector<std::vector<int>> &distances) {
    const int numberOfNodes = distances.size();
    for (int k = 0; k < numberOfNodes; k++) {
        for (int i = 0; i < numberOfNodes; i++) {
            for (int j = 0; j < numberOfNodes; j++) {
                distances[i][j] = std::min(distances[i][j],
                                           distances[i][k] + distances[k][j]);
            }
        }
    }
}

int readGraph(char *fileName, std::vector<std::vector<int>> &distances,
              std::vector<int> &terminals) {
    int numberOfNodes, numberOfEdges, numberOfTerminals, result;

    std::ifstream file(fileName);
    file >> numberOfNodes >> numberOfEdges;

    distances.resize(numberOfNodes);
    for (int i = 0; i < numberOfNodes; i++) {
        distances[i].resize(numberOfNodes, INF);
        distances[i][i] = 0;
    }

    while (numberOfEdges--) {
        int from, to, weight;
        file >> from >> to >> weight;
        distances[from - 1][to - 1] = weight;
        distances[to - 1][from - 1] = weight;
    }

    file >> numberOfTerminals;
    terminals.resize(numberOfTerminals);
    for (int &terminal : terminals) {
        file >> terminal;
        terminal--;
    }

    file >> result;
    return result;
}

#endif // COMMON_CPP

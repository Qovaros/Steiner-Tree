#ifndef COMMON_H
#define COMMON_H

#include <iostream>
#include <vector>

static int INF = 1e9;

int readGraph(std::vector<std::vector<int>> &distances,
              std::vector<int> &terminals) {
    int numberOfNodes, numberOfEdges, numberOfTerminals, result;
    std::cin >> numberOfNodes >> numberOfEdges;

    distances.resize(numberOfNodes);
    for (int i = 0; i < numberOfNodes; i++) {
        distances[i].resize(numberOfNodes, INF);
        distances[i][i] = 0;
    }

    while (numberOfEdges--) {
        int from, to, weight;
        std::cin >> from >> to >> weight;
        distances[from - 1][to - 1] = weight;
        distances[to - 1][from - 1] = weight;
    }
    for (int k = 0; k < numberOfNodes; k++) {
        for (int i = 0; i < numberOfNodes; i++) {
            for (int j = 0; j < numberOfNodes; j++) {
                distances[i][j] = std::min(distances[i][j],
                                           distances[i][k] + distances[k][j]);
            }
        }
    }

    std::cin >> numberOfTerminals;
    terminals.resize(numberOfTerminals);
    for (int &terminal : terminals) {
        std::cin >> terminal;
        terminal--;
    }

    std::cin >> result;
    return result;
}

#endif // COMMON_H

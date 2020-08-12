#ifndef COMMON_CPP
#define COMMON_CPP

#include "common.h"
#include <cmath>
#include <fstream>
#include <iostream>
#include <queue>
#include <vector>

static int INF = 1e9;

void dijkstra(const int &start, std::vector<std::vector<int>> &distances,
              const std::vector<std::vector<std::pair<int, int>>> &graph) {
    std::vector<bool> visited(distances.size());
    auto cmp = [](const std::pair<int, int> &left,
                  const std::pair<int, int> &right) {
        return (left.second > right.second);
    };
    std::priority_queue<std::pair<int, int>, std::vector<std::pair<int, int>>,
                        decltype(cmp)>
        que(cmp);
    que.push({start, 0});
    while (!que.empty()) {
        std::pair<int, int> current = que.top();
        que.pop();
        if (!visited[current.first]) {
            distances[start][current.first] = current.second;
            visited[current.first] = true;
            for (const std::pair<int, int> &i : graph[current.first]) {
                int dist = current.second + i.second;
                if (!visited[i.first] && dist < distances[start][i.first]) {
                    distances[start][i.first] = dist;
                    que.push({i.first, dist});
                }
            }
        }
    }
}

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

void compouteDistances(
    std::vector<std::vector<int>> &distances,
    const std::vector<std::vector<std::pair<int, int>>> &graph) {
    const int numberOfNodes = distances.size();
    for (int k = 0; k < numberOfNodes; k++) {
        dijkstra(k, distances, graph);
    }
}

int readGraph(std::vector<std::vector<int>> &distances,
              std::vector<std::vector<std::pair<int, int>>> &graph,
              std::vector<int> &terminals, int &numberOfEdges) {
    int numberOfNodes, numberOfTerminals, result;

    std::cin >> numberOfNodes >> numberOfEdges;

    distances.resize(numberOfNodes);
    for (int i = 0; i < numberOfNodes; i++) {
        distances[i].resize(numberOfNodes, INF);
        distances[i][i] = 0;
    }
    graph.resize(numberOfNodes);

    for (int i = 0; i < numberOfEdges; i++) {
        int from, to, weight;
        std::cin >> from >> to >> weight;
        graph[from - 1].push_back({to - 1, weight});
        graph[to - 1].push_back({from - 1, weight});
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

#endif // COMMON_CPP

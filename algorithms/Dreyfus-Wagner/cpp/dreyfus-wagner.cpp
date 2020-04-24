#include <iostream>
#include <vector>
#include <chrono>

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


int dreyfusWagner(const std::vector<std::vector<int>> &distances,
                  const std::vector<int> &terminals) {
    if (terminals.size() <= 1) {
        return 0;
    }
    const int fullMask = (1 << (terminals.size() - 1)) - 1;

    std::vector<std::vector<int>> dynamicTable(fullMask + 1);
    for (std::vector<int> &v : dynamicTable) {
        v.resize(distances.size(), INF);
    }
    for (int i = 0; i < terminals.size() - 1; i++) {
        dynamicTable[(1 << i)][terminals[i]] = 0;
    }
    for (int &i : dynamicTable[0]) {
        i = 0;
    }

    for (int mask = 1; mask <= fullMask; mask++) {
        for (int node = 0; node < distances.size(); node++) {
            for (int subMask = (mask - 1) & mask; subMask;
                 subMask = (subMask - 1) & mask) {
                dynamicTable[mask][node] =
                    std::min(dynamicTable[mask][node],
                             dynamicTable[subMask][node] +
                                 dynamicTable[mask ^ subMask][node]);
            }
        }
        for (int node1 = 0; node1 < distances.size(); node1++) {
            for (int node2 = 0; node2 < distances.size(); node2++) {
                dynamicTable[mask][node1] = std::min(
                    dynamicTable[mask][node1],
                    dynamicTable[mask][node2] + distances[node1][node2]);
            }
        }
    }
    return dynamicTable[fullMask][terminals.back()];
}

int main() {
    int z = 1;
    // std::cin >> z;
    while (z--) {
        std::vector<std::vector<int>> distances;
        std::vector<int> terminals;
        int realResult = readGraph(distances, terminals);
        auto start = std::chrono::steady_clock::now();
        int programResult = dreyfusWagner(distances, terminals);
        auto stop = std::chrono::steady_clock::now();
        if (realResult == programResult) {
            std::cout << "Correct " << realResult << std::endl;
        } else {
            std::cout << "Wrong. Should be: " << realResult
                      << ", got: " << programResult << " instead" << std::endl;
        }
        std::cout << "Time: "
                  << std::chrono::duration_cast<std::chrono::milliseconds>(
                         stop - start)
                         .count()
                  << std::endl;

    }
}
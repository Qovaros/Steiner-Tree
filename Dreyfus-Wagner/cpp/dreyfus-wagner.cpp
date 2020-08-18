#include <chrono>
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

class DreyfusWagnerStatistics {
  public:
    float distancesDuration;
    float copyDuration;
    float dreyfusWagnerDuration;
    float everythingDuration;
    int result;
};

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

DreyfusWagnerStatistics
dreyfusWagner(std::vector<std::vector<int>> &distances,
              std::vector<std::vector<std::pair<int, int>>> &graph,
              const std::vector<int> &terminals) {

    DreyfusWagnerStatistics statistics = {0.0, 0.0, 0.0, 0.0, 0};
    if (terminals.size() <= 1) {
        return statistics;
    }
    const int fullMask = (1 << (terminals.size() - 1)) - 1;

    auto beforeFloydWarshall = std::chrono::steady_clock::now();
    compouteDistances(distances, graph);
    auto afterFloydWarshall = std::chrono::steady_clock::now();
    statistics.distancesDuration =
        std::chrono::duration_cast<std::chrono::milliseconds>(
            afterFloydWarshall - beforeFloydWarshall)
            .count();

    auto beforeCopy = std::chrono::steady_clock::now();
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
    auto afterCopy = std::chrono::steady_clock::now();
    statistics.copyDuration =
        std::chrono::duration_cast<std::chrono::milliseconds>(afterCopy -
                                                              beforeCopy)
            .count();
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
    auto end = std::chrono::steady_clock::now();
    statistics.dreyfusWagnerDuration =
        std::chrono::duration_cast<std::chrono::milliseconds>(end - afterCopy)
            .count();
    statistics.everythingDuration =
        std::chrono::duration_cast<std::chrono::milliseconds>(
            end - beforeFloydWarshall)
            .count();
    statistics.result = dynamicTable[fullMask][terminals.back()];
    return statistics;
}

int main(int argc, char *argv[]) {
    std::vector<std::vector<std::pair<int, int>>> graph;
    std::vector<std::vector<int>> distances;
    std::vector<int> terminals;
    int numberOfEdges;

    auto beforeRead = std::chrono::steady_clock::now();
    int realResult = readGraph(distances, graph, terminals, numberOfEdges);
    auto afterRead = std::chrono::steady_clock::now();
    std::cout << distances.size() << ',' << numberOfEdges << ","
              << terminals.size() << ',' << std::flush;
    DreyfusWagnerStatistics stats = dreyfusWagner(distances, graph, terminals);
    std::cout << stats.distancesDuration / 1000 << ","
              << stats.copyDuration / 1000 << ","
              << stats.dreyfusWagnerDuration / 1000 << ","
              << stats.everythingDuration / 1000 << ',';
    if (realResult == stats.result) {
        std::cout << stats.result << std::endl;
    } else {
        std::cout << "incorrect" << std::endl;
    }
}
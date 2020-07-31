#include <chrono>
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

class DreyfusWagnerStatistics {
  public:
    int distancesDuration;
    int copyDuration;
    int firstPhaseDuration;
    int secondPhaseDuration;
    int everythingDuration;
    int result;
};

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

DreyfusWagnerStatistics dreyfusWagner(std::vector<std::vector<int>> &distances,
                                      const std::vector<int> &terminals) {

    DreyfusWagnerStatistics statistics = {0, 0, 0, 0, 0, 0};
    if (terminals.size() <= 1) {
        return statistics;
    }
    const int fullMask = (1 << (terminals.size() - 1)) - 1;

    auto beforeFloydWarshall = std::chrono::steady_clock::now();
    floydWarshall(distances);
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
    std::chrono::nanoseconds firstPhase(0), secondPhase(0);
    for (int mask = 1; mask <= fullMask; mask++) {
        auto beforeFirstStep = std::chrono::steady_clock::now();

        for (int node = 0; node < distances.size(); node++) {
            for (int subMask = (mask - 1) & mask; subMask;
                 subMask = (subMask - 1) & mask) {
                dynamicTable[mask][node] =
                    std::min(dynamicTable[mask][node],
                             dynamicTable[subMask][node] +
                                 dynamicTable[mask ^ subMask][node]);
            }
        }
        auto afterFirstStep = std::chrono::steady_clock::now();
        for (int node1 = 0; node1 < distances.size(); node1++) {
            for (int node2 = 0; node2 < distances.size(); node2++) {
                dynamicTable[mask][node1] = std::min(
                    dynamicTable[mask][node1],
                    dynamicTable[mask][node2] + distances[node1][node2]);
            }
        }
        auto afterSecondStep = std::chrono::steady_clock::now();
        firstPhase += std::chrono::duration_cast<std::chrono::nanoseconds>(
            afterFirstStep - beforeFirstStep);
        secondPhase += std::chrono::duration_cast<std::chrono::nanoseconds>(
            afterSecondStep - afterFirstStep);
    }
    auto end = std::chrono::steady_clock::now();
    statistics.firstPhaseDuration =
        std::chrono::duration_cast<std::chrono::microseconds>(firstPhase)
            .count();
    statistics.secondPhaseDuration =
        std::chrono::duration_cast<std::chrono::microseconds>(secondPhase)
            .count();
    statistics.everythingDuration =
        std::chrono::duration_cast<std::chrono::milliseconds>(
            end - beforeFloydWarshall)
            .count();
    statistics.result = dynamicTable[fullMask][terminals.back()];
    return statistics;
}

int main(int argc, char *argv[]) {
    if (argc < 4) {
        std::cout << "Not enough arguments. Please provide test file path "
                     "output file path and "
                     "test type name."
                  << std::endl;
        return 1;
    }
    std::ofstream outputFile(argv[2], std::fstream::app);
    std::vector<std::vector<int>> distances;
    std::vector<int> terminals;

    auto beforeRead = std::chrono::steady_clock::now();
    int realResult = readGraph(argv[1], distances, terminals);
    auto afterRead = std::chrono::steady_clock::now();
    DreyfusWagnerStatistics stats = dreyfusWagner(distances, terminals);
    if (realResult != stats.result) {
        std::cout << argv[3] << " Wrong. Should be: " << realResult
                  << ", got: " << stats.result << " instead" << std::endl;
        outputFile << argv[3] << " Wrong. Should be: " << realResult
                   << ", got: " << stats.result << " instead" << std::endl;
        return 1;
    }
    std::cout << argv[3] << " Correct " << realResult << " took "
              << stats.everythingDuration << " ms\n";
    outputFile << "-\n"
               << argv[3] << " Correct " << realResult << "\n"
               << distances.size() << " node number\n"
               << terminals.size() << " terminal number\n"
               << std::chrono::duration_cast<std::chrono::milliseconds>(
                      afterRead - beforeRead)
                      .count()
               << " ms graph read\n"
               << stats.distancesDuration << " ms distances duration\n"
               << stats.copyDuration << " ms copy duration\n"
               << stats.firstPhaseDuration << " us first phase duration\n"
               << stats.secondPhaseDuration << " us second phase duration\n"
               << stats.everythingDuration << " ms everything" << std::endl;
}
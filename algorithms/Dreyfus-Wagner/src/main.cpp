#include "common.h"
#include "dreyfus-wagner.h"
#include <chrono>
#include <fstream>
#include <iostream>
#include <vector>

int main(int argc, char *argv[]) {
    std::vector<std::vector<std::pair<int, int>>> graph;
    std::vector<std::vector<int>> distances;
    std::vector<int> terminals;
    int numberOfEdges;

    int realResult = readGraph(distances, graph, terminals, numberOfEdges);

    std::cout << distances.size() << ',' << numberOfEdges << ","
              << terminals.size() << ',' << std::flush;

    DreyfusWagnerStatistics stats =
        dreyfusWagner(distances, graph, terminals);

    std::cout << stats.distancesDuration / 1000 << ","
              << stats.copyDuration / 1000 << ","
              << stats.dreyfusWagnerDuration / 1000 << ","
              << stats.everythingDuration / 1000 << ",";
    if (realResult == stats.result) {
        std::cout << stats.result << std::endl;
    } else {
        std::cout << "incorrect" << std::endl;
    }
    return 0;
}
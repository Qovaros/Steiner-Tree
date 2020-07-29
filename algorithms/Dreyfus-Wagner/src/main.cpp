#include "common.h"
#include "dreyfus-wagner.h"
#include <chrono>
#include <fstream>
#include <iostream>
#include <vector>

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
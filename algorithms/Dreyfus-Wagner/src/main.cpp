#include "dreyfus-wagner.h"
#include "common.h"
#include <iostream>
#include <vector>
#include <chrono>

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
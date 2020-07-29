#ifndef COMMON_H
#define COMMON_H

#include <vector>

void floydWarshall(std::vector<std::vector<int>> &distances);

int readGraph(char *fileName, std::vector<std::vector<int>> &distances,
              std::vector<int> &terminals);

class DreyfusWagnerStatistics {
  public:
    int distancesDuration;
    int copyDuration;
    int firstPhaseDuration;
    int secondPhaseDuration;
    int everythingDuration;
    int result;
};

#endif // COMMON_H

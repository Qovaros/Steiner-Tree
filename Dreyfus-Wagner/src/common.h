#ifndef COMMON_H
#define COMMON_H

#include <vector>

void compouteDistances(
    std::vector<std::vector<int>> &distances,
    const std::vector<std::vector<std::pair<int, int>>> &graph);

int readGraph(std::vector<std::vector<int>> &distances,
              std::vector<std::vector<std::pair<int, int>>> &graph,
              std::vector<int> &terminals, int &numberOfEdges);

class DreyfusWagnerStatistics {
  public:
    float distancesDuration;
    float copyDuration;
    float dreyfusWagnerDuration;
    float everythingDuration;
    int result;
};

#endif // COMMON_H

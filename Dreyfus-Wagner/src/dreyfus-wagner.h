#include "common.h"
#include <vector>

DreyfusWagnerStatistics
dreyfusWagner(std::vector<std::vector<int>> &distances,
              const std::vector<std::vector<std::pair<int, int>>> &graph,
              const std::vector<int> &terminals);
#include "simulation.h"
using namespace std;

int main() {
    map<StationType, pair<int, map<int, int>>> config = {
        {StationType::A1, {1, {{1, 2}, {2, 1}}}},
        {StationType::A2, {1, {{1, 2}, {2, 1}}}},
        {StationType::A3, {1, {{1, 2}, {2, 1}}}}
    };
    Simulation sim(8.0, config);
    sim.run();
    return 0;

}
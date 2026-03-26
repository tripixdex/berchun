#pragma once
#ifndef PART_H
#define PART_H
#include <vector>
#include <utility> 
#include <random>
#include <memory>
#include <algorithm>
using namespace std;

enum class StationType { A1, A2, A3 };

class Part {
public:
    int type;
    vector<StationType> route;
    vector<pair<double, double>> processing_params;
    mutable size_t current_step = 0;

    Part(int t, const vector<StationType>& r, const vector<pair<double, double>>& params) :
        type(t),
        route(r),
        processing_params(params) {
    }

    double get_processing_time(size_t step) const {
        static random_device rd;
        static mt19937 gen(rd());
        normal_distribution<> dist(
            processing_params[step].first,  
            processing_params[step].second 
        );

        double val;
        do {
            val = dist(gen);
        } while (val < 0.01); \
        return val;
    }

    int get_type() const {
        return type;
    }

    size_t get_current_step() const {
        return current_step;
    }

    void increment_step() {
        current_step++;
    }

    const vector<StationType>& get_route() const {
        return route;
    }

    const vector<pair<double, double>>& get_processing_params() const {
        return processing_params;
    }

};

#endif
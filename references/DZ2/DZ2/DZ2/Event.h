#pragma once
#ifndef EVENT_H
#define EVENT_H

#include "Part.h"  
#include <memory>
#include <string>
#include <functional>  
using namespace std;
class Event {
public:

    double time;
    string type;
    shared_ptr<Part> part;
    StationType station;

    Event(double t, const std::string& tp,
        shared_ptr<Part> p, StationType st)
        : time(t), type(tp), part(p), station(st) {
    }

    bool operator<(const Event& other) const {
        return time >= other.time;
    }

    double get_time() const {
        return time;
    }

    string get_type() const {
        return type;
    }

    shared_ptr<Part> get_part() const {
        return part;
    }

    StationType get_station() const {
        return station;
    }

};

#endif 
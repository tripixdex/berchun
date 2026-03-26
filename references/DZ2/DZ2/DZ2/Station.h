#pragma once
#pragma once
#ifndef STATION_H
#define STATION_H
#include <vector>
#include <queue>
#include <map>
#include <memory>
#include <algorithm>
#include <numeric>
#include "Part.h"
#include "Event.h"
using namespace std;

class Station {
public:
    StationType type_;
    int machines_total_;
    int available_machines_;
    map<int, int> priorities_;
    priority_queue<pair<int, shared_ptr<Part>>> queue_;
    double busy_time_ = 0.0;
    size_t max_queue_length_ = 0;
    vector<size_t> queue_history_;


    Station(StationType t, int machines, map<int, int> prio)
        : type_(t), machines_total_(machines),
        available_machines_(machines), priorities_(prio) {

    }


    void add_to_queue(shared_ptr<Part> part) {
        int priority = priorities_[part->get_type()];
        queue_.emplace(-priority, part);
        queue_history_.push_back(queue_.size());
        max_queue_length_ = max(max_queue_length_, queue_.size());
    }

    shared_ptr<Event> process_next(double current_time) {
        if (!queue_.empty() && acquire_machine()) {
            auto part = queue_.top().second;
            queue_.pop();
            double processing_time = part->get_processing_time(part->get_current_step());
            busy_time_ += processing_time;

            return make_shared<Event>(current_time + processing_time, "завершение_обработки", part, type_);
        }
        else {
            return nullptr;
        }

    }

    bool acquire_machine() {
        if (available_machines_ > 0) {
            available_machines_--;
            return true;
        }
        else {
            return false;
        }
    }

    void release_machine() {
        available_machines_ = min(available_machines_ + 1, machines_total_);
    }


    double utilization(double total_time) const {
        if (total_time <= 0) {
            return 0;
        }
        double total_possible_time = total_time * machines_total_;
        return busy_time_ / total_possible_time;
    }

    double avg_queue() const {
        if (queue_history_.empty()) {
            return 0.0;
        }
        return accumulate(queue_history_.begin(), queue_history_.end(), 0.0) / queue_history_.size();
    }

    size_t get_max_queue_length() const {
        return max_queue_length_;
    }

    size_t get_processed_count() const {
        return queue_history_.size();
    }


};

#endif 
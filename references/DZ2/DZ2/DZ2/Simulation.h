#pragma once
#ifndef SIMULATION_H
#define SIMULATION_H
#include <iostream>
#include <queue>
#include <map>
#include <vector>
#include <string>
#include <fstream>
#include <random>
#include <memory>
#include "Station.h"
#include "Part.h"
#include "Event.h"
using namespace std;

string station_type_to_str(StationType type) {
    if (type == StationType::A1) return "A1";
    else if (type == StationType::A2) return "A2";
    else if (type == StationType::A3) return "A3";
    else return "Unknown";
}

struct CurrentEvent {
    shared_ptr<Part> part;     
    StationType station;       
    int priority;              
    double arrival_time;       

    CurrentEvent(shared_ptr<Part> p, StationType s, int prio, double time)
        : part(p), station(s), priority(prio), arrival_time(time) {
    }

    bool operator<(const CurrentEvent& other) const {
        if (priority != other.priority) {
            return priority < other.priority; 
        }
        return arrival_time > other.arrival_time; 
    }
};

class Simulation {
public:
    int completed_parts = 0;
    double current_time_ = 0;
    double simulation_time_;
    priority_queue<Event> fec_;         
    priority_queue<CurrentEvent> cec_;  
    map<StationType, Station> stations_;
    vector<string> cec_log_;           
    vector<string> fec_history_;
    vector<Event> cec_history_;        

    Simulation(double sim_time, map<StationType, pair<int, map<int, int>>> stations_config)
        : simulation_time_(sim_time) {
        for (auto& entry : stations_config) {
            stations_.emplace(
                entry.first,
                Station(
                    entry.first,
                    entry.second.first,
                    entry.second.second
                )
            );
        }
    }

    void run() {
        generate_arrivals();
        while (current_time_ < simulation_time_ && !fec_.empty()) {
            Event event = fec_.top();
            fec_.pop();
            fec_history_.push_back("Удаление из календаря\n Время: " + to_string(event.time) + " | Станок:" + station_type_to_str(event.station) + " | Событие: " + event.type + " | Запланировано событий: " + to_string(fec_.size()));
            cec_history_.push_back(event);
            current_time_ = event.time;

            if (event.type == "прибытие") {
                int priority = stations_.at(event.station).priorities_[event.part->get_type()];
                cec_.push(CurrentEvent(event.part, event.station, priority, current_time_));
                schedule_event(Event(
                    current_time_ + get_next_arrival_time(event.part->get_type()),
                    "прибытие",
                    make_shared<Part>(*event.part),
                    event.station
                ));
            }
            if (event.type == "завершение_обработки") {
                auto part = event.part;
                part->increment_step();
                auto& station = stations_.at(event.station);
                station.release_machine();
                if (part->get_current_step() < part->get_route().size()) {
                    StationType next_station = part->get_route()[part->get_current_step()];
                    int priority = stations_.at(next_station).priorities_[part->get_type()];
                    cec_.push(CurrentEvent(part, next_station, priority, current_time_));
                }
                else {
                    completed_parts++;
                    cec_log_.push_back("Деталь " + to_string(part->get_type()) + " отправлена на склад, это деталь номер " + to_string(completed_parts));
                }
                
                if (auto new_event = station.process_next(current_time_)) {
                    schedule_event(*new_event);
                }
            }

            process_cec();
        }
        save_CEC("CEC.log");
        save_FEC("FEC.log");
        print_stats();
    }

    void generate_arrivals() {
        auto part1 = make_shared<Part>(1, vector<StationType>{StationType::A1, StationType::A2, StationType::A3}, vector<pair<double, double>>{{20.0 / 60, 4.0 / 60}, { 5.0 / 60, 2.0 / 60 }, { 15.0 / 60, 5.0 / 60 }});
        schedule_event(Event(current_time_ + get_next_arrival_time(1), "прибытие", part1, StationType::A1));
        auto part2 = make_shared<Part>(2, vector<StationType>{StationType::A3, StationType::A2, StationType::A1}, vector<pair<double, double>>{ {15.0 / 60, 5.0 / 60}, { 7.0 / 60, 3.0 / 60 }, { 10.0 / 60, 3.0 / 60 }});
        schedule_event(Event(current_time_ + get_next_arrival_time(2), "прибытие", part2, StationType::A3));
    }

    void schedule_event(Event event) {
        fec_.push(event);
        fec_history_.push_back("Добавление в календарь\n Время: " + to_string(event.time) + " | Станок:" + station_type_to_str(event.station) + " | Событие: " + event.type + " | Запланировано событий: " + to_string(fec_.size()));
    }

    double get_next_arrival_time(int part_type) const {
        static random_device rd;
        static mt19937 gen(rd());
        if (part_type == 1) {
            std::normal_distribution<> dist(25.0 / 60, 4.0 / 60);
            return max(0.01, dist(gen));
        }
        else {
            normal_distribution<> dist(25.0 / 60, 6.0 / 60);
            return max(0.01, dist(gen));
        }
    }

    void process_cec() {
        while (!cec_.empty()) {
            CurrentEvent ce = cec_.top();
            cec_.pop();
            
            cec_log_.push_back("Время: " + to_string(current_time_) + " | Событие: продвижение | Станок: " + station_type_to_str(ce.station) + " | Деталь: " + to_string(ce.part->get_type()) + " | Шаг: " + to_string(ce.part->get_current_step()));
            auto& station = stations_.at(ce.station);
            station.add_to_queue(ce.part);
            if (auto new_event = station.process_next(current_time_)) {
                schedule_event(*new_event);
            }
        }
    }

    void print_stats() const {
        cout << "Stats:\n";
        cout << "Vsego obrabotano: " << completed_parts << "\n\n";
        for (auto& entry : stations_) {
            const Station& station = entry.second;
            cout << station_type_to_str(entry.first) << ":\n"
                << "  Sred ochered: " << station.avg_queue() << "\n"
                << "  Max ochered: " << station.get_max_queue_length() << "\n"
                << "  Zagruzka: " << station.utilization(current_time_) * 100 << "%\n"
                << "  Obrabotano: " << station.get_processed_count() << "\n\n";
        }
        
    }

    void save_CEC(const string& filename) const {
        ofstream file(filename);
        file << "=== CEC ===\n";
        for (auto& entry : cec_log_) {
            file << entry << "\n";
        }
        file << "\n=== Itogovaya statistika ===\n";
        file << "Vsego obrabotano sobytiy: " << cec_history_.size() << "\n";
        file << "Vsego zavershyonnyh detalei: " << completed_parts << "\n";
        
    }

    void save_FEC(const string& filename) {
        ofstream file(filename);
        file << "=== FEC ===\n";
        for (auto& entry : fec_history_) {
            file << entry << "\n";
        }
    }
};

#endif
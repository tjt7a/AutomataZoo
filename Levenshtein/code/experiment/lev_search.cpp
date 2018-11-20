//

#include "automata.h"
#include "levenshtein.h"
#include <iostream>
#include <random>
using namespace std;

/**
 *
 */
char getRandBP(mt19937 &prng, uniform_int_distribution<uint32_t> &dist){
    
    switch(dist(prng)) {
    case 0 :
        return 'a';
        break;
    case 1 :
        return 't';
        break;
    case 2 :
        return 'g';
        break;
    default :
        return 'c';
    }
}

/**
 *
 */
string genPattern(mt19937 &prng, uniform_int_distribution<uint32_t> &dist, uint32_t length) {

    string pattern = "";
    for(int i = 0; i < length; i++) {
        pattern = pattern + getRandBP(prng, dist);
    }

    return pattern;
}

/**
 *
 */
uint32_t *genInput(uint32_t length) {


}

int main(int argc, char *argv[]) {

    cout << "Hello world!" << endl;


    std::random_device random_device; // create object for seeding
    std::mt19937 engine{random_device()}; // create engine and seed it
    std::uniform_int_distribution<uint32_t> dist(0,3); // create uniform 0-3 (atgc)


    uint32_t num_trials = 10;
    uint32_t num_automata = 10;
    uint32_t input_len = 1000000;
    double report_thresh = 1.0; // I'm going to set this to be 1/1000 of input_len

    vector<uint32_t> eds;
    eds.push_back(3);
    eds.push_back(5);
    eds.push_back(10);

    uint32_t length_start = 15;
    
    for(uint32_t ed : eds) {

        for(uint32_t length = length_start; length < 100; length++) {

            cout << "Testing ED: " << ed << endl;
            cout << "Testing Length: " << length << endl;
            cout << "Testing Thresh: " << report_thresh << endl;
            
            uint32_t report_total = 0;
            cout << "Running " << num_trials << " trials..." << endl;
            
            for(uint32_t trial = 0; trial < num_trials; trial++){
                
                // Build automata
                Automata a;
                
                // run on diff automata
                for(int id = 0; id < num_automata; id++){
                    //cout << genPattern(engine, dist, i) << endl;
                    genLevenshtein(&a, id, genPattern(engine, dist, length), ed, true);
                }
                
                // Simulate automata
                a.setReport(true);
                a.setQuiet(true);
                a.initializeSimulation();
                
                // simulate
                for(uint32_t i = 0; i < input_len; i++) {   
                    a.simulate(getRandBP(engine, dist));
                }
                
                report_total += a.getReportVector().size();
                
            }
            
            // Print results
            double reports_per_filter = (double)report_total/(double)num_trials/(double)num_automata;
            cout << "Avg Reports/filter: " << reports_per_filter << endl;
            if(reports_per_filter < report_thresh){
                cout << "FELL BELOW REPORT THRESH" << endl;
                length_start = length;
                break;
            }
            
        }

    }
    
}

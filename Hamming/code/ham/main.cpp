#include "hamming.h"
#include <iostream>
#include <string>
#include <random>

using namespace std;


/**
* Usage
*/
void usage() {

    cout << "./ham -d <distance> -f <sequence file>" << endl;
    
}

/**
 *
 */
int main(int argc, char * argv[]) {


    cout << "**************************" << endl;
    cout << "     Hamming Distance        " << endl;
    cout << "    Automata Generator" << endl;
    cout << "      by Jack Wadden" << endl;
    cout << "**************************" << endl;

    
    uint32_t hamming_distance;
    uint32_t num_patterns;
    string source_fn;

    // Parse args
    if(argc != 5) {
        usage();
        exit(1);
    }else{
        for(int i = 1; i < argc; i++){
            string flag = argv[i];
            //
            if(flag.compare("-d") == 0){
                i++; 
                if(i != argc)
                    hamming_distance = atoi(argv[i]);
                else{
                    usage();
                    exit(1);
                }
                
            }else if(flag.compare("-f") == 0) {
                i++;
                if(i != argc){
                    source_fn = argv[i];
                }else{
                    usage();
                    exit(1);
                }
            }else{
                usage();
                exit(1);
            }
        }
    }

    cout << "Generating hamming..." << endl;
    
    // print configuration
    cout << "  hamming distance: " << to_string(hamming_distance) << endl;
    cout << "  pattern source: " << source_fn << endl;
    cout << endl;

    // Initialize automata
    Automata a;
    
    // open file to read lines
    ifstream file(source_fn);
    if(!file){
        cout << "Could not open pattern source file!" << endl;
        exit(1);
    }
    string line;
    uint32_t id = 0;
    while(!file.eof()){
        getline(file,line, '\n');
        if(line.empty()){
            continue;
        }
        cout << "Building filter for: " << line << endl;

        //
        genHamming(&a,
                   id,
                   line,
                   hamming_distance,
                   true); // always trim
        id++;
    }
    
    //
    a.finalizeAutomata();
    
    // emit ANML file
    string out_fn = "ham_" +
        to_string(id) + "_" +
        to_string(hamming_distance) +
        ".anml";
    a.automataToANMLFile(out_fn);
}


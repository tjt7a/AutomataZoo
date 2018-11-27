/**
 * Written by Jack Wadden
 *   some parts inspired by code written by Matthew Wallace
 */
#include "automata.h"
#include <iostream>
#include <string>
#include <random>

using namespace std;

/**
 * Returns a list of all 256 symbols in random order
 */
vector<uint32_t> getRandomizedVector() {

    vector<uint32_t> vec;
    vector<uint32_t> ordered;
    for(uint32_t i = 0; i < 256; i++){
        ordered.push_back(i);
    }

    for(uint32_t i = 0; i < 256; i++) {
        uint32_t randIndex = ((uint32_t)rand()) % ordered.size();
        vec.push_back(ordered[randIndex]);
        ordered.erase(ordered.begin() + randIndex);
    }

    return vec;
}

/**
 *
 */
void genAPPRNG(Automata *a, uint32_t id, uint32_t sides) {
    
    // Generate star capture states
    for(uint32_t i = 0; i < sides; i++) {

        string ste_id = to_string(id) + "_star_" + to_string(i);
        STE *star_ste = new STE(ste_id, "*", "none");
        if(i == 0)
            star_ste->setStart("start-of-data");
        star_ste->setReporting(true);
        star_ste->setReportCode(ste_id);
        a->rawAddSTE(star_ste);

        // get randomized charsets for leaving this node
        vector<uint32_t> randvec = getRandomizedVector();
        
        // generate transition nodes to all other states
        // add edge from star node to these transition nodes
        for(uint32_t j = 0; j < sides; j++){
            string trans_ste_id = to_string(id) + "_trans_" + to_string(i) + "_" +to_string(j);
            STE *trans_ste = new STE(trans_ste_id, "", "none");
            a->rawAddSTE(trans_ste);
            a->addEdge(star_ste, trans_ste);

            // fill with our share of random symbols
            uint32_t stride = 256/sides;
            uint32_t base = j * stride;
            for(uint32_t index = base; index < base + stride; index++){
                trans_ste->addSymbolToSymbolSet(randvec[index]);
            }
        }
        
    }

    // add all edges from all trans nodes now that all star nodes have been gen'd
    for(uint32_t from = 0; from < sides; from++) {
        for(uint32_t to = 0; to < sides; to++) {
            string from_id = to_string(id) + "_trans_" + to_string(from) + "_" + to_string(to);
            string to_id = to_string(id) + "_star_" + to_string(to);
            STE *from_ste = static_cast<STE*>(a->getElement(from_id));
            STE *to_ste = static_cast<STE*>(a->getElement(to_id));
            a->addEdge(from_ste, to_ste);
        }
    }
}


/**
* Usage
*/
void usage() {

    cout << "./apprng -s <seed> -n <number> -d <dice_size>" << endl;
    
}


/**
 * Checks for invalid markov chains
 */
void check(Automata *a, uint32_t id, uint32_t dice_size) {


    for(int from = 0; from < dice_size; from++){
        vector<STE*> exits;

        for(int to = 0; to < dice_size; to++){
            STE *s = dynamic_cast<STE*>(a->getElement(to_string(id) + "_trans_" + to_string(from) + "_" + to_string(to)));
            exits.push_back(s);
        }

        // check if there is any overlap from any bitset
        for(int i = 0; i < 256; ++i){
            int one_counter = 0;
            int zero_counter = 0;
            for(int to = 0; to < dice_size; to++){
                if(exits[to]->getBitColumn().test(i))
                    one_counter++;
                else
                    zero_counter++;
            }

            if(one_counter != 1 || zero_counter != dice_size-1) {
                cout << "FOUND INVALID MC ID: " << i << endl;
            }
        }
    }
} 

/**
 *
 */
int main(int argc, char * argv[]) {


    cout << "**************************" << endl;
    cout << "          AP PRNG        " << endl;
    cout << "    Automata Generator" << endl;
    cout << "      by Jack Wadden" << endl;
    cout << "**************************" << endl;

    uint32_t num_dice;
    uint32_t dice_size;
    uint32_t seed;
    
    if(argc != 7) {
        usage();
        exit(1);
    }else{
        for(int i = 1; i < argc; i++){
            string flag = argv[i];
            //
            if(flag.compare("-d") == 0){
                i++;
                dice_size = atoi(argv[i]);
            }else if(flag.compare("-n") == 0){
                i++;
                num_dice = atoi(argv[i]);
            }else if(flag.compare("-s") == 0){
                i++;
                seed = atoi(argv[i]);
            }else{
                usage();
                exit(1);
            }
        }
    }

    cout << "Generating prng..." << endl;
    // print configuration
    cout << "  Num dice: " << num_dice << endl;
    cout << "  Dice sides: " << dice_size << endl;
    cout << "  Seed: " << seed << endl;

    // seed prng
    srand(seed);

    Automata a;
    
    // Build dice
    for(uint32_t id = 0; id < num_dice; id++){

        genAPPRNG(&a, id, dice_size);
    }

    // sanity check
    for(uint32_t id = 0; id < num_dice; id++){
        check(&a, id, dice_size);
    }

    // emit automata
    string out_fn = "apprng_n" + to_string(num_dice) + "_d" + to_string(dice_size) + ".anml";
    a.automataToANMLFile(out_fn);
}


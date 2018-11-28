/**
 *
 */
#include "hamming.h"
#include <iostream>
#include <string>

using namespace std;

/**
 * Returns an ste in the automata given the base string "patternid_type" 
 * and col/row indices.
 */
STE *getSTE(Automata *a,
            string pattern_id_s,
            string type,
            uint32_t col,
            uint32_t row) {

    string id = pattern_id_s + "_" + type + "_" + to_string(col) + "_" + to_string(row);

    // does this element exist?
    auto it = a->getElements().find(id);
    
    STE *ste;
    if(it != a->getElements().end()){
        ste = static_cast<STE*>(a->getElement(id));
    }else{
        ste = NULL;
    }
    return ste;
}


/**
 *
 */
void genSTEs(Automata *a,
             string pattern_id_s,
             string pattern,
             uint32_t ham_distance) {

    // All elements are encoded in the following way
    // <pattern_id>_<type>_<column>_<row>
    // type can be any one of the following strings: match,mismatch

    string type = "";
    
    // Add all match elements
    for(uint32_t row = 0; row <= ham_distance; row++){
        // Matches start at every row, but start col in
        for(uint32_t col = row; col < pattern.size(); col++){

            // Add a match
            string match_id = pattern_id_s + "_match_" + to_string(col) + "_" + to_string(row);
            //cout << "Creating STE: " + match_id << endl;
            string symbol = pattern.substr(col, 1);
            STE* match_ste = new STE(match_id, symbol, "none");
            
            // when am I a start state?
            if(col == 0) {
                match_ste->setStart("all-input");
            }

            // when am I a report state?
            if(col == pattern.size() - 1){
                match_ste->setReporting(true);
            }

            a->rawAddSTE(match_ste);
        }
    }

    // Add all mismatch elements
    for(uint32_t row = 1; row <= ham_distance; row++){
        // Mismatches start at every row, but start col in
        for(uint32_t col = row - 1; col < pattern.size(); col++){

            // Add a mismatch
            string mismatch_set = "[^" + pattern.substr(col,1) + "]";
            string mismatch_id = pattern_id_s + "_mismatch_" + to_string(col) + "_" + to_string(row);
            //cout << "Creating STE: " + mismatch_id << endl;
            STE* mismatch_ste = new STE(mismatch_id, mismatch_set, "none");

            // when am I a start state?
            if(col == 0) {
                mismatch_ste->setStart("all-input");
            }

            // when am I a report state?
            if(col == pattern.size() - 1){
                mismatch_ste->setReporting(true);
            }
            
            a->rawAddSTE(mismatch_ste);
        }
    }
}

/**
 *
 */
void connectSTEs(Automata *a,
                 string pattern_id_s,
                 string pattern,
                 uint32_t ham_distance) {

    //cout << "Adding all edges..." << endl;
    // connect all matches to children
    for(uint32_t row = 0; row <= ham_distance; row++){
        for(uint32_t col = row; col < pattern.size() - 1; col++){
            // match state out edges
            STE *match_from = getSTE(a, pattern_id_s, "match", col, row);
            STE *match_to = getSTE(a, pattern_id_s, "match", col + 1, row);
    
            a->addEdge(match_from, match_to);

            if(row < ham_distance){
                STE *mismatch_to = getSTE(a, pattern_id_s, "mismatch", col + 1, row + 1);
                a->addEdge(match_from, mismatch_to);
            }
        }
    }

    // Connect all mismatches to children
    for(uint32_t row = 1; row <= ham_distance; row++){
        for(uint32_t col = row - 1; col < pattern.size() - 1; col++){


            // mismatch state out edges
            STE *mismatch_from = getSTE(a, pattern_id_s, "mismatch", col, row);
            STE *match_to = getSTE(a, pattern_id_s, "match", col + 1, row);

            a->addEdge(mismatch_from, match_to);

            if(row < ham_distance){
                STE *mismatch_to = getSTE(a, pattern_id_s, "mismatch", col + 1, row + 1);
                a->addEdge(mismatch_from, mismatch_to);
            }
        }
    }
}

/**
 *
 */
void clipHamming(Automata *a,
                 string pattern_id_s,
                 string pattern,
                 uint32_t ham_distance) {

    for(uint32_t row = 0; row <= ham_distance; row++){
        for(uint32_t col = 0; col < pattern.size(); col++){
            // if the matches (col) + (hamming distance - mismatches (row)) > size
            // we don't need this element
            // get the element
            if(col + (ham_distance - row + 1) > pattern.size()){
                STE *match_ste = getSTE(a, pattern_id_s, "match", col, row);
                if(match_ste != NULL){
                    //cout << "Removing: " << match_ste->getId() << endl;
                    a->removeElement(match_ste);
                }
                STE *mismatch_ste = getSTE(a, pattern_id_s, "mismatch", col, row);
                if(mismatch_ste != NULL){
                    //cout << "Removing: " << mismatch_ste->getId() << endl;
                    a->removeElement(mismatch_ste);
                }
            }

            // if we're on the clipped border, make sure out outputs get re-routed
            //  one row up
            if(col + (ham_distance - row + 1) == pattern.size() && col < pattern.size() - 1){
                STE *match_ste = getSTE(a, pattern_id_s, "match", col, row);
                if(match_ste != NULL){
                    //cout << "Readjusting: " << match_ste->getId() << endl;
                    STE *match_to = getSTE(a, pattern_id_s, "match", col+1, row+1);
                    a->addEdge(match_ste, match_to);
                }
                
                STE *mismatch_ste = getSTE(a, pattern_id_s, "mismatch", col, row);
                if(mismatch_ste != NULL){
                    //cout << "Readjusting: " << mismatch_ste->getId() << endl;
                    STE *match_to = getSTE(a, pattern_id_s, "match", col+1, row+1);
                    a->addEdge(mismatch_ste, match_to);
                }
                
            }
            
        }
    }
}
                    

/**
 *
 */
void genHamming(Automata *a,
                    uint32_t pattern_id,
                    string pattern,
                    uint32_t ham_distance,
                    bool restricted) {

    string pattern_id_s = to_string(pattern_id);
    genSTEs(a, pattern_id_s, pattern, ham_distance);
    connectSTEs(a, pattern_id_s, pattern, ham_distance);

    //
    if(restricted) {
        clipHamming(a, pattern_id_s, pattern, ham_distance);
    }

    // finalize
    a->finalizeAutomata();
}


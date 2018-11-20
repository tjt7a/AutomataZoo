/**
 *
 */
#include "levenshtein.h"
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
    STE *ste = static_cast<STE*>(a->getElement(id));
    return ste;
}


/**
 *
 */
void genSTEs(Automata *a,
             string pattern_id_s,
             string pattern,
             uint32_t edit_distance) {

    // All elements are encoded in the following way
    // <pattern_id>_<type>_<column>_<row>
    // type can be any one of the following strings: match,mismatch

    string type = "";
    
    // Add all elements for matches
    type = "match";
    // Matches don't start until col 1
    for(uint32_t col = 1; col <= pattern.size(); col++){
        for(uint32_t row = 0; row <= edit_distance; row++){
            string id = pattern_id_s + "_" + type + "_" + to_string(col) + "_" + to_string(row);
            //cout << "Creating STE: " + id << endl;
            //cout << pattern.substr(col - 1, 1) << endl;
            STE* ste = new STE(id, pattern.substr(col - 1, 1), "none");

            // when am I a start state?
            // on the diagonal
            if(col - row == 1) {
                ste->setStart("all-input");
            }

            // when am I a report state?
            // if we are in the lower right corner
            if( (col + (edit_distance-row)) >= pattern.size() )
                ste->setReporting(true);

            a->rawAddSTE(ste);
        }
    }

    // Add all elements for mismatches (insertions, deletions, substitutions)
    type = "mismatch";
    // Mis-matches don't start until column 1
    for(uint32_t col = 0; col <= pattern.size(); col++){
        // Only matches start at row 0
        for(uint32_t row = 1; row <= edit_distance; row++){
            string id = pattern_id_s + "_" + type + "_" + to_string(col) + "_" + to_string(row);
            STE* ste = new STE(id, "*", "none");
            //cout << "Creating STE: " + id << endl;
            //cout << "*" << endl;

            // when am I a start state?
            // if we're an initial mismatch state
            if((col == 1 && row == 1) ||
               (col == 0 && row == 1)) {
                ste->setStart("all-input");
            }

            // when am I a report state?
            // if we are in the lower right corner
            if( (col + (edit_distance-row)) >= pattern.size() )
                ste->setReporting(true);
            
            a->rawAddSTE(ste);
        }
    }    
}

/**
 *
 */
void addMatchRule(Automata *a,
                  string pattern_id_s,
                  string pattern,
                  uint32_t edit_distance,
                  STE *from,
                  uint32_t col,
                  uint32_t row) {

    // connect to next match in row, unless we're the last col (match)
    if(col != pattern.size()){
        STE *to = getSTE(a, pattern_id_s, "match", col + 1, row);
        //cout << "TO: " << to->getId() << endl;
        a->addEdge(from, to);
    }
}

/**
 *
 */
void addSubstitutionRule(Automata *a,
                         string pattern_id_s,
                         string pattern,
                         uint32_t edit_distance,
                         STE *from,
                         uint32_t col,
                         uint32_t row) {
    
    //connect to mismatch in next column and next row (substitution)
    if( row < edit_distance && col < pattern.size() ){
        STE *to = getSTE(a, pattern_id_s, "mismatch", col + 1, row + 1);
        //cout << "TO: " << to->getId() << endl;
        a->addEdge(from, to);
    }
}

/**
 *
 */
void addInsertionRule(Automata *a,
                      string pattern_id_s,
                      string pattern,
                      uint32_t edit_distance,
                      STE *from,
                      uint32_t col,
                      uint32_t row) {

    // connect to next mismatch in same column (insertion)
    if(row < edit_distance ){
        STE *to = getSTE(a, pattern_id_s, "mismatch", col, row + 1);
        //cout << "TO: " << to->getId() << endl;
        a->addEdge(from, to);
    }
}

/**
 *
 */
void addDeleteSubstitutionRule(Automata *a,
                               string pattern_id_s,
                               string pattern,
                               uint32_t edit_distance,
                               STE *from,
                               uint32_t col,
                               uint32_t row) {

    // Deletions + mismatch (substitution)
    // diagonal starting col + 2, row + 2
    uint32_t index = 2;
    bool done = (row + index > edit_distance) || (col + index > pattern.size());
    while(!done){
        STE *to = getSTE(a, pattern_id_s, "mismatch", col + index, row + index);
        //cout << "TO: " << to->getId() << endl;
        a->addEdge(from, to);
        index++;
        done = (row + index > edit_distance) || (col + index > pattern.size());       
    }
}

/**
 *
 */
void addDeleteMatchRule(Automata *a,
                        string pattern_id_s,
                        string pattern,
                        uint32_t edit_distance,
                        STE *from,
                        uint32_t col,
                        uint32_t row) {

    // Deletions + mismatch (substitution)
    // diagonal starting col + 2, row + 1
    uint32_t col_index = 2;
    uint32_t row_index = 1;
    bool done = (row + row_index > edit_distance) || (col + col_index > pattern.size());
    while(!done){
        STE *to = getSTE(a, pattern_id_s, "match", col + col_index, row + row_index);
        //cout << "TO: " << to->getId() << endl;
        a->addEdge(from, to);
        row_index++;
        col_index++;
        done = (row + row_index > edit_distance) || (col + col_index > pattern.size());
    }
}



/**
 *
 */
void connectSTEs(Automata *a,
                 string pattern_id_s,
                 string pattern,
                 uint32_t edit_distance) {

    //cout << "Adding all edges..." << endl;
    // connect all matches to children
    string type = "match";
    // Matches don't start until col 1
    for(uint32_t col = 1; col <= pattern.size(); col++){
        for(uint32_t row = 0; row <= edit_distance; row++){
            STE *from = getSTE(a, pattern_id_s, type, col, row);
            //cout << "FROM: " << from->getId() << endl;

            //cout << "Match rule..." << endl;
            addMatchRule(a, pattern_id_s, pattern, edit_distance, from, col, row);

            //cout << "Substitution rule..." << endl;
            addSubstitutionRule(a, pattern_id_s, pattern, edit_distance, from, col, row);

            //cout << "Insertion rule..." << endl;
            addInsertionRule(a, pattern_id_s, pattern, edit_distance, from, col, row);

            //cout << "Delete + Substitute rule..." << endl;
            addDeleteSubstitutionRule(a, pattern_id_s, pattern, edit_distance, from, col, row);
            //cout << "Delete + Match rule..." << endl;
            addDeleteMatchRule(a, pattern_id_s, pattern, edit_distance, from, col, row);
            
            // Note that we don't do deletions plus insertions because that's
            //  essentially equivalent to just an substitution and we don't want
            //  to double penalize
        }
    }

    // connect all mismatches to children
    type = "mismatch";
    // Matches don't start until col 1
    for(uint32_t col = 0; col <= pattern.size(); col++){
        for(uint32_t row = 1; row <= edit_distance; row++){
            STE *from = getSTE(a, pattern_id_s, type, col, row);
            //cout << "FROM: " << from->getId() << endl;

            //cout << "Match rule..." << endl;
            addMatchRule(a, pattern_id_s, pattern, edit_distance, from, col, row);

            //cout << "Substitution rule..." << endl;
            addSubstitutionRule(a, pattern_id_s, pattern, edit_distance, from, col, row);

            //cout << "Insertion rule..." << endl;
            addInsertionRule(a, pattern_id_s, pattern, edit_distance, from, col, row);

            //cout << "Delete + Substitute rule..." << endl;
            addDeleteSubstitutionRule(a, pattern_id_s, pattern, edit_distance, from, col, row);

            //cout << "Delete + Match rule..." << endl;
            addDeleteMatchRule(a, pattern_id_s, pattern, edit_distance, from, col, row);
            
        }
    }
}

/**
 *
 */
void clipLevensthein(Automata *a,
                     string pattern_id_s,
                     string pattern,
                     uint32_t edit_distance) {

    //cout << "Clipping levenshtein..." << endl;
    // UPPER LEFT CORNER
    // remove mismatches
    for(uint32_t col = 0; col <= edit_distance; col++) {
        // move from low to high
        for(uint32_t row = col; row <= edit_distance; row++) {
            if(row == 0 && col == 0)
                continue;
            // remove all mismatch STEs
            // why? any mismatches at the front will be handled by sliding window search
            a->removeElement(getSTE(a,pattern_id_s, "mismatch", col, row));
        }
    }

    // remove matches
    for(uint32_t col = 1; col <= edit_distance; col++) {
        // move from low to high
        for(uint32_t row = col; row <= edit_distance; row++) {
            // remove all match STEs
            // why? any matches here are children of mismatches
            // and will also be handled by sliding window
            a->removeElement(getSTE(a,pattern_id_s, "match", col, row));
        }
    }

    // Remove unecessary edges
    // do any starts connect to other starts?
    for(STE *start : a->getStarts()){
        for(auto o : start->getOutputSTEPointers()){
            STE *out = static_cast<STE*>(o.first);
            if(out->isStart())
                a->removeEdge(start, out);

            if(start->getOutputs().size() == 0)
                a->removeElement(start);

            if(out->getInputs().size() == 0 && !out->isStart())
                a->removeElement(out);
        
            
        }
    }

    // BOTTOM RIGHT CORNER
    // remove mismatches
    for(uint32_t col = pattern.size() - edit_distance + 1; col <= pattern.size(); col++) {
        //cout << "Clipping col: " << col << endl;
        // move from low to high
        uint32_t start_height = 1;
        uint32_t max_height = edit_distance - (pattern.size() - col);
        for(uint32_t row = start_height; row <= max_height; row++) {
            //cout << "Clipping row: " << row << endl;
            // remove all mismatch STEs
            // why? any mismatches at the front will be handled by sliding window search
            //cout << "Clipping col: " + to_string(col) + " row: " + to_string(row) << endl; 
            a->removeElement(getSTE(a,pattern_id_s, "mismatch", col, row));
        }
    }

    // remove matches
    for(uint32_t col = pattern.size() - edit_distance + 1; col <= pattern.size(); col++) {
        //cout << "Clipping col: " << col << endl;
        // move from low to high
        uint32_t start_height = 0;
        uint32_t max_height = edit_distance - (pattern.size() - col) - 1;
        for(uint32_t row = start_height; row <= max_height; row++) {
            //cout << "Clipping row: " << row << endl;
            // remove all mismatch STEs
            // why? any mismatches at the front will be handled by sliding window search
            //cout << "Clipping col: " + to_string(col) + " row: " + to_string(row) << endl; 
            a->removeElement(getSTE(a,pattern_id_s, "match", col, row));
        }
    }

    // Remove unecessary edges
    // Once we reach a report, it's not necessary to keep going
    // remove all children edges of reports
    for(Element *report : a->getReports()){
        for(auto o : report->getOutputSTEPointers()){
            STE *out = static_cast<STE*>(o.first);
            a->removeEdge(report, out);

            if(out->getInputs().size() == 0)
                a->removeElement(out);
        }
    }


}
                    

/**
 *
 */
void genLevenshtein(Automata *a,
                    uint32_t pattern_id,
                    string pattern,
                    uint32_t edit_distance,
                    bool restricted) {

    string pattern_id_s = to_string(pattern_id);
    genSTEs(a, pattern_id_s, pattern, edit_distance);
    connectSTEs(a, pattern_id_s, pattern, edit_distance);

    //
    if(restricted) {
        clipLevensthein(a, pattern_id_s, pattern, edit_distance);
    }

    // finalize
    a->finalizeAutomata();
}


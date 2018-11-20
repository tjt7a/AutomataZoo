#include "automata.h"
#include <iostream>
#include <string>

using namespace std;

/**
* Usage
*/
void usage() {

    cout << "./er <name_db_file>" << endl;
}

/**
 *
 */
void connectSTEToHandle(Automata *a, STE *ste, vector<STE*> handle) {

    for(STE *s : handle) {
        a->addEdge(ste, s);
    }
}

/**
 *
 */
void connectHandleToSTE(Automata *a, vector<STE*> handle, STE *ste) {

    for(STE *s : handle) {
        a->addEdge(s, ste);
    }
}

/**
 *
 */
pair< vector<STE*>,vector<STE*> > genFuzzy(Automata *a, string ids, string name) {

    uint32_t bailout_column = 100000; // v high essentially turns this off
    
    vector<STE*> front;
    vector<STE*> back;
    
    // Generate STEs
    for(uint32_t col = 0; col < name.size(); col++){

        // Build low match
        string ids1 = ids + "_match_0_" + to_string(col);
        string mids = ids + "_mismatch_1_" + to_string(col);
        string ids2 = ids + "_match_1_" + to_string(col);
        string symbol_set = name.substr(col,1);
        STE *ste;
        
        // zero row
        if(col < name.size() - 1){
            ste = new STE(ids1, symbol_set, "none");
            a->rawAddSTE(ste);

            if(col == 0) {
                front.push_back(ste);
            }

            if(col > bailout_column) back.push_back(ste);
        }

        // mismatch row
        string mismatch_symbol_set = "[^$" + symbol_set + "]";

        ste = new STE(mids, mismatch_symbol_set, "none");
        a->rawAddSTE(ste);
        if(col == 0)
            front.push_back(ste);

        if(col > bailout_column || col == name.size()-1) back.push_back(ste);

        // high match
        if(col > 0) {
            ste = new STE(ids2, symbol_set, "none");
            a->rawAddSTE(ste);
            if(col > bailout_column || col == name.size() - 1) back.push_back(ste);
        }

    }

    // connect all STEs
    for(uint32_t col = 0; col < name.size() - 1; col++){

        string match_0 = ids + "_match_0_" + to_string(col);
        string mismatch_1 = ids + "_mismatch_1_" + to_string(col);
        string match_1 = ids + "_match_1_" + to_string(col);
        string to_match_0 = ids + "_match_0_" + to_string(col+1);
        string to_mismatch_1 = ids + "_mismatch_1_" + to_string(col+1);
        string to_match_1 = ids + "_match_1_" + to_string(col+1);

        if(col < name.size() - 1){
            a->addEdge(match_0, to_mismatch_1);
            a->addEdge(mismatch_1, to_match_1);
        }

        if(col < name.size() - 2){
            a->addEdge(match_0, to_match_0);
        }

        if(col == name.size() - 2){
            a->addEdge(match_0, to_match_1);
        }

        if(col > 0){
            a->addEdge(match_1, to_match_1);
        }
        
    }
    
    return make_pair(front,back);
}

/**
 *
 */
void genER(Automata *a, uint32_t id, string firstname, string lastname) {

    //
    STE *start = new STE (to_string(id) + "_start", "$", "all-input");
    a->rawAddSTE(start);
    // pair is vector of inputs (pair.first) and outputs (pair.second)
    pair<vector<STE*>, vector<STE*> > handle;

    // family name
    handle = genFuzzy(a, to_string(id) + "_familyname", lastname);
    connectSTEToHandle(a, start, handle.first);
    
    // comma and space separators
    string comma1id = to_string(id) + "_comma1";
    STE *comma1 = new STE(comma1id, ",","none");
    string space0id = to_string(id) + "_space0";
    STE *space0 = new STE(space0id, "[ IVXivx]","none");
    a->rawAddSTE(comma1);
    a->rawAddSTE(space0);

    // exit from fuzzy matcher
    connectHandleToSTE(a, handle.second, comma1);
    connectHandleToSTE(a, handle.second, space0);

    // chew on roman numerals and spaces after match
    a->addEdge(space0, space0);
    a->addEdge(space0, comma1);

    // after comma, chew on spaces
    string space1id = to_string(id) + "_space1";
    STE *space1 = new STE(space1id, " ","none");
    a->rawAddSTE(space1);
    a->addEdge(comma1, space1);
    a->addEdge(space1,space1);
    
    // first name
    handle = genFuzzy(a,to_string(id) + "_firstname",firstname);
    connectSTEToHandle(a, comma1, handle.first);
    connectSTEToHandle(a, space1, handle.first);

    string dot1id = to_string(id) + "_dot1";
    STE *dot1 = new STE(dot1id, "[.]", "none");
    a->rawAddSTE(dot1);

    // connect fuzzy first match to dot (Jack -> J.)
    STE *fuzzy_first_match = static_cast<STE*>(a->getElement(to_string(id) + "_firstname_match_0_0"));
    a->addEdge(fuzzy_first_match, dot1);
    
    // final report $
    STE *final = new STE(to_string(id) + "_final", "$", "none");
    a->rawAddSTE(final);
    final->setReporting(true);
    connectHandleToSTE(a, handle.second, final);
    
    // chew on anything else until delimiter
    STE *notfinal = new STE(to_string(id) + "_notfinal", "[^$]", "none");
    a->rawAddSTE(notfinal);
    connectHandleToSTE(a, handle.second, notfinal);
    a->addEdge(notfinal, notfinal);
    a->addEdge(notfinal, final);
    a->addEdge(dot1,notfinal);
    a->addEdge(dot1,final);
}

/**
 *
 */
int main(int argc, char * argv[]) {


    cout << "**************************" << endl;
    cout << "     Entity Resolution      " << endl;
    cout << "    Automata Generator" << endl;
    cout << "      by Jack Wadden" << endl;
    cout << "**************************" << endl;

    string name_file;
    
    if(argc != 2) {
        usage();
        exit(1);
    }else{
        name_file = argv[1];
    }

    cout << "Generating Entity Resolution Automata..." << endl;
    
    // print configuration
    cout << "  source file: " << name_file << endl;
    cout << endl;

    //
    Automata a;
    
    // open file to read lines
    ifstream file(name_file);
    if(!file){
        cout << "Could not open name db file!" << endl;
        exit(1);
    }

    string line;
    uint32_t id = 0;
    while(!file.eof()){
        getline(file,line, '\n');
        if(line.empty()){
            continue;
        }

        // get first and last name
        string first_name = line.substr(line.find(',') + 2);
        string last_name = line.substr(0, line.find(','));

        //cout << "Building ER filter for: " << first_name << " : " << last_name << endl;
        genER(&a, id, first_name, last_name);
        //
        id++;
    }

    
    a.finalizeAutomata();
    
    // emit ANML file
    string out_fn = "er.anml";

    a.automataToANMLFile(out_fn);
    
}


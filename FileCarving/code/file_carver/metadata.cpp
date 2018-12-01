#include "automata.h"
#include "util.h"

using namespace std;

//
pair<STE*, STE*> addSSNs(Automata &, uint32_t *);
void addCCNs(Automata &, uint32_t *);
//pair<STE*, STE*> addEmails(Automata &, uint32_t *);
//pair<STE*, STE*> addWebsites(Automata &, uint32_t *);


/**
 *
 */
pair<STE*, STE*> addSSNs(Automata &a, uint32_t *id_counter) {

    STE *first;
    //
    vector<string> chars;
    chars.push_back("[\\d]");
    chars.push_back("[\\d]");
    chars.push_back("[\\d]");
    chars.push_back("-");
    chars.push_back("[\\d]");
    chars.push_back("[\\d]");
    chars.push_back("-");
    chars.push_back("[\\d]");
    chars.push_back("[\\d]");
    chars.push_back("[\\d]");
    chars.push_back("[\\d]");

    pair<STE*,STE*> handle = makeExactMatchChar(a, id_counter, chars);
    handle.first->setStart("all-input");
    handle.second->setReporting(true);
    handle.second->setReportCode("Possible SSN Entry");

    return handle;
}


/**
 *
 */
void addCCNs(Automata &a, uint32_t *id_counter) {

    STE *first = new STE(getNextId(id_counter), "[^0-9]", "all-input");
    a.rawAddSTE(first);
    
    vector<STE*> exits;
    // JCB
    vector<vector<string>> strings;
    strings.push_back({"3", "4", "[0-9]", "[0-9]"}); // Amex
    strings.push_back({"3", "7", "[0-9]", "[0-9]"}); // Amex
    strings.push_back({"6", "2", "0", "0"}); // China UnionPay
    strings.push_back({"8", "8", "0", "0"}); // China UnionPay

    // Diners club
    for(uint32_t i = 0; i <= 5; i++){
        string s = to_string(i);
        strings.push_back({"3", "0", s, "[0-9]"});
    }
    strings.push_back({"3", "0", "9", "[0-9]"});
    strings.push_back({"3", "6", "[0-9]", "[0-9]"});
    strings.push_back({"3", "8", "[0-9]", "[0-9]"});
    strings.push_back({"3", "9", "[0-9]", "[0-9]"});
    strings.push_back({"5", "4", "[0-9]", "[0-9]"});
    strings.push_back({"5", "5", "[0-9]", "[0-9]"});

    // Discover
    strings.push_back({"6", "0", "1", "1"});
    for(uint32_t i = 4; i <= 9; i++){
        strings.push_back({"6", "4", to_string(i), "[0-9]"});
    }
    for(uint32_t i = 1; i <= 9; i++){ // not quite exact
        strings.push_back({"6", "2", "2", to_string(i)});
    }
    strings.push_back({"6", "5", "[0-9]", "[0-9]"});


    // JCB
    for(uint32_t i = 3528; i <= 3589; i++){
        string s = to_string(i);
        strings.push_back({s.substr(0,1),s.substr(1,1),s.substr(2,1),s.substr(3,1)});
    }

    // Laser
    strings.push_back({"6", "3", "0", "4"});
    strings.push_back({"6", "7", "0", "6"});
    strings.push_back({"6", "7", "7", "1"});
    strings.push_back({"6", "7", "0", "9"});

    // Maestro
    strings.push_back({"5", "0", "1", "8"});
    strings.push_back({"5", "0", "2", "0"});
    strings.push_back({"5", "0", "3", "8"});
    strings.push_back({"5", "6", "1", "2"});
    strings.push_back({"5", "8", "9", "3"});
    strings.push_back({"6", "3", "0", "4"});
    strings.push_back({"6", "7", "5", "9"});
    strings.push_back({"6", "7", "6", "1"});
    strings.push_back({"6", "7", "6", "2"});
    strings.push_back({"6", "7", "6", "3"});
    strings.push_back({"0", "6", "0", "4"});
    strings.push_back({"6", "3", "9", "0"});

    // Dankort
    strings.push_back({"5", "0", "1", "9"});

    // Mastercard
    for(uint32_t i = 50; i <= 55; i++){
        string s = to_string(i);
        strings.push_back({s.substr(0,1),s.substr(1,1),"[0-9]","[0-9]"});
    }
    
    // Visa
    strings.push_back({"4", "[0-9]", "[0-9]", "[0-9]"});
    
    vector<pair<STE*,STE*>> handles = makeExactMatchStrings(a, id_counter, strings);

    STE *space1 = new STE(getNextId(id_counter), "[ ]", "none");
    a.rawAddSTE(space1);
    STE *space2 = new STE(getNextId(id_counter), "[ ]", "none");
    a.rawAddSTE(space2);
    STE *space3 = new STE(getNextId(id_counter), "[ ]", "none");
    a.rawAddSTE(space3);
    
    vector<string> charsets = {"[0-9]","[0-9]","[0-9]","[0-9]"};
    pair<STE*, STE*> handle1 = makeExactMatchChar(a, id_counter, charsets);
    pair<STE*, STE*> handle2 = makeExactMatchChar(a, id_counter, charsets);
    pair<STE*, STE*> exit_handle = makeExactMatchChar(a, id_counter, charsets);


    for(pair<STE*,STE*> handle : handles){
        a.addEdge(first, handle.first);
        a.addEdge(handle.second, handle1.first);
        a.addEdge(handle.second, space1);
    }

    // first connection 0-1
    a.addEdge(space1, space1);
    a.addEdge(space1, handle1.first);

    // second connection 1-2
    a.addEdge(space2, space2);
    a.addEdge(handle1.second, space2);
    a.addEdge(handle1.second, handle2.first);
    a.addEdge(space2, handle2.first);
    
    // third connection 2-exit/3
    a.addEdge(space3, space3);
    a.addEdge(handle2.second, space3);
    a.addEdge(handle2.second, exit_handle.first);
    a.addEdge(space3, exit_handle.first);
    
    // exit
    STE *exit = new STE(getNextId(id_counter), "[^0-9]", "none");
    a.rawAddSTE(exit);
    a.addEdge(exit_handle.second, exit);
    
    exit->setReporting(true);
    exit->setReportCode("Credit_Card_Number");
}


/**
 *
 */
void addEmails(Automata &a, uint32_t *id_counter) {


    // Even though this is more restrictive than the rules allow
    //  whoooo the heck puts question marks in their emails?
    STE* local = new STE(getNextId(id_counter), "[a-zA-Z0-9_.]", "all-input");
    a.rawAddSTE(local);
    STE * at = new STE(getNextId(id_counter), "@", "none");
    a.rawAddSTE(at);

    STE *domain1 = new STE(getNextId(id_counter), "[a-zA-Z0-9-]", "none");
    a.rawAddSTE(domain1);

    // technically too restrictive but weeds out lots of false positives
    STE *domain2 = new STE(getNextId(id_counter), "[a-z]", "none");
    a.rawAddSTE(domain2);
    
    STE *dot = new STE(getNextId(id_counter), "[.]", "none");
    a.rawAddSTE(dot);

    STE *final = new STE(getNextId(id_counter), "[^.a-zA-Z0-9]", "none");
    a.rawAddSTE(final);
    final->setReporting(true);
    final->setReportCode("E-mail_Address");

    // Connect all STEs
    a.addEdge(local, at);
    a.addEdge(at, domain1);
    a.addEdge(domain1, domain1);
    a.addEdge(domain1, dot);
    a.addEdge(dot, domain2);
    a.addEdge(domain2, dot);
    a.addEdge(domain2, domain2);
    a.addEdge(domain2, final);
    
}

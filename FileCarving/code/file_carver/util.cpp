#include "automata.h"

using namespace std;


/**
 *
 */
string getNextId(uint32_t * id_counter) {

    string val = "__" + to_string(*id_counter) + "__";
    (*id_counter) = (*id_counter) + 1;
    return val;
}

/**
 *
 */
pair<pair<STE*,STE*>, STE*> add4GatedMatcher(Automata &a, uint32_t *id_counter, string s) {

    pair<pair<STE*, STE*>, STE*> ret_handle;

    //
    STE *first_match = new STE(getNextId(id_counter), s.substr(0,1), "none");;
    a.rawAddSTE(first_match);
    STE *first_fail = new STE(getNextId(id_counter), "[^" + s.substr(0,1) + "]", "none");;
    a.rawAddSTE(first_fail);
    a.addEdge(first_fail, first_match);
    a.addEdge(first_fail, first_fail);
    ret_handle.first.first = first_match;
    ret_handle.first.second = first_fail;

    //
    STE *second_match = new STE(getNextId(id_counter), s.substr(1,1), "none");;
    a.rawAddSTE(second_match);
    STE *second_fail = new STE(getNextId(id_counter), "[^" + s.substr(1,1) + "]", "none");;
    a.rawAddSTE(second_fail);
    a.addEdge(second_fail, first_fail);
    a.addEdge(second_fail, first_match);
    a.addEdge(first_match, second_match);
    a.addEdge(first_match, second_fail);
    
    //
    STE *third_match = new STE(getNextId(id_counter), s.substr(2,1), "none");;
    a.rawAddSTE(third_match);
    STE *third_fail = new STE(getNextId(id_counter), "[^" + s.substr(2,1) + "]", "none");;
    a.rawAddSTE(third_fail);
    a.addEdge(third_fail, first_fail);
    a.addEdge(third_fail, first_match);
    a.addEdge(second_match, third_match);
    a.addEdge(second_match, third_fail);
    
    //
    STE *fourth_match = new STE(getNextId(id_counter), s.substr(3,1), "none");;
    a.rawAddSTE(fourth_match);
    STE *fourth_fail = new STE(getNextId(id_counter), "[^" + s.substr(3,1) + "]", "none");;
    a.rawAddSTE(fourth_fail);
    a.addEdge(fourth_fail, first_fail);
    a.addEdge(fourth_fail, first_match);
    a.addEdge(third_match, fourth_match);
    a.addEdge(third_match, fourth_fail);

    ret_handle.second = fourth_match;

    return ret_handle;
}

/**
 *
 */
STE * addCharToBitTrie(Automata &ap, uint32_t *id_counter,
                       uint32_t c, STE **zero_head, STE **one_head, uint32_t bit_length) {

    STE *node;
    // make sure the first node is populated
    if(c & 1){
        if(*one_head == NULL){
            *one_head = new STE("trie_" + getNextId(id_counter), "\\x01", "none");
            ap.rawAddSTE(*one_head);
        }
        node = *one_head; 
    }else{
        if(*zero_head == NULL){
            *zero_head = new STE("trie_" + getNextId(id_counter), "\\x00", "none");
            ap.rawAddSTE(*zero_head);
        }
        node = *zero_head; 
    }

    // for the rest of the bits, do a traversal to see if we need to add new nodes
    STE *end;
    for(int bit = 1; bit < bit_length; bit++){

        STE *matched = NULL;
        bool created = false;
        // 1
        if((c >> bit) & 1){
            for(auto e : node->getOutputSTEPointers()){
                STE *child = static_cast<STE*>(e.first);
                if(child->match(1)){
                    matched = child;
                }
            }

            // if a matching child doesn't exist, create it!
            if(matched == NULL){
                matched = new STE("trie_" + getNextId(id_counter), "\\x01", "none");
                ap.rawAddSTE(matched);
                created = true;
            }
                
        }
        // 0
        else{
            for(auto e : node->getOutputSTEPointers()){
                STE *child = static_cast<STE*>(e.first);
                if(child->match(0)){
                    matched = child;
                }
            }

            // if a matching child doesn't exist, create it!
            if(matched == NULL){
                matched = new STE("trie_" + getNextId(id_counter), "\\x00", "none");
                created = true;
                ap.rawAddSTE(matched);
            }
        }

        //
        ap.addEdge(node, matched);
        node = matched;

        //
        if(bit == (bit_length - 1) && created)
            end = node;
        else
            end = NULL;
    }

    return end;
}

/**
 *
 */
vector<STE*> rightMerge(Automata &ap, vector<STE*> ends) {

    vector<STE*> result_ends;

    // add all ends to workq, mark them
    queue<STE *> workq;
    queue<STE *> next_workq;
    for(STE * ste : ends) {
        ste->mark();
        workq.push(ste);
    }

    //
    while(!workq.empty()) {

        STE *ste1 = workq.front();
        workq.pop();

        // consider merging this element with every other element in the workq
        while(!workq.empty()){
            STE *ste2 = workq.front();
            workq.pop();
            
            if(ste1->rightCompare(ste2)){
                ap.rightMergeSTEs(ste1, ste2);
            } else {
                next_workq.push(ste2);
            }
        }

        // now that we've considered an ste, make sure we right merge its inputs
        vector<STE *> inputSTEs;
        for(auto e : ste1->getInputs()) {
            STE * parent = static_cast<STE*>(ap.getElement(e.first));
            if(!parent->isMarked()){
                parent->mark();
                inputSTEs.push_back(parent);
            }
        }

        //
        rightMerge(ap, inputSTEs);

        // save all stes that are ends
        if(ste1->getOutputSTEPointers().size() == 0)
            result_ends.push_back(ste1);
        
        // fill workq with whatever was in next_workq
        while(!next_workq.empty()){
            workq.push(next_workq.front());
            next_workq.pop();
        }
    }

    return result_ends;
}

/**
 *
 */
void commonPathMerge(Automata &ap, vector<STE*> starts) {

    // add all ends to workq, mark them
    queue<STE *> workq;
    queue<STE *> next_workq;
    for(STE * ste : starts) {
        workq.push(ste);
    }
    
    // 
    while(!workq.empty()) {

        STE *ste1 = workq.front();
        workq.pop();
        
        // consider merging this element with every other element in the workq
        while(!workq.empty()){
            STE *ste2 = workq.front();
            workq.pop();


            
            if(ste1->identicalInputs(ste2) && ste1->identicalOutputs(ste2)){
                cout << "CPMed: " << ste1->getId() << " : " << ste2->getId() << endl;
                ap.mergeSTEs(ste1, ste2);
            } else {
                next_workq.push(ste2);
            }
        }

        // now that we've considered an ste, make sure we consider its outputs
        vector<STE *> outputSTEs;
        for(auto e : ste1->getOutputSTEPointers()) {
            STE * child = static_cast<STE*>(e.first);
            if(!child->isMarked()){
                child->mark();
                outputSTEs.push_back(child);
            }
        }

        //
        commonPathMerge(ap, outputSTEs);

        // fill workq with whatever was in next_workq
        while(!next_workq.empty()){
            workq.push(next_workq.front());
            next_workq.pop();
        }
    }
}

/**
 * Converts a byte-level STE to a left/right compressed trie of bit-level STEs.
 *   Returns a pair of pairs of STEs where the first pair is both 0/1 entry STEs and d
 *   the second pair is both 0/1 exit STEs.
 */
pair<pair<STE*,STE*>, pair<STE*,STE*>> byteSTEToBitTrie(Automata &ap, uint32_t *id_counter, STE *ste, uint32_t bits_used) {
    
    STE *zero_head = NULL;
    STE *one_head = NULL;

    vector<STE*> ends;
    for(uint32_t i = 0; i < 256 ; i++){
        // if the char is in the bitset of the STE, add it to the trie
        if(ste->match(i)){
            STE *end;
            end = addCharToBitTrie(ap, id_counter, i, &zero_head, &one_head, bits_used);
            if(end != NULL)
                ends.push_back(end);
        }
    }

    // Once the trie is generated, it is perfectly left merged
    // We can actually right merge these too because they all sink to the same
    vector<STE*> result_ends;
    uint32_t size = 0;
    while(size != ap.getElements().size()){
        cout << "SIZE: " << size << endl;
        size = ap.getElements().size();
        ap.unmarkAllElements();
        result_ends = rightMerge(ap, ends);
    }

    
    // get the end pair
    STE *end_zero = NULL;
    STE *end_one = NULL;
    cout << "ENDS: " << endl;
    for(STE * end : result_ends) {
        cout << end->getId() << endl;
        if(end->match(0)){
            end_zero = end;
        }else{
            end_one = end;
        }
    }
    pair<STE*, STE*> end_pair = make_pair(end_zero, end_one);

    // get the start pair
    vector<STE*> result_starts;
    pair<STE*,STE*> start_pair = make_pair(zero_head, one_head);

    return make_pair(start_pair, end_pair);
}

/**
 *
 */
pair<STE *, STE*> makeExactMatchChar(Automata &ap, uint32_t *id_counter, vector<string> &charsets) {

    STE *head;
    STE *tail;
    STE *last_ste;

    for( int i = 0; i < charsets.size(); i++) {
        STE * new_ste = new STE(getNextId(id_counter), charsets[i], "none");

        if(i == 0) {
            head = new_ste;
            ap.rawAddSTE(head);
            last_ste = head;
        }else if(i == charsets.size() - 1) {
            tail = new_ste;
            ap.rawAddSTE(tail);
            ap.addEdge(last_ste, tail);
            last_ste = tail;
        }else{
            ap.rawAddSTE(new_ste);
            ap.addEdge(last_ste, new_ste);
            last_ste = new_ste;
        }
    }

    return make_pair(head,tail);
}

/**
 * 
 */
vector<pair<STE*,STE*> > makeExactMatchStrings(Automata &a, uint32_t *id_counter, vector<vector<string>> strings) {

    vector<pair<STE*,STE *>> handles;
    
    for(vector<string> s : strings) {
        handles.push_back(makeExactMatchChar(a, id_counter, s));
    }

    return handles;
}

/**
 * 
 */
void connectSTEs(Automata &ap, STE *head, STE*tail) {

    if(head != NULL) {
        if(tail != NULL){
            ap.addEdge(head, tail);
        }
    }
}

/**
 * Connect handle to STE
 */
void connectHandleToSTE(Automata &ap, pair<STE*, STE*> handle, STE* ste) {

    connectSTEs(ap, handle.first, ste);
    connectSTEs(ap, handle.second, ste);
}

/**
 * Connects all STEs in tail handle to all STEs in head handle
 */
void connectHandles(Automata &ap, pair<STE*,STE*> head_handle, pair<STE*,STE*> tail_handle) {
    
    connectHandleToSTE(ap, head_handle, tail_handle.first);
    connectHandleToSTE(ap, head_handle, tail_handle.second);
}

/**
 *
 */
void setHandleStart(pair<STE *,STE*> handle, string start) {
    if(handle.first != NULL)
        handle.first->setStart(start);
    if(handle.second != NULL)
        handle.second->setStart(start);
}

/**
 *
 */
void setHandleReport(pair<STE *,STE*> handle, string report_code) {
    if(handle.first != NULL){
        handle.first->setReporting(true);
        handle.first->setReportCode(report_code);
    }
    
    if(handle.second != NULL){
        handle.second->setReporting(true);
        handle.second->setReportCode(report_code);
    }
}

/**
 *
 */
pair<pair<STE *, STE*>, pair<STE *, STE*>> makeExactMatchBits(Automata &ap, uint32_t *id_counter, vector<string> &charsets) {

    pair<STE*, STE*> head_handle;
    pair<STE*, STE*> tail_handle;

    for( int i = 0; i < charsets.size(); i++) {

        // generate a new STE from the char
        STE * new_ste = new STE(getNextId(id_counter), charsets[i], "none");

        // convert this STE to a minimized bit-trie
        pair<pair<STE*,STE*>,pair<STE*,STE*>> handle = byteSTEToBitTrie(ap,
                                                                        id_counter,
                                                                        new_ste,
                                                                        8);
        // update return "handles" which point to entry and exit 0/1 bits
        if(i == 0) {
            head_handle = handle.first;
            tail_handle = handle.second;
            
        }else{
            // add all-to-all edges between handles
            connectHandles(ap, tail_handle, handle.first);
            // update tail handle to reflect new tail
            tail_handle = handle.second;
        }
    }

    return make_pair(head_handle, tail_handle);
}


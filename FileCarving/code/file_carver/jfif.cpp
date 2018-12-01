#include "automata.h"
#include "util.h"

using namespace std;

//
pair<STE*,STE*> addSOI(Automata &a, uint32_t *id_counter);
pair<STE*, STE*> addJFIFAPP0Marker(Automata &a, uint32_t *id_counter, pair<STE*, STE*>);
pair<STE*, STE*> addSOSMarker(Automata &a, uint32_t *id_counter);
pair<STE*, STE*> addEOIMarker(Automata &a, uint32_t *id_counter);
//


/**
 *
 */
void addJFIFSigs(Automata &a, uint32_t *id_counter) {

    //
    pair<STE*,STE*> handle;

    // Bit-level description
    handle = addSOI(a, id_counter);
    handle = addJFIFAPP0Marker(a, id_counter, handle);
    
    handle.second->setReporting(true);
    handle.second->setReportCode("JFIF_HEADER");

    // In practtice, these footers trigger waaaay too many false positives
    //   to be useful. Better strategy is just to move these patterns to post
    //   processing after headers are identified.
    /*
    handle = addSOSMarker(a, id_counter);
    handle.second->setReporting(true);
    handle.second->setReportCode("JFIF_SOS");

    handle = addEOIMarker(a, id_counter);
    handle.second->setReporting(true);
    handle.second->setReportCode("JFIF_EOI");
    */
    
    // clean up
    a.finalizeAutomata();
}

/**
 *
 */
pair<STE*, STE*> addSOSMarker(Automata &a, uint32_t *id_counter) {

    pair<STE*, STE*> ret_handle;
    
    vector<string> chars;
    chars.push_back("[\\xff]");
    chars.push_back("[\\xda]"); // 
    pair<STE*, STE*> handle = makeExactMatchChar(a, id_counter, chars);
    handle.first->setStart("all-input");

    return handle;
}

/**
 *
 */
pair<STE*, STE*> addEOIMarker(Automata &a, uint32_t *id_counter) {

    pair<STE*, STE*> ret_handle;
    
    vector<string> chars;
    chars.push_back("[\\xff]");
    chars.push_back("[\\xd9]"); // 
    pair<STE*, STE*> handle = makeExactMatchChar(a, id_counter, chars);
    handle.first->setStart("all-input");

    return handle;
}

/**
 *
 */
pair<STE*, STE*> addSOI(Automata &a, uint32_t *id_counter) {

    vector<string> chars = {"[\\xff]", "[\\xd8]"};
    pair<STE*, STE*> handle = makeExactMatchChar(a, id_counter, chars);
    handle.first->setStart("all-input");

    return handle;
}

/**
 *
 */
pair<STE*, STE*> addJFIFAPP0Marker(Automata &a, uint32_t *id_counter, pair<STE*, STE*> in_handle) {

    pair<STE*, STE*> ret_handle;
    
    vector<string> chars;
    chars.push_back("[\\xff]");
    chars.push_back("[\\xe0]"); // APP 0 Marker

    chars.push_back("*");
    chars.push_back("*"); // length of segment

    chars.push_back("[\\x4a]"); 
    chars.push_back("[\\x46]");
    chars.push_back("[\\x49]"); 
    chars.push_back("[\\x46]");
    chars.push_back("[\\x00]"); // Identifier

    chars.push_back("[\\x01\\x02]"); // first byte major version
    chars.push_back("[\\x00-\\x02]"); // second byte minor version

    pair<STE*, STE*> tmp_handle = makeExactMatchChar(a, id_counter, chars);
    
    ret_handle.first = tmp_handle.first;
    a.addEdge(in_handle.second, ret_handle.first);

    // pixel density must not be zero
    STE *first_nozero = new STE(getNextId(id_counter), "[^\\x00]", "none");
    a.rawAddSTE(first_nozero);
    STE *first_zero =  new STE(getNextId(id_counter), "[\\x00]", "none");
    a.rawAddSTE(first_zero);
    STE *second_nozero=  new STE(getNextId(id_counter), "[^\\x00]", "none");
    a.rawAddSTE(second_nozero);
    STE *second_any=  new STE(getNextId(id_counter), "*", "none");
    a.rawAddSTE(second_any);


    //    a.addEdge(re
    a.addEdge(tmp_handle.second, first_nozero);
    a.addEdge(tmp_handle.second, first_zero);
    
    // if first is not zero, second can be anything
    a.addEdge(first_nozero, second_any);
    //
    a.addEdge(first_zero, second_nozero);

    //
    STE *xthumb = new STE(getNextId(id_counter), "*", "none");
    a.rawAddSTE(xthumb);
    STE *ythumb = new STE(getNextId(id_counter), "*", "none");
    a.rawAddSTE(ythumb);

    a.addEdge(second_any, xthumb);
    a.addEdge(second_nozero, xthumb);
    a.addEdge(xthumb, ythumb);

    ret_handle.second = xthumb;
    
    return ret_handle;
}

#include "automata.h"
#include "util.h"

using namespace std;

//
vector<STE*> addBoxTypes(Automata &a, uint32_t *id_counter);
pair<STE*,STE*> addBoxType(Automata &a, uint32_t *id_counter, string box_type, bool start, bool report);
pair<STE*, STE*> addBoxSize(Automata &a, uint32_t *id_counter);
void addStreamID(Automata &a, uint32_t *id_counter, STE *connector, string byte, string report_code);
//

void addStreamID(Automata &a, uint32_t *id_counter, STE *connector, string byte, string report_code) {

    STE *ste = new STE(getNextId(id_counter), byte, "none");
    a.rawAddSTE(ste);
    a.addEdge(connector, ste);
    ste->setReporting(true);
    ste->setReportCode(report_code);
}

/**
 *
 */
void addMPEG2Sigs(Automata &a, uint32_t *id_counter){

    // Sources:
    // http://www.cs.columbia.edu/~delbert/docs/Dueck%20--%20MPEG-2%20Video%20Transcoding.pdf
    // http://dvd.sourceforge.net/dvdinfo/mpeghdrs.html
    
    vector<string> chars;
    // start code prefix 24 bits
    chars.push_back("\\x00");
    chars.push_back("\\x00");
    chars.push_back("\\x01");
    pair<STE*,STE*> handle = makeExactMatchChar(a, id_counter, chars);

    handle.first->setStart("all-input");
    //handle.second->setReporting(true);
    //handle.second->setReportCode("MPEG2_start_sequence");

    STE *ste = handle.second;
    
    addStreamID(a, id_counter, ste, "\\xb3", "MPEG2_vid_header");
    //addStreamID(a, id_counter, ste, "\\xb5", "MPEG2_ext_start");
    //addStreamID(a, id_counter, ste, "\\xb8", "MPEG2_gop_header");
    addStreamID(a, id_counter, ste, "\\xb7", "MPEG2_seq_end");
    addStreamID(a, id_counter, ste, "\\xb9", "MPEG2_program_end");
    //addStreamID(a, id_counter, ste, "\\x00", "MPEG2_pic_header");
    //addStreamID(a, id_counter, ste, "[\\xe0-\\xef]", "MPEG2_vid_stream");
    //addStreamID(a, id_counter, ste, "\\xba", "MPEG2_pack_header");
    // must follow first pack header of program stream
    addStreamID(a, id_counter, ste, "\\xbb", "MPEG2_system_header");
    addStreamID(a, id_counter, ste, "\\xbe", "MPEG2_padding_stream");
}


/**
 *
 */
void addMPEG4Sigs(Automata &a, uint32_t *id_counter) {

    //

    pair<pair<STE*,STE*>,STE*> handle;


    // ftyp is a base tag
    handle = add4GatedMatcher(a, id_counter, "ftyp");
    handle.first.first->setStart("all-input");
    handle.second->setReporting(true);
    handle.second->setReportCode("MPEG4_FTYP");

    pair<pair<STE*,STE*>,STE*> moov_handle;
    moov_handle = add4GatedMatcher(a, id_counter, "moov");
    a.addEdge(handle.second, moov_handle.first.first);
    a.addEdge(handle.second, moov_handle.first.second);
    moov_handle.second->setReporting(true);
    moov_handle.second->setReportCode("MPEG4_FTYP_MOOV");

    pair<pair<STE*,STE*>,STE*> mvhd_handle = add4GatedMatcher(a, id_counter, "mvhd");
    a.addEdge(moov_handle.second, mvhd_handle.first.first);
    a.addEdge(moov_handle.second, mvhd_handle.first.second);
    mvhd_handle.second->setReporting(true);
    mvhd_handle.second->setReportCode("MPEG4_FTYP_MOOV_MVHD");

    pair<pair<STE*,STE*>,STE*> trak_handle = add4GatedMatcher(a, id_counter, "trak");
    a.addEdge(moov_handle.second, trak_handle.first.first);
    a.addEdge(moov_handle.second, trak_handle.first.second);
    trak_handle.second->setReporting(true);
    trak_handle.second->setReportCode("MPEG4_FTYP_MOOV_TRAK");
    
    /*
    handle = addBoxType(a, id_counter, "ftyp", true, true);

    handle = addBoxType(a, id_counter, "moov", true, true);
    handle = addBoxType(a, id_counter, "mvhd", true, true);
    handle = addBoxType(a, id_counter, "meta", true, true);
    handle = addBoxType(a, id_counter, "hdlr", true, true);

    handle = addBoxType(a, id_counter, "trak", true, true);
    handle = addBoxType(a, id_counter, "tkhd", true, true);
    */
    
    // clean up
    a.finalizeAutomata();
}


pair<STE*,STE*> addBoxType(Automata &a, uint32_t *id_counter, string box_type, bool start, bool report) {

    vector<string> chars;
    for(int i = 0; i < box_type.size(); i++){
        cout << box_type.substr(i,1) << endl;
        chars.push_back(box_type.substr(i,1));
    }
    pair<STE*,STE*> handle = makeExactMatchChar(a, id_counter, chars);

    if(start)
        handle.first->setStart("all-input");
    if(report){
        handle.second->setReporting(true);
        handle.second->setReportCode("BOXTYPE_" + box_type);
    }
    
    //
    return handle;
}


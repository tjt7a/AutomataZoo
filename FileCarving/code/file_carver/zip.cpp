/**
 * https://users.cs.jmu.edu/buchhofp/forensics/formats/pkzip.html
 */

#include "automata.h"
#include "util.h"

using namespace std;

//
//

//
pair<STE*,STE*> addEndCentralDirectoryHeader(Automata &, uint32_t *);
pair<STE*,STE*> addLocalFileHeader(Automata &, uint32_t *);
pair<STE*,STE*> addVersionMadeBy(Automata &, uint32_t *, pair<STE*,STE*>);
pair<STE*,STE*> addVNTE(Automata &, uint32_t *, pair<STE*,STE*>);
pair<STE*,STE*> addGenPurpBitFlag(Automata &, uint32_t *, pair<STE*,STE*>);
pair<STE*,STE*> addCompressionMethod(Automata &, uint32_t *, pair<STE*,STE*>);
pair<STE*,STE*> addLastModFileTime(Automata &, uint32_t *, pair<STE*,STE*>);
//
pair<STE*,STE*> addCentralDirectoryHeader(Automata &, uint32_t *);


/**
 *
 */
Automata* genZIPSig(uint32_t *id_counter) {

    Automata *ap = new Automata();
    
    //
    pair<STE*,STE*> tail_handle;

    // Bit-level description
    tail_handle = addLocalFileHeader(*ap, id_counter);
    setHandleReport(tail_handle, "ZIP_Local_File_Header");

    // Bit-level description
    tail_handle = addCentralDirectoryHeader(*ap, id_counter);
    setHandleReport(tail_handle, "ZIP_Central_Directory_Header");

    // Convert to byte level description
    
    Automata *ap2 = ap->twoStrideAutomata();
    Automata *ap4 = ap2->twoStrideAutomata();
    Automata *ap8 = ap4->twoStrideAutomata();

    ap = ap8;
        
    // Byte-level description
    pair<STE*,STE*> handle = addEndCentralDirectoryHeader(*ap, id_counter);
    handle.second->setReporting(true);
    handle.second->setReportCode("ZIP_END_Central_Dir_Header");
    
    // clean up
    ap->finalizeAutomata();

    return ap;
}


/**
 * Returns the first and last STEs in this exact match signature
 */
pair<STE*, STE*> addEndCentralDirectoryHeader(Automata &a, uint32_t *id_counter) {

    // add zip sig
    vector<string> chars;
    chars.push_back("\\x50");
    chars.push_back("\\x4b");
    chars.push_back("\\x05");
    chars.push_back("\\x06");

    // THE REST OF THE END CDH DATA IS NON-SPECIFIC (basically just all stars)
    
    pair<STE*,STE*> handle = makeExactMatchChar( a, id_counter, chars);
    handle.first->setStart("all-input");

    return handle;


}

/**
 *
 */
pair<STE*, STE*> addCentralDirectoryHeader(Automata &ap, uint32_t *id_counter) {

    vector<string> chars;
    chars.push_back("\\x50");
    chars.push_back("\\x4b");
    chars.push_back("\\x01");
    chars.push_back("\\x02");
    auto handles = makeExactMatchBits(ap, id_counter, chars);
    
    pair<STE *, STE *> head_handle = handles.first;
    pair<STE *, STE *> tail_handle = handles.second;
    
    // Set the head of the handle to be a streaming start
    setHandleStart(head_handle, "all-input");

    tail_handle = addVersionMadeBy(ap, id_counter, tail_handle);
    tail_handle = addVNTE(ap, id_counter, tail_handle);
    return tail_handle;
}

/**
 *
 */
pair<STE*,STE*> addVersionMadeBy(Automata &ap, uint32_t *id_counter, pair<STE*,STE*> parent_handle) {

    // add zip spec version (currently just star)
    STE * ste1 = new STE(getNextId(id_counter), "*", "none");
    auto handle = byteSTEToBitTrie(ap, id_counter, ste1, 8);
    pair<STE*, STE*> head_handle = handle.first;
    pair<STE*, STE*> tail_handle = handle.second;
    connectHandles(ap, parent_handle, head_handle);

    // add upper byte compatibility
    STE * ste2 = new STE(getNextId(id_counter), "[\\x00-\x13]", "none");
    handle = byteSTEToBitTrie(ap, id_counter, ste2, 8);
    pair<STE*, STE*> head_handle2 = handle.first;
    pair<STE*, STE*> tail_handle2 = handle.second;
    connectHandles(ap, tail_handle, head_handle2);

    return tail_handle2;
}

/**
 *
 */
pair<STE*,STE*> addLocalFileHeader(Automata &ap, uint32_t *id_counter) {

    vector<string> chars;
    chars.push_back("\\x50");
    chars.push_back("\\x4b");
    chars.push_back("\\x03");
    chars.push_back("\\x04");
    auto handles = makeExactMatchBits(ap, id_counter, chars);

    pair<STE *, STE *> head_handle = handles.first;
    pair<STE *, STE *> tail_handle = handles.second;
    
    // Set the head of the handle to be a streaming start
    setHandleStart(head_handle, "all-input");

    return addVNTE(ap, id_counter, tail_handle);
}

/**
 * Adds two bytes
 */
pair<STE*,STE*> addVNTE(Automata &ap, uint32_t *id_counter, pair<STE*,STE*> parent_handle) {

    vector<string> chars;
    chars.push_back("[\\x0a-\\x7f]");

    // in practice this second byte is a little weird
    // technically should be \\x00 but it's tough to find documentation
    //  to coroborate. 
    chars.push_back("*");
    //chars.push_back("[\\x00]");
    pair<pair<STE*,STE*>,pair<STE*,STE*>> handles = makeExactMatchBits(ap, id_counter, chars);

    connectHandles(ap, parent_handle, handles.first);

    //
    return addGenPurpBitFlag(ap, id_counter, handles.second);
}

/**
 *
 */
pair<STE*, STE*> addGenPurpBitFlag(Automata &ap, uint32_t *id_counter, pair<STE*,STE*> parent_handle) {

    //  Bit 0: If set, indicates that the file is encrypted.
    STE *bit_0 = new STE(getNextId(id_counter), "[\\x00\\x01]", "none");
    ap.rawAddSTE(bit_0);
    connectHandleToSTE(ap, parent_handle, bit_0);

    // Bit 1: If the compression method used was type 6,
    // Imploding, then this bit, if set, indicates
    // an 8K sliding dictionary was used.  If clear,
    // then a 4K sliding dictionary was used.
    STE *bit_1 = new STE(getNextId(id_counter), "[\\x00\\x01]", "none");
    ap.rawAddSTE(bit_1);
    connectSTEs(ap, bit_0, bit_1);

    // Bit 2: If the compression method used was type 6,
    // Imploding, then this bit, if set, indicates
    // 3 Shannon-Fano trees were used to encode the
    // sliding dictionary output.  If clear, then 2
    // Shannon-Fano trees were used.
    STE *bit_2 = new STE(getNextId(id_counter), "[\\x00\\x01]", "none");
    ap.rawAddSTE(bit_2);
    connectSTEs(ap, bit_1, bit_2);

    // Bit 3: If this bit is set, the fields crc-32, compressed
    // size and uncompressed size are set to zero in the
    // local header.  The correct values are put in the
    // data descriptor immediately following the compressed
    // data.  (Note: PKZIP version 2.04g for DOS only
    // recognizes this bit for method 8 compression, newer
    // versions of PKZIP recognize this bit for any
    // compression method.)
    STE *bit_3 = new STE(getNextId(id_counter), "[\\x00\\x01]", "none");
    ap.rawAddSTE(bit_3);
    connectSTEs(ap, bit_2, bit_3);

    //  Bit 4: Reserved for use with method 8, for enhanced
    //  deflating.
    STE *bit_4 = new STE(getNextId(id_counter), "[\\x00\\x01]", "none");
    ap.rawAddSTE(bit_4);
    connectSTEs(ap, bit_3, bit_4);

    // Bit 5: If this bit is set, this indicates that the file is
    // compressed patched data.  (Note: Requires PKZIP
    // version 2.70 or greater)
    STE *bit_5 = new STE(getNextId(id_counter), "[\\x00\\x01]", "none");
    ap.rawAddSTE(bit_5);
    connectSTEs(ap, bit_4, bit_5);

    // Bit 6: Strong encryption.  If this bit is set, you MUST
    // set the version needed to extract value to at least
    // 50 and you MUST also set bit 0.  If AES encryption
    // is used, the version needed to extract value MUST
    // be at least 51. See the section describing the Strong
    // Encryption Specification for details.  Refer to the
    // section in this document entitled "Incorporating PKWARE 
    // Proprietary Technology into Your Product" for more
    // information.
    STE *bit_6 = new STE(getNextId(id_counter), "[\\x00\\x01]", "none");
    ap.rawAddSTE(bit_6);
    connectSTEs(ap, bit_5, bit_6);

    // Bit 7: Unused
    STE *bit_7 = new STE(getNextId(id_counter), "\\x00", "none");
    ap.rawAddSTE(bit_7);
    connectSTEs(ap, bit_6, bit_7);

    // Bit 8: Unused
    STE *bit_8 = new STE(getNextId(id_counter), "\\x00", "none");
    ap.rawAddSTE(bit_8);
    connectSTEs(ap, bit_7, bit_8);

    // Bit 9: Unused
    STE *bit_9 = new STE(getNextId(id_counter), "\\x00", "none");
    ap.rawAddSTE(bit_9);
    connectSTEs(ap, bit_8, bit_9);

    // Bit 10: Unused
    STE *bit_10 = new STE(getNextId(id_counter), "\\x00", "none");
    ap.rawAddSTE(bit_10);
    connectSTEs(ap, bit_9, bit_10);

    // Bit 11: Language encoding flag (EFS).  If this bit is set,
    // the filename and comment fields for this file
    // MUST be encoded using UTF-8. (see APPENDIX D)
    STE *bit_11 = new STE(getNextId(id_counter), "[\\x00\\x01]", "none");
    ap.rawAddSTE(bit_11);
    connectSTEs(ap, bit_10, bit_11);

    // Bit 12: Reserved by PKWARE for enhanced compression.
    STE *bit_12 = new STE(getNextId(id_counter), "[\\x00\\x01]", "none");
    ap.rawAddSTE(bit_12);
    connectSTEs(ap, bit_11, bit_12);

    // Bit 13: Set when encrypting the Central Directory to indicate
    // selected data values in the Local Header are masked to
    // hide their actual values.  See the section describing
    // the Strong Encryption Specification for details.  Refer
    // to the section in this document entitled "Incorporating 
    // PKWARE Proprietary Technology into Your Product" for
    // more information.
    STE *bit_13 = new STE(getNextId(id_counter), "[\\x00\\x01]", "none");
    ap.rawAddSTE(bit_13);
    connectSTEs(ap, bit_12, bit_13);

    //  Bit 14: Reserved by PKWARE.
    STE *bit_14 = new STE(getNextId(id_counter), "[\\x00\\x01]", "none");
    ap.rawAddSTE(bit_14);
    connectSTEs(ap, bit_13, bit_14);

    //  Bit 15: Reserved by PKWARE.
    STE *bit_15 = new STE(getNextId(id_counter), "[\\x00\\x01]", "none");
    ap.rawAddSTE(bit_15);
    connectSTEs(ap, bit_14, bit_15);

    // Add compression method
    STE *dummy = NULL;
    return addCompressionMethod(ap, id_counter, make_pair(bit_15, dummy));
}


/**
 *
 */
pair<STE*,STE*> addCompressionMethod(Automata &ap, uint32_t *id_counter, pair<STE*,STE*> parent_handle) {

    vector<string> charsets;
    charsets.push_back("[\\x00-\\x13\\x61\\x62]");
    charsets.push_back("\\x00");
    auto handle = makeExactMatchBits(ap, id_counter, charsets);
    pair<STE*,STE*> head_handle = handle.first;
    pair<STE*,STE*> tail_handle = handle.second;
    connectHandles(ap, parent_handle, head_handle);
    
    //
    return addLastModFileTime(ap, id_counter, tail_handle);
}

/**
 *
 */
pair<STE*, STE*> addLastModFileTime(Automata &ap, uint32_t *id_counter, pair<STE*,STE*> parent_handle) {

    // Add MSDOS date time format (http://www.vsft.com/hal/dostime.htm)

    // first four bits are time in two second intervalse 0-29
    STE *tmp_ste = new STE("doesnt_matter", "[\\x00-\\x1d]", "none");
    auto handle = byteSTEToBitTrie(ap, id_counter, tmp_ste, 5);
    pair<STE*, STE*> head_handle = handle.first;
    pair<STE*, STE*> tail_handle = handle.second;
    connectHandles(ap, parent_handle, head_handle);
    pair<STE*, STE*> next_parent_handle = tail_handle;
    
    // next 6 bits are minutes 0-59
    tmp_ste = new STE("doesnt_matter", "[\\x00-\\x3b]", "none");
    handle = byteSTEToBitTrie(ap, id_counter, tmp_ste, 6);
    head_handle = handle.first;
    tail_handle = handle.second;
    connectHandles(ap, next_parent_handle, head_handle);
    next_parent_handle = tail_handle;

    // next 5 bits are hours 0-23
    tmp_ste = new STE("doesnt_matter", "[\\x00-\\x17]", "none");
    handle = byteSTEToBitTrie(ap, id_counter, tmp_ste, 5);
    head_handle = handle.first;
    tail_handle = handle.second;
    connectHandles(ap, next_parent_handle, head_handle);
    next_parent_handle = tail_handle;

    //
    return tail_handle;
}

#include <algorithm>
#include <fstream>
#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <unordered_map>

//#include "re2/re2.h"
//#include "re2/stringpiece.h"
#include <hs.h>

using namespace std;

unordered_map<unsigned, string> id_map;

// Replaces all occurrences of `from' with `to' in `str'
//
// http://stackoverflow.com/questions/5343190/how-do-i-replace-all-instances-of-a-string-with-another-string
//
size_t replace_all(string& str, const string& from, const string& to) {
    if (from.empty()) return 0;

    size_t count = 0;
    size_t start_pos = 0;
    while ((start_pos = str.find(from, start_pos)) != std::string::npos) {
        str.replace(start_pos, from.length(), to);
        start_pos += to.length(); // in case 'to' contains 'from'
        count += 1;
    }

    return count;
}

// Converts a Prosite pattern to a regular expression
//
// NB - Most of this logic is lifted from ps_scan.pl
//
string prosite_to_regex(const string& pattern) {
    string regex("");
    stringstream ss(pattern);
    string bit;
    bool start_anc = false;
    bool end_anc = false;

    while (getline(ss, bit, '-')) {
        string state("");
        bool neg = false;
        bool start_anc_class = false;
        bool end_anc_class = false;

        if (bit.find("<") == 0) {
            // Start-of-string anchor
            bit = bit.substr(1);
            //start_anc = true;
        }
        if (bit.find(">") == bit.length() - 1) {
            // End-of-string anchor
            bit = bit.substr(0, bit.length() - 1);
            //end_anc = true;
        }

        if (bit[0] == '[') {
            // Character class
            state = bit.substr(1, bit.find(']') - 1);
        }
        else if (bit[0] == '{') {
            // Negated character class
            state = bit.substr(1, bit.find('}') - 1);
            neg = true;
        }
        else {
            // Literal or wildcard
            size_t rep = bit.find('(');
            if (rep == string::npos)
                state = bit;
            else
                state = bit.substr(0, rep);
        }

        // Quantification
        string range("");
        size_t rep_start = bit.find('(');
        if (rep_start != string::npos) {
            range = bit.substr(rep_start + 1, bit.find(')') - rep_start - 1);
        }

        if (state.compare("x") == 0 || state.compare("X") == 0) {
            // Wildcard
            state = ".";
        }
        else {
            // Handle B/Z unsure amino acids 
            if (neg) {
                replace_all(state, "B", "NDB");
                replace_all(state, "Z", "QEZ");
            }
            else {
                if (replace_all(state, "B", "NDB") < 1) {
                    replace_all(state, "N", "NB");
                    replace_all(state, "D", "DB");
                }
                if (replace_all(state, "Z", "QEZ") < 1) {
                    replace_all(state, "Q", "QZ");
                    replace_all(state, "E", "EZ");
                }
                state += "X";
            }
        }

        if (state.find("<") != string::npos) {
            replace_all(state, "<", "");
            //start_anc_class = true;
        }
        if (state.find(">") != string::npos) {
            replace_all(state, ">", "");
            //end_anc_class = true;
        }

        regex += "(";
        if (start_anc_class || end_anc_class)
            regex += "(?:";
        if (state.length() > 1 || neg)
            regex += "[";
        if (neg)
            regex += "^";
        regex += state;
        if (state.length() > 1 || neg)
            regex += "]";
        if (start_anc_class)
            regex += "|^)";
        else if (end_anc_class)
            regex += "|$)";
        if (range.length() > 0)
            regex += "{" + range + "}?"; // FIXME: don't hardcode greedy/ungreedy
        regex += ")";
    }

    if (start_anc)
        regex = '^' + regex;
    if (end_anc)
        regex = regex + '$';

    cout << "/" << regex << "/" << endl;
    return regex;
}



// Parse5Bs a Prosite data file into an array of Motifs
//
// TODO: keep ID and other fields
//
hs_database_t * parse_prosite(const string& motif_file, bool skip_common) {
    
    // Hyperscan database
    hs_database_t *db;
    hs_compile_error_t *compileErr;
    hs_error_t err;

    // String representation of regexes
    vector<string> expressions;

    ifstream ifs(motif_file.c_str(), ifstream::in);
    string line;
    string ac;
    string pattern;
    bool partial = false;
    bool common = false;

    vector<unsigned> ids;
    unsigned counter = 0;
    while (getline(ifs, line)) {
        
        if (line.find("AC ") == 0) {
            ac = line.substr(5, line.find(";") - 5);

            // Reset state variables
            pattern.clear();
            partial = false;
            common = false;
        }
        else if (line.find("PA ") == 0) {
            if (partial) {
                pattern += line.substr(5);
            }
            else {
                pattern = line.substr(5);
                partial = true;
            }
        }
        else {
            partial = false;
        }

        if (line.find("/SKIP-FLAG=TRUE") != string::npos) {
            common = true;
        }

        if (pattern.length() > 0 && !partial && line.compare("//") == 0) {
            if (!(common && skip_common)) {
                // Strip final '.' from pattern
                pattern = pattern.substr(0, pattern.length() - 1);
                expressions.push_back(prosite_to_regex(pattern));
                ids.push_back(counter);
                id_map[counter] = ac;
                counter++;
            }
        }
    }

    // Turn our vector of strings into a vector of char*'s to pass in to
    // hs_compile_multi. (This is just using the vector of strings as dynamic
    // storage.)
    vector<unsigned> flags;
    vector<const char*> cstrPatterns;
    for (const auto &pat : expressions) {
        cstrPatterns.push_back(pat.c_str());
    }

    // Compile expressions in database
    err = hs_compile_multi(cstrPatterns.data(), 
                           flags.data(), 
                           ids.data(),
                           cstrPatterns.size(), 
                           HS_MODE_BLOCK, 
                           nullptr, 
                           &db, 
                           &compileErr);


    // Compilation error check
    if (err != HS_SUCCESS) {
        if (compileErr->expression < 0) {
            // The error does not refer to a particular expression.
            cerr << "ERROR: " << compileErr->message << endl;
        } else {
            cerr << "ERROR: Pattern '" << expressions[compileErr->expression]
                 << "' failed compilation with error: " << compileErr->message
                 << endl;
        }

        // As the compileErr pointer points to dynamically allocated memory, if
        // we get an error, we must be sure to release it. This is not
        // necessary when no error is detected.
        hs_free_compile_error(compileErr);
        exit(-1);
    }

    return db;
}

static
int onMatch(unsigned int id, unsigned long long from, unsigned long long to,
            unsigned int flags, void *ctx) {
    
    //cout << "MATCHED" << endl;
    // Our context points to a size_t storing the match count
    size_t *matches = (size_t *)ctx;
    (*matches)++;
    cout << to << "\t" << id_map[id] << endl;
    return 0; // continue matching
}

// Scans all sequences in `sequence_file' against all motif patterns from `motifs'
void scan_sequences(const string& sequence_file, hs_database_t *db) {

    // Count of matches found during scanning
    size_t matchCount = 0;

    // Allocate hyperscan scratch
    hs_scratch_t *scratch = nullptr;
    hs_error_t err = hs_alloc_scratch(db, &scratch);
    if (err != HS_SUCCESS) {
        cerr << "ERROR: could not allocate scratch space. Exiting." << endl;
        exit(-1);
    }

    // Open input file
    ifstream ifs(sequence_file.c_str(), ifstream::in);
    string line;
    string id;

    while (getline(ifs, line)) {

        // Skip identifier lines
        if (line[0] == '>') {
            // E.g., >sp|Q02505|MUC3A_HUMAN Mucin-3A OS=Homo sapiens GN=MUC3A PE=1 SV=2
            id = line.substr(1, line.find(' ') - 1);
            continue;
        }

        //cout << line << endl;
        // Hyperscan search packet for all patterns in db
        err = hs_scan(db,
                line.c_str(),
                line.length(),
                0,
                scratch,
                onMatch,
                &matchCount);
    
        if (err != HS_SUCCESS) {
            cerr << "ERROR: Unable to scan packet. Exiting." << endl;
            exit(-1);
        }
        
    }

    //cout << "Number of matches: " << matchCount << endl;
}

// TODO: Process command line arguments
//   prosite file (default: prosite.dat)
//   uniprot sequence file (default: uniprot.fasta)
//   output format (default: pff)
//   greedy? (default: false)
//   skip common sigs? (default: true)
//   max x (default: 1)
//
int main(int argc, char* argv[]) {
    string motif_file = "prosite.dat";
    string sequence_file = "uniprot.fasta";

    if (argc == 3) {
        motif_file = argv[1];
        sequence_file = argv[2];
    }else{
        cout << "USAGE: ./ps_scan <motif_file> <sequence_file>" << endl;
        exit(1);
    }

    cerr << "motif_file = " << motif_file << endl;
    cerr << "sequence_file = " << sequence_file << endl;

    // Parse Prosite file into regular expression database
    hs_database_t *db = parse_prosite(motif_file, true);
    
    // Scan all input sequences against all motifs in the database
    //scan_sequences(sequence_file, db);

    return 0;
}

// vim: nu:et:ts=4:sw=4:fdm=syntax

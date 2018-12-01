#ifndef FC_UTIL_H
#define FC_UTIL_H

struct handle {
    STE *zero;
    STE *one;
};

typedef struct handle handle_t;

//
std::string getNextId(uint32_t *);

// char level helpers
std::pair<STE*,STE*> makeExactMatchChar(Automata &, uint32_t *, std::vector<std::string> &);
STE * addCharToBitTrie(Automata &, uint32_t *, uint32_t , STE **, STE **, uint32_t);
std::vector<std::pair<STE*,STE*>> makeExactMatchStrings(Automata &a, uint32_t *, std::vector<std::vector<std::string> >);

// bit level helpers
std::pair<std::pair<STE *, STE*>, std::pair<STE *, STE*>> makeExactMatchBits(Automata &, uint32_t *, std::vector<std::string> &);
std::vector<std::string> chars2bits(std::vector<std::string> c);
std::vector<std::string> char2bits(std::string c);
std::pair<std::pair<STE*,STE*>, std::pair<STE*,STE*>> byteSTEToBitTrie(Automata &, uint32_t *, STE*, uint32_t);

// structures
std::pair<std::pair<STE*,STE*>, STE*> add4GatedMatcher(Automata &, uint32_t *, std::string);

// automata helpers
void connectSTEs(Automata &, STE*, STE*);
void connectHandleToSTE(Automata &, std::pair<STE*, STE*>, STE *);
void connectHandles(Automata &, std::pair<STE*, STE*>, std::pair<STE*, STE*>);
void setHandleStart(std::pair<STE*, STE*>, std::string);
void setHandleReport(std::pair<STE*, STE*>, std::string);
std::vector<STE*> rightMerge(Automata &, std::vector<STE*>);
void commonPathMerge(Automata &, std::vector<STE*>);
 
#endif

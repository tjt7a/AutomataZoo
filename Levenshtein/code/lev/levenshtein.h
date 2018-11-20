#ifndef LEV_H
#define LEV_H
#include "automata.h"
#include <string>

void genLevenshtein(Automata *a,
                    uint32_t pattern_id,
                    std::string pattern,
                    uint32_t edit_distance,
                    bool restricted);
#endif

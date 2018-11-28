#ifndef HAM_H
#define HAM_H
#include "automata.h"
#include <string>

void genHamming(Automata *a,
                uint32_t pattern_id,
                std::string pattern,
                uint32_t ham_distance,
                bool restricted);
#endif

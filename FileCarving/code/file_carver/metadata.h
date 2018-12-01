#ifndef FC_METADATA_H
#define FC_METADATA_H


std::pair<STE*, STE*> addSSNs(Automata &, uint32_t *);
void addCCNs(Automata &, uint32_t *);
void addEmails(Automata &, uint32_t *);
//pair<STE*, STE*> addWebsites(Automata &, uint32_t *);  
#endif

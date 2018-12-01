/**
 *
 */
#include "automata.h"
#include "zip.h"
#include "jfif.h"
#include "metadata.h"
#include "mpeg.h"

using namespace std;

int main(int argc, char * argv[]) {

    //
    Automata *ap = new Automata();
    uint32_t id_counter = 0;

    Automata *zip_sig = genZIPSig(&id_counter);
    ap = zip_sig;

    addSSNs(*ap, &id_counter);
    addCCNs(*ap, &id_counter);
    addEmails(*ap, &id_counter);
    addJFIFSigs(*ap, &id_counter);
    addMPEG2Sigs(*ap, &id_counter);
    addMPEG4Sigs(*ap, &id_counter);
    
    ap->automataToANMLFile("file_carver.anml");
}

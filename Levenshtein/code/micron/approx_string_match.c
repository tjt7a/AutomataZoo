// Sample application for approximate string matching.
// References:
// Baeza-Yates, R., and Navarro, G. Faster Approximate String Matching. 
// Algorithmica, 23:127-158, 1999.
// See README.txt

#include <micron/ap/sys/platform.h>
#include <micron/ap/ap_defs.h>
#include <micron/ap/ap_compile.h>
#include <micron/ap/ap_anml.h>
#include <micron/ap/ap_error.h>
#include <micron/ap/ap_load.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#if defined(LINUX32) || defined(LINUX64)
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#endif

static unsigned EDIST = 1;
static unsigned WIDTH = 8;
static unsigned NUM_WIDGETS = 1;

#ifndef	min
#define	min(a,b)	(((a)>(b))?(b):(a))
#endif

static void usage(void);

static void __exit_on_error(int test, unsigned line, const char* msg)
{
    if (test){
        fprintf(stdout, "Error on line %d: %s\n", line, msg);
        usage();
        exit(1);
    }

}
#define	exit_on_error(test, msg)	__exit_on_error((test), __LINE__, msg)


// Example indexing for WIDTH=6, EDIST=3
//    m= 00 01 02 03 04 05 | mid
// ----+-------------------+-----
// k=0 |  0  1  2 -1 -1 -1 | 0
//     | -1 12 13 14 -1 -1 | 1
// k=1 | -1  3  4  5 -1 -1 | 0
//     | -1 -1 15 16 17 -1 | 1
// k=2 | -1 -1  6  7  8 -1 | 0
//     | -1 -1 -1 18 19 20 | 1
// k=3 | -1 -1 -1  9 10 11 | 0
static int index_of(unsigned m, unsigned k, int mid)
{
    exit_on_error(m < 0 || m >= WIDTH, "m >= WIDTH");
    exit_on_error(k < 0 || k > EDIST, "k > EDIST");
    exit_on_error(m < (k + mid) || m >= (k + WIDTH - EDIST + mid), "bad index_of");
    return mid*(EDIST + 1)*(WIDTH-EDIST) + k*(WIDTH-EDIST) + (m-k-mid);
}


// Handle Windows and Linux file descriptors
// Note: ANSI C int file descriptor support cannot be exported in win dll.
#if defined(WIN32) || defined(WIN64) || defined(_WIN64)
#define	close_file	CloseHandle
static file_descriptor_t open_file(const char* filename)
{
    file_descriptor_t fd;
    fd = CreateFileA(filename, GENERIC_WRITE, 0, 0, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, 0);
    exit_on_error(fd == INVALID_HANDLE_VALUE, "cannot create output file");
    return fd;
}
#else
#define	close_file	close
static file_descriptor_t open_file(const char* filename)
{
    file_descriptor_t fd;
    fd = open(filename, O_WRONLY|O_CREAT|O_TRUNC, S_IRUSR|S_IRGRP|S_IROTH|S_IWUSR);
    exit_on_error(fd < 0, "cannot create output file");
    return fd;
}
#endif


static void usage(void)
{
    printf("Levenshtein example application.\n");
    printf("Create an automaton to match a string within an error threshold.\n");
    printf("Use apemulate to test the automaton against input data.\n");
    printf("Usage: approx_string_match [options] <string to match>\n");
    printf("  --edist=<error threshold>: sets the maximum levenshtein distance, defaults to 1\n");
    printf("  --width=<width of strings>: sets the width for each query string\n");
    printf("  --number=<num widgets>: sets the number of widgets to emit\n");
    printf("  --output=<filename>: sets the output automaton file name, defaults to output.anml\n");
    printf("  -v|--verbose: prints debug messages\n");
    printf("  -h|--help: prints this message\n");
    exit(0);
}


int main(int argc, char* argv[])
{
    if(argc == 1)
        usage();

    static char	output_file[256] = { "output.anml" };
    char*		pattern;
    unsigned	options = AP_OPT_MT;
    int			i;
    unsigned k, m, mend;
    ap_anml_t	anml;		// workspace
    ap_anml_network_t bpd;	// bit-parallel diagonal structure
    ap_automaton_t amta;	// compiled automaton
    // Use platform independent type defined in micron/ap/sys/platform.h
    file_descriptor_t fd;
    ap_anml_element_ref_t* vmap;

    // Parse command line options
    for (i=1; i<argc; ++i){
        if (1 == sscanf(argv[i], "--edist=%u", &EDIST))
            continue;
        if (1 == sscanf(argv[i], "--width=%u", &WIDTH))
            continue;
        if (1 == sscanf(argv[i], "--number=%u", &NUM_WIDGETS))
            continue;
        if (1 == sscanf(argv[i], "--output=%s", output_file))
            continue;
        if (0 == strcmp(argv[i], "--help") || 0 == strcmp(argv[i], "-h"))
            usage();
        if (0 == strcmp(argv[i], "--verbose") || 0 == strcmp(argv[i], "-v"))
            {
                options |= AP_OPT_SHOW_MESSAGE|AP_OPT_SHOW_DEBUG;
                continue;
            }
        break;
    }
    
    exit_on_error((argc-i) != 0, "extra arguments!");

    vmap = calloc(NUM_WIDGETS*(WIDTH-EDIST)*(2*EDIST+1), sizeof(ap_anml_element_ref_t));

    // Create ANML object for building BPD graph
    anml = AP_CreateAnml();
    exit_on_error(!anml, "AP_CreateAnml() failed");
    exit_on_error(0 > AP_CreateAutomataNetwork(anml, &bpd, NULL),
                  "AP_CreateAutomataNetwork() failed");

    pattern = calloc(WIDTH,sizeof(char));

    time_t t;
    srand((unsigned) time(&t));

    // Loop over number of levenshtein widgets
    for(i = 0; i < NUM_WIDGETS; ++i){

        // Fill pattern with new random string sequence
        unsigned c;
        for(c = 0; c < WIDTH; c++){
        
            unsigned val = (rand() % 4);
            switch(val) {
            case 0 :
                pattern[c] = 'a';
                break;
            case 1 :
                pattern[c] = 't';
                break;
            case 2 :
                pattern[c] = 'g';
                break;
            default:
                pattern[c] = 'c';
                break;
            }
        }

        for(c = 0; c < WIDTH; c++){
            printf("%c", pattern[c]);
        }
        printf("\n");

        EDIST = min(EDIST, WIDTH-1);

	// Add vertices for non-mid elements
	for (k=0; k<=EDIST; ++k)
            {
		for (m=k, mend=WIDTH-EDIST+k; m<mend; ++m)
                    {
			int n = index_of(m, k, 0);
			struct ap_anml_element element;
			char symbols[2] = {0};

			symbols[0] = pattern[m];
			memset(&element, 0, sizeof(element));
			element.res_type = RT_STE;
			element.symbols = symbols;
			element.start = (m == k)? ALL_INPUT: NO_START;
			element.match = (WIDTH - m + k - 1) <= EDIST;
			if (element.match) element.report_code = 1;
			exit_on_error(0 > AP_AddAnmlElement(bpd, &vmap[n], &element), 
                                      "AP_AddAnmlElement() failed");
                    }
            }

	// Add vertices for mid elements
	for (k=0; k<EDIST; ++k)
            {
		for (m=k+1, mend=WIDTH-EDIST+k; m<mend; ++m)
                    {
			int n = index_of(m, k, 1);
			struct ap_anml_element element;

			memset(&element, 0, sizeof(element));
			element.res_type = RT_STE;
			element.symbols = "*";
			element.start = NO_START;
			element.match = m == (WIDTH - 1);
			if (element.match) element.report_code = 1;
			exit_on_error(0 > AP_AddAnmlElement(bpd, &vmap[n], &element),
                                      "AP_AddAnmlElement() failed");
                    }
            }

	// Add edges to link non-mid elements into a row
	for (k=0; k<=EDIST; ++k)
            {
		for (m=k, mend=WIDTH-EDIST+k-1; m<mend; ++m)
                    {
			int n1 = index_of(m, k, 0);
			int n2 = index_of(m+1, k, 0);
			exit_on_error(0 > AP_AddAnmlEdge(bpd, vmap[n1], vmap[n2], 0), 
                                      "AP_AddAnmlEdge() failed");
                    }
            }

	// Add edges to link rows
	for (k=0; k<EDIST; ++k)
            {
		for (m=k+1, mend=WIDTH-EDIST+k; m<mend; ++m)
                    {
			int rk0_m0 = index_of(m-1, k, 0);
			int rk1_m1 = index_of(m, k+1, 0);
			int rk1_m2 = index_of(m+1, k+1, 0);
			int nk0_m1 = index_of(m, k, 1);
			unsigned r, x, xend;

			//         [a]    [b]    [c]
			// row=k   (m-1)
			//           \     .
			// mid        '--> n ->-.
			//                \|/    \
			// row=k+1 (m-1)  (m)  (m+1)
			//                [b]    [c]

			// substitution + insertion
			exit_on_error(0 > AP_AddAnmlEdge(bpd, vmap[rk0_m0], vmap[nk0_m1], 0),
                                      "AP_AddAnmlEdge() failed");
			// substitution
			exit_on_error(0 > AP_AddAnmlEdge(bpd, vmap[nk0_m1], vmap[rk1_m2], 0),
                                      "AP_AddAnmlEdge() failed");
			// insertion
			exit_on_error(0 > AP_AddAnmlEdge(bpd, vmap[nk0_m1], vmap[rk1_m1], 0),
                                      "AP_AddAnmlEdge() failed");
			if (k < (EDIST-1))
                            {
				int n = index_of(m+1, k+1, 1);
				exit_on_error(n < 0, "bad index");
				// substitution
				exit_on_error(0 > AP_AddAnmlEdge(bpd, vmap[nk0_m1], vmap[n], 0),
                                              "AP_AddAnmlEdge() failed");
				for (r=k+2, x=m+2, xend=WIDTH-EDIST+r; r<=EDIST && x<xend; ++r, ++x)
                                    {
					int n = index_of(x, r, 0);
					exit_on_error(n < 0, "bad index");
					// deletion after substitution
					exit_on_error(0 > AP_AddAnmlEdge(bpd, vmap[nk0_m1], vmap[n], 0),
                                                      "AP_AddAnmlEdge() failed");
                                    }
                            }

			// deletions - epsilon transitions in paper
			for (r=k+1, x=m+1, xend=WIDTH-EDIST+r; r<=EDIST && x<xend; ++r, ++x)
                            {
				int n = index_of(x, r, 0);
				exit_on_error(0 > AP_AddAnmlEdge(bpd, vmap[rk0_m0], vmap[n], 0),
                                              "AP_AddAnmlEdge() failed");
                            }
                    }
            }

    }

    // ANML
    AP_ExportAnml(bpd, output_file,"");

    // Compile
    //free(vmap);
    //exit_on_error(0 > AP_CompileAnml(anml, &amta, 0, 0, 0, options, 0),"AP_CompileAnml() failed");
    // Save output
    //fd = open_file(output_file);
    //exit_on_error(0 > AP_Save(amta, fd), "AP_Save() failed");
    //close_file(fd);
return 0;
}

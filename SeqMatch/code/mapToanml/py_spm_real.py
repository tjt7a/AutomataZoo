# Blocker &  Ending = 255; Transaction Delimiter = 254; Itemset Delimiter = 253; ITemSet = 0:252

from micronap.sdk import *
import argparse
import sys
import os

def def_SPM_8B_macro(item_num, entry_num, sp_dict, name, opt, seq, NC):
    # Initialize the automata network
    e_subhold = []
    i_subhold = []
    p_subhold = []
        
    item_num = item_num+1 #item_num is now item_line_size
    A = Anml()
    name = name+'_8B_'+'%02dX%02d'%(item_num, entry_num)
    if opt:
        name = name+'O'
    if seq:
        name = name+'_seq'
    else:
        name = name+'_set'
    if NC:
        name = name+'_NC'
    else:
        name = name+'_C'
    #print name
    MC = A.CreateMacroDef(anmlId=name)
    
    # Build the network
    ## Elements
    ### Entry elements
    for i in range(entry_num):
        e_id = 'e%02d'%i
        if opt:
            exec("%s = MC.AddSTE(sp_dict['EB'], startType=AnmlDefs.START_OF_DATA, anmlId=e_id)"%(e_id)) #Elaheh
        else:
            exec("%s = MC.AddSTE(sp_dict['EB'], startType=AnmlDefs.ALL_INPUT, anmlId=e_id)"%(e_id))

    ### Place Holder elements
    for i in range(item_num):
        p_id = 'p%02d'%i
        exec("%s = MC.AddSTE(sp_dict['elu'], anmlId=p_id)"%(p_id)) #Elaheh

    ### Item elements
    for i in range(item_num):
        i_id = 'i%02d'%i
        if i == (item_num-1) and NC:
            exec("%s = MC.AddSTE(sp_dict['TD'], anmlId=i_id, match=True)"%(i_id))
        else:
            exec("%s = MC.AddSTE(sp_dict['TD'], anmlId=i_id)"%(i_id))

    if not NC:
        ### Counter elements
        counter = MC.AddCounter(1000, anmlId='Counter')    
        ### Ending report elements
        rep = MC.AddSTE(sp_dict['EB'], match = True, anmlId='Reporter') 
    
    ## Connections
    ### Entry -> position holder ->> item
    
    for i in range(entry_num):
        e_id = 'e%02d'%i
        p_id = 'p%02d'%i
        i_id = 'i%02d'%i
        if opt:
            exec('MC.AddAnmlEdge(%s, %s, 0)'%(p_id, e_id))
        exec('MC.AddAnmlEdge(%s, %s, 0)'%(e_id, p_id))
        exec('MC.AddAnmlEdge(%s, %s, 0)'%(e_id, i_id))

    ### position-> position; position -> item; item-> next item; item-> next position
    for i in range(item_num):
        p_id = 'p%02d'%i
        i_id = 'i%02d'%i
        exec('MC.AddAnmlEdge(%s, %s, 0)'%(p_id, p_id))
        exec('MC.AddAnmlEdge(%s, %s, 0)'%(p_id, i_id))
        if (i+1) < item_num :
            p_next = 'p%02d'%(i+1)
            i_next = 'i%02d'%(i+1)
            exec('MC.AddAnmlEdge(%s, %s, 0)'%(i_id, p_next))
            exec('MC.AddAnmlEdge(%s, %s, 0)'%(i_id, i_next))

    ### last -> counter
    if not NC:
        last_item = 'i%02d'%(item_num-1)
        exec('MC.AddAnmlEdge(%s, counter, 0)'%(last_item))
        MC.AddAnmlEdge(counter, rep, 0)
    
    ## Parameters
    ### Entry
    for i in range(entry_num):
        e_id = 'e%02d'%i
        para_name ='%'+e_id 
        exec('param = MC.AddMacroParam(para_name, %s)'%e_id)
        e_subhold.append(MC.GetMacroParamSubstitutionHolder(param))
    
    ### Place Holder & item
    for i in range(item_num-1):
    # for i in range(item_num):
        i_id = 'i%02d'%i
        p_id = 'p%02d'%i
        p_name ='%'+p_id 
        i_name ='%'+i_id 

        if not seq:
            p_name ='%NTD'
        exec('param_p = MC.AddMacroParam(p_name, %s)'%p_id)
        exec('param_i = MC.AddMacroParam(i_name, %s)'%i_id)
        p_subhold.append(MC.GetMacroParamSubstitutionHolder(param_p))
        i_subhold.append(MC.GetMacroParamSubstitutionHolder(param_i))

    ### Transaction delimiter 
    i_id = 'i%02d'%(item_num-1)
    p_id = 'p%02d'%(item_num-1)
    p_name ='%NTD'
    i_name ='%TD'
    exec('MC.AddMacroParam(p_name, %s)'%p_id)
    exec('MC.AddMacroParam(i_name, %s)'%i_id)

    ### Counter
    if not NC:
        MC.AddMacroParam('%msp', counter)

    # Export the network to an ANML file    
    MC.ExportAnml(name+'_macro'+'.anml')

    # One anml with two macro instances
    # anmlNet = A.CreateAutomataNetwork(name+'_2inst')
    # macroRef = anmlNet.AddMacroRef(MC, 'm1')
    # macroRef = anmlNet.AddMacroRef(MC, 'm2')
    # anmlNet.ExportAnml(name+'.anml')

    return (name, MC, A, e_subhold, p_subhold, i_subhold)


def def_SPM_16B_macro(item_num, entry_num, sp_dict, name, opt, seq):
    # Initialize the automata network
    A = Anml()
    name = name+'_16B_'+'%02dX%02d'%(item_num+1, entry_num)
    if opt:
        name = name+'O'
    if seq:
        name = name+'_seq'
    else:
        name = name+'_set'
    if NC:
        name = name+'_NC'
    else:
        name = name+'_C'

    print name
    MC = A.CreateMacroDef(anmlId=name)
    
    # Build the network
    ## Elements
    ### Entry elements
    for i in range(entry_num):
        e_id = 'e%02d'%i
        #   exec("%s = MC.AddSTE(sp_dict['EB'], startType=AnmlDefs.START_OF_DATA, anmlId=e_id)"%(e_id))
        if opt:
            exec("%s = MC.AddSTE(sp_dict['EB'], startType=AnmlDefs.START_OF_DATA, anmlId=e_id)"%(e_id))
        else:
            exec("%s = MC.AddSTE(sp_dict['EB'], startType=AnmlDefs.ALL_INPUT, anmlId=e_id)"%(e_id))

    ### Place Holder elements
    for i in range(item_num):
        pH_id = 'pH%02d'%i
        pL_id = 'pL%02d'%i
        exec("%s = MC.AddSTE(sp_dict['EB'], anmlId=pH_id)"%(pH_id))
        exec("%s = MC.AddSTE(sp_dict['EB'], anmlId=pL_id)"%(pL_id))

    ### Item elements
    for i in range(item_num):
        iH_id = 'iH%02d'%i
        iL_id = 'iL%02d'%i
        exec("%s = MC.AddSTE(sp_dict['EB'], anmlId=iH_id)"%(iH_id))
        exec("%s = MC.AddSTE(sp_dict['EB'], anmlId=iL_id)"%(iL_id))

    last_p = MC.AddSTE(sp_dict['NTD'], anmlId='last_p')
    if not NC:
        last_i = MC.AddSTE(sp_dict['TD'], anmlId='last_i')
    else:
        last_i = MC.AddSTE(sp_dict['TD'], anmlId='last_i', match = True)

    if not NC:
        ### Counter elements
        counter = MC.AddCounter(1000, anmlId='Counter')    
        ### Ending report elements
        rep = MC.AddSTE(sp_dict['EB'], match = True, anmlId='Reporter') 
    
    ## Connections
    ### Entry -> position holder ->> item
    
    for i in range(entry_num):
        e_id = 'e%02d'%i
        pH_id = 'pH%02d'%i
        pL_id = 'pL%02d'%i
        iH_id = 'iH%02d'%i
        exec('MC.AddAnmlEdge(%s, %s, 0)'%(e_id, pH_id))
        exec('MC.AddAnmlEdge(%s, %s, 0)'%(e_id, iH_id))
        if opt:
            exec('MC.AddAnmlEdge(%s, %s, 0)'%(pL_id, e_id))

    ### position-> position; position -> item; item-> next item; item-> next position
    for i in range(item_num):
        pH_id = 'pH%02d'%i
        pL_id = 'pL%02d'%i
        iH_id = 'iH%02d'%i
        iL_id = 'iL%02d'%i
        exec('MC.AddAnmlEdge(%s, %s, 0)'%(pH_id, pL_id))
        exec('MC.AddAnmlEdge(%s, %s, 0)'%(pL_id, pH_id))
        exec('MC.AddAnmlEdge(%s, %s, 0)'%(pL_id, iH_id))
        exec('MC.AddAnmlEdge(%s, %s, 0)'%(iH_id, iL_id))
        
        if (i+1) < item_num :
            pH_next = 'pH%02d'%(i+1)
            iH_next = 'iH%02d'%(i+1)
            exec('MC.AddAnmlEdge(%s, %s, 0)'%(iL_id, pH_next))
            exec('MC.AddAnmlEdge(%s, %s, 0)'%(iL_id, iH_next))

    ### last -> counter
    iL_id = 'iL%02d'%(item_num-1)
    exec('MC.AddAnmlEdge(%s, last_p, 0)'%(iL_id))
    exec('MC.AddAnmlEdge(%s, last_i, 0)'%(iL_id))
    MC.AddAnmlEdge(last_p, last_i, 0)
    #last_p 
    #last_i 
    if not NC:
        MC.AddAnmlEdge(last_i, counter, 0)
        MC.AddAnmlEdge(counter, rep, 0)
    
    ## Parameters
    ### Entry
    for i in range(entry_num):
        e_id = 'e%02d'%i
        para_name ='%'+e_id 
        exec('MC.AddMacroParam(para_name, %s)'%e_id)
    
    ### Place Holder & item
    for i in range(item_num):
    # for i in range(item_num):
        iH_id = 'iH%02d'%i
        iL_id = 'iL%02d'%i
        pH_id = 'pH%02d'%i
        pL_id = 'pL%02d'%i
        pH_name ='%'+pH_id 
        pL_name ='%'+pL_id 
        iH_name ='%'+iH_id 
        iL_name ='%'+iL_id 
        
        if not seq:
            pH_name ='%NTD'
            pH_name ='%NTD'
            
        exec('MC.AddMacroParam(pH_name, %s)'%pH_id)
        exec('MC.AddMacroParam(iH_name, %s)'%iH_id)
        exec('MC.AddMacroParam(pL_name, %s)'%pL_id)
        exec('MC.AddMacroParam(iL_name, %s)'%iL_id)

    ### Transaction delimiter 
    # i_id = 'i%02d'%(item_num-1)
    # p_id = 'p%02d'%(item_num-1)
    # p_name ='%NTD'
    # i_name ='%TD'
    MC.AddMacroParam('%NTD', last_p)
    MC.AddMacroParam('%TD', last_i)

    if not NC:
        ### Counter
        MC.AddMacroParam('%msp', counter)

    # Export the network to an ANML file    
    MC.ExportAnml(name+'_macro'+'.anml')

    # One anml with two macro instances
    # anmlNet = A.CreateAutomataNetwork(name+'_2inst')
    # macroRef = anmlNet.AddMacroRef(MC, 'm1')
    # macroRef = anmlNet.AddMacroRef(MC, 'm2')
    # anmlNet.ExportAnml(name+'.anml')

    return (name, MC, A)


def deter_bit(pfile):
    #print pfile
    map_file = os.path.join(os.path.dirname(pfile),"map.txt")
    #print map_file
    with open(map_file) as f:
        lastline = ([i for i in f.read().split('\n') if i][-1])
    item_num =  int(lastline.split("-->")[1])
    if item_num < 253:
        E8B = True
        E16B = False
    else:
        E8B = False
        E16B = True
    return (E8B, E16B)

def extract_set(iset, sp_dict):
    items = []
    holders = []
    values = iset.split("-")
    for v in values:
        items.append("{%d}"%int(v))
        holders.append(sp_dict['IS'])
    holders[0]=sp_dict['NTD'] 
    return (items, holders)  
    
def extract_pattern(line, sp_dict):
    i_vec = []
    p_vec = []
    seq = line.split("--")
    #print seq 
    for iset in seq:
       # print "iset =", iset
        items, holders = extract_set(iset, sp_dict)
        #print items, holders
        i_vec += items
        p_vec += holders

        # insert set delimiters
        i_vec += [sp_dict['ITD']]
        p_vec += [sp_dict['IS']]
    
	#i_vec += [sp_dict['TD']] #Elaheh
	#p_vec += [sp_dict['NTD']] #Elaheh    
    i_vec.pop()
    p_vec.pop()    
    #print i_vec
    #print p_vec
    return (i_vec, p_vec)
    
def read_patterns(pfile, sp_dict):
    i_array = []
    p_array = []
    t_array = []
    with open(pfile) as f:
        for line in f.readlines():
            if '-' in line:
                i_vec, p_vec = extract_pattern(line, sp_dict)
                i_array.append(i_vec)
                p_array.append(p_vec)
                t_array.append(line.strip('\n'))
    
    return (i_array, p_array, t_array)

def sym_replace(anml_net,i_vec, p_vec, e_subhold, p_subhold, i_subhold, macroRef, sp_dict, size):
    start = size-len(i_vec)
    #print i_vec
    #print "Elaheh"
    #print size-len(i_vec)
    #print start

    # replace entry
    # print e_subhold[0]
    # print macroRef
    e_subhold[start].ste.new_symbols = sp_dict['TD']
    anml_net.SetMacroParamSubstitution(macroRef, e_subhold[start]);

    for i, (item, pos) in enumerate(zip(i_vec, p_vec)):
        i_subhold[start+i].ste.new_symbols = item
        p_subhold[start+i].ste.new_symbols = pos
        anml_net.SetMacroParamSubstitution(macroRef, i_subhold[start+i])
        anml_net.SetMacroParamSubstitution(macroRef, p_subhold[start+i])
    

    
if __name__ == '__main__':
    # command line
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-s', '--size', required=True, type=int,
                        help='max size of sequence')
    # parser.add_argument('-e', '--entry', required=True, type=int,
    #                     help='number of entries')
    parser.add_argument('-p', '--pattern_file', required=True,
                        help='The file contain patterns')

    # if set -O: apply optimization to save one STE in each entry
    parser.add_argument('-O', action="store_true", default=False)
    # if set --set: generate automata for frequent set mining instead of sequential pattern mining
    parser.add_argument('--set', action="store_true", default=False)
    # if set --NC: don't use on-chip counters, report immediately when matching
    parser.add_argument('--NC', action="store_true", default=False)
    
    # bit_arg = parser.add_mutually_exclusive_group()
    # bit_arg.add_argument('-E8B', action='store_true')
    # bit_arg.add_argument('-E16B', action="store_true")
    
    args = parser.parse_args()
    
    sp_dict={'EB':'{255}', 'TD':'{254}', 'NTD':'{0:253}', 'ITD':'{253}', 'IS':'{0:252}', 'elu':'{0:255}'}

    item_num = args.size*2-1
    entry_num = args.size 
    
    # if entry_num > item_num:
    #     print "max size of sequence should be larger than the number of entries"
    #     sys.exit()
    opt = True
    seq = True
    NC = True # if NC, no use of on-chip counters

    E8B, E16B = deter_bit(args.pattern_file)

    if E8B :    
        name, macroDef, automaton, e_subhold, p_subhold, i_subhold = def_SPM_8B_macro(item_num, entry_num, sp_dict, "freq_seq_pattern", opt, seq, NC)


    if E16B :    
        name, macroDef, automaton = def_SPM_16B_macro(item_num, entry_num, sp_dict, "freq_seq_pattern", opt, seq, NC)
 
    i_array, p_array, t_array = read_patterns(args.pattern_file, sp_dict)

    
    # One anml file 
    #print(os.path.split(args.pattern_file)[1]
    #name = os.path.split(args.pattern_file)[-2].split('/')[1]
    #print name
    #anmlNet = automaton.CreateAutomataNetwork(name+'_')
    anmlNet = automaton.CreateAutomataNetwork("name") #Elaheh

    
    for i, (i_vec, p_vec, t_vec) in enumerate(zip(i_array, p_array, t_array)):
        #print i, i_vec, p_vec, t_vec
        macroRef = anmlNet.AddMacroRef(macroDef, 'm'+t_vec)
        sym_replace(anmlNet, i_vec, p_vec, e_subhold, p_subhold, i_subhold, macroRef, sp_dict, item_num)
    # macroRef2 = anmlNet.AddMacroRef(macroDef, 'm2')
    # macroRef1 = anmlNet.AddMacroRef(macroDef, 'm3')
    # macroRef2 = anmlNet.AddMacroRef(macroDef, 'm4')

    fname = args.pattern_file.split('.')[0]
    name = name+ '_' + fname + '.anml'
    anmlNet.ExportAnml(name)
    
    print ("The results are stored in " + name)

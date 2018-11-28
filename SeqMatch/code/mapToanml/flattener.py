#!/usr/bin/python

'''

    This is the ANML flattener. It accepts a hierarchical ANML file using
    macros, and returns a flattened version using only elements.

    *So far only support STEs, Counters, and Inverters

    usage: flattener.py <input anml filename> <output anml filename>

    Author: Tom Tracy II (tjt7a@virginia.edu)
    26 March 2016
    v1.6

'''

import sys
import xml.etree.ElementTree as ET
import copy
import os.path

VERBOSITY = False
STEP_THROUGH = False

reference_addresses = {}

delimiter = "___"

# Flatten the macro
def flatten(root, macro_subtree, macro, parent_id, connection_dictionary):

    macro_id, macro_use, activations, substitutions = grab_macro_details(macro)

    # The new id is (path-to-macro)<delimiter>(macro id)
    new_id = parent_id + delimiter + macro_id

    if VERBOSITY:
        print "new_id = ", new_id

    try:
        if VERBOSITY:
            print "Parsing: ", macro_use

        if "_macro.anml" not in macro_use:
            macro_use += '_macro.anml'

        macro_subtree = ET.parse(macro_use).getroot()

    except IOError:
        print "Failed to open Macro: ", macro_use
        exit()

    # Pause execution
    if STEP_THROUGH:
        raw_input("Press Enter to continue...")

    header = macro_subtree.find('header')
    inner_inter = header.find('interface-declarations')
    inner_params = header.find('parameter-declarations')

    inner_interface_declarations = None
    inner_parameters = None

    if inner_inter is not None:
        if VERBOSITY:
            print "Found a <interface-declarations> tag in the macro header"

        inner_interface_declarations = grab_inner_declarations(inner_inter)

    if inner_params is not None:

        if VERBOSITY:
            print "Found a <interface-declarations> tag in the macro header"

        inner_parameters = grab_inner_parameters(inner_params)

    if VERBOSITY:
        print "Done with macro header; removing from the subtree"

    if STEP_THROUGH:
        raw_input("Press Enter to continue...")

    # Strip out the header; we're done here
    macro_subtree.remove(header)

    if inner_parameters is not None:

        # If default value not over-ridden, add to substitutions
        for item in inner_parameters:

            if item not in substitutions:

                if VERBOSITY:
                    print item, " is not over-ridden, so add to substitutions"

                substitutions[item] = inner_parameters[item]

    if VERBOSITY:
        print "Updated substitutions: ", substitutions

    if STEP_THROUGH:
        raw_input("Press Enter to continue...")

    body = macro_subtree.find('body')
    port_defs = body.find('port-definitions')

    # Grab the port definitions
    ports_in, ports_out = grab_port_definitions(port_defs, new_id)

    if VERBOSITY:
        print "Done with port defs; removing from the subtree"

    if STEP_THROUGH:
        raw_input("Press Enter to continue...")

    # Strip out the port-defs; we're done here
    body.remove(port_defs)

    # Merge dictionaries
    #connection_dictionary = dict(connection_dictionary.items() + ports_in.items())
    connection_dictionary.update(ports_in)

    if VERBOSITY:
        print "Connection Dictionary Updated with ports_ins:", connection_dictionary

    if VERBOSITY:
        print "Time to replace Substitutions"

    replace_substitutions(body, substitutions)

    if VERBOSITY:
        print "Done replacing Substitutions"

    if STEP_THROUGH:
        raw_input("Press Enter to continue...")

    # Activation tags for different elements
    activation_dictionary = {
        'state-transition-element':'activate-on-match',
        'counter':'activate-on-target',
        'inverter':'activate-on-high'}

    if VERBOSITY:
        print "Time to scan the body"

    # For elements in the body
    for child in body:

        if child.tag == 'macro-reference':

            if VERBOSITY:
                print "Found a macro reference; time to flatten:"

            root, connection_dictionary = flatten(root, macro_subtree, child, new_id, connection_dictionary)

        elif child.tag in ['state-transition-element', 'counter', 'inverter']:

            if VERBOSITY:
                print "Found an STE/COUNTER/INVERTER"

            # Update the id of the element
            temp_id = new_id + delimiter + child.attrib['id']
            child.set('id', temp_id)

            if VERBOSITY:
                print "Looking for temp_id = ", temp_id

            if temp_id in ports_out:

                if VERBOSITY:
                    print "Found temp_id in ports_out"

                for out_connection in ports_out[temp_id]:

                    if VERBOSITY:
                        print "ports out:", ports_out[temp_id]
                        print "activations: ", activations

                    if len(activations.keys()) > 0:

                        if VERBOSITY:
                            print out_connection

                        # Get the port
                        out_port = out_connection.split(delimiter)[-1]
                        print "Got out port: ", out_port

                        # We're inside the macro now, but our macro is linking out, so outside the macro
                        for activation in activations[out_port]:

                            activation_string = activation_dictionary[child.tag]
                            temp_element = ET.Element(activation_string)

                            if activation[1] is not None:

                                print "Found a port in activation[1]"

                                if activation[1] is not 'cnt':
                                    link_to = parent_id + delimiter + activation[0] + delimiter + activation[1]

                                else:
                                    link_to = parent_id + delimiter + activation[0] + ":" + activation[1]

                            else:

                                print "Couldnt find a port in activation[1]"

                                link_to = parent_id + delimiter + activation[0]

                            if VERBOSITY:
                                print "Created a new temp element to link to: ", link_to

                            temp_element.set('element', link_to)
                            child.append(temp_element)

                    root.append(child)
            else:

                for link in child.findall('activate-on-match'):

                    new_value = new_id + delimiter + link.attrib['element']

                    link.set('element', new_value)

                for link in child.findall('activate-on-target'):

                    new_value = new_id + delimiter + link.attrib['element']

                    link.set('element', new_value)

                root.append(child)


        else:

            print "Oh shit; we found something we shouldnt have"
            print child.tag
            exit()

    else:
        if VERBOSITY:
            print "We have no macros!"
            print "There are no macro-references in ", parent_id


    return root, connection_dictionary

def grab_activations(activate_out):

    activations = {} # Empty dictionary of activations

    for a_f_m in activate_out.findall('activate-from-macro'):

        source = a_f_m.attrib['source']
        element = a_f_m.attrib['element'].split(':')
        element_id = element[0]

        if VERBOSITY:
            print "----------"
            print "Found <activate-from-macro> tag"
            print "source = ", source, ", element = ", element, ", element_id = ", element_id

        if len(element) == 2:
            element_port = element[1]

            if VERBOSITY:
                print "Found an element port = ", element_port
        else:
            element_port = None

            if VERBOSITY:
                print "Could not find an element port"

        destination = (element_id, element_port)

        if source not in activations:

            activations[source] = [destination, ]

            if VERBOSITY:
                print "Destination not found in activations; adding"

        else:

            activations[source].append(destination)

            if VERBOSITY:
                print "Found Activation in Activations; appending Destination"

        print "Activate source = ", source, " -> destination = ", activations[source]


        if VERBOSITY:
            print "----------"

    return activations

def grab_substitutions(substitute):

    substitutions = {} # Empty dictionary of substitutions

    for replace in substitute.findall('replace'):

        if VERBOSITY:
            print "----------"
            print "Found <replace> tag"

        parameter_name = replace.attrib['parameter-name']
        replace_with = replace.attrib['replace-with']

        if VERBOSITY:
            print "parameter-name = ", parameter_name
            print "replace_with = ", replace_with

        if replace_with:

            substitutions[parameter_name] = replace_with

            print "Adding to subtitutions dictionary"

        else:

            print "ERROR: Found a parameter... but we're not replacing... huh"

        if VERBOSITY:
            print "----------"

    return substitutions

def grab_inner_parameters(parameter_declarations):

    inner_parameters = {}

    for child in parameter_declarations:

        inner_parameters[child.attrib['parameter-name']] = child.attrib['default-value']

        if VERBOSITY:
            print "Adding parameter-name = ", child.attrib['parameter-name'], ", default-value = ", child.attrib['default-value'], "to inner parameters dictionary"

    if VERBOSITY:
        print "Found Inner Parameters: ", inner_parameters

    return inner_parameters

def grab_inner_declarations(inner_interface):

    inner_interface_declarations = {}

    for child in inner_interface:

        inner_interface_declarations[child.attrib['id']] = child.attrib['type']

        if VERBOSITY:
            print "Adding child id = ", child.attrib['id'], ", type = ", child.attrib['type'], "to inner interface declations"

    if VERBOSITY:
        print "Found Inner Interface Declarations: ", inner_interface_declarations


    return inner_interface_declarations

def grab_port_definitions(port_defs, new_id):

    ports_in = {}
    ports_out = {}

    if VERBOSITY:
        print "----------"
        print "Time to grab the port definitions"

    # Iterate through all ports in port definitions
    for child in port_defs:

        # If a port-in
        if child.tag == 'port-in':

            if VERBOSITY:
                print "Found a <port-in>"
                print "-----------------"

            for element in child:

                activate_from_name = new_id + delimiter + child.attrib['id'] # Macro_id + external port name
                new_ste_name = new_id + delimiter + element.attrib['element'] # Macro_id + STE name

                if VERBOSITY:
                    print "From port: ", activate_from_name
                    print "New Element Name: ", new_ste_name

                # Another hack to disable translation for counter
                if (':cnt' not in new_ste_name) and (':rst' not in new_ste_name):
                    new_ste_name = new_ste_name.replace(':', delimiter)

                else:
                    if VERBOSITY:
                        print "Found a :cnt or :rst port!", new_ste_name

                if VERBOSITY:
                    print "Active from: ", activate_from_name
                    print "New Element Name: ", new_ste_name

                if activate_from_name in ports_in:

                    ports_in[activate_from_name].append(new_ste_name)

                else:

                    ports_in[activate_from_name] = [new_ste_name, ]

                print "Updated ports_in: ", ports_in

        # If a port-out

        #   Does the dictionary value also include the macro id?
        #
        elif child.tag == 'port-out':

            if VERBOSITY:
                print "Found a <port-out>"
                print "------------------"

            for element in child:

                new_ste_name = new_id + delimiter + element.attrib['element']
                to_port = new_id + delimiter + child.attrib['id']

                if VERBOSITY:
                    print "New STE Name: ", new_ste_name
                    print "To Port: ", to_port

                if new_ste_name in ports_out:

                    ports_out[new_ste_name].append(to_port)

                else:

                    ports_out[new_ste_name] = [to_port, ]

            if VERBOSITY:
                print "Updated ports_out: ", ports_out

    print "----------"

    return ports_in, ports_out


def replace_substitutions(body, substitutions):

    for child in body:

        if 'symbol-set' in child.attrib:

            if child.attrib['symbol-set'] in substitutions:

                if VERBOSITY:
                    print "Replacing ", child.attrib['symbol-set'], " with ", substitutions[child.attrib['symbol-set']]

                child.set('symbol-set', substitutions[child.attrib['symbol-set']])

        if VERBOSITY:
            print child.tag, "...", child.attrib

    return 0

def grab_macro_details(macro):

    activations = {}
    substitutions = {}

    macro_id = macro.attrib['id']
    macro_use = macro.attrib['use']

    if VERBOSITY:
        print "Grabbing macro details for (id =", macro_id, ", use =", macro_use, ")"

    # Replace macro_use with actual address
    if macro_use in reference_addresses:

        macro_use = reference_addresses[macro_use]

        if VERBOSITY:
            print "Replacing macro_use = ", macro_use, " with reference address = ", macro.attrib['use']

    else:
        print "Couldnt replace ", macro_use

    # Not necessarily used
    activate_out = macro.find('activate-out')
    subs = macro.find('substitutions')

    # Grab outward activations
    if activate_out is not None:

        if VERBOSITY:
            print "Found <activate-out> tags; time to grab activations"

        activations = grab_activations(activate_out)

    # Grab substitutions
    if subs is not None:

        if VERBOSITY:
            print "Found <substitutions> tags; time to grab substitutions"

        substitutions = grab_substitutions(subs)

    if VERBOSITY:
        print ""
        print "Macro id: ", macro_id, " Macro use: ", macro_use
        print "Activations: ", activations
        print "Substitutions: ", substitutions
        print "-------------"

    return macro_id, macro_use, activations, substitutions

# Print children
def print_children(root):
    for child in root:
        print child.tag, child.attrib
    return

# Load a library of macro definitions
def load_library(library):

    if VERBOSITY:
        print "Loading Library Dictionary"
        print "----------"

    library_dictionary = {}

    library_filename = library.attrib['ref'].strip()

    if not os.path.isfile(library_filename):
        print "Error: %s cannot be found as a valid library file" % library_filename
        exit()

    else:

        if VERBOSITY:
            print "Loading Dictionary of Macro Definitions"

        library_tree = ET.parse(library_filename)
        root = library_tree.getroot()

        library_defs = root.findall('library-definition')

        for library_def in library_defs:

            library_id = library_def.attrib['id']

            for include_macro in library_def.findall('include-macro'):

                macro_ref = include_macro.attrib['ref']
                key = library_id+'.'+macro_ref.split('.')[0]
                library_dictionary[key] = macro_ref

                if VERBOSITY:
                    print key +" -> ", macro_ref

        if VERBOSITY:
            print "----------"
            print "Done loading dictionary"

        return library_dictionary



# Main()
if __name__ == "__main__":

    # Verify argument count
    if len(sys.argv) != 3 or ['-h', '--help'] in sys.argv :
        print "Usage: flattener.py <input anml> <flattened output>"
        exit()

    else:

        # Grab input and output file names
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]

        # Parse the root XML file
        try:
            if VERBOSITY:
                print "Parsing input file: ", input_filename

            tree = ET.parse(input_filename)

        except IOError:
            print "Failed to open Input Filename: ", input_filename
            exit()

        # Grab the root node
        root = tree.getroot()

    #-----------------------------------------------------------------------------
        # If include-macros is defined at root level (older version of ANML)
        include_macros = root.findall('include-macro')

        if len(include_macros) > 0 :

            if VERBOSITY:
                print "Found <include-macro> tag"

            for include_macro in include_macros:

                macro_filename =  include_macro.attrib['ref']

                if not os.path.isfile(macro_filename):
                    print "ERROR: %s cannot be found as a valid macro " % macro_filename
                    exit()
                else:
                    reference_key = (macro_filename[0:macro_filename.find('_macro.anml')]).strip()
                    reference_addresses[reference_key] = macro_filename

                root.remove(include_macro) #We don't need it anymore
        else:
            if VERBOSITY:
                print "Could not find <include-macro> tag"

    #-----------------------------------------------------------------------------

        # If include-library is defined at the root level (ANML v1.0)
        include_library = root.find('include-library')

        if include_library is not None:

            if VERBOSITY:
                print "Found <include-library> tag"

            reference_addresses = load_library(include_library)
            root.remove(include_library)

        else:

            if VERBOSITY:
                print "Could not find <include-library> tag"

        # Pause execution
        if STEP_THROUGH:
            raw_input("Press Enter to continue...")

    #-----------------------------------------------------------------------------

        # Check if in automata level of anml
        automata_network = root.find('automata-network')

        if automata_network is not None:
            root = automata_network

            if VERBOSITY:
                print "Found the <automata-network> tag and set root"

        parent_id = 'root'

        # Empty dictionary to populate with new names and connection
        connection_dictionary = {}

        if VERBOSITY:
            print "Iterate through all <macro-reference> tags"

        # Iterate through each macro
        for macro in root.findall('macro-reference'):

            if VERBOSITY:
                print "----------"
                print "Flattening: (tag=", macro.tag, ", attrib=", macro.attrib, ")"

            # Flatten the macro (root is root and the current subtree we're into)
            root, connection_dictionary = flatten(root, root, macro, parent_id, connection_dictionary)

            # We're done with the macro; remove it
            root.remove(macro)

            if VERBOSITY:
                print " Done Flattening: ", macro.tag
                print "----------"
    #-----------------------------------------------------------------------------

        if VERBOSITY:
            print "Done with all of the macros."
            print "Connection Dictionary: ", connection_dictionary

        # Pause execution
        if STEP_THROUGH:
            raw_input("Press Enter to continue...")

        # Activation tags for different elements
        activation_dictionary = {'state-transition-element':'activate-on-match',
                    'counter':'activate-on-target',
                    'inverter':'activate-on-high'}

        if VERBOSITY:
            print "Now time to go through child elements"

        # print all children of root
        for child in root:


        #--------------------------------------------------------------------------
            # If any root elements have not been translated
            if 'id' in child.attrib:

                # We haven't prefixed then name with root yet
                if 'root' not in child.attrib['id']:

                    child.set('id', 'root' + delimiter + child.attrib['id'])

                    if VERBOSITY:
                        print "Converting id = ", child.attrib['id']

            if child.tag in activation_dictionary:

                activation_string = activation_dictionary[child.tag]

                if VERBOSITY:
                    print "Found an activation for the child: ", activation_string

            else:
                print "Could not find this child in the activation dictionary: ", child.attrib, child.tag
                continue
        #--------------------------------------------------------------------------

            activation_links = child.findall(activation_string)

            if VERBOSITY:
                print "Find all links with activation string = ", activation_string
                print "Activation Links: ", activation_links

            for link in activation_links:

                if 'root' not in link.attrib['element']:
                    old_value = "root" + delimiter + link.attrib['element']

                else:
                    old_value = link.attrib['element']

                if VERBOSITY:
                    print "Old value: ", old_value

                # If the old element value used ':', substitute for '_'; but not for counter
                if (':cnt' not in old_value) and (':rst' not in old_value):

                    old_value = old_value.replace(':', delimiter)

                    if VERBOSITY:
                        print "This element is a: ", child.tag
                        print "Found that the child is not a counter, so replace : with delimiter"
                        print old_value

                else:
                    if VERBOSITY:
                        print "Found a counter! (tag: ", child.tag

                if old_value in connection_dictionary:

                    # Make a shallow copy for this link; may need it several times
                    dests = copy.copy(connection_dictionary[old_value])

                    if VERBOSITY:
                        print "Found destinations in the connection dictionary: ", dests

                    if dests:

                        link.set('element', dests.pop(0))

                        while len(dests) > 0:
                            temp_link = copy.copy(link)
                            temp_link.set('element', dests.pop(0))
                            child.append(temp_link)

                            print "Adding link to child. Link: ", temp_link, ", child: ", child
                    else:
                        link.set('element', old_value)
                else:

                    if VERBOSITY:

                        print old_value, " not in the dictionary"

                    link.set('element', old_value)

            if STEP_THROUGH:
                raw_input("Press Enter to continue...")

        tree.write(output_filename)

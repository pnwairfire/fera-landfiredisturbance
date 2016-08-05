# ============================================================================
#
#    Author:     Kjell Swedin
#    Date:        May 05 2016 - 10h:36m
#    Purpose:   Use this script to convert the "enum class Something" into ids for the Fuelbed Manipulation Language.
#                       Run the script on the cpp file with the enums (fuelbed_ids.cpp).
#
# ============================================================================
import sys
import re

def convert_info(infile):
    line = infile.readline().strip()
    while '};' not in line:
        if line.startswith('e'):
            print(line[1:])
        line = infile.readline().strip()

def convert_litter(infile):
    line = infile.readline().strip()
    while '};' not in line:
        if line.startswith('e'):
            chunks = line.split('_')
            if len(chunks) > 2:
                print('{}_{}'.format(chunks[0][1:], ''.join([i.capitalize() for i in chunks[3:]])))
        line = infile.readline().strip()
        
def convert_unit(infile):
    line = infile.readline().strip()
    while '};' not in line:
        if line.startswith('e'):
            chunks = line.split('_')
            chunks[0] = chunks[0][1:]
            print('{}_{}'.format(chunks[0], ''.join([i.capitalize() for i in chunks[1:]])))
        line = infile.readline().strip()

def convert_species(infile):
    def interesting(line):
        return line.startswith('e') and 'RELATIVE_COVER' not in line and 'TSN' not in line
    
    line = infile.readline().strip()
    while '};' not in line:
        if interesting(line):
            chunks = line.split('_')
            chunks[0] = chunks[0][1:]
            print('SPECIES_{}'.format(''.join([i.capitalize() for i in chunks[0:-3]])))
        line = infile.readline().strip()
        

CONVERT_MAP = {
    "enum class InfoTypes" : convert_info,
    "enum class LitterTypes" : convert_litter,
    "enum class ContainUnitTypes": convert_unit,
    "enum class SpeciesTypes": convert_species,
}
def is_interesting(line):
    if line in CONVERT_MAP.keys():
        return (True, CONVERT_MAP[line])
    else:
        return (False, None)

def process(fname):
    with open(fname) as infile:
        for line in infile:
            yes, func = is_interesting(line.strip())
            if yes:
                func(infile)
                
# ============================================================================
#   Start
# ============================================================================
if len(sys.argv) > 1:
    process(sys.argv[1])
    
    
    
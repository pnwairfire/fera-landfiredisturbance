# =============================================================================
#
# Author:	Kjell Swedin
# Purpose:	Strip lines of commas the excel adds to exported csv files
#
# =============================================================================
import re
import os

def strip_commas(dir):
    filename = '{}_Script.csv'.format(dir)
    outfilename = '{}.tmp'.format(filename.split('.')[0])
    with open(filename, 'r') as infile:
        with open(outfilename, 'w+') as outfile:
            for line in infile:
                if not re.match('^,,[,]+$', line):
                    outfile.write(line)
    if os.path.exists(outfilename):
        os.system('rm {} && mv {} {}'.format(filename, outfilename, filename))
    

# ++++++++++++++++++++++++++++++++++++++++++
#  Start
# ++++++++++++++++++++++++++++++++++++++++++
spec_dirs = [
    '1_Fire',
    '2_MechAdd',
    '3_MechRemove',
    '4_Wind',
    '5_Insects'
]

for dir in spec_dirs:
    print('Processing {} ...'.format(dir))
    os.chdir(dir)
    strip_commas(dir)
    os.chdir('..')

# =============================================================================
#
# Author:	Kjell Swedin
# Purpose:	Show a segment of the regression output
#
# =============================================================================
import sys
import re




def process(filename, segment_id):
    with open(filename, 'r') as infile:
        print_flag = False
        matcher = re.compile('^[A-Z_0-9]+_[1-5]{3}$')
        for line in infile:
            line = line.rstrip()
            if matcher.match(line):
                if line.endswith(segment_id):
                    print_flag = True
                else:
                    print_flag = False
            if print_flag:
                print(line)








# ++++++++++++++++++++++++++++++++++++++++++
#   Start
# ++++++++++++++++++++++++++++++++++++++++++
if len(sys.argv) > 2:
    process(sys.argv[1], sys.argv[2].strip())
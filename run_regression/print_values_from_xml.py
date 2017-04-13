# =============================================================================
#
# Author:	Kjell Swedin
# Purpose:	Dump values from fuelbed file. This is a separate file because the libfbrw library prints to the console. 
#                   This file gets invoked from another script and the output is redirected to a file.  Could be cleaner.
#
# =============================================================================

import sys
sys.path.insert(0, '../run_disturbance/scripts')
import libfbrw

def process(filename):
    fb = libfbrw.FuelbedValues(filename)
    fb.Read()
    fb.Print()

# ++++++++++++++++++++++++++++++++++++++++++
#   Start ...
# ++++++++++++++++++++++++++++++++++++++++++
if len(sys.argv) > 1:
    process(sys.argv[1])
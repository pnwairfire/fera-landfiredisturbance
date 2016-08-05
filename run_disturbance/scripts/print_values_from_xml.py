import libfbrw
import sys

def process(filename):
    fb = libfbrw.FuelbedValues(filename)
    fb.Read()
    fb.Print()
    
if len(sys.argv) > 1:
    process(sys.argv[1])
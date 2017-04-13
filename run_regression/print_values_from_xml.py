import sys
sys.path.insert(0, '../run_disturbance/scripts')
import libfbrw

def process(filename):
    fb = libfbrw.FuelbedValues(filename)
    fb.Read()
    fb.Print()
    
if len(sys.argv) > 1:
    process(sys.argv[1])
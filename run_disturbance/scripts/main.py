#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name:        main.py
# Purpose:     Driver file for disturbance scripts
#                   Requirements - all disturbance modules must implement the "do_special()" and "get_scaling_params()" methods.
#                   This allows each disturbance to be treated identically.
#
# Author:      kjells
#
# Created:     7/14/2014
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import glob
import os
import shutil
import fbrw
import fire
import insects

# Maps a string to an imported module. DISTURBANCE_MODULE_MAP = DMM
DMM = {
    'fire': fire,
    'insects': insects,
}

# Maps a string to a LANDFIRE disturbance code. DISTURBANCE_CODE_MAP = DCM
DCM = {
    'fire': 1,
    'insects': 5,
}

OUT_DIR = 'out'
def create_output_dirs():
    if os.path.exists(OUT_DIR): shutil.rmtree(OUT_DIR)
    os.mkdir(OUT_DIR)
    
def process_independently(files):
    for f in files:
        for d in fbrw.DISTURBANCE:
            for s in fbrw.SEVERITY:
                for t in fbrw.TIMESTEP:
                    print('\nProcessing {}...'.format(f))
                    
                    # name the output file the basename plus the code for disturbance, severity, and timestep
                    #  For instance, FB_0165_FCCS.xml -> FB_0165_FCCS_511.xml
                    basename = os.path.splitext(os.path.split(f)[1])[0]
                    dist_sev_time = '{}{}{}'.format(DCM[d], s, t)
                    outname = './out/{}_{}.xml'.format(basename, dist_sev_time)
                    
                    # get the reader/writer object, pass in the aggregated code. The code will be appended
                    #  to the fuelbed_number. The required fb.Read() method will have been called before
                    #  the object is returned.
                    fb = fbrw.get_reader_writer(f, dist_sev_time)
                    
                    # invocation of the disturbance-module-specific code happens via DMM
                    DMM[d].do_special(fb, s, t)
                    fbrw.do_simple_scaling(fb, DMM[d].get_scaling_params(s, t))
                    
                    fb.Write(outname)
    


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#   Start
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if len(sys.argv) > 1:
    files = sys.argv[1:]
    create_output_dirs()
    process_independently(files)
    exit(0)

print('\nError: missing files to process')
print('\tpython main.py ../fuelbeds/*.xml\n')
exit(1)
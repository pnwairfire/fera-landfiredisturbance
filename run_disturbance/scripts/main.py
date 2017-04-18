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
import requests
from inspect import getsourcefile
from os.path import abspath


def get_dir_for_this_file():
    path = abspath(getsourcefile(lambda:0))
    return os.path.dirname(path)
    
thisfile_dir = get_dir_for_this_file()
invoking_dir = os.getcwd()

FBWRITER_LIB = 'libfbrw.so'
def retrive_fbwrite_library():
    def latest(r):
        builds = []
        # line looks like - '<a href="504/">504/</a>   29-Dec-2016 16:33    -'
        for i in r.iter_lines():
            i = i.decode('latin_1')
            try:
                builds.append(int(i.split('>')[1].split('/')[0]))
            except:
                pass
        return max(builds)
        
    def remove_lib():
        try:
            os.remove(FBWRITER_LIB)
        except OSError:
            pass        
    
    os.chdir(thisfile_dir)
    remove_lib()
    query = 'http://172.16.0.120:8081/artifactory/simple/generic-local/fbwriter_lib'
    r = requests.get(query)
    latest_build = latest(r)
    
    cmd = 'wget http://172.16.0.120:8081/artifactory/generic-local/fbwriter_lib/{}/libfbrw.so '.format(latest_build)
    os.system(cmd)
  
    retval = True if os.path.exists(FBWRITER_LIB) else False
    print('\n retval is {}\n'.format(retval))
    return retval

if retrive_fbwrite_library():
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
def create_output_dirs(invocation_dir):
    out = os.path.join(invocation_dir, OUT_DIR)
    if os.path.exists(out): shutil.rmtree(out)
    print('\n 000 Current dir is {} 000\n'.format(os.getcwd()))
    os.mkdir(out)
    return out

'''    
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
                    fb = fbrw.get_reader_writer_set_fbnum(f, dist_sev_time)
                    
                    # invocation of the disturbance-module-specific code happens via DMM
                    DMM[d].do_special(fb, s, t)
                    fbrw.do_simple_scaling(fb, DMM[d].get_scaling_params(s, t))
                    
                    fb.Write(outname)
'''
                    
def process_dependently(files, outdir):
    for f in files:
        f = os.path.join(invoking_dir, f)
        for d in fbrw.DISTURBANCE:
            for s in fbrw.SEVERITY:
                # name the output file the basename plus the code for disturbance, severity, and timestep
                #  For instance, FB_0165_FCCS.xml -> FB_0165_FCCS_511.xml
                basename = os.path.splitext(os.path.split(f)[1])[0]
                
                # get the reader/writer object, pass in the aggregated code. 
                #  The required fb.Read() method will have been called before
                #  the object is returned.
                fb = fbrw.get_reader_writer(f)
                
                for t in fbrw.TIMESTEP:
                    dist_sev_time = '{}{}{}'.format(DCM[d], s, t)
                    outname = '{}/{}_{}.xml'.format(outdir, basename, dist_sev_time)
                    
                    # invocation of the disturbance-module-specific code happens via DMM
                    DMM[d].do_special(fb, s, t)
                    fbrw.do_simple_scaling(fb, DMM[d].get_scaling_params(s, t))
                    fbrw.set_fb_number(fb, dist_sev_time)
                    fb.Write(outname)


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#   Start
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if len(sys.argv) > 1:
    files = sys.argv[1:]
    outdir = create_output_dirs(invoking_dir)
    process_dependently(files, outdir)
    os.chdir(invoking_dir)
    exit(0)

print('\nError: missing files to process')
print('\tpython main.py ../fuelbeds/*.xml\n')
exit(1)
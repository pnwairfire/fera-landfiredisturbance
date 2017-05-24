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
    return retval

if retrive_fbwrite_library():
    import fbrw
import fire
import wind
import insects

# Maps a string to an imported module. DISTURBANCE_MODULE_MAP = DMM
DMM = {
    'fire': fire,
    'wind': wind,
    'insects': insects,
}

# Maps a string to a LANDFIRE disturbance code. DISTURBANCE_CODE_MAP = DCM
DCM = {
    'fire': 1,
    #'mechanical_add': 2,
    #'mechanical_remove': 3,
    'wind': 4,
    'insects': 5,
}

'''
{ 1,"Broadleaf Forest" },
{ 2,"Conifer Forest" },
{ 3,"Grassland" },
{ 4,"Mixed Forest" },
{ 5,"Savanna" },
{ 6,"Shrubland" },
{ 7,"Slash" },

{ 7,"SRM 107: Western Juniper-Big Sagebrush-Bluebunch Wheatgrass" },
{ 165,"SRM 210: Bitterbrush" },
{ 186,"SRM 314: Big Sagebrush-Bluebunch Wheatgrass" },
{ 187,"SRM 315: Big Sagebrush-Idaho Fescue" },
{ 188,"SRM 316: Big Sagebrush-Rough Fescue" },
{ 189,"SRM 317: Bitterbrush-Bluebunch Wheatgrass" },
{ 190,"SRM 318: Bitterbrush-Idaho Fescue" },
{ 191,"SRM 319: Bitterbrush-Rough Fescue" },
{ 192,"SRM 320: Black Sagebrush-Bluebunch Wheatgrass" },
{ 193,"SRM 321: Black Sagebrush-Idaho Fescue" },
{ 196,"SRM 324: Threetip Sagebrush-Idaho Fescue" },
{ 197,"SRM 401: Basin Big Sagebrush" },
{ 198,"SRM 402: Mountain Big Sagebrush" },
{ 199,"SRM 403: Wyoming Big Sagebrush" },
{ 200,"SRM 404: Treetip Sagebrush" },
{ 201,"SRM 405: Black Sagebrush" },
{ 202,"SRM 406: Low Sagebrush" },
{ 203,"SRM 407: Stiff Sagebrush" },
{ 204,"SRM 408: Other Sagebrush Types" },
{ 205,"SRM 409: Tall Forb (Great Basin)" },
'''
MINIMUM_CANOPY_COVER = 'minimum_canopy_cover'
VALID_VEG_FORMS = 'valid_vegetation_forms'
VALID_COVER_TYPES = 'valid_cover_types'

FUELBED_PREREQUISITES = {
    'fire': {},
    #'mechanical_add': {},
    #'mechanical_remove': {},
    'wind': {},
    'insects': {
        VALID_VEG_FORMS: ([1,2,4,5,6], fbrw.prereq_vegform_insects),
        MINIMUM_CANOPY_COVER: (30, fbrw.prereq_canopy_cover),
    }
}

def satisfies_prereqs(fb, disturbance_type):
    retval = (True, None)
    prereqs = FUELBED_PREREQUISITES[disturbance_type]
    for pr in prereqs.keys():
        value, func = prereqs[pr]
        check, reason = func(fb, value)
        if not check:
            retval = (False, reason)
            assert reason, 'Error: missing reason - {}'.format(func)
            break
    return retval
    

OUT_DIR = 'out'
def create_output_dirs(invocation_dir):
    out = os.path.join(invocation_dir, OUT_DIR)
    if os.path.exists(out): shutil.rmtree(out)
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
        print(f)
        
        for d in fbrw.DISTURBANCE:                       
            for s in fbrw.SEVERITY:
                #  The required fb.Read() method will have been called before
                #  the object is returned.
                fb = fbrw.get_reader_writer(f)
                original_fb_number = fbrw.get_fb_number(fb).strip()
                check_prereqs, reason = satisfies_prereqs(fb, d)
                
                if check_prereqs:
                    # name the output file the basename plus the code for disturbance, severity, and timestep
                    #  For instance, FB_0165_FCCS.xml -> FB_0165_FCCS_511.xml
                    basename = os.path.splitext(os.path.split(f)[1])[0]
                    for t in fbrw.TIMESTEP:
                        dist_sev_time = '{}{}{}'.format(DCM[d], s, t)
                        outname = '{}/{}_{}.xml'.format(outdir, basename, dist_sev_time)
                        
                        # invocation of the disturbance-module-specific code happens via DMM
                        DMM[d].do_special(fb, s, t)
                        
                        # scale operations happen second
                        fbrw.do_simple_scaling(fb, DMM[d].get_scaling_params(s, t))                        
                        
                        fb_number = '{}_{}'.format(original_fb_number, dist_sev_time)
                        fbrw.set_fb_number(fb, fb_number)
                        fb.Write(outname)
                        print('Writing {}\n'.format(outname))
                else:
                    print('Skipping "{}" bad prereqs for disturbance {}\n\tReason: {}'.format(f, d, reason))


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#   Start
#   This script is invoked with a file glob indicating the files to process.
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
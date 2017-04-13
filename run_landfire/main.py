# =============================================================================
#
# Author:	Kjell Swedin
# Purpose:	Drive the calculations of the entire suite of disturbances against the fuelbeds that ship with FFT
#                   Run FCCS on the generated fuelbeds
#                    - produces FCCS results .csv file
#                    - produces a Consume loadings file
#                    - third file that Susan needs to specify
#
# =============================================================================
import os
import zipfile
import shutil
import requests

FUELBED_ZIP = 'fuelbeds.zip'
FUELBED_DIR = 'fuelbeds'

OUTPUT_DIR = 'out'

# Get the appropriate fuelbeds
def get_fuelbeds():
    def clean_slate():
        try:
            os.remove(FUELBED_ZIP)
            shutil.rmtree(FUELBED_DIR)
        except:
            pass
    
    success = True
    clean_slate()
    cmd = 'wget http://172.16.0.120:8081/artifactory/generic-local/Fuelbeds/3.0/{}'.format(FUELBED_ZIP)
    os.system(cmd)
    if os.path.exists(FUELBED_ZIP):
        with zipfile.ZipFile(FUELBED_ZIP, 'r') as zip:
            zip.extractall('.')
    else:
        print('\nError: could not retrieve zipfile\n')
        success = False
    return success
        
def invoke_run_disturbance():
    cmd = ' python3 ../run_disturbance/scripts/main.py ./{}/*.xml > /dev/null'.format(FUELBED_DIR)
    #cmd = ' python3 ../run_disturbance/scripts/main.py {}/*.xml'.format(FUELBED_DIR)
    os.system(cmd)
    print('\n --- Current dir is {} ---\n'.format(os.getcwd()))

FCCS = 'fuelbed.jar'    
def get_and_run_fccs():
    print('\nIn get_and_run_fccs()\n')
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
        
    try:
        os.remove(FCCS)
    except OSError:
        pass        
    
    query = 'http://172.16.0.120:8081/artifactory/simple/generic-local/fccs'
    r = requests.get(query)
    latest_build = latest(r)
    cmd = 'wget http://172.16.0.120:8081/artifactory/generic-local/fccs/{}/fuelbed.jar'.format(latest_build)
    os.system(cmd)
    
    if os.path.exists(FCCS):
        cmd = 'java -jar {} {}/*.xml > /dev/null'.format(FCCS, OUTPUT_DIR)
        print('\n --- Current dir is {} --- Run FCCS...\n'.format(os.getcwd()))
        os.system(cmd)
    else:
        print('\nError: could not retrieve FCCS jar file\n')


# ++++++++++++++++++++++++++++++++++++++++++
#  Start...
# ++++++++++++++++++++++++++++++++++++++++++
if get_fuelbeds():
    invoke_run_disturbance()
    get_and_run_fccs()
    
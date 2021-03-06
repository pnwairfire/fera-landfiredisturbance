# =============================================================================
#
# Author:   Kjell Swedin
# Purpose: Drive regression test
#
# =============================================================================
import os
import sys
import pandas as pd
import glob
import numpy as np
import re

CALCULATED_VALUES = 'calculated_values.csv'
EXPECTED_VALUES = 'expected.csv'
SCRATCH_FILENAME = 'zorK123.csv'
OUTDIR = './out'

OPTIONAL_LOADING = {
    'eGROUND_FUEL_BASAL_ACCUMULATION_LOADING',
    'eGROUND_FUEL_DUFF_LOWER_LOADING',
    'eGROUND_FUEL_DUFF_UPPER_LOADING',
    'eGROUND_FUEL_SQUIRREL_MIDDENS_LOADING',
    'eMOSS_LICHEN_LITTER_GROUND_LICHEN_LOADING',
    'eMOSS_LICHEN_LITTER_LITTER_LOADING',
    'eMOSS_LICHEN_LITTER_MOSS_LOADING',
    'eSHRUBS_PRIMARY_LAYER_LOADING',
    'eSHRUBS_SECONDARY_LAYER_LOADING'
    }
    
# Disturbance spec directories
DDIRS = [
    '1_Fire',
    '2_MechAdd',
    '3_MechRemove',
    '4_Wind',
    '5_Insects'
]
DDIRS_MAP = {
    'fire': '1_Fire',
    'mechadd': '2_MechAdd',
    'mechremove': '3_MechRemove',
    'wind': '4_Wind',
    'insects': '5_Insects'
}


# =============================================================================
#   Remove all the artifacts generated by running this script -- "make clean"
# =============================================================================
CLEAN = 'clean'
def clean():
    def on_error():
        print('some sort of error...')
    
    for i in [CALCULATED_VALUES, EXPECTED_VALUES, SCRATCH_FILENAME]:
        try:
            os.remove(i)
        except: pass
    for i in [OUTDIR]:
        try:
            cmd = 'rm -fr {}'.format(OUTDIR)
            os.system(cmd)
        except: pass
        
def is_clean(argv):
    yes_clean = False
    for j in [i.lower() for i in argv]:
        if CLEAN in j:
            yes_clean = True
            break
    return yes_clean

def calculate_values(disturbances):
    cmd = 'python3 ../run_disturbance/scripts/main.py {} regression_fuelbeds/*.xml > /dev/null'.format(' '.join(disturbances))
    print(cmd)
    os.system(cmd)

def collect_calculated_values():
    def get_values(filename):
        cmd = 'python3 print_values_from_xml.py {}> {}'.format(filename, SCRATCH_FILENAME)
        os.system(cmd)
        df = pd.read_csv(SCRATCH_FILENAME, header=None, names=['Variable', 'Value'])
        df.fillna(0, inplace=True)
        os.unlink(SCRATCH_FILENAME)
        return df

    def get_values_from_files():
        first_time = True
        df_out = None
        files = glob.glob('{}/*.xml'.format(OUTDIR))
        for f in files:
            print(f)
            df = get_values(f)
            colname = f[len(OUTDIR)+1:].split('.')[0]
            if not first_time:
                df_out[colname] = df.Value
            else:
                df_out = pd.DataFrame({'Variable': df.Variable, colname: df.Value})
                first_time = False
        df_out.to_csv(CALCULATED_VALUES, index=False)
    get_values_from_files()
    
def build_expected_value_csv(disturbances):
    def load_dataframe_merge_if_possible(file, df0):
        print('Trying to load {}...'.format(file))
        df = pd.read_csv(file);
        cols = [col for col in df.columns if 'Variable' == col or re.match('^FB_.+\d\d\d$', col)]
        drop_these = set(df.columns).difference(cols)
        df.drop(drop_these, axis=1, inplace=True)
        
        # start with an empty dataframe, in which case no merge happens. Subsequent invocations
        #  should merge and it should succeed
        if not df0.empty:
            df0 = df0.merge(df, on='Variable')
        else:
            df0 = df
        return df0
        
    def build_individual_expected_value_files(disturbances):
        curr_dir = os.getcwd()
        os.chdir('../specifications')
        for dir in disturbances:
            dir = DDIRS_MAP[dir]
            os.chdir(dir)
            files = glob.glob('*.csv')
            df = pd.DataFrame()
            for f in files:
                if re.match('^\d\d_.+$', f):
                    df = load_dataframe_merge_if_possible(f, df)
            outfile = '../{}_expected.csv'.format(dir.split('_')[1].lower())
            df.to_csv(outfile , index=False)
            os.chdir('..')
        os.chdir(curr_dir)


    build_individual_expected_value_files(disturbances)
    
    files = []
    for d in disturbances:
        files.append('../specifications/{}_expected.csv'.format(d))
    
    df_result = pd.read_csv(files[0])
    for f in files[1:]:
        print('   Merging {} expected values'.format(f))
        df = pd.read_csv(f)
        df_result = pd.merge(df_result, df, on='Variable')
    df_result.to_csv(EXPECTED_VALUES, index=False)
    
def compare_outputs():
    def compare_item(zip_item):
        # item looks like: ((14, 60.0), (14, '60'))
        retval = False
        try:
            calculated = float(zip_item[1][1])
            retval = np.isclose(zip_item[0][1], calculated, rtol=1e-02)
        except:
            pass
        return retval
        
    print('\n\nComparing outputs...')    
    df_expected = pd.read_csv(EXPECTED_VALUES)
    df_calculated = pd.read_csv(CALCULATED_VALUES)
    compare_these = set(df_expected.columns).intersection(set(df_calculated.columns))
    skip_these = set(df_calculated.columns).difference(set(df_expected.columns))
    
    # drop columns that expected doesn't have
    df_calculated.drop(skip_these, axis=1, inplace=True)
    if len(skip_these):
        print('\nDropping these columns in the comparison... this is a bad sign...')
        for i in skip_these:
            print('\t{}'.format(i))
        print()
    
    # remove rows that expected doesn't have
    df_calculated = df_calculated[df_calculated.Variable.isin(df_expected.Variable)]
    
    # check - remove this if the optional loading rows are removed from the specifications
    assert set() == set(df_expected.Variable).difference(set(df_calculated.Variable))
    
    # remove optional loading columns
    df_expected = df_expected[df_expected.Variable.isin(df_calculated.Variable)]
    
    # order identically
    df_expected = df_expected.sort_values('Variable').reset_index(drop=True)
    df_calculated = df_calculated.sort_values('Variable').reset_index(drop=True)
    
    columns = sorted(list(df_expected.columns))
    columns.remove('Variable')
    compare_count = 0
    compare_successful = 0
    compare_failed = 0
    files_skipped = []
    for column in columns:
        print(' --- ', column)
        if column in df_calculated.columns:
            column_errors = 0
            for count, i in enumerate(zip(df_expected.get(column).iteritems(), df_calculated.get(column).iteritems())):
                if not compare_item(i):
                    compare_failed += 1
                    column_errors += 1
                    print('\tFAILURE: {} expected\t: {} calculated ({}_{})'.format(
                            np.round(float(i[0][1]), 3),
                            np.round(float(i[1][1]), 3),
                            df_expected.Variable[i[0][0]], column.split('_')[-1]))
                else:
                    compare_successful += 1
                compare_count += 1
            print('\t{} errors in {} comparisons'.format(column_errors, count))
        else:
            print('\tskipped. Not in calculated columns'.format())
            files_skipped.append(column)
    
    if len(files_skipped):
        print('\nThe following files did not have calculated values. Were they skipped?')
        for i in files_skipped:
            print('\t{}'.format(i))
    print('\n{} Comparisons\n\t{} Successful\n\t{} Unsuccessful'.format(compare_count, compare_successful, compare_failed))
    return compare_failed

# Allow command line arguments to limit regressions to specified disturbances    
def get_disturbance_dirs(args):
    ddirs = []
    check_against = [i.split('_')[1].lower() for i in DDIRS]
    if len(args) > 0:
        for item in args:
            item = item.lower()
            for d in check_against:
                if item in d:
                    ddirs.append(item)
    else:
        ddirs = check_against
    return ddirs
    
    
# ++++++++++++++++++++++++++++++++++++++++++
#  Start...
# ++++++++++++++++++++++++++++++++++++++++++
clean()
if len(sys.argv) > 1 and is_clean(sys.argv):
    exit(0)
else:
    ddirs = get_disturbance_dirs(sys.argv[1:])
    print(ddirs)
    calculate_values(ddirs)
    collect_calculated_values()
    build_expected_value_csv(ddirs)
    result = compare_outputs()
    exit(result)

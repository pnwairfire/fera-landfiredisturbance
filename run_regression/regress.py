# =============================================================================
#
# Author:   Kjell Swedin
# Purpose: Drive regression test
#
# =============================================================================
import os
import pandas as pd
import glob
import numpy as np

CALCULATED_VALUES = 'calculated_values.csv'
EXPECTED_VALUES = 'expected.csv'

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


def calculate_values():
    cmd = 'cd ../run_disturbance && python ./scripts/main.py ./regression_fuelbeds/*.xml > /dev/null && cd ../run_regression'
    os.system(cmd)

def collect_calculated_values():
    cmd = 'cd ../run_disturbance/scripts && python ./collect_values.py > /dev/null'
    os.system(cmd)
    cmd = 'mv ../run_disturbance/scripts/{} .'.format(CALCULATED_VALUES)
    os.system(cmd)
    
    
def build_expected_value_csv():
    files = glob.glob('../specifications/*.xlsx')
    df_result = pd.read_excel(files[0], sheetname='Expected')
    df_result.drop([i for i in df_result.columns if i.endswith('FCCS')], axis=1, inplace=True)
    for f in files[1:]:
        df = pd.read_excel(f, sheetname='Expected')
        df.drop([i for i in df.columns if i.endswith('FCCS')], axis=1, inplace=True)
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
    
    # remove rows that expected doesn't have
    df_calculated = df_calculated[df_calculated.Variable.isin(df_expected.Variable)]
    
    # check - remove this if the optional loading rows are removed from the specifications
    assert set() == set(df_expected.Variable).difference(set(df_calculated.Variable))
    
    # remove optional loading columns
    df_expected = df_expected[df_expected.Variable.isin(df_calculated.Variable)]
    
    # order identically
    df_expected = df_expected.sort_values('Variable').reset_index(drop=True)
    df_calculated = df_calculated.sort_values('Variable').reset_index(drop=True)
    
    columns = list(df_expected.columns)
    columns.remove('Variable')
    compare_count = 0
    compare_successful = 0
    compare_failed = 0
    for column in columns:
        print(column)
        for i in zip(df_expected.get(column).iteritems(), df_calculated.get(column).iteritems()):
            if not compare_item(i):
                compare_failed += 1
                print('\tFAILURE: {} expected\t: {} calculated ({})'.format(
                        np.round(float(i[0][1]), 3),
                        np.round(float(i[1][1]), 3),
                        df_expected.Variable[i[0][0]]))
            else:
                compare_successful += 1
            compare_count += 1
            
    print('\n{} Comparisons\n\t{} Successful\n\t{} Unsuccessful'.format(compare_count, compare_successful, compare_failed))
    
    
# ++++++++++++++++++++++++++++++++++++++++++
#  Start
# ++++++++++++++++++++++++++++++++++++++++++
calculate_values()
collect_calculated_values()
build_expected_value_csv()
compare_outputs()

# =============================================================================
#
# Author:	Kjell Swedin
# Purpose:	Use data from the fccs_summary file and the consume loadings file to synthesize a FOFEM input file
#
# =============================================================================
import pandas as pd
import os
import numpy as np

FCCS_SUMMARY = 'deliverables/fccs_summary.csv'
CONSUME_LOADINGS = 'deliverables/consume_loadings.csv'
FOFEM_INPUT_CSV = 'deliverables/fofem_input.csv'
RND = 4

# FOFEM col names
'''
FCCSID       Fuelbed_number
Fuelbed      Fuelbed_name
Shrub        Shrub_primary_crown_load + shrub_primary_secondary_load (do not include needle drape)
Herb         Herb_primary_load + herb_secondary_load
0-1/4        Woody_sound_1hr_load
1/4-1        Woody_sound_10hr_load
1-3          Woody_sound_100hr_load
3+           Woody_sound_1000hr_load+Woody_sound_10k_load + Woody_sound_GT10k_load
             + Woody_rotten_1000hr_load+Woody_rotten_10k_load + Woody_rotten_GT10k_load 
%Rotten      Percent of 1000-hr wood that is rotten (%)	Calculated as (rotten 3+ wood/total 3+wood) * 100 
Distribution Would be great to characterize the distribution
             (weighted towards smaller size classes = left,
             even across size classes = even or weighted towards larger size classes = right)
Litter       LLM_litter_load
Duff         Ground_upperduff_load + Ground_lowerduff_load
Duff Depth   duff_upper_depth + duff_lower_depth
'''

MAGIC_DIVIDER = 5
def calc_woody_distribution(smaller, larger):
    return np.where(
        (smaller - larger) > MAGIC_DIVIDER, 'Left',
        (np.where(-MAGIC_DIVIDER > (smaller - larger), 'Right', 'Even')))
    

def process():
    retval = True
    try:
        df_fccs = pd.read_csv(FCCS_SUMMARY)
        df_consume = pd.read_csv(CONSUME_LOADINGS, header=1)
        df_fccs.fillna(0, inplace=True)
        df_consume.fillna(0, inplace=True)
        df_result = pd.DataFrame()
        
        df_result['FCCSID'] = df_fccs.Fuelbed_number
        df_result['Fuelbed'] = df_fccs.Fuelbed_name
        df_result['Shrub'] = (df_fccs.Shrub_primary_load + df_fccs.Shrub_secondary_load).round(RND)
        df_result['Herb'] = (df_fccs.Herb_primary_load + df_fccs.Herb_secondary_load).round(RND)
        df_result['0-1/4'] = df_fccs.Woody_sound_1hr_load.round(RND)
        df_result['1/4-1'] = df_fccs.Woody_sound_10hr_load.round(RND)
        df_result['1-3'] = df_fccs.Woody_sound_100hr_load.round(RND)
        df_result['3+'] = (df_fccs.Woody_sound_1000hr_load \
                          + df_fccs.Woody_sound_10khr_load \
                          + df_fccs.Woody_sound_GT10k_load \
                          + df_fccs.Woody_rotten_1000hr_load \
                          + df_fccs.Woody_rotten_10k_load \
                          + df_fccs.Woody_rotten_GT10k_load).round(RND)
        df_result['%Rotten'] = (
                          (df_fccs.Woody_rotten_1000hr_load
                          + df_fccs.Woody_rotten_10k_load
                          + df_fccs.Woody_rotten_GT10k_load) / df_result['3+']).round(RND)

        df_result['Distribution'] = calc_woody_distribution(
                (df_fccs.Woody_sound_1hr_load+df_fccs.Woody_sound_10hr_load+df_fccs.Woody_sound_100hr_load),
                df_result['3+'])
        df_result['Litter'] = df_fccs.LLM_litter_load.round(RND)
        df_result['Duff'] = (df_fccs.Ground_upperduff_load + df_fccs.Ground_lowerduff_load).round(RND)
        df_result['Duff Depth'] = (df_consume.duff_upper_depth + df_consume.duff_lower_depth).round(RND)
        
        df_result.to_csv(FOFEM_INPUT_CSV, index=False)
    except:
        retval = False
    return retval
    
    
    
# ++++++++++++++++++++++++++++++++++++++++++
#   Start ...
# ++++++++++++++++++++++++++++++++++++++++++
exit_val = 1
print(os.getcwd())
if os.path.exists(FCCS_SUMMARY) and os.path.exists(CONSUME_LOADINGS):
    exit_val = 0 if process() else 1
else:
    print('\nError: Required input files (fccs_summary, consume_loadings) are missing.\n')

# repeat for baseline files
FCCS_SUMMARY = 'baseline/fccs_summary.csv'
CONSUME_LOADINGS = 'baseline/consume_loadings.csv'
FOFEM_INPUT_CSV = 'baseline/fofem_input.csv'

if os.path.exists(FCCS_SUMMARY) and os.path.exists(CONSUME_LOADINGS):
    exit_val = 0 if process() else 1
else:
    print('\nError: Required input files (fccs_summary, consume_loadings) are missing.\n')
    
    
exit(exit_val)
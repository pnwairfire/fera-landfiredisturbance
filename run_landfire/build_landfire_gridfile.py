# =============================================================================
#
# Author:	Kjell Swedin
# Purpose:	Use data from the fccs_summary file and the consume loadings file to
#           assemble the landfire grid file.
#
# =============================================================================
import pandas as pd
import os
import numpy as np

FCCS_SUMMARY = 'deliverables/fccs_summary.csv'
CONSUME_LOADINGS = 'deliverables/consume_loadings.csv'
LANDFIRE_GRID_CSV = 'deliverables/landfire_grid.csv'
RND = 4

def process():
    retval = True
    try:
        df_fccs = pd.read_csv(FCCS_SUMMARY)
        df_consume = pd.read_csv(CONSUME_LOADINGS, header=1)
        df_fccs.fillna(0, inplace=True)
        df_consume.fillna(0, inplace=True)
        df_result = pd.DataFrame()
        
        df_result['FCCSID'] = df_fccs.Fuelbed_number
        df_result['Fuelbed Name'] = df_fccs.Fuelbed_name
        df_result['filename'] = df_fccs.Filename
        df_result['Canopy_total_biomass_tpa'] = ( \
                df_fccs.Tree_aboveground_load \
                + df_fccs.Snag_class1_aboveground_load \
                + df_fccs.Snag_class1_other_load \
                + df_fccs.Snag_class2_load \
                + df_fccs.Snag_class3_load \
                + df_fccs.Ladderfuels_load).round(RND)
        df_result['Canopy_available_fuel_tpa'] = ( \
                df_fccs.Tree_over_crown_load \
                + df_fccs.Tree_mid_crown_load \
                + df_fccs.Tree_under_crown_load \
                + df_fccs.Snag_class1_foliage_crown_load \
                + df_fccs.Snag_class2_load \
                + df_fccs.Snag_class3_load \
                + df_fccs.Ladderfuels_load).round(RND)
        df_result['Shrub_tpa'] = ( \
                df_fccs.Shrub_primary_load \
                + df_fccs.Shrub_secondary_load \
                + df_fccs.Shrub_needleDrape_load).round(RND)
        df_result['Herb_tpa'] = (df_fccs.Herb_primary_load + df_fccs.Herb_secondary_load).round(RND)
        df_result['Wood_tpa'] = ( \
                df_fccs.Woody_sound_1hr_load \
                + df_fccs.Woody_sound_10hr_load \
                + df_fccs.Woody_sound_100hr_load \
                + df_fccs.Woody_sound_1000hr_load \
                + df_fccs.Woody_sound_10khr_load \
                + df_fccs.Woody_sound_GT10k_load \
                + df_fccs.Woody_rotten_1000hr_load \
                + df_fccs.Woody_rotten_10k_load \
                + df_fccs.Woody_rotten_GT10k_load \
                + df_fccs.Woody_pile_load \
                + df_fccs.Woody_stumps_rotten_load \
                + df_fccs.Woody_stumps_lightered_load).round(RND)
        df_result['LLM_tpa'] = ( \
                df_fccs.LLM_litter_load \
                + df_fccs.LLM_lichen_load \
                + df_fccs.LLM_moss_load).round(RND)
        df_result['Ground_tpa'] = ( \
                df_fccs.Ground_upperduff_load \
                + df_fccs.Ground_lowerduff_load \
                + df_fccs.Ground_basalaccum_load \
                + df_fccs.Ground_squirrelmid_load).round(RND)
        df_result['Total_available_fuel_tpa'] = (df_consume.Total_available_fuel_loading).round(RND)
        df_result['Total_aboveground_biomass_tpa'] = (df_fccs.Total_aboveground_biomass).round(RND)

        df_result.to_csv(LANDFIRE_GRID_CSV, index=False)
    except Exception as e:
        print('\nException: {}'.format(e))
        retval = False
    return retval
    
    
    
# ++++++++++++++++++++++++++++++++++++++++++
#   Start ...
# ++++++++++++++++++++++++++++++++++++++++++
exit_val = 1
if os.path.exists(FCCS_SUMMARY) and os.path.exists(CONSUME_LOADINGS):
    exit_val = 0 if process() else 1
else:
    print('\nError: Required input files (fccs_summary, consume_loadings) are missing.\n')
    
# repeat for baseline files
FCCS_SUMMARY = 'baseline/fccs_summary.csv'
CONSUME_LOADINGS = 'baseline/consume_loadings.csv'
LANDFIRE_GRID_CSV = 'baseline/landfire_grid.csv'
    
if os.path.exists(FCCS_SUMMARY) and os.path.exists(CONSUME_LOADINGS):
    exit_val = 0 if process() else 1
else:
    print('\nError: Required input files (fccs_summary, consume_loadings) are missing.\n')
    
exit(exit_val)
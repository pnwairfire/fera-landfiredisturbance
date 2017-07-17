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

FCCS_SUMMARY = 'fccs_summary.csv'
CONSUME_LOADINGS = 'consume_loadings.csv'
LANDFIRE_GRID_CSV = 'landfire_grid.csv'
RND = 4

# Column specs - everything from fccs_summary.csv except as noted
'''
Variable                                    Mapping                             
FCCSID                                                                  
Fuelbed Name                                                            
filename                                                                
Canopy_total_biomass_tpa                    Tree_aboveground_load + Snag_class1_aboveground_load + Snag_class1_other_load + Snag_class2_load + Snag_class3_load + Ladderfuels_load,
Canopy_available_fuel_tpa                   Tree_over_crown_load + Tree_mid_crown_load + Tree_under_crown_load + Snag_class1_foliage_load + Snag_class2_load + Snag_class3_load + Ladderfuels_load
Shrub_tpa                                   Shrub_primary_crown_load + shrub_primary_secondary_load + shrub_needledrape_load
Herb_tpa                                    Herb_primary_load + herb_secondary_load
Wood_tpa                                    Sum of all wood categories EXCEPT for:  Woody_stumps_sound_load
LLM_tpa                                     LLM_litter_load + LLM_lichen_load + LLM_moss_load
Ground_tpa                                  Ground_upperduff_load + Ground_lowerduff_load + Ground_basalaccum_load + Ground_squirrelmid_load
Total available fuel(consume_loadings.csv)  Total_available_fuel_loading
Total aboveground biomass                   Total_aboveground_biomass
'''


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
        print("1")
        df_result['Canopy_total_biomass_tpa'] = ( \
                df_fccs.Tree_aboveground_load \
                + df_fccs.Snag_class1_aboveground_load \
                + df_fccs.Snag_class1_other_load \
                + df_fccs.Snag_class2_load \
                + df_fccs.Snag_class3_load \
                + df_fccs.Ladderfuels_load).round(RND)
        print("2")
        df_result['Canopy_total_biomass_tpa'] = ( \
                df_fccs.Tree_over_crown_load \
                + df_fccs.Tree_mid_crown_load \
                + df_fccs.Tree_under_crown_load \
                + df_fccs.Snag_class1_foliage_load \
                + df_fccs.Snag_class2_load \
                + df_fccs.Snag_class3_load \
                + df_fccs.Ladderfuels_load).round(RND)
        print("3")
        df_result['Shrub_tpa'] = ( \
                df_fccs.Shrub_primary_crown_load \
                + df_fccs.Shrub_primary_load \
                + df_fccs.Shrub_secondary_load \
                + df_fccsshrub_needledrape_load).round(RND)
        print("4")
        df_result['Herb_tpa'] = (df_fccs.Herb_primary_load + df_fccs.Herb_secondary_load).round(RND)
        print("5")
        df_result['Wood_tpa'] = ( \
                df_fccs.Tree_over_crown_load \
                + df_fccs.Tree_mid_crown_load \
                + df_fccs.Tree_under_crown_load \
                + df_fccs.Snag_class1_foliage_load \
                + df_fccs.Snag_class2_load \
                + df_fccs.Snag_class3_load \
                + df_fccs.Ladderfuels_load).round(RND)

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
exit(exit_val)
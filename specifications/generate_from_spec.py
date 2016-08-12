# =============================================================================
#
# Author:   Kjell Swedin
# Purpose: Read excel spreadsheet and emit chunks of python code that can be pasted into disturbance scripts
#
# =============================================================================
import sys
import pandas as pd
import sympy

valid = {
    'eFUELBED_NUMBER',
    'eFUELBED_NAME',
    'eFUELBED_DESCRIPTION',
    'eECOREGION',
    'eVEGETATION_FORM',
    'eSTRUCTURAL_CLASS',
    'eCOVER_TYPE',
    'eCHANGE_AGENT',
    'eNATURAL_FIRE_REGIME',
    'eCONDITION_CLASS',
    'eUSER_NAME',
    'eADDRESS',
    'eAFFILIATION',
    'ePHONE',
    'eFILE_OWNER_EMAIL',
    'eNOTES',
    'eDATE_COLLECTED',
    'eFUELBED_CONFIDENCE',
    'eLITTER_ARRANGEMENT',
    'eLITTER_LITTER_TYPE_SHORT_NEEDLE_PINE_RELATIVE_COVER',
    'eLITTER_LITTER_TYPE_LONG_NEEDLE_PINE_RELATIVE_COVER',
    'eLITTER_LITTER_TYPE_OTHER_CONIFER_RELATIVE_COVER',
    'eLITTER_LITTER_TYPE_BROADLEAF_DECIDUOUS_RELATIVE_COVER',
    'eLITTER_LITTER_TYPE_BROADLEAF_EVERGREEN_RELATIVE_COVER',
    'eLITTER_LITTER_TYPE_PALM_FROND_RELATIVE_COVER',
    'eLITTER_LITTER_TYPE_GRASS_RELATIVE_COVER',
    'eSHRUBS_NEEDLE_DRAPE_AFFECTS_FIRE_BEHAVIOR',
    'eCANOPY_LADDER_FUELS_MAXIMUM_HEIGHT',
    'eCANOPY_LADDER_FUELS_MINIMUM_HEIGHT',
    'eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_DIAMETER',
    'eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_HEIGHT',
    'eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_STEM_DENSITY',
    'eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_DIAMETER',
    'eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_HEIGHT',
    'eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_HEIGHT_TO_CROWN_BASE',
    'eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_PERCENT_COVER',
    'eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_STEM_DENSITY',
    'eCANOPY_SNAGS_CLASS_2_DIAMETER',
    'eCANOPY_SNAGS_CLASS_2_HEIGHT',
    'eCANOPY_SNAGS_CLASS_2_STEM_DENSITY',
    'eCANOPY_SNAGS_CLASS_3_DIAMETER',
    'eCANOPY_SNAGS_CLASS_3_HEIGHT',
    'eCANOPY_SNAGS_CLASS_3_STEM_DENSITY',
    'eCANOPY_TREES_MIDSTORY_DIAMETER_AT_BREAST_HEIGHT',
    'eCANOPY_TREES_MIDSTORY_HEIGHT',
    'eCANOPY_TREES_MIDSTORY_HEIGHT_TO_LIVE_CROWN',
    'eCANOPY_TREES_MIDSTORY_PERCENT_COVER',
    'eCANOPY_TREES_MIDSTORY_STEM_DENSITY',
    'eCANOPY_TREES_OVERSTORY_DIAMETER_AT_BREAST_HEIGHT',
    'eCANOPY_TREES_OVERSTORY_HEIGHT',
    'eCANOPY_TREES_OVERSTORY_HEIGHT_TO_LIVE_CROWN',
    'eCANOPY_TREES_OVERSTORY_PERCENT_COVER',
    'eCANOPY_TREES_OVERSTORY_STEM_DENSITY',
    'eCANOPY_TREES_TOTAL_PERCENT_COVER',
    'eCANOPY_TREES_UNDERSTORY_DIAMETER_AT_BREAST_HEIGHT',
    'eCANOPY_TREES_UNDERSTORY_HEIGHT',
    'eCANOPY_TREES_UNDERSTORY_HEIGHT_TO_LIVE_CROWN',
    'eCANOPY_TREES_UNDERSTORY_PERCENT_COVER',
    'eCANOPY_TREES_UNDERSTORY_STEM_DENSITY',
    'eGROUND_FUEL_BASAL_ACCUMULATION_DEPTH',
    'eGROUND_FUEL_BASAL_ACCUMULATION_NUMBER_PER_UNIT_AREA',
    'eGROUND_FUEL_BASAL_ACCUMULATION_RADIUS',
    'eGROUND_FUEL_BASAL_ACCUMULATION_LOADING',
    'eGROUND_FUEL_DUFF_LOWER_DEPTH',
    'eGROUND_FUEL_DUFF_LOWER_PERCENT_COVER',
    'eGROUND_FUEL_DUFF_LOWER_LOADING',
    'eGROUND_FUEL_DUFF_UPPER_DEPTH',
    'eGROUND_FUEL_DUFF_UPPER_PERCENT_COVER',
    'eGROUND_FUEL_DUFF_UPPER_LOADING',
    'eGROUND_FUEL_SQUIRREL_MIDDENS_DEPTH',
    'eGROUND_FUEL_SQUIRREL_MIDDENS_NUMBER_PER_UNIT_AREA',
    'eGROUND_FUEL_SQUIRREL_MIDDENS_RADIUS',
    'eGROUND_FUEL_SQUIRREL_MIDDENS_LOADING',
    'eHERBACEOUS_PRIMARY_LAYER_HEIGHT',
    'eHERBACEOUS_PRIMARY_LAYER_LOADING',
    'eHERBACEOUS_PRIMARY_LAYER_PERCENT_COVER',
    'eHERBACEOUS_PRIMARY_LAYER_PERCENT_LIVE',
    'eHERBACEOUS_SECONDARY_LAYER_HEIGHT',
    'eHERBACEOUS_SECONDARY_LAYER_LOADING',
    'eHERBACEOUS_SECONDARY_LAYER_PERCENT_COVER',
    'eHERBACEOUS_SECONDARY_LAYER_PERCENT_LIVE',
    'eMOSS_LICHEN_LITTER_GROUND_LICHEN_DEPTH',
    'eMOSS_LICHEN_LITTER_GROUND_LICHEN_PERCENT_COVER',
    'eMOSS_LICHEN_LITTER_GROUND_LICHEN_LOADING',
    'eMOSS_LICHEN_LITTER_LITTER_DEPTH',
    'eMOSS_LICHEN_LITTER_LITTER_PERCENT_COVER',
    'eMOSS_LICHEN_LITTER_LITTER_LOADING',
    'eMOSS_LICHEN_LITTER_MOSS_DEPTH',
    'eMOSS_LICHEN_LITTER_MOSS_PERCENT_COVER',
    'eMOSS_LICHEN_LITTER_MOSS_LOADING',
    'eSHRUBS_PRIMARY_LAYER_HEIGHT',
    'eSHRUBS_PRIMARY_LAYER_PERCENT_COVER',
    'eSHRUBS_PRIMARY_LAYER_PERCENT_LIVE',
    'eSHRUBS_PRIMARY_LAYER_LOADING',
    'eSHRUBS_SECONDARY_LAYER_HEIGHT',
    'eSHRUBS_SECONDARY_LAYER_PERCENT_COVER',
    'eSHRUBS_SECONDARY_LAYER_PERCENT_LIVE',
    'eSHRUBS_SECONDARY_LAYER_LOADING',
    'eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH',
    'eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER',
    'eWOODY_FUEL_PILES_CLEAN_LOADING',
    'eWOODY_FUEL_PILES_DIRTY_LOADING',
    'eWOODY_FUEL_PILES_VERYDIRTY_LOADING',
    'eWOODY_FUEL_ROTTEN_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_GREATER_THAN_TWENTY_INCHES',
    'eWOODY_FUEL_ROTTEN_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_NINE_TO_TWENTY_INCHES',
    'eWOODY_FUEL_ROTTEN_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_THREE_TO_NINE_INCHES',
    'eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_GREATER_THAN_TWENTY_INCHES',
    'eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_NINE_TO_TWENTY_INCHES',
    'eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_THREE_TO_NINE_INCHES',
    'eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES',
    'eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH',
    'eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH',
    'eWOODY_FUEL_STUMPS_LIGHTERED_PITCHY_DIAMETER',
    'eWOODY_FUEL_STUMPS_LIGHTERED_PITCHY_HEIGHT',
    'eWOODY_FUEL_STUMPS_LIGHTERED_PITCHY_STEM_DENSITY',
    'eWOODY_FUEL_STUMPS_ROTTEN_DIAMETER',
    'eWOODY_FUEL_STUMPS_ROTTEN_HEIGHT',
    'eWOODY_FUEL_STUMPS_ROTTEN_STEM_DENSITY',
    'eWOODY_FUEL_STUMPS_SOUND_DIAMETER',
    'eWOODY_FUEL_STUMPS_SOUND_HEIGHT',
    'eWOODY_FUEL_STUMPS_SOUND_STEM_DENSITY'
}

def emit_for_step(pd_series, severity, timestep):
    # severity and timestep are only for error reporting
    noteworthy = []
    for item in pd_series.iteritems():
        id = item[0]
        try:
            if id in valid:
                if str(item[1]).startswith('*'):
                    multiplier = item[1].split('=')[1].strip()
                    
                    # use sympy to parse/simplify arithmetic expressions eg. - (1/0.05) * 0.5
                    multiplier = sympy.sympify(multiplier).round(3)
                    
                    print('(libfbrw.FBTypes.{}, {}),'.format(item[0], multiplier))
                else:
                    if 'nan' in str(item[1]): continue
                    noteworthy.append('{} : {}'.format(item[1], item[0]))
            else:
                print('Invalid id - {}'.format(id))
        except:
            print('\nException {} : {} {}'.format(id, severity, timestep))
            
    if len(noteworthy):
        print('\n --------  Check these ----------')
        for i in noteworthy:
            print('\t{}'.format(i))

TIMESTEPS = ['Time Step 1', 'Time Step 2', 'Time Step 3']
def process_disturbance_spec(filename):
    def make_sorted_severity_list(unsorted_list):
        tmp = {}
        for i in unsorted_list:
            tmp[i[:2]] = i
        retval = []
        retval.append(tmp['Lo'])
        retval.append(tmp['Mo'])
        retval.append(tmp['Hi'])
        return retval
        
    df = pd.read_excel(filename, sheetname='Specs', header=[0,1])
    
    #  columns will vary by disturbance, but should always have the severity specifier
    severity_columns = make_sorted_severity_list(
        [i for i in df.columns.levels[0] if 'Low' in i or 'Moderate' in i or 'High' in i])
    
    for s in severity_columns:
        for t in TIMESTEPS:
            print('\n{} : {}'.format(s, t))
            emit_for_step(df[s][t], s, t)
                
# ++++++++++++++++++++++++++++++++++++++++++
#  Start
# ++++++++++++++++++++++++++++++++++++++++++
if len(sys.argv) > 1:
    for f in sys.argv[1:]:
        process_disturbance_spec(f)
else:
    print('\nPlease supply a spreadsheet file from which to derive the python code.\n')
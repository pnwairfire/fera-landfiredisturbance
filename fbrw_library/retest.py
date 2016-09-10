import libfbrw
import glob

buckets = [
    libfbrw.FBTypes.eFUELBED_NUMBER,
    libfbrw.FBTypes.eFUELBED_NAME,
    libfbrw.FBTypes.eFUELBED_DESCRIPTION,
    libfbrw.FBTypes.eECOREGION,
    libfbrw.FBTypes.eVEGETATION_FORM,
    libfbrw.FBTypes.eSTRUCTURAL_CLASS,
    libfbrw.FBTypes.eCOVER_TYPE,
    libfbrw.FBTypes.eCHANGE_AGENT,
    libfbrw.FBTypes.eNATURAL_FIRE_REGIME,
    libfbrw.FBTypes.eCONDITION_CLASS,
    libfbrw.FBTypes.eUSER_NAME,
    libfbrw.FBTypes.eADDRESS,
    libfbrw.FBTypes.eAFFILIATION,
    libfbrw.FBTypes.ePHONE,
    libfbrw.FBTypes.eFILE_OWNER_EMAIL,
    libfbrw.FBTypes.eNOTES,
    libfbrw.FBTypes.eDATE_COLLECTED,
    libfbrw.FBTypes.eFUELBED_CONFIDENCE,
    libfbrw.FBTypes.eLITTER_ARRANGEMENT,
    libfbrw.FBTypes.eLITTER_LITTER_TYPE_SHORT_NEEDLE_PINE_RELATIVE_COVER,
    libfbrw.FBTypes.eLITTER_LITTER_TYPE_LONG_NEEDLE_PINE_RELATIVE_COVER,
    libfbrw.FBTypes.eLITTER_LITTER_TYPE_OTHER_CONIFER_RELATIVE_COVER,
    libfbrw.FBTypes.eLITTER_LITTER_TYPE_BROADLEAF_DECIDUOUS_RELATIVE_COVER,
    libfbrw.FBTypes.eLITTER_LITTER_TYPE_BROADLEAF_EVERGREEN_RELATIVE_COVER,
    libfbrw.FBTypes.eLITTER_LITTER_TYPE_PALM_FROND_RELATIVE_COVER,
    libfbrw.FBTypes.eLITTER_LITTER_TYPE_GRASS_RELATIVE_COVER,
    libfbrw.FBTypes.eSHRUBS_NEEDLE_DRAPE_AFFECTS_FIRE_BEHAVIOR,
    libfbrw.FBTypes.eCANOPY_LADDER_FUELS_MAXIMUM_HEIGHT,
    libfbrw.FBTypes.eCANOPY_LADDER_FUELS_MINIMUM_HEIGHT,
    libfbrw.FBTypes.eCANOPY_LADDER_FUELS_TYPE,
    libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_DIAMETER,
    libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_HEIGHT,
    libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_STEM_DENSITY,
    libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_DIAMETER,
    libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_HEIGHT,
    libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_HEIGHT_TO_CROWN_BASE,
    libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_PERCENT_COVER,
    libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_STEM_DENSITY,
    libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_DIAMETER,
    libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_HEIGHT,
    libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_STEM_DENSITY,
    libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_DIAMETER,
    libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_HEIGHT,
    libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_STEM_DENSITY,
    libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_DIAMETER_AT_BREAST_HEIGHT,
    libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_HEIGHT,
    libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_HEIGHT_TO_LIVE_CROWN,
    libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_PERCENT_COVER,
    libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_STEM_DENSITY,
    libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_DIAMETER_AT_BREAST_HEIGHT,
    libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_HEIGHT,
    libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_HEIGHT_TO_LIVE_CROWN,
    libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_PERCENT_COVER,
    libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_STEM_DENSITY,
    libfbrw.FBTypes.eCANOPY_TREES_TOTAL_PERCENT_COVER,
    libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_DIAMETER_AT_BREAST_HEIGHT,
    libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_HEIGHT,
    libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_HEIGHT_TO_LIVE_CROWN,
    libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_PERCENT_COVER,
    libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_STEM_DENSITY,
    libfbrw.FBTypes.eGROUND_FUEL_BASAL_ACCUMULATION_DEPTH,
    libfbrw.FBTypes.eGROUND_FUEL_BASAL_ACCUMULATION_NUMBER_PER_UNIT_AREA,
    libfbrw.FBTypes.eGROUND_FUEL_BASAL_ACCUMULATION_RADIUS,
    libfbrw.FBTypes.eGROUND_FUEL_DUFF_LOWER_DEPTH,
    libfbrw.FBTypes.eGROUND_FUEL_DUFF_LOWER_PERCENT_COVER,
    libfbrw.FBTypes.eGROUND_FUEL_DUFF_UPPER_DEPTH,
    libfbrw.FBTypes.eGROUND_FUEL_DUFF_UPPER_PERCENT_COVER,
    libfbrw.FBTypes.eGROUND_FUEL_SQUIRREL_MIDDENS_DEPTH,
    libfbrw.FBTypes.eGROUND_FUEL_SQUIRREL_MIDDENS_NUMBER_PER_UNIT_AREA,
    libfbrw.FBTypes.eGROUND_FUEL_SQUIRREL_MIDDENS_RADIUS,
    libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_HEIGHT,
    libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_LOADING,
    libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_COVER,
    libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_LIVE,
    libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_HEIGHT,
    libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_LOADING,
    libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_COVER,
    libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_LIVE,
    libfbrw.FBTypes.eMOSS_LICHEN_LITTER_GROUND_LICHEN_DEPTH,
    libfbrw.FBTypes.eMOSS_LICHEN_LITTER_GROUND_LICHEN_PERCENT_COVER,
    libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_DEPTH,
    libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_PERCENT_COVER,
    libfbrw.FBTypes.eMOSS_LICHEN_LITTER_MOSS_DEPTH,
    libfbrw.FBTypes.eMOSS_LICHEN_LITTER_MOSS_PERCENT_COVER,
    libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_HEIGHT,
    libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER,
    libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_LIVE,
    libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_HEIGHT,
    libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER,
    libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_LIVE,
    libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH,
    libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER,
    libfbrw.FBTypes.eWOODY_FUEL_PILES_CLEAN_LOADING,
    libfbrw.FBTypes.eWOODY_FUEL_PILES_DIRTY_LOADING,
    libfbrw.FBTypes.eWOODY_FUEL_PILES_VERYDIRTY_LOADING,
    libfbrw.FBTypes.eWOODY_FUEL_ROTTEN_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_GREATER_THAN_TWENTY_INCHES,
    libfbrw.FBTypes.eWOODY_FUEL_ROTTEN_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_NINE_TO_TWENTY_INCHES,
    libfbrw.FBTypes.eWOODY_FUEL_ROTTEN_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_THREE_TO_NINE_INCHES,
    libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_GREATER_THAN_TWENTY_INCHES,
    libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_NINE_TO_TWENTY_INCHES,
    libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_THREE_TO_NINE_INCHES,
    libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,
    libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,
    libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,
    libfbrw.FBTypes.eWOODY_FUEL_STUMPS_LIGHTERED_PITCHY_DIAMETER,
    libfbrw.FBTypes.eWOODY_FUEL_STUMPS_LIGHTERED_PITCHY_HEIGHT,
    libfbrw.FBTypes.eWOODY_FUEL_STUMPS_LIGHTERED_PITCHY_STEM_DENSITY,
    libfbrw.FBTypes.eWOODY_FUEL_STUMPS_ROTTEN_DIAMETER,
    libfbrw.FBTypes.eWOODY_FUEL_STUMPS_ROTTEN_HEIGHT,
    libfbrw.FBTypes.eWOODY_FUEL_STUMPS_ROTTEN_STEM_DENSITY,
    libfbrw.FBTypes.eWOODY_FUEL_STUMPS_SOUND_DIAMETER,
    libfbrw.FBTypes.eWOODY_FUEL_STUMPS_SOUND_HEIGHT,
    libfbrw.FBTypes.eWOODY_FUEL_STUMPS_SOUND_STEM_DENSITY,
]

files = glob.glob('fuelbeds/*_new.xml')

for f in files:
    fb = libfbrw.FuelbedValues(f)
    print('\n{}\n'.format(f))
    fb.Read()
    for bucket in buckets:
        value = fb.GetValue(bucket)
        if "666" != value:
            print('FAILED : {} : {}'.format(bucket, value))
        else:
            print('SUCCESS : {} : {}'.format(bucket, value))
    
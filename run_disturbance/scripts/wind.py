# =============================================================================
#
# Author:	Kjell Swedin
# Purpose:	Wind disturbance
#
# =============================================================================
import sys
import libfbrw
import fbrw
import special_processing as sp

scale_these = {
    fbrw.SEVERITY[0]: {
        fbrw.TIMESTEP[0]: [
            (libfbrw.FBTypes.eCANOPY_TREES_TOTAL_PERCENT_COVER,0.850,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_PERCENT_COVER,0.850,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_STEM_DENSITY,0.850,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_PERCENT_COVER,0.850,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_STEM_DENSITY,0.850,""),
            (libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_STEM_DENSITY,0.850,""),
            (libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_PERCENT_COVER,0.850,""),
            (libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_STEM_DENSITY,0.850,""),
            (libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_STEM_DENSITY,0.850,""),
            (libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_STEM_DENSITY,0.850,""),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER,0.900,""),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_LIVE,0.900,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER,0.900,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_LIVE,0.900,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH,1.250,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER,1.250,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,1.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,1.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,1.500,""),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_DEPTH,1.250,""),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_PERCENT_COVER,1.250,""),
        ],
        fbrw.TIMESTEP[1]: [
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER,1.100,""),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_LIVE,1.100,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER,1.100,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_LIVE,1.100,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_LOADING,1.100,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_COVER,1.100,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_LOADING,1.100,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_COVER,1.100,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_THREE_TO_NINE_INCHES,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_NINE_TO_TWENTY_INCHES,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_GREATER_THAN_TWENTY_INCHES,0.750,""),
            (libfbrw.FBTypes.eGROUND_FUEL_DUFF_UPPER_DEPTH,1.250,""),
            (libfbrw.FBTypes.eGROUND_FUEL_DUFF_UPPER_PERCENT_COVER,1.250,""),
        ],
        fbrw.TIMESTEP[2]: [
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER,1.010,""),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_LIVE,1.010,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER,1.010,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_LIVE,1.010,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH,0.250,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER,0.250,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,0.250,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,0.250,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,0.250,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_THREE_TO_NINE_INCHES,0.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_NINE_TO_TWENTY_INCHES,0.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_GREATER_THAN_TWENTY_INCHES,0.500,""),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_DEPTH,0.800,""),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_PERCENT_COVER,0.800,""),
        ],
    },
    fbrw.SEVERITY[1]: {
        fbrw.TIMESTEP[0]: [
            (libfbrw.FBTypes.eCANOPY_TREES_TOTAL_PERCENT_COVER,0.550,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_PERCENT_COVER,0.550,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_STEM_DENSITY,0.550,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_PERCENT_COVER,0.550,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_STEM_DENSITY,0.550,""),
            (libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_STEM_DENSITY,0.550,""),
            (libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_PERCENT_COVER,0.550,""),
            (libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_STEM_DENSITY,0.550,""),
            (libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_STEM_DENSITY,0.550,""),
            (libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_STEM_DENSITY,0.550,""),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER,0.700,""),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_LIVE,0.700,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER,0.700,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_LIVE,0.700,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH,1.500,"min=1"),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER,1.500,"min=75"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,2.000,"min=2"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,2.000,"min=1"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,2.000,"min=0.2"),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_DEPTH,1.500,""),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_PERCENT_COVER,1.500,""),
        ],
        fbrw.TIMESTEP[1]: [
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER,1.300,""),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_LIVE,1.300,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER,1.300,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_LIVE,1.300,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_LOADING,1.200,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_COVER,1.200,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_LOADING,1.200,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_COVER,1.200,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_THREE_TO_NINE_INCHES,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_NINE_TO_TWENTY_INCHES,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_GREATER_THAN_TWENTY_INCHES,0.750,""),
            (libfbrw.FBTypes.eGROUND_FUEL_DUFF_UPPER_DEPTH,1.500,""),
            (libfbrw.FBTypes.eGROUND_FUEL_DUFF_UPPER_PERCENT_COVER,1.500,""),
        ],
        fbrw.TIMESTEP[2]: [
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER,1.300,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER,1.300,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_LIVE,1.300,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,0.250,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,0.250,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,0.250,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_THREE_TO_NINE_INCHES,0.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_NINE_TO_TWENTY_INCHES,0.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_GREATER_THAN_TWENTY_INCHES,0.500,""),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_DEPTH,0.750,""),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_PERCENT_COVER,0.750,""),
        ],
    },
    fbrw.SEVERITY[2]: {
        fbrw.TIMESTEP[0]: [
            (libfbrw.FBTypes.eCANOPY_TREES_TOTAL_PERCENT_COVER,0.250,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_PERCENT_COVER,0.250,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_STEM_DENSITY,0.250,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_PERCENT_COVER,0.250,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_STEM_DENSITY,0.250,""),
            (libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_STEM_DENSITY,0.250,""),
            (libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_PERCENT_COVER,0.250,""),
            (libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_STEM_DENSITY,0.250,""),
            (libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_STEM_DENSITY,0.250,""),
            (libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_STEM_DENSITY,0.250,""),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER,0.500,""),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_LIVE,0.500,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER,0.500,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_LIVE,0.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH,2.000,"min=1"),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER,2.000,"min=75"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,3.000,"min=2"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,3.000,"min=1"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,3.000,"min=0.2"),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_DEPTH,2.000,""),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_PERCENT_COVER,2.000,""),
        ],
        fbrw.TIMESTEP[1]: [
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER,1.500,""),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_LIVE,1.500,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER,1.500,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_LIVE,1.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_LOADING,1.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_COVER,1.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_LOADING,1.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_COVER,1.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_THREE_TO_NINE_INCHES,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_NINE_TO_TWENTY_INCHES,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_GREATER_THAN_TWENTY_INCHES,0.750,""),
            (libfbrw.FBTypes.eGROUND_FUEL_DUFF_UPPER_DEPTH,2.000,""),
            (libfbrw.FBTypes.eGROUND_FUEL_DUFF_UPPER_PERCENT_COVER,2.000,""),
        ],
        fbrw.TIMESTEP[2]: [
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER,1.500,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER,1.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,0.250,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,0.250,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,0.250,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_THREE_TO_NINE_INCHES,0.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_NINE_TO_TWENTY_INCHES,0.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_GREATER_THAN_TWENTY_INCHES,0.500,""),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_DEPTH,0.750,""),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_PERCENT_COVER,0.750,""),
        ],
    },
}
            
def placeholder(fb):
    pass
    
def sound_wood_loadings(fb, multiplier, min1, min2, min3):
    def is_empty():
        total = 0.0
        ids = [
            libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,
            libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,
            libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,
            libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_THREE_TO_NINE_INCHES,
            libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_NINE_TO_TWENTY_INCHES,
            libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_GREATER_THAN_TWENTY_INCHES
        ]
        for i in ids:
            value = fb.GetValue(i)
            try:
                total += float(value)
            except:
                pass
        return total > 0

    def check_and_set(fb, os, ms, check_value, id, multiplier, min):
        if os > check_value or ms > check_value:
            fbrw.scale(fb, id, multiplier, min)
        else:
            pass
            #fb.SetValue(id, "")
        
    os_diameter = fb.GetValue(libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_DIAMETER_AT_BREAST_HEIGHT)
    os_diameter = float(os_diameter) if len(os_diameter) else 0.0
    ms_diameter = fb.GetValue(libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_DIAMETER_AT_BREAST_HEIGHT)
    ms_diameter = float(ms_diameter) if len(ms_diameter) else 0.0
    
    check_and_set(fb, os_diameter, ms_diameter, 3,
        libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_THREE_TO_NINE_INCHES,
        multiplier, 'min={}'.format(min1))
    check_and_set(fb, os_diameter, ms_diameter, 9,
        libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_NINE_TO_TWENTY_INCHES,
        multiplier, 'min={}'.format(min2))
    check_and_set(fb, os_diameter, ms_diameter, 20,
        libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_GREATER_THAN_TWENTY_INCHES,
        multiplier, 'min={}'.format(min3))
    
    if is_empty():
        fb.SetNodeEmpty(libfbrw.FBNodeWithSpeciesType.eWOODY_FUEL_SOUND_WOOD_ALL_SOUND_WOOD)
        
        
 
  
special_funcs = {
    fbrw.SEVERITY[0]: {
        fbrw.TIMESTEP[0]: [ (sound_wood_loadings, 2, 0, 0, 0) ],
        fbrw.TIMESTEP[1]: [ (placeholder,), (sp.process_sound_wood, 0.25)],
        fbrw.TIMESTEP[2]: [ (placeholder,), (sp.process_sound_wood, 0.5)],
    },
    fbrw.SEVERITY[1]: {
        fbrw.TIMESTEP[0]: [ (sound_wood_loadings, 2.5, 3, 6.5, 7.5) ],
        fbrw.TIMESTEP[1]: [ (placeholder,), (sp.process_sound_wood, 0.25)],
        fbrw.TIMESTEP[2]: [ (placeholder,), (sp.process_sound_wood, 0.5)],
    },
    fbrw.SEVERITY[2]: {
        fbrw.TIMESTEP[0]: [ (sound_wood_loadings, 4, 3, 6.5, 7.5) ],
        fbrw.TIMESTEP[1]: [ (placeholder,), (sp.process_sound_wood, 0.25)],
        fbrw.TIMESTEP[2]: [ (placeholder,), (sp.process_sound_wood, 0.5)],
    }
}
  
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#   Required functions for a disturbance module
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def do_special(fb, severity, timestep):
    for item in special_funcs[severity][timestep]:
        func = item[0]
        if len(item) > 1:
            args = item[1:]
            func(fb, *args)
        else:
            func(fb)
        
def get_scaling_params(severity, timestep):
    return scale_these[severity][timestep]
        
        
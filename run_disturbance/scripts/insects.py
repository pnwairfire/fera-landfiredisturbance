#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Name:        insects.py
# Purpose:     Transformations for Insects and Disease
#
#
# Author:      kjells
#
# Created:     7/7/2014
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import libfbrw
import fbrw
import special_processing as sp

scale_these = {
    fbrw.SEVERITY[0]: {
        fbrw.TIMESTEP[0]: [
            (libfbrw.FBTypes.eCANOPY_TREES_TOTAL_PERCENT_COVER,0.900,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_HEIGHT_TO_LIVE_CROWN,1.100,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_PERCENT_COVER,0.900,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_STEM_DENSITY,0.900,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_HEIGHT_TO_LIVE_CROWN,1.100,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_PERCENT_COVER,0.900,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_STEM_DENSITY,0.900,""),
        ],
        fbrw.TIMESTEP[1]: [
            (libfbrw.FBTypes.eCANOPY_TREES_TOTAL_PERCENT_COVER,0.950,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_PERCENT_COVER,0.950,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_STEM_DENSITY,0.950,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_PERCENT_COVER,0.950,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_STEM_DENSITY,0.950,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH,1.100,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER,1.100,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,1.100,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,1.100,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,1.100,""),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_DEPTH,1.100,""),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_PERCENT_COVER,1.100,""),
        ],
        fbrw.TIMESTEP[2]: [
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH,1.100,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER,1.100,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,1.100,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,1.100,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,1.100,""),
        ],
    },
    fbrw.SEVERITY[1]: {
        fbrw.TIMESTEP[0]: [
            (libfbrw.FBTypes.eCANOPY_TREES_TOTAL_PERCENT_COVER,0.600,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_HEIGHT_TO_LIVE_CROWN,1.200,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_PERCENT_COVER,0.600,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_STEM_DENSITY,0.600,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_HEIGHT_TO_LIVE_CROWN,1.200,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_PERCENT_COVER,0.600,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_STEM_DENSITY,0.600,""),
        ],
        fbrw.TIMESTEP[1]: [
            (libfbrw.FBTypes.eCANOPY_TREES_TOTAL_PERCENT_COVER,0.900,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_PERCENT_COVER,0.900,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_STEM_DENSITY,0.900,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_PERCENT_COVER,0.900,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_STEM_DENSITY,0.900,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_LOADING,1.250,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_COVER,1.250,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_LOADING,1.250,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_COVER,1.250,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH,1.250,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER,1.250,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,1.250,"min=3"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,1.250,"min=2"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,1.250,"min=1"),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_DEPTH,1.500,""),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_PERCENT_COVER,1.500,""),
        ],
        fbrw.TIMESTEP[2]: [
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH,1.250,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER,1.250,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,1.250,"min=3"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,1.250,"min=2"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,1.250,"min=1"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_THREE_TO_NINE_INCHES,1.250,"min=4"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_NINE_TO_TWENTY_INCHES,1.250,"min=4"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_GREATER_THAN_TWENTY_INCHES,1.250,"min=4"),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_DEPTH,0.667,""),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_PERCENT_COVER,0.667,""),
            (libfbrw.FBTypes.eGROUND_FUEL_DUFF_UPPER_DEPTH,1.100,""),
            (libfbrw.FBTypes.eGROUND_FUEL_DUFF_UPPER_PERCENT_COVER,1.100,""),
        ],
    },
    fbrw.SEVERITY[2]: {
        fbrw.TIMESTEP[0]: [
            (libfbrw.FBTypes.eCANOPY_TREES_TOTAL_PERCENT_COVER,0.250,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_HEIGHT_TO_LIVE_CROWN,1.300,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_PERCENT_COVER,0.250,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_STEM_DENSITY,0.250,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_HEIGHT_TO_LIVE_CROWN,1.300,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_PERCENT_COVER,0.250,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_STEM_DENSITY,0.250,""),
        ],
        fbrw.TIMESTEP[1]: [
            (libfbrw.FBTypes.eCANOPY_TREES_TOTAL_PERCENT_COVER,0.900,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_PERCENT_COVER,0.900,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_STEM_DENSITY,0.900,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_PERCENT_COVER,0.900,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_STEM_DENSITY,0.900,""),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER,1.250,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER,1.250,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_LOADING,1.400,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_COVER,1.400,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_LOADING,1.400,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_COVER,1.400,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH,1.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER,1.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,1.250,"min=3"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,1.250,"min=2"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,1.250,"min=1"),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_DEPTH,2.000,""),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_PERCENT_COVER,2.000,""),
        ],
        fbrw.TIMESTEP[2]: [
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,1.250,"min=3"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,1.250,"min=2"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,1.250,"min=1"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_THREE_TO_NINE_INCHES,2.000,"min=4"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_NINE_TO_TWENTY_INCHES,2.000,"min=4"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_GREATER_THAN_TWENTY_INCHES,2.000,"min=4"),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_DEPTH,0.500,""),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_PERCENT_COVER,0.500,""),
            (libfbrw.FBTypes.eGROUND_FUEL_DUFF_UPPER_DEPTH,1.300,""),
            (libfbrw.FBTypes.eGROUND_FUEL_DUFF_UPPER_PERCENT_COVER,1.300,""),
        ],
    },
}
    
def placeholder(fb):
    pass
  
special_funcs = {
    fbrw.SEVERITY[0]: {
        fbrw.TIMESTEP[0]: [ (sp.process_canopy_v1, 0.1, 0.1, 0.1) ],
        fbrw.TIMESTEP[1]: [ (sp.process_canopy_v2, False), (sp.process_sound_wood, 0.25)],
        fbrw.TIMESTEP[2]: [ (sp.process_canopy_v3,), (sp.process_sound_wood, 0.5)],
    },
    fbrw.SEVERITY[1]: {
        fbrw.TIMESTEP[0]: [ (sp.process_canopy_v1, 0.4, 0.4, 0.4) ],
        fbrw.TIMESTEP[1]: [ (sp.process_canopy_v4,), (sp.process_sound_wood, 0.25)],
        fbrw.TIMESTEP[2]: [ (sp.process_canopy_v2, False), (sp.process_sound_wood, 0.5)],
    },
    fbrw.SEVERITY[2]: {
        fbrw.TIMESTEP[0]: [ (sp.process_canopy_v1, 0.75, 0.75, 0.75) ],
        fbrw.TIMESTEP[1]: [ (sp.process_canopy_v4,), (sp.process_sound_wood, 0.25)],
        fbrw.TIMESTEP[2]: [ (sp.process_canopy_v2, False), (sp.process_sound_wood, 0.5)],
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
    
        
        
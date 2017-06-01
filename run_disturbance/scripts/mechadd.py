# =============================================================================
#
# Author:	Kjell Swedin
# Purpose:	Mechanical add disturbance
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
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_DIAMETER_AT_BREAST_HEIGHT,1.100,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_HEIGHT_TO_LIVE_CROWN,1.250,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_PERCENT_COVER,0.750,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_STEM_DENSITY,0.750,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_DIAMETER_AT_BREAST_HEIGHT,1.100,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_HEIGHT_TO_LIVE_CROWN,1.250,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_PERCENT_COVER,0.750,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_STEM_DENSITY,0.750,""),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_PERCENT_COVER,0.250,""),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_STEM_DENSITY,0.250,""),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER,0.750,""),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_LIVE,0.500,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER,0.750,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_LIVE,0.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_LOADING,0.750,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_COVER,0.750,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_LIVE,0.750,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_LOADING,0.750,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_COVER,0.750,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_LIVE,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH,1.250,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER,1.250,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,1.250,"min=0.5"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,1.250,"min=1"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,1.250,"min=0.5"),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_DEPTH,1.250,""),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_PERCENT_COVER,1.250,""),
        ],
        fbrw.TIMESTEP[1]: [
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER,1.100,""),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_LIVE,2.000,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER,1.100,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_LIVE,2.000,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_LOADING,1.250,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_COVER,1.250,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_LIVE,1.333,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_LOADING,1.250,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_COVER,1.250,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_LIVE,1.333,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_THREE_TO_NINE_INCHES,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_NINE_TO_TWENTY_INCHES,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_GREATER_THAN_TWENTY_INCHES,0.750,""),
        ],
        fbrw.TIMESTEP[2]: [
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER,1.100,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER,1.100,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_LOADING,1.250,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_COVER,1.250,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_LOADING,1.250,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_COVER,1.250,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH,0.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER,0.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,0.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,0.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,0.500,""),
        ],
    },
    fbrw.SEVERITY[1]: {
        fbrw.TIMESTEP[0]: [
            (libfbrw.FBTypes.eCANOPY_TREES_TOTAL_PERCENT_COVER,0.670,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_DIAMETER_AT_BREAST_HEIGHT,1.250,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_HEIGHT_TO_LIVE_CROWN,1.500,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_PERCENT_COVER,0.500,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_STEM_DENSITY,0.500,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_DIAMETER_AT_BREAST_HEIGHT,1.250,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_HEIGHT_TO_LIVE_CROWN,1.500,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_PERCENT_COVER,0.500,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_STEM_DENSITY,0.500,""),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_DIAMETER_AT_BREAST_HEIGHT,0,""),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_HEIGHT_TO_LIVE_CROWN,0,""),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_HEIGHT,0,""),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_PERCENT_COVER,0,""),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_STEM_DENSITY,0,""),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER,0.500,""),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_LIVE,0.250,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER,0.500,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_LIVE,0.250,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_LOADING,0.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_COVER,0.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_LIVE,0.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_LOADING,0.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_COVER,0.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_LIVE,0.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH,1.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER,1.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,1.500,"min=1"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,1.500,"min=2"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,1.500,"min=1"),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_DEPTH,1.500,""),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_PERCENT_COVER,1.500,""),
        ],
        fbrw.TIMESTEP[1]: [
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER,1.250,""),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_LIVE,4.000,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER,1.250,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_LIVE,4.000,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_LOADING,1.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_COVER,1.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_LIVE,2.000,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_LOADING,1.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_COVER,1.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_LIVE,2.000,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_THREE_TO_NINE_INCHES,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_NINE_TO_TWENTY_INCHES,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_GREATER_THAN_TWENTY_INCHES,0.750,""),
        ],
        fbrw.TIMESTEP[2]: [
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER,1.250,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER,1.250,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_LOADING,1.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_COVER,1.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_LOADING,1.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_COVER,1.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH,0.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER,0.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,0.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,0.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,0.500,""),
            (libfbrw.FBTypes.eGROUND_FUEL_DUFF_UPPER_DEPTH,1.200,""),
            (libfbrw.FBTypes.eGROUND_FUEL_DUFF_UPPER_PERCENT_COVER,1.200,""),
        ],
    },
    fbrw.SEVERITY[2]: {
        fbrw.TIMESTEP[0]: [
            (libfbrw.FBTypes.eCANOPY_TREES_TOTAL_PERCENT_COVER,0.330,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_DIAMETER_AT_BREAST_HEIGHT,1.250,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_HEIGHT_TO_LIVE_CROWN,1.500,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_PERCENT_COVER,0.250,""),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_STEM_DENSITY,0.250,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_DIAMETER_AT_BREAST_HEIGHT,1.250,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_HEIGHT_TO_LIVE_CROWN,1.500,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_PERCENT_COVER,0.250,""),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_STEM_DENSITY,0.250,""),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_DIAMETER_AT_BREAST_HEIGHT,0,""),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_HEIGHT_TO_LIVE_CROWN,0,""),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_HEIGHT,0,""),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_PERCENT_COVER,0,""),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_STEM_DENSITY,0,""),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER,0.250,""),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_LIVE,0.250,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER,0.250,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_LIVE,0.250,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_LOADING,0.250,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_COVER,0.250,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_LIVE,0.250,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_LOADING,0.250,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_COVER,0.250,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_LIVE,0.250,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH,2.000,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER,2.000,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,2.000,"min=1.5"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,2.000,"min=3"),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,2.000,"min=1.5"),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_DEPTH,1.750,""),
            (libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_PERCENT_COVER,1.750,""),
        ],
        fbrw.TIMESTEP[1]: [
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER,1.500,""),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_LIVE,4.000,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER,1.500,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_LIVE,4.000,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_LOADING,1.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_COVER,1.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_LIVE,4.000,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_LOADING,1.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_COVER,1.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_LIVE,4.000,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_THREE_TO_NINE_INCHES,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_NINE_TO_TWENTY_INCHES,0.750,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_GREATER_THAN_TWENTY_INCHES,0.750,""),
        ],
        fbrw.TIMESTEP[2]: [
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER,1.500,""),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER,1.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_LOADING,1.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_COVER,1.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_LOADING,1.500,""),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_COVER,1.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH,0.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER,0.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES,0.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH,0.500,""),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH,0.500,""),
            (libfbrw.FBTypes.eGROUND_FUEL_DUFF_UPPER_DEPTH,1.400,""),
            (libfbrw.FBTypes.eGROUND_FUEL_DUFF_UPPER_PERCENT_COVER,1.400,""),
        ],
    },
}
            
def placeholder(fb):
    pass
  
special_funcs = {
    fbrw.SEVERITY[0]: {
        fbrw.TIMESTEP[0]: [ (sp.add_stumps, 0.25, 0.25) ],
        fbrw.TIMESTEP[1]: [ (sp.process_sound_wood, 0.25) ],
        fbrw.TIMESTEP[2]: [ (sp.sound_to_rotten_stumps,), (sp.process_sound_wood, 0.5)],
    },
    fbrw.SEVERITY[1]: {
        fbrw.TIMESTEP[0]: [ (sp.add_stumps, 0.5, 0.5) ],
        fbrw.TIMESTEP[1]: [ (sp.process_sound_wood, 0.25) ],
        fbrw.TIMESTEP[2]: [ (sp.sound_to_rotten_stumps,), (sp.process_sound_wood, 0.5)],
    },
    fbrw.SEVERITY[2]: {
        fbrw.TIMESTEP[0]: [ (sp.add_stumps, 0.75, 0.75) ],
        fbrw.TIMESTEP[1]: [ (sp.process_sound_wood, 0.25)],
        fbrw.TIMESTEP[2]: [ (sp.sound_to_rotten_stumps,), (sp.process_sound_wood, 0.5)],
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
        
        
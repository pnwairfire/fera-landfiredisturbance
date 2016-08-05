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

scale_these = {
    fbrw.SEVERITY[0]: {
        fbrw.TIMESTEP[0]: [
            (libfbrw.FBTypes.eCANOPY_TREES_TOTAL_PERCENT_COVER, 0.9),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_HEIGHT_TO_LIVE_CROWN, 1.1),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_PERCENT_COVER, 0.9),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_STEM_DENSITY, 0.9),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_HEIGHT_TO_LIVE_CROWN, 1.1),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_PERCENT_COVER, 0.9),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_STEM_DENSITY, 0.9),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_HEIGHT_TO_LIVE_CROWN, 1.1),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_PERCENT_COVER, 0.9),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_STEM_DENSITY, 0.9),
            ],
        fbrw.TIMESTEP[1]: [
            (libfbrw.FBTypes.eCANOPY_TREES_TOTAL_PERCENT_COVER, 0.95),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_HEIGHT_TO_LIVE_CROWN, 1.05),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_PERCENT_COVER, 0.95),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_STEM_DENSITY, 0.95),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_PERCENT_COVER, 0.95),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_STEM_DENSITY, 0.95),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_HEIGHT_TO_LIVE_CROWN, 1.05),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_PERCENT_COVER, 0.95),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_STEM_DENSITY, 0.95),
            ],
        fbrw.TIMESTEP[2]: []
    },
    fbrw.SEVERITY[1]: {
        fbrw.TIMESTEP[0]: [
            (libfbrw.FBTypes.eCANOPY_TREES_TOTAL_PERCENT_COVER, 0.6),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_HEIGHT_TO_LIVE_CROWN, 1.2),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_PERCENT_COVER, 0.6),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_STEM_DENSITY, 0.6),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_HEIGHT_TO_LIVE_CROWN, 1.2),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_PERCENT_COVER, 0.6),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_STEM_DENSITY, 0.6),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_HEIGHT_TO_LIVE_CROWN, 1.1),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_PERCENT_COVER, 0.8),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_STEM_DENSITY, 0.8),
            ],
        fbrw.TIMESTEP[1]: [
            (libfbrw.FBTypes.eCANOPY_TREES_TOTAL_PERCENT_COVER, 0.9),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_PERCENT_COVER, 0.9),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_STEM_DENSITY, 0.9),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_PERCENT_COVER, 0.9),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_STEM_DENSITY, 0.9),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_PERCENT_COVER, 0.9),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_STEM_DENSITY, 0.9),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_HEIGHT, 1.25),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER, 1.25),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_HEIGHT, 1.25),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER, 1.25),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_HEIGHT, 1.25),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_LOADING, 1.25),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_COVER, 1.25),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_HEIGHT, 1.25),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_LOADING, 1.25),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_COVER, 1.25),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH, 1.2),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER, 1.2),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES, 1.2),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH, 1.2),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH, 1.2)
            ],
        fbrw.TIMESTEP[2]: [
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH, 1.25),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER, 1.25),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES, 1.25),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH, 1.25),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH, 1.25),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_GREATER_THAN_TWENTY_INCHES, 1.25),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_NINE_TO_TWENTY_INCHES, 1.25),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_THREE_TO_NINE_INCHES, 1.25)
            ]
    },
    fbrw.SEVERITY[2]: {
        fbrw.TIMESTEP[0]: [
            (libfbrw.FBTypes.eCANOPY_TREES_TOTAL_PERCENT_COVER, 0.25),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_HEIGHT_TO_LIVE_CROWN, 1.5),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_PERCENT_COVER, 0.25),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_STEM_DENSITY, 0.25),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_HEIGHT_TO_LIVE_CROWN, 1.5),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_PERCENT_COVER, 0.25),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_STEM_DENSITY, 0.25),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_HEIGHT_TO_LIVE_CROWN, 1.5),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_PERCENT_COVER, 0.3),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_STEM_DENSITY, 0.3),
            ],
        fbrw.TIMESTEP[1]: [
            (libfbrw.FBTypes.eCANOPY_TREES_TOTAL_PERCENT_COVER, 0.9),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_PERCENT_COVER, 0.9),
            (libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_STEM_DENSITY, 0.9),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_PERCENT_COVER, 0.9),
            (libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_STEM_DENSITY, 0.9),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_PERCENT_COVER, 0.9),
            (libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_STEM_DENSITY, 0.9),
            (libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER, 1.4),
            (libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER, 1.4),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_LOADING, 1.4),
            (libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_COVER, 1.4),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_LOADING, 1.4),
            (libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_COVER, 1.4),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH, 1.3),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER, 1.3),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES, 1.3),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH, 1.3),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH, 1.3)
            ],
        fbrw.TIMESTEP[2]: [
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_DEPTH, 1.4),
            (libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER, 1.4),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ONE_TO_THREE_INCHES, 1.4),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_QUARTER_INCH_TO_ONE_INCH, 1.4),
            (libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_ZERO_TO_THREE_INCHES_ZERO_TO_QUARTER_INCH, 1.4)
            ]
    },
}

def process_canopy_one(fb, pct_cover_multiplier, ossd_multiplier, mssd_multiplier):
    substitutions = [
        (libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_HEIGHT_TO_CROWN_BASE,
            libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_HEIGHT_TO_LIVE_CROWN),
        (libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_DIAMETER,
            libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_DIAMETER_AT_BREAST_HEIGHT),
        (libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_HEIGHT,
            libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_HEIGHT)
    ]
    for s in substitutions:
        fbrw.assign_if_not_exist(fb, s[0], s[1])
        
    os_cover = fb.GetValue(libfbrw.FBTypes.eCANOPY_TREES_TOTAL_PERCENT_COVER)
    snag_cover = fb.GetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_PERCENT_COVER)
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_PERCENT_COVER,
            fbrw.add(snag_cover, fbrw.mul(os_cover, pct_cover_multiplier)))
    
    os_stem_density = fb.GetValue(libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_STEM_DENSITY)
    ms_stem_density = fb.GetValue(libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_STEM_DENSITY)
    snag_stem_density = fb.GetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_STEM_DENSITY)
    tmp = fbrw.add(fbrw.mul(os_stem_density, ossd_multiplier), fbrw.mul(ms_stem_density, mssd_multiplier))
    new_density = fbrw.add(snag_stem_density, tmp)
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_STEM_DENSITY, new_density)
    
def process_canopy_low_two(fb):
    # assign 'with_foliage' to 'others', save 'others'
    other_diameter = fbrw.assign_and_return_current(fb,
        libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_DIAMETER,
        libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_DIAMETER)
    other_height = fbrw.assign_and_return_current(fb,
        libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_HEIGHT,
        libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_HEIGHT)
    other_sd = fbrw.assign_and_return_current(fb,
        libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_STEM_DENSITY,
        libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_STEM_DENSITY)

    # zero 'with_foliage'
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_DIAMETER, '0')
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_HEIGHT, '0')
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_HEIGHT_TO_CROWN_BASE, '0')
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_PERCENT_COVER, '0')
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_STEM_DENSITY, '0')
    
    # move 'other' values into 'class_2', save class_2
    two_diameter = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_DIAMETER, other_diameter)
    two_height = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_HEIGHT, other_height)
    two_sd = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_STEM_DENSITY, other_sd)
    
    # move 'class_2' to 'class_3'
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_DIAMETER, two_diameter)
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_HEIGHT, two_height)
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_STEM_DENSITY, two_sd)
    
def process_canopy_low_three(fb):
    # zero 'others', save values
    other_diameter = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_DIAMETER, '0')
    other_height = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_HEIGHT, '0')
    other_sd = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_STEM_DENSITY, '0')
    
    # move 'other' values into 'class_2', save class_2
    two_diameter = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_DIAMETER, other_diameter)
    two_height = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_HEIGHT, other_height)
    two_sd = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_STEM_DENSITY, other_sd)
    
    # move 'class_2' to 'class_3'
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_DIAMETER, two_diameter)
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_HEIGHT, two_height)
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_STEM_DENSITY, two_sd)
    
def process_canopy_moderate_two(fb):
    # assign 'with_foliage' to 'others', save 'others'
    other_diameter = fbrw.assign_and_return_current(fb,
        libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_DIAMETER,
        libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_DIAMETER)
    other_height = fbrw.assign_and_return_current(fb,
        libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_HEIGHT,
        libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_HEIGHT)
    other_sd = fbrw.assign_and_return_current(fb,
        libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_STEM_DENSITY,
        libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_STEM_DENSITY)
    
    # move 'other' values into 'class_2', save class_2
    two_diameter = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_DIAMETER, other_diameter)
    two_height = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_HEIGHT, other_height)
    two_sd = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_STEM_DENSITY, other_sd)
    
    # move 'class_2' to 'class_3'
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_DIAMETER, two_diameter)
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_HEIGHT, two_height)
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_STEM_DENSITY, two_sd)
    
    process_canopy_one(fb, 0.1, 0.1, 0.1)

    
    
def placeholder(fb):
    pass
  
special_funcs = {
    fbrw.SEVERITY[0]: {
        fbrw.TIMESTEP[0]: [ (process_canopy_one, 0.1, 0.1, 0.1) ],
        fbrw.TIMESTEP[1]: [ (process_canopy_low_two,) ],
        fbrw.TIMESTEP[2]: [ (process_canopy_low_three,) ],
    },
    fbrw.SEVERITY[1]: {
        fbrw.TIMESTEP[0]: [ (process_canopy_one, 0.4, 0.4, 0.4) ],
        fbrw.TIMESTEP[1]: [ (process_canopy_moderate_two,) ],
        fbrw.TIMESTEP[2]: [ (process_canopy_low_two,) ],
    },
    fbrw.SEVERITY[2]: {
        fbrw.TIMESTEP[0]: [ (process_canopy_one, 0.75, 0.75, 0.75) ],
        fbrw.TIMESTEP[1]: [ (process_canopy_moderate_two,) ],
        fbrw.TIMESTEP[2]: [ (process_canopy_low_two,) ],
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
    
        
        
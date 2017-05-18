# =============================================================================
#
# Author:	Kjell Swedin
# Purpose:	Disturbance processing routines that are NOT simple scaling operations. They are called from the 
#                   do_special() function that every distrubance script must implement.
#
#                   Note: the functions are used from different timesteps and severities so informative names are 
#                   hard to come by. 
#
# =============================================================================
import libfbrw
import fbrw


def process_canopy_v1(fb, pct_cover_multiplier, ossd_multiplier, mssd_multiplier):
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
    fbrw.assign_species_if_not_exist(fb,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_SPECIES_SPECIES_DESCRIPTION,
        libfbrw.FBSpeciesTypes.eCANOPY_TREES_OVERSTORY_SPECIES_SPECIES_DESCRIPTION)
        
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
    
def process_canopy_v2(fb, zero_snags_with_foliage):
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

    if zero_snags_with_foliage:
        fb.SetNodeEmpty(libfbrw.FBNodeWithSpeciesType.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE)
    
    # move 'other' values into 'class_2', save class_2
    two_diameter = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_DIAMETER, other_diameter)
    two_height = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_HEIGHT, other_height)
    two_sd = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_STEM_DENSITY, other_sd)
    fbrw.assign_species_if_not_exist(fb,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_2_SPECIES_SPECIES_DESCRIPTION,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_SPECIES_SPECIES_DESCRIPTION)
    
    # move 'class_2' to 'class_3'
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_DIAMETER, two_diameter)
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_HEIGHT, two_height)
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_STEM_DENSITY, two_sd)
    fbrw.assign_species_if_not_exist(fb,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_3_SPECIES_SPECIES_DESCRIPTION,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_2_SPECIES_SPECIES_DESCRIPTION)
    
def process_canopy_v3(fb):
    # zero 'others', save values
    other_diameter = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_DIAMETER, '0')
    other_height = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_HEIGHT, '0')
    other_sd = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_STEM_DENSITY, '0')
    fb.SetNodeEmpty(libfbrw.FBNodeWithSpeciesType.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS)
    
    # move 'other' values into 'class_2', save class_2
    two_diameter = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_DIAMETER, other_diameter)
    two_height = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_HEIGHT, other_height)
    two_sd = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_STEM_DENSITY, other_sd)
    fbrw.assign_species_if_not_exist(fb,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_2_SPECIES_SPECIES_DESCRIPTION,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_SPECIES_SPECIES_DESCRIPTION)
    
    # move 'class_2' to 'class_3'
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_DIAMETER, two_diameter)
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_HEIGHT, two_height)
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_STEM_DENSITY, two_sd)
    fbrw.assign_species_if_not_exist(fb,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_3_SPECIES_SPECIES_DESCRIPTION,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_2_SPECIES_SPECIES_DESCRIPTION)
    
    
def process_canopy_v4(fb):
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
    fbrw.assign_species_if_not_exist(fb,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_2_SPECIES_SPECIES_DESCRIPTION,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_SPECIES_SPECIES_DESCRIPTION)
    
    # move 'class_2' to 'class_3'
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_DIAMETER, two_diameter)
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_HEIGHT, two_height)
    fb.SetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_STEM_DENSITY, two_sd)
    fbrw.assign_species_if_not_exist(fb,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_3_SPECIES_SPECIES_DESCRIPTION,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_2_SPECIES_SPECIES_DESCRIPTION)
    
    process_canopy_v1(fb, 0.1, 0.1, 0.1)
    
def process_sound_wood(fb, swood_multiplier):
    fbrw.add_scaled_value_to_specified(
        fb,
        libfbrw.FBTypes.eWOODY_FUEL_ROTTEN_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_THREE_TO_NINE_INCHES,
        libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_THREE_TO_NINE_INCHES,
        swood_multiplier)
    fbrw.add_scaled_value_to_specified(
        fb,
        libfbrw.FBTypes.eWOODY_FUEL_ROTTEN_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_NINE_TO_TWENTY_INCHES,
        libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_NINE_TO_TWENTY_INCHES,
        swood_multiplier)
    fbrw.add_scaled_value_to_specified(
        fb,
        libfbrw.FBTypes.eWOODY_FUEL_ROTTEN_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_GREATER_THAN_TWENTY_INCHES,
        libfbrw.FBTypes.eWOODY_FUEL_SOUND_WOOD_LOADINGS_GREATER_THAN_THREE_INCHES_GREATER_THAN_TWENTY_INCHES,
        swood_multiplier)





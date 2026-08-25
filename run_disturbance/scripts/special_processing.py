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
    fbrw.set_value(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_PERCENT_COVER,
            fbrw.add(snag_cover, fbrw.mul(os_cover, pct_cover_multiplier)))
    
    os_stem_density = fb.GetValue(libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_STEM_DENSITY)
    ms_stem_density = fb.GetValue(libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_STEM_DENSITY)
    snag_stem_density = fb.GetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_STEM_DENSITY)
    tmp = fbrw.add(fbrw.mul(os_stem_density, ossd_multiplier), fbrw.mul(ms_stem_density, mssd_multiplier))
    new_density = fbrw.add(snag_stem_density, tmp)
    fbrw.set_value(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_STEM_DENSITY, new_density)
    
    # set dbh for snags w/ foliage 
    os_dbh = fb.GetValue(libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_DIAMETER_AT_BREAST_HEIGHT)
    ms_dbh = fb.GetValue(libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_DIAMETER_AT_BREAST_HEIGHT)
    
    if not len(os_stem_density): os_stem_density = "0"
    if not len(os_dbh): os_dbh = "0"
    snag_dbh_overstory_numerator = fbrw.mul(os_stem_density, os_dbh)
    if not len(ms_stem_density): ms_stem_density = "0"
    if not len(ms_dbh): ms_dbh = "0"
    snag_dbh_midstory_numerator = fbrw.mul(ms_stem_density, ms_dbh)
    snag_dbh_numerator = fbrw.add(snag_dbh_overstory_numerator, snag_dbh_midstory_numerator)
    
    snag_dbh_denominator = fbrw.add(os_stem_density, ms_stem_density)
    if float(snag_dbh_denominator) > 0: 
        snag_dbh = str(float(snag_dbh_numerator) / float(snag_dbh_denominator))
    else:
        snag_dbh = "0"
    fbrw.set_value(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_DIAMETER, snag_dbh)


# call this at step 2 and 3 (before c1_snags_without_foliage)
def c2_snags(fb):
    snag_other_diameter = fb.GetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_DIAMETER)
    snag_other_height = fb.GetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_HEIGHT)
    snag_other_stem_density = fb.GetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_STEM_DENSITY)
    
    fbrw.assign_species_if_not_exist(fb,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_2_SPECIES_SPECIES_DESCRIPTION,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_SPECIES_SPECIES_DESCRIPTION)
    
    fbrw.set_value(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_DIAMETER, snag_other_diameter)
    fbrw.set_value(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_HEIGHT, snag_other_height)
    fbrw.set_value(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_STEM_DENSITY, snag_other_stem_density)
    

# call this at step 2 (after c2_snags)
def c1_snags_without_foliage(fb):
    snag_with_foliage_diameter = fb.GetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_DIAMETER)
    snag_with_foliage_height = fb.GetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_HEIGHT)
    snag_with_foliage_stem_density = fb.GetValue(libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_STEM_DENSITY)

    fbrw.assign_species_if_not_exist(fb,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_SPECIES_SPECIES_DESCRIPTION,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_SPECIES_SPECIES_DESCRIPTION)
    
    fbrw.set_value(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_DIAMETER, snag_with_foliage_diameter)
    fbrw.set_value(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_HEIGHT, snag_with_foliage_height)
    fbrw.set_value(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_STEM_DENSITY, snag_with_foliage_stem_density)
    
    
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
    else:
        process_canopy_v1(fb, 0.05, 0.05, 0.05)
    
    # move 'other' values into 'class_2', save class_2
    two_diameter = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_DIAMETER, other_diameter)
    two_height = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_HEIGHT, other_height)
    two_sd = fbrw.assign_and_return_current(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_2_STEM_DENSITY, other_sd)
    fbrw.assign_species_if_not_exist(fb,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_2_SPECIES_SPECIES_DESCRIPTION,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_1_ALL_OTHERS_SPECIES_SPECIES_DESCRIPTION)
    
    # move 'class_2' to 'class_3'
    fbrw.set_value(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_DIAMETER, two_diameter)
    fbrw.set_value(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_HEIGHT, two_height)
    fbrw.set_value(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_STEM_DENSITY, two_sd)
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
    fbrw.set_value(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_DIAMETER, two_diameter)
    fbrw.set_value(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_HEIGHT, two_height)
    fbrw.set_value(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_STEM_DENSITY, two_sd)
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
    fbrw.set_value(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_DIAMETER, two_diameter)
    fbrw.set_value(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_HEIGHT, two_height)
    fbrw.set_value(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_STEM_DENSITY, two_sd)
    fbrw.assign_species_if_not_exist(fb,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_3_SPECIES_SPECIES_DESCRIPTION,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_2_SPECIES_SPECIES_DESCRIPTION)
    
    process_canopy_v1(fb, 0.1, 0.1, 0.1)
    
        
def process_canopy_v133(fb):
    # zero with_foliage
    fb.SetNodeEmpty(libfbrw.FBNodeWithSpeciesType.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE)

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
    fbrw.set_value(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_DIAMETER, two_diameter)
    fbrw.set_value(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_HEIGHT, two_height)
    fbrw.set_value(fb, libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_3_STEM_DENSITY, two_sd)
    fbrw.assign_species_if_not_exist(fb,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_3_SPECIES_SPECIES_DESCRIPTION,
        libfbrw.FBSpeciesTypes.eCANOPY_SNAGS_CLASS_2_SPECIES_SPECIES_DESCRIPTION)

    
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
        
# Sound stumps get a fixed height of 0.5 meters (1.64 feet) regardless of severity/timestep.
STUMP_SOUND_HEIGHT_FEET = '1.64'

def add_stumps(fb, ossd_multiplier, mssd_multiplier):
    os_stem_density = fb.GetValue(libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_STEM_DENSITY)
    ms_stem_density = fb.GetValue(libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_STEM_DENSITY)
    tmp = fbrw.add(fbrw.mul(os_stem_density, ossd_multiplier), fbrw.mul(ms_stem_density, mssd_multiplier))

    stump_stem_density = fb.GetValue(libfbrw.FBTypes.eWOODY_FUEL_STUMPS_SOUND_STEM_DENSITY)
    new_density = fbrw.add(stump_stem_density, tmp)

    fbrw.set_value(fb, libfbrw.FBTypes.eWOODY_FUEL_STUMPS_SOUND_STEM_DENSITY, new_density)

    add_stump_diameter(fb, os_stem_density, ms_stem_density)
    add_stump_height(fb)
    add_stump_species(fb)

# Diameter = stem-density-weighted average of overstory and midstory DBH (same
# pattern as the snag_dbh calculation in process_canopy_v1). Falls back to '0'
# when neither layer has any stems.
def add_stump_diameter(fb, os_stem_density, ms_stem_density):
    os_dbh = fb.GetValue(libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_DIAMETER_AT_BREAST_HEIGHT)
    ms_dbh = fb.GetValue(libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_DIAMETER_AT_BREAST_HEIGHT)

    # fbrw.mul() only guards its first argument against an empty string, so the
    # diameter operands (2nd arg) need to be blanked to '0' explicitly here -
    # same reasoning as the equivalent guards in process_canopy_v1's snag_dbh calc.
    if not len(os_dbh): os_dbh = '0'
    if not len(ms_dbh): ms_dbh = '0'

    numerator = fbrw.add(fbrw.mul(os_stem_density, os_dbh), fbrw.mul(ms_stem_density, ms_dbh))
    denominator = fbrw.add(os_stem_density, ms_stem_density)
    stump_dbh = str(float(numerator) / float(denominator)) if float(denominator) > 0 else '0'

    fbrw.set_value(fb, libfbrw.FBTypes.eWOODY_FUEL_STUMPS_SOUND_DIAMETER, stump_dbh)

def add_stump_height(fb):
    fbrw.set_value(fb, libfbrw.FBTypes.eWOODY_FUEL_STUMPS_SOUND_HEIGHT, STUMP_SOUND_HEIGHT_FEET)

# Species = overstory + midstory species combined. When both layers have
# species, each layer's relative covers (100% each = 200% combined) are merged
# by TSN and scaled back to 100%. When only one layer has species, use it as-is.
def add_stump_species(fb):
    os_species = fb.GetSpeciesValue(libfbrw.FBSpeciesTypes.eCANOPY_TREES_OVERSTORY_SPECIES_SPECIES_DESCRIPTION)
    ms_species = fb.GetSpeciesValue(libfbrw.FBSpeciesTypes.eCANOPY_TREES_MIDSTORY_SPECIES_SPECIES_DESCRIPTION)

    if os_species and ms_species:
        combined = combine_and_scale_species([os_species, ms_species])
    elif os_species:
        combined = os_species
    elif ms_species:
        combined = ms_species
    else:
        combined = []

    if combined:
        fb.SetSpeciesValue(libfbrw.FBSpeciesTypes.eWOODY_FUEL_STUMPS_SOUND_SPECIES_SPECIES_DESCRIPTION, combined)

# Merge same-TSN entries across the given species lists (each assumed to sum to
# 100%), then scale down so the combined total is 100%. SetSpeciesValue silently
# drops the assignment unless the sum is *exactly* 100.0, so any floating-point
# rounding from the merge is nudged into the largest entry before returning.
def combine_and_scale_species(species_lists):
    totals = {}
    for species_list in species_lists:
        for s in species_list:
            totals[s.tsn] = totals.get(s.tsn, 0.0) + float(s.relativeCover)

    scale_factor = 1.0 / len(species_lists)
    scaled = {tsn: cover * scale_factor for tsn, cover in totals.items()}

    residual = 100.0 - sum(scaled.values())
    if residual:
        biggest_tsn = max(scaled, key=scaled.get)
        scaled[biggest_tsn] += residual

    return [libfbrw.Species(tsn, str(cover)) for tsn, cover in scaled.items()]

def sound_to_rotten_stumps(fb):
    substitutions = [
        (libfbrw.FBTypes.eWOODY_FUEL_STUMPS_ROTTEN_DIAMETER,
            libfbrw.FBTypes.eWOODY_FUEL_STUMPS_SOUND_DIAMETER),
        (libfbrw.FBTypes.eWOODY_FUEL_STUMPS_ROTTEN_HEIGHT,
            libfbrw.FBTypes.eWOODY_FUEL_STUMPS_SOUND_HEIGHT),
    ]
    for s in substitutions:
        fbrw.assign_if_not_exist(fb, s[0], s[1])
        
    fbrw.assign_species_if_not_exist(fb,
        libfbrw.FBSpeciesTypes.eWOODY_FUEL_STUMPS_ROTTEN_SPECIES_SPECIES_DESCRIPTION,
        libfbrw.FBSpeciesTypes.eWOODY_FUEL_STUMPS_SOUND_SPECIES_SPECIES_DESCRIPTION)
        
    fbrw.add_scaled_value_to_specified(
        fb,
        libfbrw.FBTypes.eWOODY_FUEL_STUMPS_ROTTEN_STEM_DENSITY,
        libfbrw.FBTypes.eWOODY_FUEL_STUMPS_SOUND_STEM_DENSITY,
        1)
        
    fb.SetNodeEmpty(libfbrw.FBNodeWithSpeciesType.eWOODY_FUEL_STUMPS_SOUND)
    
def sound_to_lightered_pitchy_stumps(fb):
    substitutions = [
        (libfbrw.FBTypes.eWOODY_FUEL_STUMPS_LIGHTERED_PITCHY_DIAMETER,
            libfbrw.FBTypes.eWOODY_FUEL_STUMPS_SOUND_DIAMETER),
        (libfbrw.FBTypes.eWOODY_FUEL_STUMPS_LIGHTERED_PITCHY_HEIGHT,
            libfbrw.FBTypes.eWOODY_FUEL_STUMPS_SOUND_HEIGHT),
        (libfbrw.FBTypes.eWOODY_FUEL_STUMPS_LIGHTERED_PITCHY_STEM_DENSITY,
            libfbrw.FBTypes.eWOODY_FUEL_STUMPS_SOUND_STEM_DENSITY),
    ]
    for s in substitutions:
        fbrw.assign_if_not_exist(fb, s[0], s[1])
        
    fbrw.assign_species_if_not_exist(fb,
        libfbrw.FBSpeciesTypes.eWOODY_FUEL_STUMPS_LIGHTERED_PITCHY_SPECIES_SPECIES_DESCRIPTION,
        libfbrw.FBSpeciesTypes.eWOODY_FUEL_STUMPS_SOUND_SPECIES_SPECIES_DESCRIPTION)





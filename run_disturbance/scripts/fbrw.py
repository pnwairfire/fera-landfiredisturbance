# =============================================================================
#
# Author:   Kjell Swedin
# Purpose:  Encapsulates common operations when working with the Fuelbed Read/Write shared library (libfbrw).
#
# =============================================================================

# Shared library (C++ implementation exposed via pybind)
import libfbrw

# Use to cap percentage values at 100
PERCENT_IDS = [
    libfbrw.FBTypes.eCANOPY_SNAGS_CLASS_1_CONIFERS_WITH_FOLIAGE_PERCENT_COVER,
    libfbrw.FBTypes.eCANOPY_TREES_MIDSTORY_PERCENT_COVER,
    libfbrw.FBTypes.eCANOPY_TREES_OVERSTORY_PERCENT_COVER,
    libfbrw.FBTypes.eCANOPY_TREES_TOTAL_PERCENT_COVER,
    libfbrw.FBTypes.eCANOPY_TREES_UNDERSTORY_PERCENT_COVER,
    libfbrw.FBTypes.eGROUND_FUEL_DUFF_LOWER_PERCENT_COVER,
    libfbrw.FBTypes.eGROUND_FUEL_DUFF_UPPER_PERCENT_COVER,
    libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_COVER,
    libfbrw.FBTypes.eHERBACEOUS_PRIMARY_LAYER_PERCENT_LIVE,
    libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_COVER,
    libfbrw.FBTypes.eHERBACEOUS_SECONDARY_LAYER_PERCENT_LIVE,
    libfbrw.FBTypes.eMOSS_LICHEN_LITTER_GROUND_LICHEN_PERCENT_COVER,
    libfbrw.FBTypes.eMOSS_LICHEN_LITTER_LITTER_PERCENT_COVER,
    libfbrw.FBTypes.eMOSS_LICHEN_LITTER_MOSS_PERCENT_COVER,
    libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_COVER,
    libfbrw.FBTypes.eSHRUBS_PRIMARY_LAYER_PERCENT_LIVE,
    libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_COVER,
    libfbrw.FBTypes.eSHRUBS_SECONDARY_LAYER_PERCENT_LIVE,
    libfbrw.FBTypes.eWOODY_FUEL_ALL_DOWNED_WOODY_FUEL_TOTAL_PERCENT_COVER,
    libfbrw.FBTypes.eLITTER_LITTER_TYPE_SHORT_NEEDLE_PINE_RELATIVE_COVER,
    libfbrw.FBTypes.eLITTER_LITTER_TYPE_LONG_NEEDLE_PINE_RELATIVE_COVER,
    libfbrw.FBTypes.eLITTER_LITTER_TYPE_OTHER_CONIFER_RELATIVE_COVER,
    libfbrw.FBTypes.eLITTER_LITTER_TYPE_BROADLEAF_DECIDUOUS_RELATIVE_COVER,
    libfbrw.FBTypes.eLITTER_LITTER_TYPE_BROADLEAF_EVERGREEN_RELATIVE_COVER,
    libfbrw.FBTypes.eLITTER_LITTER_TYPE_PALM_FROND_RELATIVE_COVER,
    libfbrw.FBTypes.eLITTER_LITTER_TYPE_GRASS_RELATIVE_COVER
]

# Project-wide constants
DISTURBANCE = ['fire', 'insects']
SEVERITY = [1,2,3]  # low, medium, high
TIMESTEP = [1,2,3]  # first, second, third


def add(s1, s2):
    if not len(s1): s1 = 0
    if not len(s2): s2 = 0
    try:
        return str((float(s1) + float(s2)))
    except:
        assert False, "Error in add() a = {}. b = {}".format(s1, s2)
        pass

def mul(s1, s2):
    if not len(s1): s1 = 0
    #if not len(s2): s2 = 0
    try:
        return str((float(s1) * float(s2)))
    except:
        assert False, "Error in mul()"
        pass

# ++++++++++++++++++++++++++++++++++++++++++
#   Take 2 id values. Retrieve and scale the value represented by the
#   scaled_value_id. Add it to the value at the add_to_id.
# ++++++++++++++++++++++++++++++++++++++++++
def add_scaled_value_to_specified(fb, add_to_id, scaled_value_id, scale_factor=1):
    add_to = fb.GetValue(add_to_id)
    scaled_addend = mul(fb.GetValue(scaled_value_id), scale_factor)
    fb.SetValue(add_to_id, add(add_to, scaled_addend))

# ++++++++++++++++++++++++++++++++++++++++++
#   Take the proposed_value and an expression like "min=3" and
#   apply the expression if it applies.
#   Return the modified value if the expression applies or the 
#   original value if not
# ++++++++++++++++++++++++++++++++++++++++++
def apply_conditional_modifier(proposed_value, conditional_modifier):
    retval = proposed_value
    if conditional_modifier:
        cm_lower = conditional_modifier.lower()
        if 'min' in cm_lower:
            chunks = cm_lower.split('=')
            compare_to = int(chunks[1].strip())
            if compare_to > float(proposed_value):
                retval = '{}'.format(compare_to)
        else:
            print('\nError: unknown conditional modifier - "{}"\n'.format(cm_lower))
            exit(1)
    return retval
        
def scale(fb, id, scale_factor, conditional_modifier=''):
    v = fb.GetValue(id)
    scaled_value = mul(v, scale_factor)
    if id in PERCENT_IDS and float(scaled_value) > 100:
        scaled_value = '100'
    scaled_value = apply_conditional_modifier(scaled_value, conditional_modifier)
    fb.SetValue(id, scaled_value)

def exists_value(fb, id):
    check = fb.GetValue(id)
    if len(check):
        try:
            check_number = float(check)
            return check_number > 0.0
        except:
            pass
    return False

def exists_species(fb, id):
    check = fb.GetSpeciesValue(id)
    return True if len(check) else False

def assign_if_not_exist(fb, check, assign_id):
   if not exists_value(fb, check):
       fb.SetValue(check, fb.GetValue(assign_id))

def assign_species_if_not_exist(fb, check, assign_id):
   if not exists_species(fb, check):
       fb.SetSpeciesValue(check, fb.GetSpeciesValue(assign_id))

# assign_from could be an actual value, or, an FBTypes type
def assign_and_return_current(fb, assign_to, assign_from):
    current = fb.GetValue(assign_to)
    val = assign_from
    if isinstance(assign_from, libfbrw.FBTypes):
        val = fb.GetValue(assign_from)
        
    if val:
        fb.SetValue(assign_to, val)
    else:
        fb.SetValue(assign_to, '')
    return current
    
def do_simple_scaling(fb, scale_these):
    for item in scale_these:
        xpath_variable, scaling_factor, conditional_modifier = item
        scale(fb, xpath_variable, scaling_factor, conditional_modifier)
        
def set_fb_number(fb, set_number_to):
    fb_num = fb.SetValue(libfbrw.FBTypes.eFUELBED_NUMBER, set_number_to)
        
def get_fb_number(fb):
    return fb.GetValue(libfbrw.FBTypes.eFUELBED_NUMBER)

def get_reader_writer(filename):
    fb = libfbrw.FuelbedValues(filename)
    fb.Read()
    # Default is False, uncomment next line to see debug messages
    #fb.EnableDebugPrint(True)
    return fb
    
# ++++++++++++++++++++++++++++++++++++++++++
#   Only apply disturbance rules to fuelbeds that 'qualify'. Use
#   the following prerequisite functions to check
# ++++++++++++++++++++++++++++++++++++++++++
def prereq_canopy_cover(fb, minimum_value):
    retval = (False, 'Invalid/empty canopy cover')
    try:
        cc = fb.GetValue(libfbrw.FBTypes.eCANOPY_TREES_TOTAL_PERCENT_COVER)
        if len(cc) and (float(cc) >= minimum_value):
            retval = (True, None)
        else: 
            retval = (False, 'Invalid canopy cover. Minimum = {}, this fuelbed = {}'.format(minimum_value, cc))
    except:
        pass    # initial error is the best we can do.
    return retval
    
# general case - pass in the identifiers that are valid
def prereq_vegform(fb, valid_vegforms):
    retval = (False, 'Invalid/empty vegetation form.')
    try:
        vf = fb.GetValue(libfbrw.FBTypes.eVEGETATION_FORM)
        if len(vf):
            retval = (int(vf) in valid_vegforms, None)
            if not retval[0]:
                retval = (False, 'Invalid vegetation form. Allowed = {}, this fuelbed = {}'.format(valid_vegforms, vf))
    except:
        pass    # initial error is the best we can do.
    return retval

VALID_COVER_TYPES = [7,165,186,187,188,189,190,191,192,193,196,197,198,199,200,201,202,203,204,205]    
def check_covertype(fb):
    def get_covertype(possible_ct):
        try:
            tmp = int(possible_ct)
            return True, tmp
        except:
            pass
        return False, 0
        
    retval = (False, 'Invalid/empty cover type.')
    try:
        cover_types = fb.GetValue(libfbrw.FBTypes.eCOVER_TYPE)
        if len(cover_types):
            for ct in cover_types:
                good, ct_val = get_covertype(ct)
                if good and ct_val in VALID_COVER_TYPES:
                    retval = (True, None)
            if not retval[0]:
                retval = (False, 'Invalid cover type. This fuelbed = {}\n\tallowed = {}'.format(cover_types, VALID_COVER_TYPES))
    except Exception as e:
        print(e)
        retval = (False, 'Invalid cover type. This fuelbed = {}\n\tallowed = {}'.format(cover_types, valid_covertypes))
    return retval
    

# non-general case, special handling for shrublands
SHRUBLANDS = 6
def prereq_vegform_insects(fb, valid_vegforms):
    retval = (False, 'Invalid/empty vegetation form.')
    try:
        vf = fb.GetValue(libfbrw.FBTypes.eVEGETATION_FORM)
        if len(vf):
            vf_num = int(vf)
            if SHRUBLANDS == vf_num:
                check, reason = check_covertype(fb)
                retval = (check, reason)
            else:
                retval = (vf_num in valid_vegforms, None)
                if not retval[0]:
                    retval = (False, 'Invalid vegetation form. Allowed = {}, this fuelbed = {}'.format(valid_vegforms, vf))
    except Exception as e:
        print(e)    # initial error is the best we can do.
    return retval
    
    
    
    
    

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
#DISTURBANCE = ['fire', 'insects']
DISTURBANCE = ['insects']
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

def exists(fb, id):
    check = fb.GetValue(id)
    if len(check):
        try:
            check_number = float(check)
            return check_number > 0.0
        except:
            pass
    return False

def assign_if_not_exist(fb, check, assign_id):
   if not exists(fb, check):
       fb.SetValue(check, fb.GetValue(assign_id))

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
    return fb
    
def get_reader_writer_set_fbnum(filename, disturbance_severity_timestep_code):
    fb = libfbrw.FuelbedValues(filename)
    fb.Read()
    fb_num = fb.GetValue(libfbrw.FBTypes.eFUELBED_NUMBER)
    fb_num = fb.SetValue(libfbrw.FBTypes.eFUELBED_NUMBER, '{}_{}'.format(fb_num, disturbance_severity_timestep_code))
    return fb    
    
# ++++++++++++++++++++++++++++++++++++++++++
#   Only apply disturbance rules to fuelbeds that 'qualify'. Use
#   the following prerequisite functions to check
# ++++++++++++++++++++++++++++++++++++++++++
def prereq_canopy_cover(fb, minimum_value):
    cc = fb.GetValue(libfbrw.FBTypes.eCANOPY_TREES_TOTAL_PERCENT_COVER)
    if len(cc):
        return (float(cc) >= minimum_value, None)
    return (False, 'Invalid canopy cover. Minimun = {}, this fuelbed = {}'.format(minimum_value, cc))
    
def prereq_vegform(fb, valid_vegforms):
    vf = fb.GetValue(libfbrw.FBTypes.eVEGETATION_FORM)
    if len(vf):
        return (int(vf) in valid_vegforms, None)
    return (False, 'Invalid vegetation form. Allowed = {}, this fuelbed = {}'.format(valid_vegforms, vf))
    
def prereq_covertype(fb, valid_covertypes):
    def get_covertype(possible_ct):
        try:
            tmp = int(possible_ct)
            return True, tmp
        except:
            pass
        return False, 0
        
    cover_types = fb.GetValue(libfbrw.FBTypes.eCOVER_TYPE)
    if len(cover_types):
        for ct in cover_types:
            good, ct_val = get_covertype(ct)
            if good and ct_val in valid_covertypes:
                return (True, None)
    return (False, 'Invalid cover type. This fuelbed = {}, allowed = {}'.format(cover_types, valid_covertypes))

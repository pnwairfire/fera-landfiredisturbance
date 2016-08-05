# =============================================================================
#
# Author:   Kjell Swedin
# Purpose:  Encapsulates common operations when working with the Fuelbed Read/Write shared library (libfbrw).
#
# =============================================================================

# Shared library (C++ implementation exposed via pybind)
import libfbrw

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
        
def scale(fb, id, scale_factor):
    v = fb.GetValue(id)
    fb.SetValue(id, mul(v, scale_factor))

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
        
    # KS - should this be:
    # val = 0
    # fb.SetValue(assign_to, val)
    if val:
        fb.SetValue(assign_to, val)
    return current
    
def do_simple_scaling(fb, scale_these):
    for item in scale_these:
        scale(fb, item[0], item[1])

def get_reader_writer(filename, disturbance_severity_timestep_code):
    fb = libfbrw.FuelbedValues(filename)
    fb.Read()
    fb_num = fb.GetValue(libfbrw.FBTypes.eFUELBED_NUMBER)
    fb_num = fb.SetValue(libfbrw.FBTypes.eFUELBED_NUMBER, '{}_{}'.format(fb_num, disturbance_severity_timestep_code))
    return fb
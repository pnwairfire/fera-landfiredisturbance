import pandas as pd
import numpy as np
import re

# Fire across severities at the first timestep
FIRE_ALLSEVERITY_TS1 = '\d+_1.1$'
MECHADD_ALLSEVERITY_TS1 = '\d+_2.1$'
MECHREMOVE_ALLSEVERITY_TS1 = '\d+_3.1$'
WIND_ALLSEVERITY_TS1 = '\d+_4.1$'
INSECTS_ALLSEVERITY_TS1 = '\d+_5.1$'

DISTURBANCES = [
    FIRE_ALLSEVERITY_TS1,
    MECHADD_ALLSEVERITY_TS1,
    MECHREMOVE_ALLSEVERITY_TS1,
    WIND_ALLSEVERITY_TS1,
    INSECTS_ALLSEVERITY_TS1
]

# ========================================================================================
#  Returns a True|False mask array. Use to pick fuelbeds based on disturbance.
#  severity, timestep.  
# ========================================================================================
def get_mask(df, regex):
    return [True if j else False for j in (re.match(regex, i) for i in df.Fuelbed_number)]

def write_group_csv(gb, dist_id):
    df_out = pd.DataFrame()
    sgroups = sorted([int(i) for i in gb.groups])
    for g in sgroups:
        df_out = df_out.append(gb.get_group(str(g))[['Fuelbed_number','Fuelbed_name', 'Benchmark_ROS','Total_aboveground_biomass']])
    df_out.to_csv('ros_biomass_{}.csv'.format(dist_id), index=False)    

def build_visualizer(gb, cols_values, dist_id):
    df_means = pd.DataFrame()
    for c in cols_values: 
        s1 = gb.nth([0]).get(c).mean().round(2)
        s2 = gb.nth([1]).get(c).mean().round(2)
        s3 = gb.nth([2]).get(c).mean().round(2)
        arrow = '='    # equals
        if s1 > s2 and s2 > s3:
            arrow = '&darr;'
        if s1 < s2 and s2 < s3:
            arrow = '&uarr;'
            
        line = '{},{},{},{},{}'.format(arrow, c, s1, s2, s3)
        #print(line)
        df_means = df_means.append({'Trend':arrow, 'Name':c, 'S1_mean':s1, 'S2_mean':s2, 'S3_mean':s3}, ignore_index=True)

    df_means = df_means[['Trend','Name','S1_mean','S2_mean','S3_mean']]
    from IPython.display import HTML
    df_means.to_html('means_{}.html'.format(dist_id), index=False, escape=False)

def process(filename):
    df = pd.read_csv(filename)
    df.fillna(0, inplace=True)

    # get the non-empty, numeric column names
    cols_values = df.columns.values
    cols_values = np.delete(cols_values, [0,1,2,16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,len(cols_values)-1])

    for disturbance in DISTURBANCES:
        dist_id = disturbance.split('_')[1][0]
        print('Dist id is "{}"'.format(dist_id))
        mask = get_mask(df, disturbance)
        df_tmp = df.loc[mask]
        gb = df_tmp.groupby(by=df_tmp.Fuelbed_number.apply(lambda x: x.split('_')[0]))
        write_group_csv(gb, dist_id)

        build_visualizer(gb, cols_values, dist_id)

# ========================================================================================
#  Start
# ========================================================================================
process('fccs_summary.csv')

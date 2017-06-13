# =============================================================================
#
# Author:	Kjell Swedin
# Purpose:	Examine Landfire disturbance outputs
#
# =============================================================================

import pandas as pd

def duplicate_base_for_grouping():
    with open('summary_base.csv', 'r') as infile:
        with open('s2.csv', 'w+') as outfile:
            outfile.write(infile.readline())
            for line in infile:
                chunks = line.split(',')
                fn = chunks[1]
                new_fn = '{0:0>4}'.format(fn)
                for i in range(1,6):
                    tmp_fn = '{}_{}00'.format(new_fn, i)
                    chunks[1] = tmp_fn
                    outfile.write(','.join(chunks))
                
def concat_and_group():
    df_orig = pd.read_csv('s2.csv')
    df_lf = pd.read_csv('fccs_summary.csv')
    df_concat = pd.concat([df_lf, df_orig], ignore_index=True)
    df_concat.fillna(0, inplace=True)
    df_concat.drop([i for i in df_concat.columns if i.startswith('Custom_')], axis=1, inplace=True)
    gb = df_concat.groupby(lambda x: '{:0>4}_{}'.format(df_concat.iloc[x].Fuelbed_number.split('_')[0], \
                                      df_concat.iloc[x].Fuelbed_number.split('_')[1][0]))
    return gb
    
def compare_000(gb):
    interesting = ['Fuelbed_number',
        'Tree_aboveground_load', 'Snag_class1_wood_load', 'Snag_class1_aboveground_load',
        'Snag_class1_other_load', 'Snag_class2_load', 'Snag_class3_load',    
    ]
    fire_groups = [g for g in sorted(gb.groups) if g.endswith('1')]
    gb_fire = [g for g in (gb.get_group(i) for i in fire_groups)]    
    suspect = []
    df_suspect = pd.DataFrame()
    for i in gb_fire:
        tmp = i[interesting].iloc[[0,3,6,-1]]
        for j in [2,1,0]:
            if tmp.iloc[j].Snag_class1_wood_load > tmp.iloc[-1].Tree_aboveground_load:
                df_suspect = pd.concat([df_suspect, tmp], ignore_index=True)
                break
    df_suspect.to_html('suspect.html', index=False)
    
# ++++++++++++++++++++++++++++++++++++++++++
#  Start...
# ++++++++++++++++++++++++++++++++++++++++++
duplicate_base_for_grouping()
gb = concat_and_group()
print(gb.get_group('0004_1').iloc[-1])
compare_000(gb)
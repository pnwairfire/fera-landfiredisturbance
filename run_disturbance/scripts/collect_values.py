import pandas as pd
import glob
import io
import os
import libfbrw

SCRATCH_FILENAME = 'zorK123.csv'
OUTDIR = '../out'

def get_values_from_file(filename):
    cmd = 'python print_values_from_xml.py {}> {}'.format(filename, SCRATCH_FILENAME)
    os.system(cmd)
    df = pd.read_csv(SCRATCH_FILENAME, header=None, names=['Variable', 'Value'])
    df.fillna(0, inplace=True)
    os.unlink(SCRATCH_FILENAME)
    return df

def process():
    first_time = True
    df_out = None
    files = glob.glob('{}/*.xml'.format(OUTDIR))
    for f in files:
        print(f)
        df = get_values_from_file(f)
        colname = f[len(OUTDIR)+1:].split('.')[0]
        if not first_time:
            df_out[colname] = df.Value
        else:
            df_out = pd.DataFrame({'Variable': df.Variable, colname: df.Value})
            first_time = False
    df_out.to_csv('calculated_values.csv', index=False)
            
    
    
process()    
    
    
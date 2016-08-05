import pandas as pd
import subprocess
import io
import os
import libfbrw

SCRATCH_FILENAME = 'zorK123.csv'

def get_values_from_file(filename):
    cmd = 'python print_values_from_xml.py {}> {}'.format(filename, SCRATCH_FILENAME)
    os.system(cmd)
    df = pd.read_csv(SCRATCH_FILENAME, header=None, names=['Variable', 'Value'])
    df.fillna(0, inplace=True)
    os.unlink(SCRATCH_FILENAME)
    return df
    
def build_column_name(dist, severity, filename):
    replace_me = ''
    replace_with = ''
    if '_one' in filename:
        replace_me = '_one'
        replace_with = '_111'
    elif '_two' in filename:
        replace_me = '_two'
        replace_with = '_112'
    elif '_three' in filename:
        replace_me = '_three'
        replace_with = '_113'
    else:
        assert False
        
    return filename.replace(replace_me, replace_with.format(dist, severity))[:-4]

def process():
    first_time = True
    df_out = None
    c = subprocess.run(['find', '../out', '-name', '*.xml'], stdout=subprocess.PIPE, universal_newlines=True)
    for line in io.StringIO(c.stdout):
        line = line.strip()
        dist, severity, filename = line[7:].split('/')
        df = get_values_from_file(line)
        colname = build_column_name(dist, severity, filename)
        print(colname)
        if not first_time:
            df_out[colname] = df.Value
        else:
            df_out = pd.DataFrame({'Variable': df.Variable, colname: df.Value})
            first_time = False
    df_out.to_csv('calculated_values.csv', index=False)
            
    
    
process()    
    
    
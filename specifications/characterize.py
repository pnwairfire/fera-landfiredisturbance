from collections import defaultdict
import re
import sympy
import pandas as pd

INFILE = 'spec_all.csv'

def times_key(key):
    return key.startswith('*') or key.startswith('"*')

def check_expression(cells, keys):
    print('\nIllegal expressions:')
    for key in keys:
        for item in cells[key]:
            chunks = item.split('=')
            if 2 == len(chunks):
                expr = chunks[1].strip()
                try:
                    sympy.sympify(expr)
                except:
                    print('\t{}'.format(expr))
            else:
                print('\t{}'.format(item))
                
def handle_cell(cell_str, cell_dict, weird):
    if ' ' in cell_str:
        key = cell_str.split(' ')[0]
        if len(key) and not ' ' == key and not re.match('^\d\d\d$', key):
            cell_dict[key].append(cell_str)
    else:
        if not cell_str.startswith('e') and not re.match('^\d\d\d$', cell_str):
            weird[cell_str] = cell_str
            
def print_results(cell_dict, weird):
    print('\nWeird')
    for key in weird.keys():
        print('\t{} : {}'.format(key, weird[key]))
    print('\nKeys')
    for key in cell_dict.keys():
        print('\t{}'.format(key))
    print('\nCells')
    for key in cell_dict.keys():
        print(' {}'.format(key))
        for val in cell_dict[key]:
            print('\t{}'.format(val))
    times_keys = [key for key in cell_dict.keys() if times_key(key)]
    check_expression(cell_dict, times_keys)

                
def original_process():
    cell_dict = defaultdict(list)
    weird = defaultdict(list)
    with open(INFILE, 'r') as infile:
        for line in infile:
            chunks = line.strip().split(',')
            for chunk in chunks[2:]:
                chunk = chunk.strip()
                if ' ' in line:
                    key = chunk.split(' ')[0]
                    if len(key) and not ' ' == key and not re.match('^\d\d\d$', key):
                        cell_dict[key].append(chunk)
                else:
                    if not chunk.startswith('e'):
                        weird[chunk] = chunk
        print_results(cell_dict, weird)
        
def process():
    cell_dict = defaultdict(list)
    weird = defaultdict(list)
    df = pd.read_csv(INFILE, header=1)
    df.fillna("", inplace=True)
    for col in df.columns[2:]:
        for cell in df.get(col).iteritems():
            cell_str = cell[1].strip()
            handle_cell(cell_str, cell_dict, weird)
    print_results(cell_dict, weird)
        
    

# ++++++++++++++++++++++++++++++++++++++++++
#   Start
# ++++++++++++++++++++++++++++++++++++++++++
#original_process()    
process()
    
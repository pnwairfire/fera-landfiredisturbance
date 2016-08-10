# =============================================================================
#
# Author:  Kjell Swedin
# Purpose: Build a single csv file from multiple specification files to compare against calculated values.
#
# =============================================================================
import pandas as pd
import glob

def build():
    files = glob.glob('../specifications/*.xlsx')
    df_result = pd.read_excel(files[0], sheetname='Expected')
    df_result.drop([i for i in df_result.columns if i.endswith('FCCS')], axis=1, inplace=True)
    for f in files[1:]:
        df = pd.read_excel(f, sheetname='Expected')
        df.drop([i for i in df.columns if i.endswith('FCCS')], axis=1, inplace=True)
        df_result = pd.merge(df_result, df, on='Variable')
    df_result.to_csv('expected.csv', index=False)
    
    
build()
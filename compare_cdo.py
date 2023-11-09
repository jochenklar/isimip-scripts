import argparse

import numpy as np
import pandas as pd

'''
cdo_df should be the output of:
cdo -s outputtab,date,value,nohead -fldmean -ifthen -selname,m_VAR MASK.ncINPUT.nc > OUTPUT.csv
'''

parser = argparse.ArgumentParser()
parser.add_argument('cdo_df')
parser.add_argument('isimip_df')
args = parser.parse_args()

cdo_df = pd.read_csv(args.cdo_df, delim_whitespace=True, names=['date', 'value'])
print(cdo_df)
cdo_df['date'] = cdo_df['date'].apply(lambda t: pd.Timestamp(np.datetime64(t)))

isimip_df = pd.read_csv(args.isimip_df, names=['date', 'value'], header=0)
isimip_df['date'] = isimip_df['date'].apply(lambda t: pd.Timestamp(np.datetime64(t)))
print(isimip_df)

pd.testing.assert_frame_equal(cdo_df, isimip_df, rtol=1e-6)

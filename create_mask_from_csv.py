import argparse

import pandas as pd
import xarray as xr

from isimip_utils.netcdf import init_dataset

FILL_VALUE = -128


parser = argparse.ArgumentParser()
parser.add_argument('input_path')
parser.add_argument('output_path')
parser.add_argument('-c', dest='data_column')

args = parser.parse_args()

df = pd.read_csv(args.input_path, delimiter=';')

ds = init_dataset(args.input_path, time=None, diskless=True)

data_column = args.data_column if args.data_column else df.columns[-1]

varible_names = sorted(column_name for column_name in df[data_column].unique() if column_name not in [None, 0, '0'])
for varible_name in varible_names:
    variable = ds.createVariable(f'm_{varible_name}', 'b', ('lat', 'lon'),
                                 fill_value=FILL_VALUE, compression='zlib')
    variable.missing_value = FILL_VALUE
    variable[:, :] = 0

ds = xr.open_dataset(xr.backends.NetCDF4DataStore(ds))

for varible_name in varible_names:
    variable_df = df.loc[df[data_column] == varible_name]
    variable_lat = xr.DataArray(variable_df.lat, dims="points")
    variable_lon = xr.DataArray(variable_df.lon, dims="points")

    ds[f'm_{varible_name}'].loc[{'lat': variable_lat, 'lon': variable_lon}] = 1

ds.to_netcdf(args.output_path)

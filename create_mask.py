import argparse

import geopandas
import shapely
import xarray as xr

from isimip_utils.netcdf import init_dataset

FILL_VALUE = -128


parser = argparse.ArgumentParser()
parser.add_argument('input_path')
parser.add_argument('output_path')
parser.add_argument('-n', '--name-column')

args = parser.parse_args()

def get_variable_name(index, row):
    if args.name_column:
        return f'm_{row[args.name_column]}'.replace(' ', '_').lower()
    else:
        return f'm_{index}'

df = geopandas.read_file(args.input_path)

ds = init_dataset(args.input_path, time=None, diskless=True)

for index, row in df.iterrows():
    variable_name = get_variable_name(index, row)
    variable = ds.createVariable(variable_name, 'b', ('lat', 'lon'),
                                 fill_value=FILL_VALUE, compression='zlib')

    for column_name in df.columns:
        if column_name != 'geometry':
            setattr(variable, column_name.lower(), row[column_name])
    variable.missing_value = FILL_VALUE
    variable[:, :] = 1

ds = xr.open_dataset(xr.backends.NetCDF4DataStore(ds))
ds.rio.write_crs(df.crs, inplace=True)

for index, row in df.iterrows():
    variable_name = get_variable_name(index, row)
    variable = ds[variable_name]

    geometry = shapely.geometry.mapping(row['geometry'])

    mask = variable.rio.clip([geometry], drop=False)
    variable[:, :] = mask[:, :]

ds.to_netcdf(args.output_path)

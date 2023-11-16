import geopandas
import shapely
import xarray as xr

from isimip_utils.netcdf import init_dataset

INPUT_PATH = 'FishMIP_regional_models.shp'
OUTPUT_PATH = 'FishMIP_regional_models.nc'
FILL_VALUE = -128

df = geopandas.read_file(INPUT_PATH)
print(df)

ds = init_dataset(OUTPUT_PATH, time=None, diskless=True)

for index, row in df.iterrows():
    variable_name = f'm_RME{index:0>2}'
    variable = ds.createVariable(variable_name, 'b', ('lat', 'lon'),
                                 fill_value=FILL_VALUE, compression='zlib')
    variable.region = row.region
    variable[:, :] = 1

ds = xr.open_dataset(xr.backends.NetCDF4DataStore(ds))
ds.rio.write_crs(df.crs, inplace=True)

for index, row in df.iterrows():
    variable_name = f'm_RME{index:0>2}'
    variable = ds[variable_name]

    geometry = shapely.geometry.mapping(row['geometry'])

    mask = variable.rio.clip([geometry], drop=False)
    variable[:, :] = mask[:, :]

ds.to_netcdf(OUTPUT_PATH)

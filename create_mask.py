import argparse

import geopandas
import netCDF4 as nc
import numpy as np
import rioxarray  # noqa: F401
import shapely
import xarray as xr

FILL_VALUE_FLOAT = 1e+20
FILL_VALUE_BOOL = -128


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', help='path to the input file')
    parser.add_argument('output_path', help='path to the output file')
    parser.add_argument('--nlat', dest='n_lat', help='number of grid points in latitude direction',
                        type=int, default=720)
    parser.add_argument('--nlon', dest='n_lon', help='number of grid points in longitude direction',
                        type=int, default=360)

    args = parser.parse_args()

    # get number of gridpoints and spacing
    d_lon = 360.0 / args.n_lon
    d_lat = 180.0 / args.n_lat

    # read shapefile/geojson using geopandas
    df = geopandas.read_file(args.input_path)

    # create a diskless netcdf file using python-netCDF4
    ds = nc.Dataset(args.output_path, 'w', format='NETCDF4_CLASSIC', diskless=True)
    ds.createDimension('lon', args.n_lon)
    ds.createDimension('lat', args.n_lat)

    # create lon variable
    lon = ds.createVariable('lon', 'f8', ('lon',), fill_value=FILL_VALUE_FLOAT)
    lon.standard_name = 'longitude'
    lon.long_name = 'Longitude'
    lon.units = 'degrees_east'
    lon.axis = 'X'
    lon[:] = np.arange(-180 + 0.5 * d_lon, 180, d_lon)

    # create lat variable
    lat = ds.createVariable('lat', 'f8', ('lat',), fill_value=FILL_VALUE_FLOAT)
    lat.standard_name = 'latitude'
    lat.long_name = 'Latitude'
    lat.units = 'degrees_north'
    lat.axis = 'Y'
    lat[:] = np.arange(90 - 0.5 * d_lat, -90, -d_lat)

    # create mask variable, with the properties of the shape
    for index, row in df.iterrows():
        variable_name = f'm_{index}'
        variable = ds.createVariable(variable_name, 'b', ('lat', 'lon'),
                                     fill_value=FILL_VALUE_BOOL, compression='zlib')

        for key, value in row.items():
            if isinstance(value, (str, int, float)):
                setattr(variable, key.lower(), value)

        variable[:, :] = np.ones((args.n_lat, args.n_lon))

    # convert to a crs-aware xarray dataset
    ds = xr.open_dataset(xr.backends.NetCDF4DataStore(ds))
    ds.rio.write_crs(df.crs, inplace=True)

    # loop over shape variables and create masks
    for index, row in df.iterrows():
        variable_name = f'm_{index}'
        variable = ds[variable_name]

        geometry = shapely.geometry.mapping(row['geometry'])

        mask = variable.rio.clip([geometry], drop=False)
        variable[:, :] = mask[:, :]

    # write mask netcdf files
    ds.to_netcdf(args.output_path)


if __name__ == '__main__':
    main()

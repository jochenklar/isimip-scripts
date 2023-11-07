#!/usr/bin/env python
from pathlib import Path

import netCDF4 as nc
import numpy as np
import numpy.ma as ma

FILL_VALUE = 1.e+20

TIME_STEPS = 100
START_TIME = 150000
END_TIME = 180000

rng = np.random.default_rng()

def main():
    with init_dataset('random.nc') as ds:
        ds.variables['var'][:] = rng.standard_normal((TIME_STEPS, 720, 360)) * 100

    with init_dataset('point.nc') as ds:
        ds.variables['var'][:] = 0.0
        ds.variables['var'][:, 360:361, 45:46] = 1.0

    with init_dataset('mask.nc') as ds:
        ds.variables['var'][:] = ma.masked
        ds.variables['var'][:, 350:371, 80:101] = 1.0

    with init_dataset('linear.nc') as ds:
        ds.variables['var'][:] = np.linspace(0.0, 2.0, num=TIME_STEPS)[:, None, None]

    with init_dataset('sine.nc') as ds:
        ds.variables['var'][:] = np.sin(np.linspace(-2*np.pi, 2*np.pi, num=TIME_STEPS)[:, None, None]) * 100 + 100

def init_dataset(file_path):
    print(f'generating {file_path} ...')

    ds = nc.Dataset(file_path, 'w', format='NETCDF4_CLASSIC')
    ds.createDimension('time', None)
    ds.createDimension('lon', 720)
    ds.createDimension('lat', 360)

    time = ds.createVariable('time', 'f8', ('time',))
    time.standard_name = 'time'
    time.long_name = 'Time'
    time.units = 'days since 1601-1-1 00:00:00'
    time.calendar = 'proleptic_gregorian'

    lon = ds.createVariable('lon', 'f8', ('lon',))
    lon.standard_name = 'longitude'
    lon.long_name = 'Longitude'
    lon.units = 'degrees_east'
    lon.axis = 'X'

    lat = ds.createVariable('lat', 'f8', ('lat',))
    lat.standard_name = 'latitude'
    lat.long_name = 'Latitude'
    lat.units = 'degrees_north'
    lat.axis = 'Y'

    var = ds.createVariable('var', 'f8', ('time', 'lat', 'lon'), fill_value=FILL_VALUE, compression='zlib')
    var.standard_name = 'var'
    var.long_name = 'Variable'
    var.units = '1'
    var.missing_value = FILL_VALUE

    time[:] = np.arange(START_TIME, END_TIME, (END_TIME - START_TIME) / TIME_STEPS)
    lon[:] = np.arange(-179.75, 180.25, 0.5)
    lat[:] = np.arange(89.75, -90.25, -0.5)

    return ds

if __name__ == '__main__':
    main()

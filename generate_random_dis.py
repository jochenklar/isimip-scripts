import netCDF4 as nc
import numpy as np

FILL_VALUE = 1.e+20

TIME_STEPS = 1000
START_TIME = 150000
END_TIME = 180000

rng = np.random.default_rng()

ds = nc.Dataset('random.nc', 'w', format='NETCDF4_CLASSIC')
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

dis = ds.createVariable('dis', 'f8', ('time', 'lat', 'lon'), fill_value=FILL_VALUE, compression='zlib')
dis.standard_name = 'discharge'
dis.long_name = 'Discharge'
dis.units = 'm3 s-1'
dis.missing_value = FILL_VALUE

time[:] = np.arange(START_TIME, END_TIME, (END_TIME - START_TIME) / TIME_STEPS)
lon[:] = np.arange(-179.75, 180.25, 0.5)
lat[:] = np.arange(89.75, -90.25, -0.5)
dis[:] = rng.standard_normal((TIME_STEPS, 720, 360)) * 1000

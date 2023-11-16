#!/usr/bin/env python
import numpy as np
import numpy.ma as ma
from isimip_utils.netcdf import init_dataset

TIME_STEPS = 100
START_TIME = 150000
END_TIME = 180000

rng = np.random.default_rng()

def main():
    time = np.arange(START_TIME, END_TIME, (END_TIME - START_TIME) / TIME_STEPS)
    var = {
        'long_name': 'Variable',
        'units': '1'
    }

    with init_dataset('random.nc', time=time, var=var) as ds:
        ds.variables['var'][:] = rng.standard_normal((TIME_STEPS, 720, 360)) * 100

    with init_dataset('point.nc', time=time, var=var) as ds:
        ds.variables['var'][:] = 0.0
        ds.variables['var'][:, 360:361, 45:46] = 1.0

    with init_dataset('mask.nc', time=time, var=var) as ds:
        ds.variables['var'][:] = ma.masked
        ds.variables['var'][:, 350:371, 80:101] = 1.0

    with init_dataset('linear.nc', time=time, var=var) as ds:
        ds.variables['var'][:] = np.linspace(0.0, 2.0, num=TIME_STEPS)[:, None, None]

    with init_dataset('sine.nc', time=time, var=var) as ds:
        ds.variables['var'][:] = np.sin(np.linspace(-2*np.pi, 2*np.pi, num=TIME_STEPS)[:, None, None]) * 100 + 100


if __name__ == '__main__':
    main()

#!/usr/bin/env python
from pathlib import Path

import numpy as np
import numpy.ma as ma

from isimip_utils.netcdf import init_dataset

TIME_STEPS = 100
START_TIME = 150000
END_TIME = 180000

rng = np.random.default_rng()

base_path = Path('data')

def main():
    time = np.arange(START_TIME, END_TIME, (END_TIME - START_TIME) / TIME_STEPS)
    var = {
        'long_name': 'Variable',
        'units': '1'
    }

    with init_dataset(base_path / 'constant.nc', time=time, var=var) as ds:
        ds.variables['var'][:] = 100

    with init_dataset(base_path / 'random.nc', time=time, var=var) as ds:
        ds.variables['var'][:] = rng.standard_normal((TIME_STEPS, 720, 360)) * 100

    with init_dataset(base_path / 'point.nc', time=time, var=var) as ds:
        ds.variables['var'][:] = 0.0
        ds.variables['var'][:, 45:46, 360:361] = 1.0

    with init_dataset(base_path / 'mask.nc', time=time, var=var) as ds:
        ds.variables['var'][:] = ma.masked
        ds.variables['var'][:, 80:101, 350:371] = 1.0

    with init_dataset(base_path / 'linear.nc', time=time, var=var) as ds:
        ds.variables['var'][:] = np.linspace(0.0, 2.0, num=TIME_STEPS)[:, None, None]

    with init_dataset(base_path / 'sine.nc', time=time, var=var) as ds:
        ds.variables['var'][:] = np.sin(np.linspace(-2*np.pi, 2*np.pi, num=TIME_STEPS)[:, None, None]) * 100 + 100


if __name__ == '__main__':
    main()

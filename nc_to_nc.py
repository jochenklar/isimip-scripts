import numpy as np
import xarray as xr

# takes 5 minutes using xr.concat
# takes 3 1/2 minutes with pre allocated ds w/o compression
# takes 4 1/2 minutes with pre allocated ds with compression

rng = np.random.default_rng()

n = 10000

idxs = np.arange(n)
lons = -180 + rng.random(n) * 360.0
lats = -90 + rng.random(n) * 180.0

paths = [
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_1901_1910.nc',
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_1911_1920.nc',
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_1921_1930.nc',
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_1931_1940.nc',
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_1941_1950.nc',
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_1951_1960.nc',
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_1961_1970.nc',
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_1971_1980.nc',
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_1981_1990.nc',
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_1991_2000.nc',
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_2001_2010.nc',
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_2011_2019.nc',
]

var_name = None
times = None
for path in paths:
    with xr.open_dataset(path) as ds:
        if var_name is None:
            var_name = next(iter(ds.data_vars))
            times = ds['time']
        else:
            times = xr.concat([times, ds['time']], 'time')

var = xr.DataArray(
    dims=['idx', 'time'],
    coords={
        'idx': idxs,
        'time': times
    })

for path in paths:
    print(path)

    with xr.load_dataset(path) as ds:
        for idx, lon, lat in zip(idxs, lons, lats):
            ds_point = ds.sel(lon=lon, lat=lat, method='nearest')
            var.loc[idx, ds_point['time'][0]:ds_point['time'][-1]] = ds_point[var_name]

ds_points = xr.Dataset(
    data_vars={
        'lon': (['idx'], lons),
        'lat': (['idx'], lats),
        var_name: (['idx', 'time'], var.data),
    },
    coords={
        'idx': idxs,
        'time': times
    }
)

print(ds_points)

ds_points.to_netcdf('data/points.nc', encoding={var_name: {'zlib': True, 'complevel': 5}})

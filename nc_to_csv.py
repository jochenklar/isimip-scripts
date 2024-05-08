from pathlib import Path

import xarray as xr

# takes 7:43.50 for one path

paths = [
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_2011_2019.nc',
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_1901_1910.nc',
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_1911_1920.nc',
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_1981_1990.nc',
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_1961_1970.nc',
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_1991_2000.nc',
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_1921_1930.nc',
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_1971_1980.nc',
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_2001_2010.nc',
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_1931_1940.nc',
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_1941_1950.nc',
    '~/data/isimip/datasets/ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/GSWP3-W5E5/gswp3-w5e5_obsclim_pr_global_daily_1951_1960.nc',
]

var = 'pr'

maskpath = '~/data/isimip/datasets/ISIMIP3a/InputData/geo_conditions/landseamask/landseamask.nc'

outpath = Path('data/nc_to_csv')

mask = xr.load_dataset(maskpath)

nlat, nlon = mask['mask'].shape

for path in paths:
    ds = xr.load_dataset(path)

    for i in range(nlat):
        print(i)
        for j in range(nlon):
            if mask['mask'][i, j].values > 0:
                csv_path = outpath / str(i) / (Path(path).stem + f'_{i}_{j}.csv')
                csv_path.parent.mkdir(exist_ok=True, parents=True)
                ds[var][:, i, j].to_dataframe().to_csv(csv_path, mode='a', header=False)

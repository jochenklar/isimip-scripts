from pathlib import Path

import xarray as xr

base_path = Path('~/isimip/')

path = 'ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/CHELSA-W5E5v1.0/chelsa-w5e5v1.0_obsclim_tas_90arcsec_global_daily_200806.nc'
path = 'ISIMIP3a/InputData/climate/atmosphere/obsclim/global/daily/historical/CHELSA-W5E5v1.0/chelsa-w5e5v1.0_obsclim_tas_30arcsec_global_daily_200806.nc'

ds = xr.open_dataset(base_path / path)
print(ds)
print()
print(ds.rio.bounds())

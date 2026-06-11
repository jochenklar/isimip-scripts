from pathlib import Path

import geopandas

BASE_PATH = Path('/Users/jochen/data/isimip/dam_locations/shapefiles/')

INPUT_NAME = 'remain_v8_05_watergap2-2e_gswp3-w5e5_obsclim_histsoc_default_qtot_global_monthly_1901_2019'

# INPUT_NAME = 'remain_v8_27_watergap2-2e_ukesm1-0-ll_w5e5_historical_histsoc_default_qtot_global_monthly_1850_2014'

# path = (BASE_PATH / INPUT_NAME / INPUT_NAME).with_suffix('.shp')
path = (BASE_PATH / INPUT_NAME)

print(path)

df = geopandas.read_file(path)
print(df)

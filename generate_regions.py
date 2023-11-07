import json
from pathlib import Path

from netCDF4 import Dataset

path = Path('/Users/jochen/data/isimip/qa/regions/streamflow_basins_1509.nc')
ds = Dataset(path)

regions = []
for variable_name in ds.variables:
    if variable_name.startswith('m_'):
        code = variable_name.replace('m_', '').replace('_', '-').lower()
        regions.append({
            'type': 'mask',
            'specifier': f'streamflow-{code.lower()}',
            'mask_path': str(path),
            'mask_variable': str(variable_name)
        })

with path.with_suffix('.json').open('w') as fp:
    json.dump(regions, fp, indent=2)

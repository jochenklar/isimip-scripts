import argparse
import json
import re
from pathlib import Path

from netCDF4 import Dataset

argparse

parser = argparse.ArgumentParser()
parser.add_argument('prefix')
parser.add_argument('path')
args = parser.parse_args()

path = Path(args.path)

ds = Dataset(path)

regions = []
for variable_name in ds.variables:
    if variable_name.startswith('m_'):
        code = re.sub(r'^m_', '', variable_name).replace('_', '-').lower()
        regions.append({
            'type': 'mask',
            'specifier': f'{args.prefix}-{code}',
            'mask_path': str(args.path),
            'mask_variable': variable_name
        })

with path.with_suffix('.json').open('w') as fp:
    json.dump(regions, fp, indent=2)

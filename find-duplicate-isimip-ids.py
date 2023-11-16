import argparse
import os
from pathlib import Path

from netCDF4 import Dataset

parser = argparse.ArgumentParser()
parser.add_argument('path')

args = parser.parse_args()

found = set()
duplicate = []
missing = []

for path, dirs, files in os.walk(args.path):
    print(path)
    for file_name in files:
        file_path = Path(path) / file_name
        if file_path.suffix == '.nc4' and 'DIVISION' not in path:
            with Dataset(file_path, 'r') as ds:
                try:
                    isimip_id = ds.isimip_id
                except AttributeError:
                    missing.append(str(file_path))
                else:
                    if isimip_id in found:
                        duplicate.append(str(file_path))
                    else:
                        found.add(isimip_id)

Path('duplicate.txt').write_text(os.linesep.join(duplicate))
Path('missing.txt').write_text(os.linesep.join(missing))

import argparse
from pathlib import Path

import rioxarray  # noqa: F401
import xarray as xr

parser = argparse.ArgumentParser()
parser.add_argument('path')

args = parser.parse_args()

path = Path(args.path).expanduser()

ds = xr.open_dataset(path)
print(ds)
print()
print(ds.rio.bounds())

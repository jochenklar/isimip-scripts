import argparse

import geopandas
import pandas

parser = argparse.ArgumentParser()
parser.add_argument('input_path', help='path to the input file')

args = parser.parse_args()

# read shapefile/geojson using geopandas
df = geopandas.read_file(args.input_path)

pandas.set_option('display.max_rows', len(df))
print(df)

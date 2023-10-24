import argparse

parser = argparse.ArgumentParser()
parser.add_argument('lon', type=float)
parser.add_argument('lat', type=float)

args = parser.parse_args()

x = round((args.lon + 179.75) * 2)
y = round((89.75 - args.lat) * 2)

print(x, y)

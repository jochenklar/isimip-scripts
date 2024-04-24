#!/usr/bin/env python3
import argparse

import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('file1')
parser.add_argument('file2')
parser.add_argument('--header', type=int)

args = parser.parse_args()

header = args.header or 'infer'

df1 = pd.read_csv(args.file1, header=header)
df2 = pd.read_csv(args.file2, header=header)

if args.verbose:
    print(df1)
    print(df2)

pd.testing.assert_frame_equal(df1, df2)

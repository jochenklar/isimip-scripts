#!/usr/bin/env python

import logging
from pathlib import Path

import requests

from isimip_utils.cli import ArgumentParser, setup_env, setup_logs
from isimip_utils.netcdf import open_dataset

setup_env()
setup_logs(log_level="INFO")

parser = ArgumentParser()
parser.add_argument('paths', nargs="+")
parser.add_argument('--data-url', default='http://data.isimip.org')

args = parser.parse_args()

response = requests.get(f'{args.data_url}/api/v1/ids/', stream=True)
response.raise_for_status()

isimip_ids = {}
for line in response.iter_lines():
    isimip_id, path = line.decode().split()
    isimip_ids[isimip_id] = path

for path in args.paths:
    for file_path in Path(path).rglob('**/*.nc'):
        if not file_path.is_symlink():
            with open_dataset(file_path) as ds:
                try:
                    isimip_id = ds.getncattr('isimip_id')

                    if isimip_id in isimip_ids:
                        logging.error('%s %s already found in %s', isimip_id, file_path, isimip_ids[isimip_id])
                    else:
                        logging.info('%s %s', isimip_id, file_path)
                        isimip_ids[isimip_id] = file_path
                except AttributeError:
                    logging.warning('no isimip_id for %s', file_path)

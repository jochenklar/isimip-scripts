import json
import time
import zipfile
from pathlib import Path

import requests

repository_api = 'https://data.isimip.org/api/v1/'
files_api = 'https://files.isimip.org/api/v2/'

mask_path = Path('data') / 'test_mask.nc'

response = requests.get(f'{repository_api}datasets', params={
    'simulation_round': 'ISIMIP3b',
    'product': 'OutputData',
    'climate_forcing': 'ipsl-cm6a-lr',
    'climate_scenario': 'historical',
    'sector': 'marine-fishery_global',
    'model': 'apecosm',
    'variable': 'tcb'
})
response.raise_for_status()
response_data = response.json()
dataset = response_data['results'][0]
paths = [file['path'] for file in dataset['files']]

operations = [
    {
        'operation': 'cutout_bbox',
        'bbox': [
             60,  # west
             90,  # east
            -70,  # south
            -55   # north
        ]
    },
    {
        'operation': 'mask_mask',
        'mask': mask_path.name,
        'var': 'region'
    }
]

response = requests.post(files_api, files={
    'data': json.dumps({
        'paths': paths,
        'operations': operations
    }),
    mask_path.name: mask_path.read_bytes(),
})
response.raise_for_status()
job = response.json()
print(job['status'], job['meta'])

while job['status'] in ['queued', 'started']:
    time.sleep(2)
    job = requests.get(job['job_url']).json()
    print(job['status'], job['meta'])

if job['status'] == 'finished':
    zip_path = Path('data') / job['file_name']
    with requests.get(job['file_url'], stream=True) as response:
        with zip_path.open('wb') as fp:
            for chunk in response.iter_content(chunk_size=8192):
                fp.write(chunk)

    out_path = zip_path.with_suffix('')
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(out_path)

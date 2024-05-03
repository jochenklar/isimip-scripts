import json
import time
import zipfile
from pathlib import Path

import requests
import structlog

log = structlog.get_logger()

data_api_url = 'https://data.isimip.org/api/v1'
files_api_url = 'https://files.isimip.org/api/v2'

# path to the local shapefile or geojson
shape_path = Path('data') / 'LMEs66' / 'LMEs66.zip'
# shape_path = Path('data') / 'FishMIP_regional_models' / 'FishMIP_regional_models.zip'

# index of the geometry to use in the shape file
shape_index = 0

# path to store the downloads
download_path = Path('download')

# query to repository to obtain datasets
params = {
    'simulation_round': 'ISIMIP3b',
    'climate_forcing': 'gfdl-esm4',
    'climate_scenario': ['ssp126', 'ssp370','ssp585'],
    'climate_variable': 'tos'
}

# first request: obtain datasets from repository
log.info('querying repository', params=json.dumps(params, indent=2))
datasets_response = requests.get(f'{data_api_url}/datasets/', params=params)
datasets_response.raise_for_status()
datasets = datasets_response.json()['results']
log.info('datasets found', datasets=json.dumps([dataset['path'] for dataset in datasets], indent=2))

# collect paths for all files from the returned datasets
paths = []
for dataset in datasets_response.json()['results']:
    for file in dataset['files']:
        paths.append(file['path'])
log.info('files found', files=json.dumps(paths, indent=2))

# create request data for the files api
data = {
    'paths': paths,
    'operations': [
        {
            'operation': 'create_mask',
            'shape': shape_path.name,
            'mask': shape_path.with_suffix('.nc').name,
        },
        {
            'operation': 'mask_mask',
            'mask': shape_path.with_suffix('.nc').name,
            'var': f'm_{shape_index}'
        }
    ]
}

# second request: start the job on the files api
log.info('posting to the files api', data=json.dumps(data, indent=2))
response = requests.post(files_api_url, files={
    'data': json.dumps(data),
    shape_path.name: Path(shape_path).read_bytes(),
})

# check for errors
try:
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    log.error(
        'an error occured',
        status=response.status_code,
        response=json.dumps(response.json(), indent=2) if response.status_code == 400 else response.text
    )
    raise e

# extract the job object from the response
job = response.json()
log.info('job retrieved', job=json.dumps(job, indent=2))

while job['status'] in ['queued', 'started']:
    time.sleep(4)  # wait for 4 sec

    # following requests: check the status of the job
    job = requests.get(job['job_url']).json()
    log.info('job retrieved', job=json.dumps(job, indent=2))

if job['status'] == 'finished':
    # download file
    zip_path = Path(download_path) / job['file_name']
    zip_path.parent.mkdir(exist_ok=True)
    log.info('downloading', zip_path=str(zip_path.resolve()))
    with requests.get(job['file_url'], stream=True) as response:
        with zip_path.open('wb') as fp:
            for chunk in response.iter_content(chunk_size=8192):
                 fp.write(chunk)

    # extract zip file
    out_path = zip_path.with_suffix('')
    out_path.mkdir(exist_ok=True)
    log.info('extracting', out_path=str(out_path.resolve()))
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(out_path)

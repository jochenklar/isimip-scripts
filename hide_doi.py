#!/usr/bin/env python3
import os

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from rich import print

load_dotenv()

old_doi = '10.48364/isimip.428389'
new_doi = '10.48364/isimip.682793'

url = f'https://api.datacite.org/dois/{old_doi}'

auth = HTTPBasicAuth(
    os.getenv('DATACITE_USERNAME'),
    os.getenv('DATACITE_PASSWORD')
)

payload = {
    "data": {
        "type": "dois",
        "attributes": {
            # "event": "hide",
            # "url": f"https://data.isimip.org/{new_doi}",
            "relatedIdentifiers": [
                {
                    "relatedIdentifier": f"https://doi.org/{new_doi}",
                    "relatedIdentifierType": "DOI",
                    "relationType": "IsIdenticalTo"
                }
            ]
        }
    }
}

response = requests.put(url, json=payload, auth=auth)
print(response, response.json())

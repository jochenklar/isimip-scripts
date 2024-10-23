#!/usr/bin/env python3
#
# see also https://api.crossref.org/swagger-ui/index.html
#
import argparse
import re
from datetime import datetime

import requests
import structlog

logger = structlog.get_logger()

datacite_url = 'https://api.datacite.org/dois/'
crossref_url = 'https://api.crossref.org/works/'

datacite_headers = crossref_headers = {
    'User-Agent': 'ISIMIP/1.0 (https://www.isimip.org; mailto:jochen.klar@pik-potsdam.de)'
}

parser = argparse.ArgumentParser()
parser.add_argument('doi')
parser.add_argument('-o|--output-path', dest='output_path')

args = parser.parse_args()

citations = []

match = re.search(r'(10\.\d{5}\/ISIMIP\.\d{6})\.*(\d*)$', args.doi)
if match:
    doi = match.group(1)
    version = match.group(2)
    if version:
        versions = [doi] + [f'{doi}.{v}' for v in range(1, int(version) + 1)]
    else:
        versions = [doi]
else:
    parser.error('Could not parse DOI')

for doi in versions:
    logger.info('querying datacite', doi=doi)
    datacite_response = requests.get(datacite_url + doi, headers=datacite_headers)
    datacite_response.raise_for_status()
    datacite_data = datacite_response.json().get('data', {})

    datacite_related_identifiers = {
        related_identifier.get('relatedIdentifier') for related_identifier in
        datacite_data.get('attributes', {}).get('relatedIdentifiers', [])
    }

    datacite_citations = {
        citation.get('id') for citation in
        datacite_data.get('relationships', {}).get('citations', {}).get('data', [])
    }

    for citation_doi in (datacite_citations - datacite_related_identifiers):
        logger.info('querying crossref', doi=citation_doi)
        try:
            crossref_response = requests.get(crossref_url + citation_doi, headers=crossref_headers)
            crossref_response.raise_for_status()
            crossref_data = crossref_response.json().get('message', {})
        except requests.exceptions.HTTPError:
            logger.error('error with crossref api', doi=citation_doi, status=crossref_response.status_code)
            continue

        citation = {
            'doi': f'https://doi.org/{citation_doi}',
            'authors': ', '.join([
                '{given} {family}'.format(**author)
                for author in crossref_data.get('author', [])
            ]),
            'timestamp': crossref_data.get('created', {}).get('timestamp'),
            'title': crossref_data.get('title')[0],
            'publisher': crossref_data.get('publisher')
        }
        citation['year'] = datetime.fromtimestamp(citation['timestamp'] / 1e3).year \
                           if citation['timestamp'] else '????'
        citation['str'] = '{authors} ({year}): {title}. {publisher}. {doi}'.format(**citation)
        citations.append(citation)

print()
for citation in sorted(citations, key=lambda c: c['timestamp'], reverse=True):
    print(citation['str'] + '\n')

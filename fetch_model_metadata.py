#!/usr/bin/env python3
import argparse
import json
import re
from urllib.request import urlopen

CREATOR_KEYS = ['name', 'givenName', 'familyName', 'nameIdentifiers', 'affiliations']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('simulation_round')
    parser.add_argument('model_id', nargs='+')
    parser.add_argument('-o', dest='output_file')

    args = parser.parse_args()

    model_ids = args.model_id

    metadata = {
        'creators': [],
        'relatedIdentifiers': []
    }
    cleaned_metadata = {
        'creators': [],
        'relatedIdentifiers': []
    }

    for model_id in model_ids:
        model_json = fetch_json(model_id)
        model_url = f'https://www.isimip.org/impactmodels/details/{model_id}/'
        model_name = model_json[args.simulation_round]['titles'][0]['title']

        metadata['creators'] += model_json[args.simulation_round]['creators']

        metadata['relatedIdentifiers'].append({
            'relationType': 'IsDocumentedBy',
            'relatedIdentifier': model_url,
            'relatedIdentifierType': 'URL',
            'citation': f'Detailed description on isimip.org: {model_name} {model_url}',
            'resourceTypeGeneral': 'Text'
        })
        metadata['relatedIdentifiers'] += model_json[args.simulation_round]['related_identifiers']

    for creator in metadata['creators']:
        if creator.get('name') is None:
            creator['familyName'] = creator['givenName']
            creator['givenName'] = creator.pop('firstName')
            creator['name'] = creator['givenName'] + ' ' + creator['familyName']

        name_identifier = creator.pop('nameIdentifier', None)
        if name_identifier:
            creator['nameIdentifiers'] = [
                {
                    'nameIdentifier': name_identifier,
                    'nameIdentifierScheme': creator.pop('nameIdentifierScheme', 'ORCID')
                }
            ]
        cleaned_metadata['creators'].append({key: creator[key] for key in CREATOR_KEYS if key in creator})

    for identifier in metadata['relatedIdentifiers']:
        if identifier['relatedIdentifier']:
            if identifier['relatedIdentifierType'] == 'DOI' and not identifier['relatedIdentifier'].startswith('http'):
                identifier['relatedIdentifier'] = 'https://doi.org/' + identifier['relatedIdentifier']

            if 'title' in identifier:
                # substitute one or more commas which are not followed by a whitespace
                # and append DOI URL
                identifier['citation'] = re.sub(r',+([^\s])', r', \1',
                                                identifier.pop('title')) + '. ' + identifier['relatedIdentifier']

                # overide other fields of the isimip.org api
                identifier['relationType'] = 'Cites'
                identifier['resourceTypeGeneral'] = 'PeerReview'

            cleaned_metadata['relatedIdentifiers'].append(identifier)

    dump_json(cleaned_metadata, args.output_file)


def fetch_json(model_id):
    url = f'https://www.isimip.org/api/impactmodels/{model_id}/datacite/'
    return json.load(urlopen(url))


def dump_json(data, output_file):
    print(json.dumps(data, indent=2))

    if output_file:
        with open(output_file, 'w') as fp:
            json.dump(data, fp, indent=2)


if __name__ == '__main__':
    main()

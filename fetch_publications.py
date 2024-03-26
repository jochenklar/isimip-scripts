import json
import urllib.request
from collections import defaultdict
from datetime import datetime

url = 'https://publications.pik-potsdam.de/rest/items/search?format=json'
payload = {
    "query": {
        "bool": {
            "must": [
                {
                    "term": {
                        "publicState": {
                            "value" : "RELEASED",
                            "boost" : 1.0
                        }
                    }
                },
                {
                    "term": {
                        "versionState": {
                            "value" : "RELEASED",
                            "boost" : 1.0
                        }
                    }
                },
                {
                    "term": {
                        "metadata.creators.person.identifier.id": {
                            "value": "/persons/resource/matthias.mengel",
                            "boost": 1.0
                        }
                    }
                }
            ],
            "adjust_pure_negative": True,
            "boost" : 1.0
        }
    },
    "sort" : [
        {
            "metadata.datePublishedOnline" : {
                "order" : "DESC"
            }
        }
    ],
    "size" : "5000",
    "from" : "0"
}

request = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={
    'Content-Type': 'application/json'
})

def process_creators(metadata):
    return ', '.join([process_creator(creator) for creator in metadata.get('creators')])

def process_creator(creator):
    if 'givenName' in creator['person']:
        return '{familyName}, {givenName}'.format(**creator['person'])
    else:
        return '{familyName}'.format(**creator['person'])

def process_year(metadata):
    date_str = metadata.get('datePublishedOnline') or metadata.get('datePublishedInPrint')

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        try:
            date = datetime.strptime(date_str, '%Y-%m')
        except ValueError:
            date = datetime.strptime(date_str, '%Y')

    return date.year

def process_source(metadata):
    source_str = ''

    if 'sources' in metadata:
        source = metadata['sources'][0]

        source_str += '<i><b>{title}</b></i>'.format(**source)

        if 'volume' in source:
            source_str += ' {volume}'.format(**source)

            if 'issue' in source:
                source_str += '({issue})'.format(**source)

        if 'startPage' in source and 'endPage' in source:
            source_str += ' {startPage}-{endPage}'.format(**source)

        if 'sequenceNumber' in source:
            source_str += ' {sequenceNumber}'.format(**source)

        if source['genre'] == 'BOOK':
            source_str += ' {publisher}'.format(publisher=source.get('publishingInfo', {}).get('publisher'))

    return source_str

def process_identifier(metadata):
    for identifier in metadata.get('identifiers', []):
        if identifier['type'] == 'DOI':
            return '<a href="https://doi.org/{id}">https://doi.org/{id}</a>'.format(**identifier)

    return ''

output = defaultdict(lambda: defaultdict(list))

with urllib.request.urlopen(request) as response:
    content = response.read().decode()
    for result in json.loads(content).get('records', []):
        metadata = result.get('data', {}).get('metadata', {})

        creators = process_creators(metadata)
        year = process_year(metadata)
        title = metadata.get('title')
        source = process_source(metadata)
        identifier = process_identifier(metadata)

        citation = f'{creators} ({year}). {title}. {source}. {identifier}'

        output[metadata['genre']][year].append(citation)

for genre, years in output.items():
    print(f'<p>{genre}</p>')
    for year, items in sorted(years.items(), reverse=True):
        print(f'<p>{year}</p>')
        for item in items:
            print(f'<p>{item}</p>')

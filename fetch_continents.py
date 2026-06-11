import json

from SPARQLWrapper import JSON, SPARQLWrapper

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setReturnFormat(JSON)

query = """
    SELECT ?countryLabel ?iso2 ?continentLabel WHERE {
      ?country wdt:P31 wd:Q6256.          # instance of country
      ?country wdt:P30 ?continent.        # located on continent
      ?country wdt:P297 ?iso2.            # ISO 3166-1 alpha-2 code

      SERVICE wikibase:label {
        bd:serviceParam wikibase:language "en".
      }
    }
    ORDER BY ?continentLabel ?countryLabel
"""

sparql.setQuery(query)

# Execute the query and process results
results = sparql.query().convert()

continents = [
    {
        'country': result['iso2']['value'].lower(),
        'continent': result['continentLabel']['value'],
    }
    for result in results["results"]["bindings"]
]

print(json.dumps(continents, indent=2))

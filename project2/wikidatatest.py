import json
from SPARQLWrapper import SPARQLWrapper, JSON
import ssl

QUERY_URL = 'http://query.wikidata.org/sparql'

if __name__ == '__main__':
    ssl._create_default_https_context = ssl._create_unverified_context

    query = """
    SELECT ?p
    (SAMPLE(?name) as ?name) (SAMPLE(?birth) as ?birth) (SAMPLE(?facebook) as ?facebook) (SAMPLE(?twitter) as ?twitter)
    (SAMPLE(?instagram) as ?instagram) (SAMPLE(?url) as ?url) (SAMPLE(?official_site) as ?official_site)
    (SAMPLE(?country_name) as ?country_name)
    WHERE {
      ?p wdt:P106 wd:Q177220 .
      ?p wdt:P1559 ?name .
      OPTIONAL {?p wdt:P569 ?birth}
      OPTIONAL {?p wdt:P2013 ?facebook}
      OPTIONAL {?p wdt:P2002 ?twitter}
      OPTIONAL {?p wdt:P2003 ?instagram}
      OPTIONAL {?p wdt:P854 ?url}
      OPTIONAL {?p wdt:P856 ?official_site}
      OPTIONAL {?p wdt:P27 ?country .
                ?country wdt:P1448 ?country_name}
      FILTER(REGEX(STR(?name), "Justin.*$"))
    } GROUP BY ?p
    """
    sparql = SPARQLWrapper(QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print(results)

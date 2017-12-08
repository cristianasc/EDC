from SPARQLWrapper import SPARQLWrapper, JSON
import ssl
from itertools import groupby

QUERY_URL = 'http://query.wikidata.org/sparql'


def perform_query(query, keys):
    """
        Override the SSL verification
    """
    ssl._create_default_https_context = ssl._create_unverified_context

    sparql = SPARQLWrapper(QUERY_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return parse_response(results, keys)


def parse_response(results, keys=None):
    response = []

    if keys is None:
        keys = results["head"]["vars"]

    for binding in results["results"]["bindings"]:
        r = {}

        for key in keys:
            if key not in binding:
                continue

            values = binding[key]["value"].split(",")

            if len(values) > 1:
                r[key] = []

                for value in values:
                    r[key].append(value.replace("T00:00:00Z", ""))
            else:
                r[key] = values[0].replace("T00:00:00Z", "")

        response.append(r)

    if len(response) == 0:
        return []

    return response if len(response) > 1 else response[0]

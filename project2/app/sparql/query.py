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

    r = {}

    for key in keys:
        try:
            if len(results["results"]["bindings"]) > 0:
                values = results["results"]["bindings"][0][key]["value"].split(",")

                if len(values) > 1:
                    r[key] = []

                    for value in values:
                        r[key].append(value.replace("T00:00:00Z", ""))
                else:
                    r[key] = values[0].replace("T00:00:00Z", "")

        except KeyError:
            continue

    return r

from .query import perform_query


def search_artist_info(name):
    query = """
        SELECT ?p
        (SAMPLE(?name) as ?name) (SAMPLE(?birth) as ?birth) (SAMPLE(?facebook) as ?facebook) (SAMPLE(?twitter) as ?twitter)
        (SAMPLE(?instagram) as ?instagram) (SAMPLE(?url) as ?url) (SAMPLE(?official_site) as ?official_site)
        (SAMPLE(?country_name) as ?country_name)
        WHERE {
          ?p wdt:P106 wd:Q177220 .
          ?p rdfs:label ?name .
          OPTIONAL {?p wdt:P569 ?birth}
          OPTIONAL {?p wdt:P2013 ?facebook}
          OPTIONAL {?p wdt:P2002 ?twitter}
          OPTIONAL {?p wdt:P2003 ?instagram}
          OPTIONAL {?p wdt:P854 ?url}
          OPTIONAL {?p wdt:P856 ?official_site}
          OPTIONAL {?p wdt:P27 ?country .
                    ?country wdt:P1448 ?country_name}
          FILTER(REGEX(STR(?name), "%s.*$"))
        } GROUP BY ?p
        """ % name

    keys = [
        "p",
        "birth",
        "facebook",
        "twitter",
        "instagram",
        "url",
        "official_site",
        "country"
    ]

    return perform_query(query, keys)


def search_artist_genre(identifier):
    query = """
        SELECT ?p
        (GROUP_CONCAT(DISTINCT ?genre_name ; SEPARATOR=",") as ?genre)
        WHERE
        {
          <%s> rdfs:label ?p.
          FILTER(LANG(?p) = "en")
          OPTIONAL {<%s> wdt:P136 ?genre .
                    ?genre rdfs:label ?genre_name.
                    FILTER(LANG(?genre_name) = "en")}
        }
        GROUP BY ?p
    """ % (identifier, identifier)

    keys = [
        "genre"
    ]

    return perform_query(query, keys)


def search_artist_relationships(identifier):
    query = """
        SELECT ?p
        (GROUP_CONCAT(DISTINCT ?father_name ; SEPARATOR=",") as ?father)
        (GROUP_CONCAT(DISTINCT ?mother_name ; SEPARATOR=",") as ?mother)
        (GROUP_CONCAT(DISTINCT ?sibling_name ; SEPARATOR=",") as ?sibling)
        WHERE
        {
          <%s> rdfs:label ?p.
          FILTER(LANG(?p) = "en")
          OPTIONAL {<%s> wdt:P22 ?father .
                    ?father rdfs:label ?father_name.
                    FILTER(LANG(?father_name) = "en")}
          OPTIONAL {<%s> wdt:P25 ?mother .
                    ?mother rdfs:label ?mother_name.
                    FILTER(LANG(?mother_name) = "en")}
          OPTIONAL {<%s> wdt:P3373 ?sibling .
                    ?sibling rdfs:label ?sibling_name.
                    FILTER(LANG(?sibling_name) = "en")}
        }
        GROUP BY ?p
    """ % (identifier, identifier, identifier, identifier)

    keys = [
        "father",
        "mother",
        "sibling"
    ]

    return perform_query(query, keys)


def search_artist_occupations(identifier):
    query = """
        SELECT ?p
        (GROUP_CONCAT(DISTINCT ?occupations_name ; SEPARATOR=",") as ?occupations)
        WHERE
        {
          <%s> rdfs:label ?p.
          FILTER(LANG(?p) = "en")
          OPTIONAL {<%s> wdt:P106 ?occupations .
                    ?occupations rdfs:label ?occupations_name.
                    FILTER(LANG(?occupations_name) = "en")}
        }
        GROUP BY ?p
    """ % (identifier, identifier)

    keys = [
        "occupations"
    ]

    return perform_query(query, keys)


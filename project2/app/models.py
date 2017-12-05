from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
import json


class Database:
    def __init__(self):
        self.endpoint = "http://localhost:7200"
        self.repo_name = "Spotify"
        self.client = ApiClient(endpoint=self.endpoint)
        self.accessor = GraphDBApi(self.client)

    def get_new_releases(self):
        query = """
                PREFIX foaf: <http://xmlns.com/foaf/spec/>
                SELECT ?name 
                WHERE {
                    ?p foaf:name_album ?name .
                }"""

        payload_query = {"query": query}
        data = json.loads(self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name))
        return (data["results"]["bindings"])[0:10]

    def get_new_releases_image(self):
        query = """
                PREFIX foaf: <http://xmlns.com/foaf/spec/>
                PREFIX spot: <http://new-releases.org/pred/>
                SELECT ?name ?url
                WHERE
                    {
                    ?p spot:image ?name .
                    ?name foaf:url ?url .
                    filter regex(str(?name), "300" )
                }"""

        payload_query = {"query": query}
        data = json.loads(self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name))
        return (data["results"]["bindings"])[0:10]


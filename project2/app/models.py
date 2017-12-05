from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient


class Database:
    def __init__(self):
        self.endpoint = "http://localhost:7200"
        self.repo_name = "Spotify"
        self.client = ApiClient(endpoint=self.endpoint)
        self.accessor = GraphDBApi(self.client)

        """album's names"""
    def get_new_releases(self):
        query = """
                PREFIX foaf: <http://xmlns.com/foaf/spec/>
                SELECT ?name 
                WHERE {
                    ?p foaf:name_album ?name .
                }"""

        payload_query = {"query": query}
        data = self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name)
        print(data)


from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient


class Database:
   def __init__(self):
        self.endpoint = "http://localhost:7200"
        self.repo_name = "Spotify"
        self.client = ApiClient(endpoint=self.endpoint)
        self.accessor = GraphDBApi(self.client)
        payload = {
            "repositoryID": self.repo_name,
            "label": "Spotify Database",
            "ruleset": "owl-horst-optimized"
        }
        self.accessor.create_repository(body=payload)
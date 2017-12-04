from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient


class Database:
    def __init__(self):
        self.endpoint = "http://localhost:7200"
        self.repo_name = "Spotify"
        self.client = ApiClient(endpoint=self.endpoint)
        self.accessor = GraphDBApi(self.client)


    def get_new_releases(self):
        print("new_releases")


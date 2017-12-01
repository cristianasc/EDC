from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient


class Database:
    def __init__(self):
        endpoint = "http://localhost:7200"
        repo_name = "Spotify"
        client = ApiClient(endpoint=endpoint)
        accessor = GraphDBApi(client)
import xmltodict, dicttoxml
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
import json, requests
import lxml.etree as ET


class Database:
    def __init__(self):
        self.endpoint = "http://localhost:7200"
        self.repo_name = "Spotify"
        self.client = ApiClient(endpoint=self.endpoint)
        self.accessor = GraphDBApi(self.client)
        payload = {
            "repositoryID": self.repo_name,
            "label": "Spotify",
            "ruleset": "owl-horst-optimized"
        }

        self.accessor.create_repository(body=payload)

        dom = ET.parse("new-releases.xml")
        xslt = ET.parse("new-releases.xslt")
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        content = ET.tostring(newdom, pretty_print=False).decode()
        file = open("new-releases.rdf", "w")
        file.write(content)

        dom = ET.parse("top-tracks.xml")
        xslt = ET.parse("top-tracks.xslt")
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        content = ET.tostring(newdom, pretty_print=False).decode()
        file = open("top-tracks.rdf", "w")
        file.write(content)

        dom = ET.parse("recently-played-by-user.xml")
        xslt = ET.parse("recently-played-by-user.xslt")
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        content = ET.tostring(newdom, pretty_print=False).decode()
        #file = open("recently-played-by-user.rdf", "w")
        #file.write(content)

        self.accessor.upload_data_file("new-releases.rdf", repo_name=self.repo_name)
        self.accessor.upload_data_file("top-tracks.rdf", repo_name=self.repo_name)

    """api queries"""

    def new_releases(self, token):
        headers = {"Authorization": "Bearer " + token["access_token"]}
        r = requests.get('https://api.spotify.com/v1/browse/new-releases', headers=headers)
        xmlString = xmltodict.unparse(json.loads(r.text), pretty=True)
        file = open("new-releases.xml", "w")
        file.write(xmlString)

    def top_tracks(self, token):
        headers = {"Authorization": "Bearer " + token["access_token"]}
        r = requests.get('https://api.spotify.com/v1/me/top/tracks', headers=headers)
        xmlString = xmltodict.unparse(json.loads(r.text), pretty=True)
        file = open("top-tracks.xml", "w")
        file.write(xmlString)

    def recently_played_by_user(self, token):
        headers = {"Authorization": "Bearer " + token}
        r = requests.get('https://api.spotify.com/v1/me/player/recently-played', headers=headers)
        xmlString = dicttoxml.dicttoxml(json.loads(r.text))
        file = open("recently-played-by-user.xml", "wb")
        file.write(xmlString)

    def getArtist(self, token, id):
        headers = {"Authorization": "Bearer " + token}
        r = requests.get('https://api.spotify.com/v1/artists/'+id, headers=headers)
        xmlString = dicttoxml.dicttoxml(json.loads(r.text))
        file = open("artist.xml", "wb")
        file.write(xmlString)

    """database queries"""
    def get_new_releases(self):
        query = """
                PREFIX foaf: <http://xmlns.com/foaf/spec/>
                SELECT ?name 
                WHERE {
                    ?p foaf:name_album ?name .
                }"""

        payload_query = {"query": query}
        data = json.loads(self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name))
        return ((data["results"]["bindings"]))

    def get_new_releases_image(self):
        query = """
                PREFIX foaf: <http://xmlns.com/foaf/spec/>
                PREFIX spot: <http://new-releases.org/pred/>
                SELECT ?url
                WHERE
                    {
                    ?p spot:image ?name .
                    ?name foaf:url ?url .
                    filter regex(str(?name), "300" )
                }"""

        payload_query = {"query": query}
        data = json.loads(self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name))
        return data["results"]["bindings"]

    def get_top_tracks(self):
        query = """
                PREFIX foaf: <http://xmlns.com/foaf/spec/>
                PREFIX spot: <http://top-tracks.org/pred/>
                SELECT ?name ?src
                WHERE {
                    ?p foaf:name_track ?name .
                    ?p spot:image ?url .
                    ?url foaf:url ?src .
                    filter regex(str(?url), "300" )
                }"""

        payload_query = {"query": query}
        data = json.loads(self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name))
        return ((data["results"]["bindings"]))

    def get_top_tracks_artists(self):
        query = """
                PREFIX foaf: <http://xmlns.com/foaf/spec/>
                PREFIX spot: <http://top-tracks.org/pred/>
                SELECT ?name ?nameartist ?id
                WHERE {
                    ?p foaf:name_track ?name .
                    ?p spot:artists ?artists .
                    ?artists foaf:name ?nameartist .
                    ?artists spot:id ?id .
                }"""

        payload_query = {"query": query}
        data = json.loads(self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name))
        return data["results"]["bindings"]


    def get_recently_played_by_user(self):
        query = """
                        PREFIX foaf: <http://xmlns.com/foaf/spec/>
                        SELECT ?name
                        WHERE {
                        ?p foaf:name_track ?name .
                        }"""

        payload_query = {"query": query}
        data = json.loads(self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name))
        return ((data["results"]["bindings"])[0:10])

    def get_artist_by_id(self):
        query = """
                        PREFIX foaf: <http://xmlns.com/foaf/spec/>
                        SELECT ?name
                        WHERE {
                        ?p foaf:name ?name .
                        }"""

        payload_query = {"query": query}
        data = json.loads(self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name))
        return ((data["results"]["bindings"])[0:10])



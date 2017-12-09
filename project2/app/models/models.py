import xmltodict, dicttoxml
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
import json, requests
import lxml.etree as ET
from .query import parse_response


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
        file = open("recently-played-by-user.rdf", "w")
        file.write(content)

        self.accessor.upload_data_file("new-releases.rdf", repo_name=self.repo_name)
        self.accessor.upload_data_file("top-tracks.rdf", repo_name=self.repo_name)
        self.accessor.upload_data_file("recently-played-by-user.rdf", repo_name=self.repo_name)

    def parse_artists(self, artist):
        artist = bytes(bytearray(artist, encoding='utf-8'))
        dom = ET.fromstring(artist)
        xslt = ET.parse("artists.xslt")
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        content = ET.tostring(newdom, pretty_print=False).decode()
        return content

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

    def getArtist(self, token, artist):
        headers = {"Authorization": "Bearer " + token}
        r = requests.get('https://api.spotify.com/v1/search?q=' + artist + '&type=artist', headers=headers)
        xmlString = xmltodict.unparse(json.loads(r.text), pretty=True)
        return xmlString

    """database queries"""

    def comment(self, uid, name, comment, music_id):
        update = """
                    PREFIX foaf: <http://xmlns.com/foaf/spec/>
                    PREFIX spot: <http://comments.org/pred/>
                    INSERT DATA {
                         <http://comments.com/items/"""+music_id+"""> foaf:profile_id \""""+uid+"""\" ;
                                                       spot:profile_name \""""+name+"""\";
                                                       spot:comment \""""+comment+"""\" .
                    }"""


        payload_query = {"update": update}
        self.accessor.sparql_update(body=payload_query, repo_name=self.repo_name)



    def get_comments(self, music_id):
        query = """PREFIX foaf: <http://xmlns.com/foaf/spec/>
                   PREFIX spot: <http://comments.org/pred/>
                   SELECT ?user_id ?name ?comment
                   WHERE{
                            <http://comments.com/items/"""+music_id+"""> foaf:profile_id ?user_id .
                            <http://comments.com/items/"""+music_id+"""> spot:profile_name ?name .
                            <http://comments.com/items/"""+music_id+"""> spot:comment ?comment .
                    }
                    """

        payload_query = {"query": query}
        data = json.loads(self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name))
        data = parse_response(data)
        return data

    def get_new_releases(self):
        query = """
                PREFIX foaf: <http://xmlns.com/foaf/spec/>
                PREFIX spot: <http://new-releases.org/pred/>
                SELECT ?name ?id ?src ?width
				(GROUP_CONCAT(DISTINCT ?nameartist ; SEPARATOR=",") as ?artists)
				(GROUP_CONCAT(DISTINCT ?artist_id ; SEPARATOR=",") as ?ids)
                WHERE {
                    ?p foaf:name_album ?name .
                    ?p spot:id ?id .
                    ?p spot:image ?url .
                    ?url spot:width ?width .
                    ?url foaf:url ?src .
                    ?p spot:artists ?artists .
                    ?artists foaf:name ?nameartist .
                    ?artists spot:id ?artist_id .
                    filter regex(str(?url), "300" )
                }
				GROUP BY  ?name ?id ?src ?width
                """

        payload_query = {"query": query}
        data = json.loads(self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name))
        data = parse_response(data)
        return data

    def get_top_tracks(self):
        query = """
                PREFIX foaf: <http://xmlns.com/foaf/spec/>
                PREFIX spot: <http://top-tracks.org/pred/>
                SELECT ?name ?id ?src ?ids ?artists ?width
				(GROUP_CONCAT(DISTINCT ?nameartist ; SEPARATOR=",") as ?artists)
				(GROUP_CONCAT(DISTINCT ?artist_id ; SEPARATOR=",") as ?ids)
                WHERE {
                    ?p foaf:name_track ?name . 
                    ?p spot:id ?id .
                    ?p spot:image ?url .
                    ?url spot:width ?width .
                    ?url foaf:url ?src .
                    ?p spot:artists ?artists .
                    ?artists foaf:name ?nameartist .
                    ?artists spot:id ?artist_id .
                    filter regex(str(?url), "300" )
                }
				GROUP BY  ?name ?id ?src ?width
				"""

        payload_query = {"query": query}
        data = json.loads(self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name))
        data = parse_response(data)
        return data

    def get_recently_played_by_user(self):
        query = """
                PREFIX foaf: <http://xmlns.com/foaf/spec/>
                PREFIX spot: <http://recently-played-by-user.org/pred/>
                SELECT ?id ?name ?href30sec ?image ?artists
                (GROUP_CONCAT(DISTINCT ?nameartist ; SEPARATOR=",") as ?artists)
                WHERE {
                    ?p spot:track ?track .
                    ?track spot:id ?id .
                    ?track spot:preview_url ?href30sec .
                    ?track foaf:name ?name .
                    ?p spot:artists ?artist .
                    ?artist foaf:name ?nameartist .
                    ?p spot:image ?url .
                    ?url foaf:url ?image .
                    filter regex(str(?url), "300" )
                }
                GROUP BY ?id ?name ?href30sec ?image
                """

        payload_query = {"query": query}
        data = parse_response(json.loads(self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name)))
        return data

    def get_artists_info(self):
        query = """
                PREFIX foaf: <http://xmlns.com/foaf/spec/>
                PREFIX spot: <http://artists.org/pred/>
                SELECT ?name ?id ?image ?followers
                WHERE {
                        ?p foaf:name_artist ?name .
                        ?p spot:id ?id .
                        ?p spot:followers ?followers .
                        ?p spot:image ?url .
                        ?url foaf:url ?image .
                        filter regex(str(?url), "300" )
                }"""

        payload_query = {"query": query}
        data = json.loads(self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name))
        return ((data["results"]["bindings"]))

    def get_music_info(self, id, token=None):
        query = """
            PREFIX foaf: <http://xmlns.com/foaf/spec/>
            PREFIX spot: <http://top-tracks.org/pred/>
            SELECT ?name_track ?external_urls ?href ?disc_number ?popularity ?preview_url ?track_number ?artists
            (GROUP_CONCAT(DISTINCT ?nameartist ; SEPARATOR=",") as ?artists)
            (GROUP_CONCAT(DISTINCT ?images_url ; SEPARATOR=",") as ?image_url)
            (GROUP_CONCAT(DISTINCT ?artist_id ; SEPARATOR=",") as ?artists_ids)
            WHERE {
                ?id spot:id \""""+id+"""\" .
                ?id foaf:name_track ?name_track .
                ?id spot:external_urls ?external_urls .
                ?id spot:href ?href .
                ?id spot:disc_number ?disc_number .
                ?id spot:popularity ?popularity .
                ?id spot:preview_url ?preview_url .
                ?id spot:track_number ?track_number .
                ?id spot:artists ?artists .
                ?artists foaf:name ?nameartist .
                ?artists spot:id ?artist_id .
                ?id spot:image ?images .
                ?images foaf:url ?images_url .
            } GROUP BY ?name_track ?external_urls ?href ?disc_number ?popularity ?preview_url ?track_number
        """
        payload_query = {"query": query}
        data = parse_response(json.loads(self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name)))

        if len(data) == 0:
            # means it's empty
            # new releases
            query = """
                PREFIX foaf: <http://xmlns.com/foaf/spec/>
                PREFIX spot: <http://new-releases.org/pred/>
                SELECT ?name_track ?external_urls ?href ?preview_url
                (GROUP_CONCAT(DISTINCT ?nameartist ; SEPARATOR=",") as ?artists)
                (GROUP_CONCAT(DISTINCT ?images_url ; SEPARATOR=",") as ?image_url)
                (GROUP_CONCAT(DISTINCT ?artist_id ; SEPARATOR=",") as ?artists_ids)
                WHERE {
                    ?id spot:id \""""+id+"""\" .
                    ?id foaf:name_album ?name_track .
                    ?id spot:external_urls ?external_urls .
                    ?id spot:href ?href .
				    OPTIONAL {?id spot:preview_url ?preview_url .}
                    ?id spot:artists ?artists .
                    ?artists foaf:name ?nameartist .
                    ?artists spot:id ?artist_id .
                    ?id spot:image ?images .
                    ?images foaf:url ?images_url .
                } GROUP BY ?name_track ?external_urls ?href ?preview_url
            """
            payload_query = {"query": query}
            data = parse_response(json.loads(self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name)))

        if len(data) == 0:
            # means it's empty
            # recently played by user
            query = """
                    PREFIX foaf: <http://xmlns.com/foaf/spec/>
                    PREFIX spot: <http://recently-played-by-user.org/pred/>
                    SELECT ?name_track ?external_urls ?href ?preview_url
                    (GROUP_CONCAT(DISTINCT ?nameartist ; SEPARATOR=",") as ?artists)
                    (GROUP_CONCAT(DISTINCT ?artist_id ; SEPARATOR=",") as ?artists_ids)
                    (GROUP_CONCAT(DISTINCT ?image ; SEPARATOR=",") as ?image_url)
                    WHERE {
                        ?p spot:track ?track .
                        ?track spot:id \""""+id+"""\" .
                        ?track spot:preview_url ?preview_url .
                        ?track spot:external_urls ?external_urls .
                        ?track foaf:name ?name_track .
                        ?track spot:href ?href .
                        ?p spot:artists ?artist .
                        ?artist foaf:name ?nameartist .
                        ?artist spot:id ?artist_id .
                        ?p spot:image ?url .
                        ?url foaf:url ?image .
                    }
                    GROUP BY ?name_track ?external_urls ?href ?preview_url
                """
            payload_query = {"query": query}
            data = parse_response(json.loads(self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name)))

        if len(data) == 0 and token is not None:
            # means it's empty
            # get track from spotify
            data = {
                "name_track": "",
                "popularity": 0,
                "track_number": 1,
                "preview_url": "",
                "image_url": [],
                "href": "",
                "external_urls": "",
                "disc_number": 1,
                "artists_ids": [],
                "artists": []
            }

            # Get track
            headers = {"Authorization": "Bearer " + token}
            r = requests.get('https://api.spotify.com/v1/tracks/' + id, headers=headers)
            r = json.loads(r.text)

            if "name" in r:
                data["name_track"] = r["name"]

            if "popularity" in r:
                data["popularity"] = r["popularity"]

            if "track_number" in r:
                data["track_number"] = r["track_number"]

            if "preview_url" in r:
                data["preview_url"] = r["preview_url"]

            if "album" in r and "images" in r["album"]:
                data["image_url"] = [image["url"] for image in r["album"]["images"]]

            if "href" in r:
                data["href"] = r["href"]

            if "external_urls" in r:
                data["external_urls"] = r["external_urls"]["spotify"]

            if "disc_number" in r:
                data["disc_number"] = r["disc_number"]

            if "artists" in r:
                data["artists"] = [artist["name"] for artist in r["artists"]]

            if "artists_ids" in r:
                data["artists_ids"] = [artist["id"] for artist in r["artists"]]

        return data

    def search_artists(self, name):
        query = """
            PREFIX foaf:  <http://xmlns.com/foaf/spec/>
            PREFIX spot:  <http://new-releases.org/pred/>
            PREFIX spot2: <http://top-tracks.org/pred/>
            PREFIX spot3: <http://recently-played-by-user.org/pred/>
            PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?nameartist (SAMPLE(?artist_id) AS ?artist_id)  {
                {
                    SELECT ?nameartist ?artist_id
                    WHERE {
                        ?p spot:artists ?artists .
                        ?artists foaf:name ?nameartist .
                        ?artists spot:id ?artist_id .
                    }
                }UNION {
                    SELECT ?nameartist ?artist_id
                    WHERE {
                        ?p spot2:artists ?artists .
                        ?artists foaf:name ?nameartist .
                        ?artists spot2:id ?artist_id .
                    }

                }UNION {
                    SELECT ?nameartist ?artist_id
                    WHERE {
                        ?p spot3:track ?track .
                        ?p spot3:artists ?artists .
                        ?artists foaf:name ?nameartist .
                        ?artists spot3:id ?artist_id .
                    }
                }
                FILTER(REGEX(STR(?nameartist), "%s.*$", "i"))
            } GROUP BY ?nameartist
        """ % name

        payload_query = {"query": query}
        data = parse_response(json.loads(self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name)))

        return data

    def search_musics_and_albums(self, name):
        query = """
            PREFIX foaf:  <http://xmlns.com/foaf/spec/>
            PREFIX spot:  <http://new-releases.org/pred/>
            PREFIX spot2: <http://top-tracks.org/pred/>
            PREFIX spot3: <http://recently-played-by-user.org/pred/>
            PREFIX rdfs:  <http://www.w3.org/2000/01/rdf-schema#>

            SELECT DISTINCT ?name ?id  {
                {
                    # new releases
                    SELECT ?name ?id ?name_artist
                    WHERE {
                        ?p foaf:name_album ?name .
                        ?p spot:id ?id .
                        ?p spot:artists ?artists .
                        ?artists foaf:name ?name_artist
                    }
                }UNION {
                    # top tracks
                    SELECT ?name ?id
                    WHERE {
                        ?p foaf:name_track ?name .
                        ?p spot2:id ?id .
                        ?p spot2:artists ?artists .
                        ?artists foaf:name ?name_artist
                    }

                }UNION {
                    # recent played by user
                    SELECT ?name ?id
                    WHERE {
                        ?p spot3:track ?track .
                        ?track foaf:name ?name .
                        ?track spot3:id ?id .
                        ?p spot:artists ?artist .
                        ?artist foaf:name ?name_artist .
                    }
                }
                FILTER(REGEX(STR(?name), "%s.*$", "i") || REGEX(STR(?name_artist), "%s.*$", "i"))
            }
        """ % (name, name)

        payload_query = {"query": query}
        data = parse_response(json.loads(self.accessor.sparql_select(body=payload_query, repo_name=self.repo_name)))

        return data
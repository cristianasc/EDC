from django.core.management.base import BaseCommand
from app.models import Database
import lxml.etree as ET
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
import urllib.request


class Command(BaseCommand):
    help = 'Imports and creates the database'

    def handle(self, *args, **options):
        db = Database()

        payload = {
            "repositoryID": db.repo_name,
            "label": "Spotify",
            "ruleset": "owl-horst-optimized"
        }

        db.accessor.create_repository(body=payload)

        dom = ET.parse("new-releases.xml")
        xslt = ET.parse("new-releases.xslt")
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        content = ET.tostring(newdom, pretty_print=False).decode()
        file = open("new-releases.rdf", "w")
        file.write(content)

        #db.accessor.upload_data_file("new-releases.rdf", repo_name=db.repo_name)

        update = """INSERT DATA {
        <http://dbpedia.org/resource/University_of_Leipzig>
        <http://dbpedia.org/property/students>
        "12345678"
        }"""

        query = {"update": update}
        db.accessor.sparql_update(body=query, repo_name=db.repo_name)

        query = """PREFIX fb: <http://rdf.freebase.com/ns/>
                PREFIX dbpedia: <http://dbpedia.org/resource/>

                SELECT ?s ?p ?o
                WHERE {
                    ?s ?p ?o .
                }"""

        payload_query = {"query": query}
        print(db.accessor.sparql_select(body=payload_query, repo_name=db.repo_name))
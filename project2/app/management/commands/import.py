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

        dom = ET.parse("new-releases.xml")
        xslt = ET.parse("new-releases.xslt")
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        content = ET.tostring(newdom, pretty_print=False).decode()
        file = open("new-releases.rdf", "w")
        file.write(content)

        db.accessor.upload_data_file("new-releases.rdf", repo_name=db.repo_name)

        '''query = {"update": content}
        db.accessor.sparql_update(body=query, repo_name=db.repo_name)'''
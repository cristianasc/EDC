from django.core.management.base import BaseCommand
from BaseXClient import BaseXClient
import lxml.etree as ET
import urllib.request


from app.models import Database


class Command(BaseCommand):
    help = 'Imports and creates a basex database'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        url = options["url"]

        fp = urllib.request.urlopen(url)
        file_content = fp.read()
        fp.close()

        dom = ET.fromstring(file_content)
        xslt = ET.parse("transformation.xslt")
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        content = ET.tostring(newdom, pretty_print=False).decode()

        session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
        session.create("database", content)
        session.create("likes", "<?xml version='1.0' encoding='utf-8'?>"
                                     "<likes> <new/> </likes>")

        Database().likes_xml()
        session.create("comments", "<?xml version='1.0' encoding='utf-8'?>"
                                   "<comments>"
                                   "</comments>")

        print(session.info())
        print(session.execute("xquery doc('database')"))

        session.close()

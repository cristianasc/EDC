from django.core.management.base import BaseCommand
from BaseXClient import BaseXClient
import lxml.etree as ET

from app.models import Database


class Command(BaseCommand):
    help = 'Imports and creates a basex database'

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str)

    def handle(self, *args, **options):
        file_name = options["file_name"]

        dom = ET.parse(file_name)
        xslt = ET.parse("transformation.xslt")
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        content = ET.tostring(newdom, pretty_print=False).decode()

        session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
        session.create("database", content)
        session.create("likes", "<?xml version='1.0' encoding='utf-8'?>"
                                     "<likes>"

        Database().likes_xml()
        session.create("comments", "<?xml version='1.0' encoding='utf-8'?>"
                                   "<comments>"
                                   "</comments>")

        print(session.info())
        print(session.execute("xquery doc('database')"))

        session.close()

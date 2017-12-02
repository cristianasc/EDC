from django.core.management.base import BaseCommand
from app.models import Database
import lxml.etree as ET
import urllib.request


class Command(BaseCommand):
    help = 'Imports and creates the database'

    def handle(self, *args, **options):

        dom = ET.fromstring("new-releases.xml")
        xslt = ET.parse("new-releases.xslt")
        transform = ET.XSLT(xslt)
        newdom = transform(dom)
        content = ET.tostring(newdom, pretty_print=False).decode()

        db = Database()
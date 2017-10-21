from django.core.management.base import BaseCommand
from BaseXClient import BaseXClient


class Command(BaseCommand):
    help = 'Imports and creates a basex database'

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str)

    def handle(self, *args, **options):
        file_name = options["file_name"]

        f = open(file_name, 'r', encoding='utf-8')

        session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
        session.create("database", f.read())
        session.create("likes", "<?xml version='1.0' encoding='utf-8'?>"
                                     "<likes>"
                                        "<new> "
                                            "</like>"
                                            "</dislike>"
                                            "<userid/>"
                                        "</new>"
                                     "</likes>")
        session.create("comments", "<?xml version='1.0' encoding='utf-8'?>"
                                   "<comments>"
                                   "</comments>")

        print(session.info())
        print(session.execute("xquery doc('database')"))

        session.close()

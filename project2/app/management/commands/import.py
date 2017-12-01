from django.core.management.base import BaseCommand
from app.models import Database

class Command(BaseCommand):
    help = 'Imports and creates the database'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        pass

from django.core.management.base import BaseCommand
from app.models import Database


class Command(BaseCommand):
    help = 'Imports and creates the database'

    def handle(self, *args, **options):
        db = Database()
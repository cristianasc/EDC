from django.core.management.base import BaseCommand
from app.models import Database



class Command(BaseCommand):
    help = 'Sync spotify artists'

    def handle(self, *args, **options):
        db = Database()
        headers = {"Authorization": "Bearer "}

        for artist in db.get_artists():
            db.put_artist(headers, artist['name'], artist['id'])



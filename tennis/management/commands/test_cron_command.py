from django.core.management.base import BaseCommand

import datetime

from tennis.models import CourtLocation


class Command(BaseCommand):
    help = """let's test cron
        """

    def handle(self, *args, **options):

        CourtLocation.objects.create(name='Test {}'.format(datetime.datetime.now()))

        print('created a new CourtLocation')

        return

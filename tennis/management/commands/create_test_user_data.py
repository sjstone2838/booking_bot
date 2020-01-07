from django.core.management.base import BaseCommand

from django.contrib.auth.models import User
from tennis.models import UserProfile
from tennis.models import CourtLocation
from tennis.models import BookingParameter
# from tennis.models import Booking

# from utils import execute
# from utils import random_date
# from pydash import py_
# import random


class Command(BaseCommand):
    help = """python manage.py create_test_user_data
    Creates some fake user date.
    """

    def handle(self, *args, **options):
        user = User.objects.get_or_create(
            first_name='Sam',
            last_name='Stone',
            username='sam.stone@opendoor.com',
            email='sam.stone@opendoor.com'
        )[0]

        UserProfile.objects.get_or_create(
            user=user,
            spotery_login=user.email,
            spotery_password='abcde12345'
        )[0]

        court_location = CourtLocation.objects.get_or_create(
            name='Hamilton Rec'
        )[0]

        BookingParameter.objects.get_or_create(
            user=user,
            court_location=court_location,
            day_of_week='Saturday',
            time_of_day=10.5
        )[0]

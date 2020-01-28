from django.core.management.base import BaseCommand

from tennis.models import BookingParameter
from tennis.models import Booking

import datetime

from .spotery_constants import LOCAL_TIME_ZONE


class Command(BaseCommand):
    help = """python manage.py execute_pending_bookings
        Attempts to book all bookings with status=pending.
        """

    def handle(self, *args, **options):

        booking_parameters = BookingParameter.objects.filter(active=True)

        new_pending_booking_count = 0
        for i, bp in enumerate(booking_parameters):

            # start by considering bookings for tomorrow (not today)
            date_counter = datetime.datetime.now() + datetime.timedelta(days=1)

            advance_another_day = True

            # advance until date_counter is the next instance of the desired day of week
            while advance_another_day:

                if date_counter.strftime('%A') == bp.day_of_week:
                    advance_another_day = False

                else:
                    date_counter = date_counter + datetime.timedelta(days=1)

            next_datetime_to_book = LOCAL_TIME_ZONE.localize(datetime.datetime(
                date_counter.year,
                date_counter.month,
                date_counter.day,
                int(bp.time_of_day),
                int((bp.time_of_day - int(bp.time_of_day)) * 60)
            ), is_dst=True)

            booking, created = Booking.objects.get_or_create(
                user=bp.user,
                court_location=bp.court_location,
                datetime=next_datetime_to_book,
            )

            if created:
                print('Creating booking {}'.format(i))
                new_pending_booking_count += 1
            else:
                print('Booking {} already exists'.format(i))

        print('New pending booking count: {}'.format(new_pending_booking_count))

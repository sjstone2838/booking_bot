from django.core.management.base import BaseCommand

from tennis.models import BookingParameter
from tennis.models import Booking

import datetime

from .spotery_constants import LOCAL_TIME_ZONE
# from .spotery_constants import MAX_LOOKAHEAD_DAYS
# from .spotery_constants import CALENDAR_ADVANCE_TIME

'''
Notes on the crontab

Run this in the terminal:
$ crontab -e

Then put the following 1 line in the crontab file:
*/1 * * * * source ~/.virtualenvs/booking_bot/bin/activate && cd ~/code/booking_bot && python manage.py test_cron_command

This will run (1) activate a virtual_env called booking_bot, (2) cd to the root directory of the
Django project, and (3) run the command in tennis/management/commands/test_cron_command.py

Note that the following line silences crontab mail / output:
MAILTO="" # silences crontab mail

'''


class Command(BaseCommand):
    help = """python manage.py execute_pending_bookings
        Attempts to book all bookings with status=pending.
        """

    def handle(self, *args, **options):

        booking_parameters = BookingParameter.objects.filter(active=True)

        new_pending_booking_count = 0
        for i, bp in enumerate(booking_parameters):

            date_counter = datetime.datetime.now() + datetime.timedelta(days=1)

            advance_another_day = True
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

            print('Creating booking {}'.format(i))

            booking, created = Booking.objects.get_or_create(
                user=bp.user,
                court_location=bp.court_location,
                datetime=next_datetime_to_book,
            )

            if created:
                new_pending_booking_count += 1

        print('New pending booking count: {}'.format(new_pending_booking_count))

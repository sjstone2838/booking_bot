from django.core.management.base import BaseCommand

from django.core.mail import EmailMessage
from django.utils import timezone

from django.contrib.auth.models import User
from tennis.models import Booking

import pytz
import datetime as dt

pacific = pytz.timezone('US/Pacific')


class Command(BaseCommand):
    help = """python manage.py summarize_bookings
        Sends an email to all superusers about bookings.
        """

    def handle(self, *args, **options):
        superuser_emails = [u.email for u in User.objects.filter(is_superuser=True)]

        now = timezone.now()

        t1 = now + dt.timedelta(days=-1)
        t1_bookings = Booking.objects.filter(created__range=[t1, now])

        t7 = now + dt.timedelta(days=-7)
        t7_bookings = Booking.objects.filter(created__range=[t7, now])

        all_bookings = Booking.objects.filter(created__lte=now)

        user_stats = ''
        usernames = list(all_bookings.filter(status='Succeeded').values_list(
            'user__username', flat=True))
        for u in set(usernames):
            user_stats += ('<li>{}: {}</li>'.format(u, usernames.count(u)))

        court_stats = ''
        court_locations = list(all_bookings.filter(status='Succeeded').values_list(
            'court_location__name', flat=True))
        for cl in set(court_locations):
            court_stats += ('<li>{}: {}</li>'.format(cl, court_locations.count(cl)))

        email = EmailMessage(
            'Booking Bot Daily Summary',
            '''\
            <html>
              <head></head>
              <body>
                <p>Last 1 Day: {} successful bookings out of {} attempted ({:.0f}%).</p>
                <p>Last 7 Days: {} successful bookings out of {} attempted ({:.0f}%).</p>
                <p>All Time: {} successful bookings out of {} attempted ({:.0f}%).</p>
                <p>All Time successful bookings by user</p>
                <ol>{}</ol>
                <p>All Time successful bookings by court</p>
                <ol>{}</ol>
              </body>
            </html>
            '''.format(
                len(t1_bookings.filter(status='Succeeded')), len(t1_bookings), len(t1_bookings.filter(status='Succeeded')) / len(t1_bookings) * 100,

                len(t7_bookings.filter(status='Succeeded')), len(t7_bookings), len(t7_bookings.filter(status='Succeeded')) / len(t7_bookings) * 100,

                len(all_bookings.filter(status='Succeeded')), len(all_bookings), len(all_bookings.filter(status='Succeeded')) / len(all_bookings) * 100,

                user_stats,
                court_stats

            ),
            'bart.booking.2020@gmail.com',
            superuser_emails,
        )
        email.content_subtype = "html"
        email.send()

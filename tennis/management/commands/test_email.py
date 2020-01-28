from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage


class Command(BaseCommand):
    help = """send an email
        """

    def handle(self, *args, **options):

        email = EmailMessage(
            'Hello',
            'Body goes here',
            'bart.booking.2020@gmail.com',
            ['sjstone1987+test@gmail.com'],
            # ['bcc@example.com'],
            # reply_to=['another@example.com'],
            # headers={'Message-ID': 'foo'},
        )

        email.attach_file('media/booking_screenshots/booking_id_31.png')

        email.send()

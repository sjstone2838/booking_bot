from django.db import models

# from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# This will create a token for each new user automatically
from django.conf import settings
# from rest_framework.authtoken.models import Token


class TimeStampedModel(models.Model):
    # Provides self-updating 'created' and 'modified' fields.
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    spotery_login = models.CharField(max_length=200, blank=True, default='')
    spotery_password = models.CharField(max_length=200, blank=True, default='')

    def __unicode__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)


COURT_LOCATION_CHOICES = (
    ('Alice Marbles', 'Alice Marbles'),
    ('Crocker Amazon', 'Crocker Amazon'),
    ('Dolores Park', 'Dolores Park'),
    ('Hamilton Rec', 'Hamilton Rec'),
    ('Mountain Lake Park', 'Mountain Lake Park'),
)

class CourtLocation(TimeStampedModel):
	name = models.CharField(
        max_length=1000,
        choices=COURT_LOCATION_CHOICES,
        blank=False, default='Alice Marbles')


DAY_OF_WEEK_CHOICES = (
	('Monday', 'Monday'),
	('Tuesday', 'Tuesday'),
	('Wednesday', 'Wednesday'),
	('Thursday', 'Thursday'),
	('Friday', 'Friday'),
	('Saturday', 'Saturday'),
	('Sunday', 'Sunday'),
)

class BookingParameter(TimeStampedModel):
	user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name="booking_parameters")
	court_location = models.ForeignKey(CourtLocation, blank=False, on_delete=models.CASCADE, related_name="booking_parameters")
	day_of_week = models.CharField(
        max_length=1000,
        choices=DAY_OF_WEEK_CHOICES,
        blank=False, default='Saturday')
	time_of_day = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(24.0)],)
    

class Booking(TimeStampedModel):
	user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, related_name="bookings")
	court_location = models.ForeignKey(CourtLocation, blank=False, on_delete=models.CASCADE, related_name="bookings")
	court_number = models.CharField(max_length=100, blank=False, default='1')
	datetime = models.DateTimeField(blank=False)
	booking_number = models.CharField(max_length=100, blank=True)
	failure_reason = models.CharField(max_length=100, blank=True)














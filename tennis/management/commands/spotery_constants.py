import pytz


ROOT_URL = '''https://spotery.com/f/adf.task-flow?
adf.tfDoc=%2FWEB-INF%2Ftaskflows%2Ffacility%2Ftf-faci-detail.xml&
adf.tfId=tf-faci-detail&psOrgaAlias=sfrp'''

BOOKING_LENGTH_MINUTES = 90

# New dates become available in Spotery 7 days ahead at 8:00am US Pacific Time
# For example, on 2020-01-05 23:59 a user can book any spot on 2020-01-12
# But none of the spots on 2020-01-13. This holds until 2020-01-06 07:59
# and then at 2020-01-06 08:00 all spots on 2020-01-13 become available for
# booking.
LOCAL_TIME_ZONE = pytz.timezone('US/Pacific')
MAX_LOOKAHEAD_DAYS = 7
CALENDAR_ADVANCE_TIME = 8

# Expect this delay to be used in full on the happy path
# (hence name "long pole"). For example, this is used to check
# if a the modal warning that a user already has a booking pops up.
# Since it normally DOES NOT, we wait the full amount and then proceed.
LONG_POLE_WAIT = 2

# This delay will normally not take the full course, it is a maximum
# that will only be encountered if the server takes a long time to respond
DRIVER_WAIT = 10

from django.contrib import admin

from .models import UserProfile
from .models import CourtLocation
from .models import BookingParameter
from .models import Booking

def standard_fields(model):
    fields = []
    for field in model._meta.fields:
        if field.get_internal_type() != "ManyToManyField":
            fields.append(field.name)
    return tuple(fields)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = standard_fields(UserProfile)
    list_display_links = list_display
admin.site.register(UserProfile, UserProfileAdmin)

class CourtLocationAdmin(admin.ModelAdmin):
    list_display = standard_fields(CourtLocation)
    list_display_links = list_display
admin.site.register(CourtLocation, CourtLocationAdmin)

class BookingParameterAdmin(admin.ModelAdmin):
    list_display = standard_fields(BookingParameter)
    list_display_links = list_display
admin.site.register(BookingParameter, BookingParameterAdmin)

class BookingAdmin(admin.ModelAdmin):
    list_display = standard_fields(Booking)
    list_display_links = list_display
admin.site.register(Booking, BookingAdmin)
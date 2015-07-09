from django.contrib import admin
from .models import Schedule, TimeSlot

admin.site.register((Schedule, TimeSlot))

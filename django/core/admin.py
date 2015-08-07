from django.contrib import admin
from .models import (
    Address,
    Employee,
    Employer,
    Shift,
    ShiftType,
)

admin.site.register((
    Address,
    Employee,
    Employer,
    Shift,
    ShiftType,
))

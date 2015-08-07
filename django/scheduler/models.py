from django.conf import settings
from django.db import models
from core.fields import DayOfTheWeekField


class TimeSlot(models.Model):
    day = DayOfTheWeekField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    # since Django only supports naive time objects,
    # we have to store the time zone
    # TODO unnecessary?
    timezone = models.CharField(max_length=100, default=settings.TIME_ZONE)

    def __str__(self):
        return "%s to %s on %s" % (
            self.start_time, self.end_time, self.get_day_display()
        )


class Schedule(models.Model):
    time_slots = models.ManyToManyField(
        TimeSlot, verbose_name="list of time slots")

    employee = models.OneToOneField('core.Employee')

    def __str__(self):
        return "%s's schedule with %i time slots" % (
            self.employee,
            len(self.time_slots.all())
        )

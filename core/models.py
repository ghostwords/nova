from datetime import time
from django.db import models


class ShiftType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    rating_categories = models.ManyToManyField(
        'review.RatingCategory',
        # TODO
        #limit_choices_to={
        #    'category_type': RatingCategory.CATEGORY_TYPE_EMPLOYEE
        #},
        verbose_name="list of rating categories"
    )

    def __str__(self):
        return self.name


class Shift(models.Model):
    shift_type = models.ForeignKey(ShiftType)

    start_datetime = models.DateTimeField("start time")
    end_datetime = models.DateTimeField("end time")

    employer = models.ForeignKey('core.Employer')
    employee = models.ForeignKey('core.Employee', blank=True, null=True)

    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s %s shift" % (
            self.employer,
            self.start_datetime.date(),
            self.shift_type
        )


# TODO inherit from django.contrib.auth.models.User?
class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    # TODO phone number/texting

    shift_types = models.ManyToManyField(ShiftType)

    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def _get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)
    full_name = property(_get_full_name)

    def is_available(self, shift_type, start_dt, end_dt):
        if not self.shift_types.filter(id=shift_type.id):
            return False

        # is this employee already booked for this day/time?
        if Shift.objects.filter(
            employee=self,
            start_datetime__gte=start_dt,
            end_datetime__lte=end_dt
        ):
            return False

        def daytime_to_time(d):
            return time(d.hour, d.minute, d.second, d.microsecond, d.tzinfo)

        # get time slots for this day of the week
        for slot in self.schedule.time_slots.filter(day=start_dt.weekday()):
            start_time = daytime_to_time(start_dt)
            end_time = daytime_to_time(end_dt)

            if start_time >= slot.start_time and end_time <= slot.end_time:
                return True

        return False


# TODO inherit from django.contrib.auth.models.User?
class Employer(models.Model):
    name = models.CharField(max_length=100)
    address = models.OneToOneField('Address', null=True)

    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Address(models.Model):
    street = models.CharField(max_length=200)

    class Meta():
        verbose_name_plural = "addresses"

    def __str__(self):
        return self.street

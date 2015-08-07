from datetime import datetime, time
from django.test import TestCase
# TODO from freezegun import freeze_time
from pytz import timezone

from .fields import DayOfTheWeekField
from .models import Employee, Employer, Shift, ShiftType
from scheduler.models import Schedule, TimeSlot


# TODO https://github.com/vinta/awesome-python#testing
class EmployeeTests(TestCase):
    def setUp(self):
        tz_eastern = timezone('America/New_York')
        tz_pacific = timezone('America/Los_Angeles')

        self.datetimes = {
            'available_dst': (
                # Saturday July 4th 2015 4 PM to 5 PM EDT
                tz_eastern.localize(datetime(2015, 7, 4, 16)),
                tz_eastern.localize(datetime(2015, 7, 4, 17))
            ),
            'right_time_wrong_day': (
                # Sunday July 5th 2015 4 PM to 5 PM EDT
                tz_eastern.localize(datetime(2015, 7, 5, 16)),
                tz_eastern.localize(datetime(2015, 7, 5, 17))
            ),
            'right_day_right_time_wrong_tz': (
                # Saturday July 4th 2015 4 PM to 5 PM PDT
                tz_pacific.localize(datetime(2015, 7, 4, 16)),
                tz_pacific.localize(datetime(2015, 7, 4, 17))
            ),
            'available_non_dst': (
                # Saturday December 5th 2015 4 PM to 5 PM EST
                tz_eastern.localize(datetime(2015, 12, 5, 16)),
                tz_eastern.localize(datetime(2015, 12, 5, 17))
            ),
            'available_different_tz': (
                # Saturday July 4th 2015 1 PM to 2 PM PDT
                tz_pacific.localize(datetime(2015, 7, 4, 13)),
                tz_pacific.localize(datetime(2015, 7, 4, 14))
            )
        }

        # June 6th 2015 3:30 PM to 6:15 PM EDT
        shift_start_dt = tz_eastern.localize(datetime(2015, 6, 6, 15, 30))
        shift_end_dt = tz_eastern.localize(datetime(2015, 6, 6, 18, 15))

        # set up shift type(s)
        self.shift_type = ShiftType.objects.create(name='Daycare')

        # set up an employee
        self.employee = Employee.objects.create(
            first_name='Billy',
            last_name='Corgan'
        )
        self.employee.shift_types.add(self.shift_type)

        # available on Saturdays, 3:30 PM to 6:30 PM EDT (TODO EDT???)
        # TODO daylight saving time screws with time saving in db?
        time_slot = TimeSlot.objects.create(
            day=DayOfTheWeekField.DAY_OF_WEEK_SATURDAY,
            start_time=time(15, 30),
            end_time=time(18, 15),
            # TODO unnecessary?
            timezone=tz_eastern
        )
        schedule = Schedule.objects.create(
            employee=self.employee
        )
        schedule.time_slots.add(time_slot)

        # set up an employer
        self.employer = Employer.objects.create(name='Park Slope Food Coop')

        # set up a shift
        self.shift = Shift.objects.create(
            shift_type=self.shift_type,
            employer=self.employer,
            employee=self.employee,
            start_datetime=shift_start_dt,
            end_datetime=shift_end_dt
        )

    def test_is_available_dst(self):
        """
        is_available() should return True when the employee is available.
        """
        self.assertEqual(
            self.employee.is_available(
                self.shift_type,
                self.datetimes['available_dst'][0],
                self.datetimes['available_dst'][1]
            ),
            True
        )

    # TODO why isn't this failing?
    def test_is_available_non_dst(self):
        """
        is_available() should return True when the employee is available,
        regardless of daylight saving time.
        """
        self.assertEqual(
            self.employee.is_available(
                self.shift_type,
                self.datetimes['available_non_dst'][0],
                self.datetimes['available_non_dst'][1]
            ),
            True
        )

    def test_is_available_different_timezone(self):
        """
        is_available() should return True for a day and time that match across
        time zones.
        """
        self.assertEqual(
            self.employee.is_available(
                self.shift_type,
                self.datetimes['available_different_tz'][0],
                self.datetimes['available_different_tz'][1]
            ),
            True
        )

    def test_is_unavailable_on_wrong_day(self):
        """
        is_available() should return False when the desired times are for a
        different day of the week
        """
        self.assertEqual(
            self.employee.is_available(
                self.shift_type,
                self.datetimes['right_time_wrong_day'][0],
                self.datetimes['right_time_wrong_day'][1]
            ),
            False
        )

    def test_is_unavailable_for_wrong_shift(self):
        """
        is_available() should return False when the desired times are for a
        different day of the week
        """
        self.assertEqual(
            self.employee.is_available(
                ShiftType.objects.create(name="Dog walker"),
                self.datetimes['available_dst'][0],
                self.datetimes['available_dst'][1]
            ),
            False
        )

    def test_is_unavailable_when_booked(self):
        """
        is_available() should return False when the employee is already booked.
        """
        self.assertEqual(
            self.employee.is_available(
                self.shift_type,
                self.shift.start_datetime,
                self.shift.end_datetime
            ),
            False
        )

    def test_is_unavailable_when_day_and_times_match_in_a_tz_naive_way(self):
        """
        is_available() should return False when the day of the week and the
        times match, but only a timezone-naive way
        """
        self.assertEqual(
            self.employee.is_available(
                self.shift_type,
                self.datetimes['right_day_right_time_wrong_tz'][0],
                self.datetimes['right_day_right_time_wrong_tz'][1]
            ),
            False
        )

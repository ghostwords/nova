from django.db import models
from django.utils.translation import ugettext as _


class DayOfTheWeekField(models.PositiveSmallIntegerField):
    DAY_OF_WEEK_MONDAY = 0
    DAY_OF_WEEK_TUESDAY = 1
    DAY_OF_WEEK_WEDNESDAY = 2
    DAY_OF_WEEK_THURSDAY = 3
    DAY_OF_WEEK_FRIDAY = 4
    DAY_OF_WEEK_SATURDAY = 5
    DAY_OF_WEEK_SUNDAY = 6
    DAY_OF_WEEK_CHOICES = (
        (DAY_OF_WEEK_MONDAY, _('Monday')),
        (DAY_OF_WEEK_TUESDAY, _('Tuesday')),
        (DAY_OF_WEEK_WEDNESDAY, _('Wednesday')),
        (DAY_OF_WEEK_THURSDAY, _('Thursday')),
        (DAY_OF_WEEK_FRIDAY, _('Friday')),
        (DAY_OF_WEEK_SATURDAY, _('Saturday'),),
        (DAY_OF_WEEK_SUNDAY, _('Sunday'))
    )

    description = _("Day of the week enum")

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = self.DAY_OF_WEEK_CHOICES
        super(DayOfTheWeekField, self).__init__(*args, **kwargs)

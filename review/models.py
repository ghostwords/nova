from django.db import models
from django.utils import timezone


class RatingCategory(models.Model):
    CATEGORY_TYPE_EMPLOYEE = 1
    CATEGORY_TYPE_EMPLOYER = 2
    CATEGORY_TYPE_CHOICES = (
        (CATEGORY_TYPE_EMPLOYEE, 'employee'),
        (CATEGORY_TYPE_EMPLOYER, 'employer')
    )

    name = models.CharField(max_length=50, unique=True)
    text = models.CharField(max_length=200)
    category_type = models.PositiveSmallIntegerField(
        choices=CATEGORY_TYPE_CHOICES)

    class Meta():
        verbose_name_plural = "rating categories"

    def __str__(self):
        return "%s %s rating category" % (
            self.name, self.get_category_type_display())


class Review(models.Model):
    rating_category = models.ForeignKey(RatingCategory)
    score = models.PositiveSmallIntegerField()
    shift = models.ForeignKey(
        'core.Shift',
        limit_choices_to={
            'active': True,
            'employee': not None,
            'end_datetime__lte': timezone.now()
        }
    )

    def __str__(self):
        return "%s rated %i on %s for the %s" % (
            (
                self.shift.employee if self.rating_category.category_type ==
                RatingCategory.CATEGORY_TYPE_EMPLOYEE else self.shift.employer
            ),
            self.score,
            self.rating_category.name,
            self.shift
        )

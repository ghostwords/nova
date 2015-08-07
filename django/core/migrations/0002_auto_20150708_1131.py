# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shifttype',
            name='rating_categories',
            field=models.ManyToManyField(verbose_name='list of rating categories', to='review.RatingCategory'),
        ),
        migrations.AddField(
            model_name='shift',
            name='employee',
            field=models.ForeignKey(null=True, to='core.Employee', blank=True),
        ),
        migrations.AddField(
            model_name='shift',
            name='employer',
            field=models.ForeignKey(to='core.Employer'),
        ),
        migrations.AddField(
            model_name='shift',
            name='shift_type',
            field=models.ForeignKey(to='core.ShiftType'),
        ),
        migrations.AddField(
            model_name='employer',
            name='address',
            field=models.OneToOneField(null=True, to='core.Address'),
        ),
        migrations.AddField(
            model_name='employee',
            name='shift_types',
            field=models.ManyToManyField(to='core.ShiftType'),
        ),
    ]

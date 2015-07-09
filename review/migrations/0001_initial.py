# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RatingCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('text', models.CharField(max_length=200)),
                ('category_type', models.PositiveSmallIntegerField(choices=[(1, 'employee'), (2, 'employer')])),
            ],
            options={
                'verbose_name_plural': 'rating categories',
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('score', models.PositiveSmallIntegerField()),
                ('rating_category', models.ForeignKey(to='review.RatingCategory')),
                ('shift', models.ForeignKey(to='core.Shift')),
            ],
        ),
    ]

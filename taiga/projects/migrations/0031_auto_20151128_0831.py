# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0030_auto_20151128_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='total_activity_last_month',
            field=models.PositiveIntegerField(verbose_name='activity last month', default=0, db_index=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='total_activity_last_week',
            field=models.PositiveIntegerField(verbose_name='activity last week', default=0, db_index=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='total_activity_last_year',
            field=models.PositiveIntegerField(verbose_name='activity last year', default=0, db_index=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='total_fans_last_month',
            field=models.PositiveIntegerField(verbose_name='fans last month', default=0, db_index=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='total_fans_last_week',
            field=models.PositiveIntegerField(verbose_name='fans last week', default=0, db_index=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='total_fans_last_year',
            field=models.PositiveIntegerField(verbose_name='fans last year', default=0, db_index=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='totals_updated_datetime',
            field=models.DateTimeField(verbose_name='updated date time', db_index=True, auto_now_add=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import connection, migrations, models
from django.utils.timezone import utc
import datetime


def update_likes(apps, schema_editor):
    model = apps.get_model("projects", "Project")
    type = apps.get_model("contenttypes", "ContentType").objects.get_for_model(model)

    sql="""
        INSERT INTO likes_likes (
            content_type_id,
            object_id,
            count,
            count_week,
            count_month,
            count_year,
            updated_datetime)
        WITH
        totals AS (SELECT
        	object_id as project_id,
        	COUNT(likes_like.object_id) total,
        	MAX (created_date) updated_datetime
        	FROM likes_like
        	WHERE content_type_id = {type_id}
        	GROUP BY object_id),
        totals_week AS (SELECT
        	object_id as project_id,
        	COUNT(likes_like.object_id) total_week
        	FROM likes_like
        	WHERE content_type_id = {type_id}
        	AND likes_like.created_date > current_date - interval '7' day
        	GROUP BY object_id),
        totals_month AS (SELECT
        	object_id as project_id,
        	COUNT(likes_like.object_id) total_month
        	FROM likes_like
        	WHERE content_type_id = {type_id}
        	AND likes_like.created_date > current_date - interval '30' day
        	GROUP BY object_id),
        totals_year AS (SELECT
        	object_id as project_id,
        	COUNT(likes_like.object_id) total_year
        	FROM likes_like
        	WHERE content_type_id = {type_id}
        	AND likes_like.created_date > current_date - interval '365' day
        	GROUP BY object_id)
        SELECT
            '{type_id}',
        	totals.project_id,
        	COALESCE(total, 0) total,
        	COALESCE(total_week, 0) total_week,
        	COALESCE(total_month, 0) total_month,
        	COALESCE(total_year, 0) total_year,
        	totals.updated_datetime
        FROM totals
        LEFT JOIN totals_week ON totals.project_id = totals_week.project_id
        LEFT JOIN totals_month ON totals.project_id = totals_month.project_id
        LEFT JOIN totals_year ON totals.project_id = totals_year.project_id
    """.format(type_id=type.id, tbl=model._meta.db_table)

    cursor = connection.cursor()
    cursor.execute(sql)


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='likes',
            name='count_month',
            field=models.PositiveIntegerField(default=0, verbose_name='count last month'),
        ),
        migrations.AddField(
            model_name='likes',
            name='count_week',
            field=models.PositiveIntegerField(default=0, verbose_name='count last week'),
        ),
        migrations.AddField(
            model_name='likes',
            name='count_year',
            field=models.PositiveIntegerField(default=0, verbose_name='count last year'),
        ),
        migrations.AddField(
            model_name='likes',
            name='updated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 27, 7, 8, 9, 656814, tzinfo=utc), auto_now_add=True, verbose_name='updated date time'),
            preserve_default=False,
        ),
        migrations.RunPython(update_likes),
    ]

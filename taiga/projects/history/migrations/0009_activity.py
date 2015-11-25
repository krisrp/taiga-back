# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import connection, migrations, models

def create_activity(apps, schema_editor):
    sql="""
        INSERT INTO history_activity (
            project_id,
            count,
            count_week,
            count_month,
            count_year,
            updated_datetime)
        WITH
        totals AS (SELECT
        	split_part(timeline_timeline.namespace, ':', 2)::integer as project_id,
        	count(timeline_timeline.namespace) total,
        	MIN (created) updated_datetime
        	FROM timeline_timeline
        	WHERE namespace LIKE 'project:%'
        	GROUP BY namespace),
        totals_week AS (SELECT
        	split_part(timeline_timeline.namespace, ':', 2)::integer as project_id,
        	count(timeline_timeline.namespace) total_week
        	FROM timeline_timeline
        	WHERE namespace LIKE 'project:%'
        	AND timeline_timeline.created > current_date - interval '7' day
        	GROUP BY namespace),
        totals_month AS (SELECT
        	split_part(timeline_timeline.namespace, ':', 2)::integer as project_id,
        	count(timeline_timeline.namespace) total_month
        	FROM timeline_timeline
        	WHERE namespace LIKE 'project:%'
        	AND timeline_timeline.created > current_date - interval '30' day
        	GROUP BY namespace),
        totals_year AS (SELECT
        	split_part(timeline_timeline.namespace, ':', 2)::integer as project_id,
        	count(timeline_timeline.namespace) total_year
        	FROM timeline_timeline
        	WHERE namespace LIKE 'project:%'
        	AND timeline_timeline.created > current_date - interval '365' day
        	GROUP BY namespace)
        SELECT
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
    """
    cursor = connection.cursor()
    cursor.execute(sql)


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0029_project_is_looking_for_people'),
        ('history', '0008_auto_20150508_1028'),
        ('timeline', '0004_auto_20150603_1312'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('count', models.PositiveIntegerField(verbose_name='count', default=0)),
                ('count_week', models.PositiveIntegerField(verbose_name='count last week', default=0)),
                ('count_month', models.PositiveIntegerField(verbose_name='count last month', default=0)),
                ('count_year', models.PositiveIntegerField(verbose_name='count last year', default=0)),
                ('updated_datetime', models.DateTimeField(verbose_name='updated date time', auto_now_add=True)),
                ('project', models.ForeignKey(related_name='activity', to='projects.Project', verbose_name='project')),
            ],
            options={
                'verbose_name_plural': 'Activity',
                'verbose_name': 'Activity',
            },
        ),
        migrations.RunPython(create_activity),
    ]

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
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('count', models.PositiveIntegerField(default=0, verbose_name='count')),
                ('count_week', models.PositiveIntegerField(default=0, verbose_name='count last week')),
                ('count_month', models.PositiveIntegerField(default=0, verbose_name='count last month')),
                ('count_year', models.PositiveIntegerField(default=0, verbose_name='count last year')),
                ('updated_datetime', models.DateTimeField(auto_now_add=True, verbose_name='updated date time')),
                ('project', models.OneToOneField(verbose_name='project', related_name='activity', to='projects.Project')),
            ],
            options={
                'verbose_name': 'Activity',
                'verbose_name_plural': 'Activity',
            },
        ),
        migrations.RunPython(create_activity),
    ]

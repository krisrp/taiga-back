# Copyright (C) 2014-2015 Andrey Antukh <niwi@niwi.be>
# Copyright (C) 2014-2015 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014-2015 David Barragán <bameda@dbarragan.com>
# Copyright (C) 2014-2015 Anler Hernández <hello@anler.me>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from django.contrib.contenttypes import generic
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from datetime import timedelta

class Likes(models.Model):
    content_type = models.ForeignKey("contenttypes.ContentType")
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey("content_type", "object_id")
    count = models.PositiveIntegerField(null=False, blank=False, default=0, verbose_name=_("count"))
    count_week = models.PositiveIntegerField(null=False, blank=False, default=0,
                                             verbose_name=_("count last week"))

    count_month = models.PositiveIntegerField(null=False, blank=False, default=0,
                                              verbose_name=_("count last month"))

    count_year = models.PositiveIntegerField(null=False, blank=False, default=0,
                                             verbose_name=_("count last year"))

    updated_datetime = models.DateTimeField(null=False, blank=False, auto_now_add=True,
                                            verbose_name=_("updated date time"))

    class Meta:
        verbose_name = _("Likes")
        verbose_name_plural = _("Likes")
        unique_together = ("content_type", "object_id")

    @property
    def project(self):
        if hasattr(self.content_object, 'project'):
            return self.content_object.project
        return None

    def __str__(self):
        return self.count

    def refresh(self, save=True):
        now = timezone.now()
        self.updated_datetime = now

        qs = Like.objects.filter(content_type=self.content_type, object_id=self.object_id)
        self.count = qs.count()

        qs_week = qs.filter(created_date__gte=now-timedelta(days=7))
        self.count_week = qs_week.count()

        qs_month = qs.filter(created_date__gte=now-timedelta(days=30))
        self.count_month = qs_month.count()

        qs_year = qs.filter(created_date__gte=now-timedelta(days=365))
        self.count_year = qs_year.count()

        if save:
            self.save()


class Like(models.Model):
    content_type = models.ForeignKey("contenttypes.ContentType")
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey("content_type", "object_id")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False,
                             related_name="likes", verbose_name=_("user"))
    created_date = models.DateTimeField(null=False, blank=False, auto_now_add=True,
                                        verbose_name=_("created date"))

    class Meta:
        verbose_name = _("Like")
        verbose_name_plural = _("Likes")
        unique_together = ("content_type", "object_id", "user")

    @property
    def project(self):
        if hasattr(self.content_object, 'project'):
            return self.content_object.project
        return None

    def __str__(self):
        return self.user.get_full_name()

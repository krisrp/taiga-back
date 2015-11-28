# Copyright (C) 2014-2015 Andrey Antukh <niwi@niwi.be>
# Copyright (C) 2014-2015 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014-2015 David Barragán <bameda@dbarragan.com>
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

from taiga.base.api import serializers

from django.utils import timezone


class ActivityResourceSerializerMixin(serializers.ModelSerializer):
    pass
    """
    total_activity = serializers.SerializerMethodField("get_total_activity")
    total_activity_last_week = serializers.SerializerMethodField("get_total_activity_last_week")
    total_activity_last_month = serializers.SerializerMethodField("get_total_activity_last_month")
    total_activity_last_year = serializers.SerializerMethodField("get_total_activity_last_year")

    def get_total_activity(self, obj):
        if not hasattr(obj, "activity"):
            return 0

        return obj.activity.count

    def _get_total_activity_last_days(self, obj, days, attribute):
        if not hasattr(obj, "activity"):
            return 0

        now = timezone.now()
        if (now - obj.activity.updated_datetime).days > days:
            return 0

        return getattr(obj.activity, attribute)

    def get_total_activity_last_week(self, obj):
        return self._get_total_activity_last_days(obj, 7, "count_week")

    def get_total_activity_last_month(self, obj):
        return self._get_total_activity_last_days(obj, 30, "count_month")

    def get_total_activity_last_year(self, obj):
        return self._get_total_activity_last_days(obj, 365, "count_year")
    """

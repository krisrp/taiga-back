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


class FanResourceSerializerMixin(serializers.ModelSerializer):
    is_fan = serializers.SerializerMethodField("get_is_fan")
    #total_fans = serializers.SerializerMethodField("get_total_fans")
    #total_fans_last_week = serializers.SerializerMethodField("get_total_fans_last_week")
    #total_fans_last_month = serializers.SerializerMethodField("get_total_fans_last_month")
    #total_fans_last_year = serializers.SerializerMethodField("get_total_fans_last_year")

    def get_is_fan(self, obj):
        if "request" in self.context:
            user = self.context["request"].user
            return user.is_fan(obj)

        return False
    """
    def get_total_fans(self, obj):
        return obj.likes.count

    def _get_total_fans_last_days(self, obj, days, attribute):
        now = timezone.now()

        if obj.likes.count() == 0:
            return 0

        likes = obj.likes.get()
        if (now - likes.updated_datetime).days > days:
            return 0

        return getattr(likes, attribute)

    def get_total_fans_last_week(self, obj):
        return self._get_total_fans_last_days(obj, 7, "count_week")

    def get_total_fans_last_month(self, obj):
        return self._get_total_fans_last_days(obj, 30, "count_month")

    def get_total_fans_last_year(self, obj):
        return self._get_total_fans_last_days(obj, 365, "count_year")
    """

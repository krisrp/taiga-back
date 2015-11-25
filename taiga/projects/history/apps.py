# Copyright (C) 2014-2015 Andrey Antukh <niwi@niwi.be>
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

from django.apps import AppConfig
from django.db.models import signals

from . import signals as handlers
from taiga.projects.history.models import HistoryEntry


def connect_history_signals():
    signals.post_save.connect(handlers.on_new_history_entry, sender=HistoryEntry, dispatch_uid="history")


def disconnect_history_signals():
    signals.post_save.disconnect(sender=HistoryEntry, dispatch_uid="history")


class HistoryAppConfig(AppConfig):
    name = "taiga.projects.history"
    verbose_name = "History App Config"

    def ready(self):
        connect_history_signals()

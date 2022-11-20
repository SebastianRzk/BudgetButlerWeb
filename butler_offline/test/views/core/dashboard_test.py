import unittest

from butler_offline.core import time
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.database_util import untaint_database
from butler_offline.core import file_system
from butler_offline.views.core import dashboard
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler
from datetime import date


class TestUebersicht(unittest.TestCase):

    def set_up(self):
        file_system.INSTANCE = FileSystemStub()
        persisted_state.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_init_withEmptyDatabase(self):
        self.set_up()
        dashboard.index(GetRequest())

    def test_should_return_month_list(self):
        self.set_up()
        feburary = date(2018, 2, 13)
        time.stub_today_with(feburary)

        result = dashboard.index(GetRequest())

        assert result[
                   'zusammenfassung_monatsliste'] == "['August', 'September', 'Oktober', 'November', 'Dezember', 'Januar', 'Februar']"

    def test_withEntry_shouldReturnGermanDate(self):
        self.set_up()
        db = persisted_state.database_instance()
        time.stub_today_with(date(2019, 2, 17))
        db.einzelbuchungen.add(date(2019, 2, 16), 'eine einnahme kategorie', 'some name', 10)
        untaint_database(database=db)


        result = dashboard.index(GetRequest())
        print(result['ausgaben_des_aktuellen_monats'])
        assert result['ausgaben_des_aktuellen_monats'] == [
            {'index': 0, 'Datum': '16.02.2019', 'Name': 'some name', 'Kategorie': 'eine einnahme kategorie',
             'Wert': '10,00', 'Dynamisch': False, 'Tags': []}]

import unittest

from butler_offline.test.RequestStubs import GetRequest
from butler_offline.test.FileSystemStub import FileSystemStub
from butler_offline.core import FileSystem
from butler_offline.views import dashboard
from butler_offline.viewcore import viewcore
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.converter import datum_to_german
from datetime import datetime
from datetime import date

class TestUebersicht(unittest.TestCase):

    def set_up(self):
        FileSystem.INSTANCE = FileSystemStub()
        viewcore.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_init_withEmptyDatabase(self):
        self.set_up()
        dashboard.index(GetRequest())

    def test_should_return_month_list(self):
        self.set_up()
        feburary = date(2018,2,13)
        viewcore.stub_today_with(feburary)

        result = dashboard.index(GetRequest())

        assert result['zusammenfassung_monatsliste'] == "['August', 'September', 'Oktober', 'November', 'Dezember', 'Januar', 'Februar']"


    def test_withEntry_shouldReturnGermanDate(self):
        self.set_up()
        db = viewcore.database_instance()
        today = datetime.now().date()
        db.einzelbuchungen.add(today, 'eine einnahme kategorie', 'some name', 10)

        result = dashboard.index(GetRequest())
        print(result['ausgaben_des_aktuellen_monats'])
        assert result['ausgaben_des_aktuellen_monats'] == [{'index': 0, 'Datum': datum_to_german(today), 'Name': 'some name', 'Kategorie': 'eine einnahme kategorie', 'Wert': '10,00', 'Dynamisch': False, 'Tags': []}]

import unittest

from mysite.test.RequestStubs import GetRequest
from mysite.test.FileSystemStub import FileSystemStub
from mysite.core import FileSystem
from mysite.views import dashboard
from mysite.viewcore import viewcore
from mysite.viewcore import request_handler
from datetime import datetime
from mysite.viewcore.converter import datum_to_german

class TestUebersicht(unittest.TestCase):

    def set_up(self):
        FileSystem.INSTANCE = FileSystemStub()
        viewcore.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_init_withEmptyDatabase(self):
        self.set_up()
        dashboard.index(GetRequest())

    def test_withEntry_shouldReturnGermanDate(self):
        self.set_up()
        db = viewcore.database_instance()
        today = datetime.now().date()
        db.einzelbuchungen.add(today, 'eine einnahme kategorie', 'some name', 10)

        result = dashboard.index(GetRequest())
        assert result['ausgaben_des_aktuellen_monats'][0]['datum'] == datum_to_german(today)

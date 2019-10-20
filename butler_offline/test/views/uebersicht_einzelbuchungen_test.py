import unittest

from butler_offline.test.FileSystemStub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.test.RequestStubs import PostRequest
from butler_offline.core import FileSystem
from butler_offline.views import uebersicht_einzelbuchungen
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore import request_handler


class TestUebersicht(unittest.TestCase):

    def set_up(self):
        FileSystem.INSTANCE = FileSystemStub()
        viewcore.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_transaction_id_should_be_in_context(self):
        self.set_up()
        context = uebersicht_einzelbuchungen.index(GetRequest())
        assert 'ID' in context

    def add_test_data(self):
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('12.12.2012'), 'Test einnahme kategorie', 'test einnahme name', 100)
        einzelbuchungen.add(datum('13.12.2012'), 'Test ausgabe kategorie', 'test azsgabe name', -100)

    def test_init_withEmptyDatabase(self):
        self.set_up()
        uebersicht_einzelbuchungen.index(GetRequest())

    def test_withEntry_shouldReturnGermanDateFormat(self):
        self.set_up()
        self.add_test_data()
        result = uebersicht_einzelbuchungen.index(GetRequest())
        assert result['alles']['2012.12'][0]['datum'] == '12.12.2012'

    def test_init_filledDatabase(self):
        self.set_up()
        self.add_test_data()
        uebersicht_einzelbuchungen.index(GetRequest())

    def test_getRequest_withEinnahme_shouldReturnEditLinkOfEinnahme(self):
        self.set_up()
        self.add_test_data()
        result = uebersicht_einzelbuchungen.index(GetRequest())
        item = result['alles']['2012.12'][0]
        assert float(item['wert']) > 0
        assert item['link'] == 'addeinnahme'
        item = result['alles']['2012.12'][1]
        assert float(item['wert']) < 0
        assert item['link'] == 'addausgabe'

    def test_delete(self):
        self.set_up()
        self.add_test_data()
        uebersicht_einzelbuchungen.index(PostRequest({'action': 'delete', 'delete_index': '1'}))
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        assert einzelbuchungen.select().sum() == 100

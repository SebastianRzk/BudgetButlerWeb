import unittest

from mysite.test.FileSystemStub import FileSystemStub
from mysite.test.RequestStubs import GetRequest
from mysite.test.RequestStubs import PostRequest
from mysite.core import FileSystem
from mysite.views import uebersicht_einzelbuchungen
from mysite.viewcore import viewcore
from mysite.viewcore.converter import datum_from_german as datum
from mysite.viewcore import request_handler

class TestUebersicht(unittest.TestCase):

    def set_up(self):
        FileSystem.INSTANCE = FileSystemStub()
        viewcore.DATABASE_INSTANCE = None
        request_handler.stub_me()

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
        uebersicht_einzelbuchungen.index(PostRequest({'action':'delete', 'delete_index':'1'}))
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        assert einzelbuchungen.select().sum() == 100

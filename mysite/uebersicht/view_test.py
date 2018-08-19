import unittest

from test import DBManagerStub
from test.RequestStubs import GetRequest
from test.RequestStubs import PostRequest
from core.DatabaseModule import Database
from uebersicht import views
from viewcore import viewcore
from viewcore.converter import datum_from_german as datum
from viewcore import request_handler

class TestUebersicht(unittest.TestCase):

    def set_up(self):
        DBManagerStub.setup_db_for_test()
        request_handler.stub_me()

    def add_test_data(self):
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum("12.12.2012"), "Test einnahme kategorie", "test einnahme name", 100)
        einzelbuchungen.add(datum("13.12.2012"), "Test ausgabe kategorie", "test azsgabe name", -100)


    def test_init_withEmptyDatabase(self):
        self.set_up()
        views.index(GetRequest())

    def test_init_filledDatabase(self):
        self.set_up()
        self.add_test_data()
        views.index(GetRequest())


    def test_getRequest_withEinnahme_shouldReturnEditLinkOfEinnahme(self):
        self.set_up()
        self.add_test_data()
        result = views.index(GetRequest())
        item = result['alles']['2012.12'][0]
        assert float(item['wert']) > 0
        assert item['link'] == "addeinnahme"
        item = result['alles']['2012.12'][1]
        assert float(item['wert']) < 0
        assert item['link'] == "addeinzelbuchung"


    def test_delete(self):
        self.set_up()
        self.add_test_data()
        views.index(PostRequest({'action':'delete', 'delete_index':'1'}))
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        assert einzelbuchungen.select().sum() == 100

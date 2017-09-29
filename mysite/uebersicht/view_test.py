import unittest

from test import DBManagerStub
from adddauerauftrag.view_test import PostRequest, GetRequest
from core.DatabaseModule import Database
from uebersicht import views
import viewcore
from viewcore.converter import datum


class TestUebersicht(unittest.TestCase):

    def set_up(self):
        DBManagerStub.setup_db_for_test()

    def add_test_data(self):
        einzelbuchungen = viewcore.viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum("12/12/2012"), "Test einnahme kategorie", "test einnahme name", 100)
        einzelbuchungen.add(datum("13/12/2012"), "Test ausgabe kategorie", "test azsgabe name", -100)


    def test_init_withEmptyDatabase(self):
        self.set_up()
        views.handle_request(GetRequest())

    def test_init_filledDatabase(self):
        self.set_up()
        self.add_test_data()
        views.handle_request(GetRequest())


    def test_getRequest_withEinnahme_shouldReturnEditLinkOfEinnahme(self):
        self.set_up()
        self.add_test_data()
        result = views.handle_request(GetRequest())
        print("#################################################")
        print(result['alles']['2012.12'][0])
        item = result['alles']['2012.12'][0]
        assert float(item['wert']) > 0
        assert item['link'] == "addeinnahme"
        item = result['alles']['2012.12'][1]
        assert float(item['wert']) < 0
        assert item['link'] == "addeinzelbuchung"


    def test_delete(self):
        self.set_up()
        self.add_test_data()
        result = views.handle_request(PostRequest({'action':'delete', 'delete_index':'1'}))
        einzelbuchungen = viewcore.viewcore.database_instance().einzelbuchungen
        assert einzelbuchungen.select().sum() == 100

if __name__ == '__main__':
    unittest.main()

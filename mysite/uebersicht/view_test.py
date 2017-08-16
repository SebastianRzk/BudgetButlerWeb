# Create your tests here.
'''
'''

import unittest

from core.DatabaseModule import Database
from uebersicht import views
import viewcore
from viewcore.converter import datum


class TestUebersicht(unittest.TestCase):

    def set_up(self):
        print("create new database")
        viewcore.viewcore.DATABASE_INSTANCE = Database("test")
        viewcore.viewcore.DATABASES = ['test']
        viewcore.viewcore.TEST = True

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
        (_, _, _, _, wert, _, link) = result['alles']['2012.12'][0]
        assert float(wert) > 0
        assert link == "addeinnahme"
        (_, _, _, _, wert, _, link) = result['alles']['2012.12'][1]
        assert float(wert) < 0
        assert link == "addeinzelbuchung"


if __name__ == '__main__':
    unittest.main()

class GetRequest():
    method = "GET"

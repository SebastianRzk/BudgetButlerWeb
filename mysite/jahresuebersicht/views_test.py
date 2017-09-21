import os
import sys
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from adddauerauftrag.view_test import PostRequest
from core.DatabaseModule import Database
from jahresuebersicht import views
import viewcore
from viewcore.converter import datum



class Jahresuebersicht(unittest.TestCase):

    def setUp(self):
        print("create new database")
        self.testdb = Database("test")
        viewcore.viewcore.DATABASE_INSTANCE = self.testdb
        viewcore.viewcore.DATABASES = ['test']
        viewcore.viewcore.TEST = True

    def test_init(self):
        self.setUp()
        views.handle_request(GetRequest())


    def teste_contextValues_withSingleEinnahmeAndSingleAusgabe(self):
        self.setUp()
        self.testdb.einzelbuchungen.add(datum('10/10/2010'), 'some kategorie', 'some name', -100)
        self.testdb.einzelbuchungen.add(datum('10/10/2010'), 'eine einnahme kategorie', 'some name', 10)

        result_context = views.handle_request(PostRequest({'date':'2010', 'mode':''}))

        assert result_context['zusammenfassung_ausgaben'] == [['some kategorie', '-100.00', 'checked', 'f56954']]
        assert result_context['zusammenfassung_einnahmen'] == [['eine einnahme kategorie', '10.00', 'checked', '3c8dbc']]



    def teste_contextValues_withMutlibleEinnahmeAndAusgabe(self):
        self.setUp()
        self.testdb.einzelbuchungen.add(datum('10/10/2010'), 'some kategorie', 'some name', -100)
        self.testdb.einzelbuchungen.add(datum('10/10/2010'), 'eine einnahme kategorie', 'some name', 10)
        self.testdb.einzelbuchungen.add(datum('10/10/2010'), 'some kategorie', 'some name', -100)
        self.testdb.einzelbuchungen.add(datum('10/10/2010'), 'eine einnahme kategorie', 'some name', 10)
        self.testdb.einzelbuchungen.add(datum('10/10/2010'), 'some kategorie2', 'some name', -100)
        self.testdb.einzelbuchungen.add(datum('10/10/2010'), 'eine einnahme kategorie2', 'some name', 10)

        result_context = views.handle_request(PostRequest({'date':'2010', 'mode':''}))

        assert result_context['zusammenfassung_ausgaben'] == [['some kategorie', '-200.00', 'checked', '00a65a'], ['some kategorie2', '-100.00', 'checked', '00c0ef']]
        assert result_context['zusammenfassung_einnahmen'] == [['eine einnahme kategorie', '20.00', 'checked', '3c8dbc'], ['eine einnahme kategorie2', '10.00', 'checked', 'f56954']]


class GetRequest():
    method = "GET"
    POST = {}

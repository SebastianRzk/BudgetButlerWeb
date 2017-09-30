import os
import sys
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from test import DBManagerStub
from test.RequestStubs import GetRequest
from test.RequestStubs import PostRequest
from core.DatabaseModule import Database
from jahresuebersicht import views
from viewcore import viewcore
from viewcore.converter import datum



class Jahresuebersicht(unittest.TestCase):

    def set_up(self):
        DBManagerStub.setup_db_for_test()

    def test_init(self):
        self.set_up()
        views.handle_request(GetRequest())


    def teste_contextValues_withSingleEinnahmeAndSingleAusgabe(self):
        self.set_up()
        db = viewcore.database_instance()
        db.einzelbuchungen.add(datum('10/10/2010'), 'some kategorie', 'some name', -100)
        db.einzelbuchungen.add(datum('10/10/2010'), 'eine einnahme kategorie', 'some name', 10)

        result_context = views.handle_request(PostRequest({'date':'2010', 'mode':''}))

        assert result_context['zusammenfassung_ausgaben'] == [['some kategorie', '-100.00', 'checked', 'f56954']]
        assert result_context['zusammenfassung_einnahmen'] == [['eine einnahme kategorie', '10.00', 'checked', '3c8dbc']]



    def teste_contextValues_withMutlibleEinnahmeAndAusgabe(self):
        self.set_up()
        db = viewcore.database_instance()
        db.einzelbuchungen.add(datum('10/10/2010'), 'some kategorie', 'some name', -100)
        db.einzelbuchungen.add(datum('10/10/2010'), 'eine einnahme kategorie', 'some name', 10)
        db.einzelbuchungen.add(datum('10/10/2010'), 'some kategorie', 'some name', -100)
        db.einzelbuchungen.add(datum('10/10/2010'), 'eine einnahme kategorie', 'some name', 10)
        db.einzelbuchungen.add(datum('10/10/2010'), 'some kategorie2', 'some name', -100)
        db.einzelbuchungen.add(datum('10/10/2010'), 'eine einnahme kategorie2', 'some name', 10)

        result_context = views.handle_request(PostRequest({'date':'2010', 'mode':''}))

        assert result_context['zusammenfassung_ausgaben'] == [['some kategorie', '-200.00', 'checked', '00a65a'], ['some kategorie2', '-100.00', 'checked', '00c0ef']]
        assert result_context['zusammenfassung_einnahmen'] == [['eine einnahme kategorie', '20.00', 'checked', '3c8dbc'], ['eine einnahme kategorie2', '10.00', 'checked', 'f56954']]


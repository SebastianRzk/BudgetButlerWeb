import unittest

from mysite.test.FileSystemStub import FileSystemStub
from mysite.test.RequestStubs import GetRequest
from mysite.test.RequestStubs import PostRequest
from mysite.core import FileSystem
from mysite.views import uebersicht_jahr
from mysite.viewcore import viewcore
from mysite.viewcore.converter import datum_from_german as datum
from mysite.viewcore import request_handler



class Jahresuebersicht(unittest.TestCase):

    def set_up(self):
        FileSystem.INSTANCE = FileSystemStub()
        viewcore.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        uebersicht_jahr.index(GetRequest())


    def teste_contextValues_withSingleEinnahmeAndSingleAusgabe(self):
        self.set_up()
        db = viewcore.database_instance()
        db.einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)
        db.einzelbuchungen.add(datum('10.10.2010'), 'eine einnahme kategorie', 'some name', 10)

        result_context = uebersicht_jahr.index(PostRequest({'date':'2010', 'mode':''}))

        assert result_context['zusammenfassung_ausgaben'] == [['some kategorie', '-100.00', 'f56954']]
        assert result_context['zusammenfassung_einnahmen'] == [['eine einnahme kategorie', '10.00', '3c8dbc']]
        assert 'eine einnahme kategorie' in result_context['einnahmen']
        assert result_context['einnahmen']['eine einnahme kategorie']['values'] == '[10.00]'



    def teste_contextValues_withMutlibleEinnahmeAndAusgabe(self):
        self.set_up()
        db = viewcore.database_instance()
        db.einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)
        db.einzelbuchungen.add(datum('10.10.2010'), 'eine einnahme kategorie', 'some name', 10)
        db.einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)
        db.einzelbuchungen.add(datum('10.10.2010'), 'eine einnahme kategorie', 'some name', 10)
        db.einzelbuchungen.add(datum('10.10.2010'), 'some kategorie2', 'some name', -100)
        db.einzelbuchungen.add(datum('10.10.2010'), 'eine einnahme kategorie2', 'some name', 10)

        result_context = uebersicht_jahr.index(PostRequest({'date':'2010', 'mode':''}))

        assert result_context['zusammenfassung_ausgaben'] == [['some kategorie', '-200.00', '00a65a'], ['some kategorie2', '-100.00', '00c0ef']]
        assert result_context['zusammenfassung_einnahmen'] == [['eine einnahme kategorie', '20.00', '3c8dbc'], ['eine einnahme kategorie2', '10.00', 'f56954']]
        assert result_context['buchungen'][0]['wert'] == ['30.00']
        assert result_context['buchungen'][1]['wert'] == ['300.00']

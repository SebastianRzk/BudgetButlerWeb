import unittest

from butler_offline.viewcore.state import persisted_state
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest, PostRequest
from butler_offline.test.database_util import untaint_database
from butler_offline.core import file_system
from butler_offline.views.einzelbuchungen import uebersicht_jahr
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore import request_handler



class Jahresuebersicht(unittest.TestCase):

    def set_up(self):
        file_system.INSTANCE = FileSystemStub()
        persisted_state.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        uebersicht_jahr.index(GetRequest())


    def teste_contextValues_withSingleEinnahmeAndSingleAusgabe(self):
        self.set_up()
        db = persisted_state.database_instance()
        db.einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)
        db.einzelbuchungen.add(datum('10.10.2010'), 'eine einnahme kategorie', 'some name', 10)
        untaint_database(database=db)

        result_context = uebersicht_jahr.index(PostRequest({'date': '2010', 'mode': ''}))

        assert result_context['zusammenfassung_ausgaben'] == [['some kategorie', '-100.00', '#f56954']]
        assert result_context['zusammenfassung_einnahmen'] == [['eine einnahme kategorie', '10.00', '#3c8dbc']]
        assert 'eine einnahme kategorie' in result_context['einnahmen']
        assert result_context['einnahmen']['eine einnahme kategorie']['values'] == '[10.00]'
        assert result_context['jahre'] == [2010]
        assert result_context['selected_date'] == 2010

    def teste_contextValues_withMutlibleEinnahmeAndAusgabe(self):
        self.set_up()
        db = persisted_state.database_instance()
        db.einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)
        db.einzelbuchungen.add(datum('10.10.2010'), 'eine einnahme kategorie', 'some name', 10)
        db.einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)
        db.einzelbuchungen.add(datum('10.10.2010'), 'eine einnahme kategorie', 'some name', 10)
        db.einzelbuchungen.add(datum('10.10.2010'), 'some kategorie2', 'some name', -100)
        db.einzelbuchungen.add(datum('10.10.2010'), 'eine einnahme kategorie2', 'some name', 10)
        untaint_database(database=db)

        result_context = uebersicht_jahr.index(PostRequest({'date': '2010', 'mode': ''}))

        assert result_context['zusammenfassung_ausgaben'] == [['some kategorie', '-200.00', '#00a65a'], ['some kategorie2', '-100.00', '#00c0ef']]
        assert result_context['zusammenfassung_einnahmen'] == [['eine einnahme kategorie', '20.00', '#3c8dbc'], ['eine einnahme kategorie2', '10.00', '#f56954']]
        assert result_context['buchungen'][0]['wert'] == ['30.00']
        assert result_context['buchungen'][1]['wert'] == ['300.00']

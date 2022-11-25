import unittest

from butler_offline.viewcore.state import persisted_state
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest, PostRequest
from butler_offline.test.database_util import untaint_database
from butler_offline.views.einzelbuchungen import uebersicht_monat
from butler_offline.core import file_system
from butler_offline.viewcore.context import get_error_message
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore import request_handler


class Monatsuebersicht(unittest.TestCase):

    def set_up(self):
        file_system.INSTANCE = FileSystemStub()
        persisted_state.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        uebersicht_monat.index(GetRequest())

    def test_withNoData_shouldGenerateErrorPage(self):
        self.set_up()
        context = uebersicht_monat.index(GetRequest())
        assert get_error_message(context)

    def teste_mitMehrAusgabenAlsEinnahmen(self):
        self.set_up()
        db = persisted_state.database_instance()
        db.einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)
        db.einzelbuchungen.add(datum('10.10.2010'), 'eine einnahme kategorie', 'some name', 10)
        untaint_database(database=db)

        result_context = uebersicht_monat.index(PostRequest({'date': '2010_10'}))

        assert result_context['gesamt'] == '-100.00'
        assert result_context['gesamt_einnahmen'] == '10.00'

        assert result_context['einnahmen'] == [('eine einnahme kategorie', '10.00', '#3c8dbc')]
        assert result_context['einnahmen_labels'] == ['eine einnahme kategorie']
        assert result_context['einnahmen_data'] == ['10.00']

        assert result_context['ausgaben'] == [('some kategorie', '-100.00', '#f56954')]
        assert result_context['ausgaben_labels'] == ['some kategorie']
        assert result_context['ausgaben_data'] == ['100.00']

    def teste_gleitkommadarstellung_monats_zusammenfassung(self):
        self.set_up()
        db = persisted_state.database_instance()
        db.einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)
        untaint_database(database=db)

        result_context = uebersicht_monat.index(PostRequest({'date': '2010_10'}))

        assert result_context['wert_uebersicht_gruppe_1'] == '0.00'
        assert result_context['wert_uebersicht_gruppe_2'] == '100.00'

    def teste_gleitkommadarstellung_jahress_zusammenfassung(self):
        self.set_up()
        db = persisted_state.database_instance()
        db.einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)
        untaint_database(database=db)

        result_context = uebersicht_monat.index(PostRequest({'date': '2010_10'}))

        assert result_context['wert_uebersicht_jahr_gruppe_1'] == '0.00'
        assert result_context['wert_uebersicht_jahr_gruppe_2'] == '100.00'


    def teste_mitUnterschiedlichenMonaten_shouldSelectNeusterMonat(self):
        self.set_up()
        db = persisted_state.database_instance()
        db.einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)
        db.einzelbuchungen.add(datum('10.10.2011'), 'eine einnahme kategorie', 'some name', 10)
        untaint_database(database=db)

        result_context = uebersicht_monat.index(GetRequest())

        assert result_context['selected_date'] == '2011_10'

    def teste_datumsdarstellung_einzelbuchungsliste(self):
        self.set_up()
        db = persisted_state.database_instance()
        db.einzelbuchungen.add(datum('10.10.2011'), 'eine einnahme kategorie', 'some name', 10)
        untaint_database(database=db)

        result_context = uebersicht_monat.index(GetRequest())

        assert result_context['zusammenfassung'][0][0] == '10.10.2011'


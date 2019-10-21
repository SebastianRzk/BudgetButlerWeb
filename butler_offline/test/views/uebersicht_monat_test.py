import unittest

from butler_offline.core import time
from butler_offline.test.FileSystemStub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.test.RequestStubs import PostRequest
from butler_offline.views import uebersicht_monat
from butler_offline.core import FileSystem
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore import request_handler


class Monatsuebersicht(unittest.TestCase):

    def set_up(self):
        FileSystem.INSTANCE = FileSystemStub()
        viewcore.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        uebersicht_monat.index(GetRequest())

    def test_withNoData_shouldGenerateErrorPage(self):
        self.set_up()
        context = uebersicht_monat.index(GetRequest())
        assert context['%Errortext']

    def teste_mitMehrAusgabenAlsEinnahmen(self):
        self.set_up()
        db = viewcore.database_instance()
        db.einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)
        db.einzelbuchungen.add(datum('10.10.2010'), 'eine einnahme kategorie', 'some name', 10)

        result_context = uebersicht_monat.index(PostRequest({'date':'2010_10'}))

        assert result_context['gesamt'] == '-100.00'
        assert result_context['gesamt_einnahmen'] == '10.00'

        assert result_context['einnahmen'] == [('eine einnahme kategorie', '10.00', '3c8dbc')]
        assert result_context['einnahmen_labels'] == ['eine einnahme kategorie']
        assert result_context['einnahmen_data'] == ['10.00']

        assert result_context['ausgaben'] == [('some kategorie', '-100.00', 'f56954')]
        assert result_context['ausgaben_labels'] == ['some kategorie']
        assert result_context['ausgaben_data'] == ['100.00']

    def teste_gleitkommadarstellung_monats_zusammenfassung(self):
        self.set_up()
        db = viewcore.database_instance()
        db.einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)

        result_context = uebersicht_monat.index(PostRequest({'date':'2010_10'}))

        assert result_context['wert_uebersicht_gruppe_1'] == '0.00'
        assert result_context['wert_uebersicht_gruppe_2'] == '100.00'

    def teste_gleitkommadarstellung_jahress_zusammenfassung(self):
        self.set_up()
        db = viewcore.database_instance()
        db.einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)

        result_context = uebersicht_monat.index(PostRequest({'date':'2010_10'}))

        assert result_context['wert_uebersicht_jahr_gruppe_1'] == '0.00'
        assert result_context['wert_uebersicht_jahr_gruppe_2'] == '100.00'


    def teste_mitUnterschiedlichenMonaten_shouldSelectNeusterMonat(self):
        self.set_up()
        db = viewcore.database_instance()
        db.einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)
        db.einzelbuchungen.add(datum('10.10.2011'), 'eine einnahme kategorie', 'some name', 10)

        result_context = uebersicht_monat.index(GetRequest())

        assert result_context['selected_date'] == '2011_10'

    def teste_datumsdarstellung_einzelbuchungsliste(self):
        self.set_up()
        db = viewcore.database_instance()
        db.einzelbuchungen.add(datum('10.10.2011'), 'eine einnahme kategorie', 'some name', 10)

        result_context = uebersicht_monat.index(GetRequest())

        assert result_context['zusammenfassung'][0][0] == '10.10.2011'


class Abrechnung(unittest.TestCase):
    def set_up(self):
        FileSystem.INSTANCE = FileSystemStub()
        viewcore.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        uebersicht_monat.abrechnen(GetRequest())

    def test_get_should_return_actual_month(self    ):
        self.set_up()
        time.stub_today_with(datum('10.10.2012'))
        context = uebersicht_monat.abrechnen(GetRequest())
        time.reset_viewcore_stubs()

        assert context['element_titel'] == 'Abrechnung vom 10/2012'

    def test_post_with_date_should_return_date(self):
        self.set_up()
        context = uebersicht_monat.abrechnen(PostRequest({'date': '2011_9'}))
        assert context['element_titel'] == 'Abrechnung vom 9/2011'

    def test_optionen(self):
        self.set_up()

        context = uebersicht_monat.abrechnen(PostRequest({'date': '2011_9', 'einnahmen': 'einnahmen'}))
        self.contains_only_header(context['abrechnungstext'], '---Einnahmen---')
        context = uebersicht_monat.abrechnen(PostRequest({'date': '2011_9', 'ausgaben': 'ausgaben'}))
        self.contains_only_header(context['abrechnungstext'], '---Ausgaben---')
        context = uebersicht_monat.abrechnen(PostRequest({'date': '2011_9', 'zusammenfassung_einnahmen': 'zusammenfassung_einnahmen'}))
        self.contains_only_header(context['abrechnungstext'], 'Einnahmen ')
        context = uebersicht_monat.abrechnen(PostRequest({'date': '2011_9', 'zusammenfassung_ausgaben': 'zusammenfassung_ausgaben'}))
        self.contains_only_header(context['abrechnungstext'], 'Ausgaben ')

    def contains_only_header(self, report, header):
        all_headers = ['---Einnahmen---', 'Einnahmen ', '---Ausgaben---', 'Ausgaben ']
        for h in all_headers:
            if h != header:
                assert h not in report
            else:
                assert h in report



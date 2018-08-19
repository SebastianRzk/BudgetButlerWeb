import os
import sys
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from test import DBManagerStub
from test.RequestStubs import GetRequest
from test.RequestStubs import PostRequest
from monatsuebersicht import views
from viewcore import viewcore
from viewcore.converter import datum_from_german as datum
from viewcore import request_handler


class Monatsuebersicht(unittest.TestCase):

    def set_up(self):
        DBManagerStub.setup_db_for_test()
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        views.index(GetRequest())

    def test_withNoData_shouldGenerateErrorPage(self):
        self.set_up()
        context = views.index(GetRequest())
        assert context['%Errortext']

    def teste_mitMehtAusgabenAlsEinnahmen(self):
        self.set_up()
        db = viewcore.database_instance()
        db.einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)
        db.einzelbuchungen.add(datum('10.10.2010'), 'eine einnahme kategorie', 'some name', 10)

        result_context = views.index(PostRequest({'date':'2010_10'}))

        assert result_context['gesamt'] == '-100.00'
        assert result_context['gesamt_einnahmen'] == '10.00'

        assert result_context['einnahmen'] == [('eine einnahme kategorie', '10.00', '3c8dbc')]
        assert result_context['einnahmen_labels'] == ['eine einnahme kategorie']
        assert result_context['einnahmen_data'] == ['10.00']

        assert result_context['ausgaben'] == [('some kategorie', '-100.00', 'f56954')]
        assert result_context['ausgaben_labels'] == ['some kategorie']
        assert result_context['ausgaben_data'] == ['100.00']

    def teste_mitUnterschiedlichenMonaten_shouldSelectNeusterMonat(self):
        self.set_up()
        db = viewcore.database_instance()
        db.einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)
        db.einzelbuchungen.add(datum('10.10.2011'), 'eine einnahme kategorie', 'some name', 10)

        result_context = views.index(GetRequest())

        assert result_context['selected_date'] == '2011_10'


class Abrechnung(unittest.TestCase):
    def set_up(self):
        DBManagerStub.setup_db_for_test()
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        views.abrechnen(GetRequest())

    def test_get_should_return_actual_month(self    ):
        self.set_up()
        viewcore.stub_today_with(datum('10.10.2012'))
        context = views.abrechnen(GetRequest())
        viewcore.reset_viewcore_stubs()

        assert context['element_titel'] == 'Abrechnung vom 10/2012'

    def test_post_with_date_should_return_date(self):
        self.set_up()
        context = views.abrechnen(PostRequest({'date': '2011_9'}))
        assert context['element_titel'] == 'Abrechnung vom 9/2011'

    def test_optionen(self):
        self.set_up()

        context = views.abrechnen(PostRequest({'date': '2011_9', 'content': ['einnahmen']}))
        self.contains_only_header(context['abrechnungstext'], '---Einnahmen---')
        context = views.abrechnen(PostRequest({'date': '2011_9', 'content': ['ausgaben']}))
        self.contains_only_header(context['abrechnungstext'], '---Ausgaben---')
        context = views.abrechnen(PostRequest({'date': '2011_9', 'content': ['zusammenfassung_einnahmen']}))
        self.contains_only_header(context['abrechnungstext'], 'Einnahmen ')
        context = views.abrechnen(PostRequest({'date': '2011_9', 'content': ['zusammenfassung_ausgaben']}))
        self.contains_only_header(context['abrechnungstext'], 'Ausgaben ')

    def contains_only_header(self, report, header):
        all_headers = ['---Einnahmen---', 'Einnahmen ', '---Ausgaben---', 'Ausgaben ']
        for h in all_headers:
            if h != header:
                assert h not in report
            else:
                assert h in report



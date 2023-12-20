from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.test.request_stubs import GetRequest, PostRequest
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore.renderhelper import Betrag, BetragListe
from butler_offline.views.einzelbuchungen import uebersicht_monat
from butler_offline.viewcore.requirements import KEINE_BUCHUNGEN_ERFASST_MESSAGE
from butler_offline.test.test import assert_keine_message_set, assert_info_message_keine_buchungen_erfasst_in_context


def test_init():
    uebersicht_monat.handle_request(
        GetRequest(),
        uebersicht_monat.UebersichtMonatContext(einzelbuchungen=Einzelbuchungen())
    )


def test__with_no_data__should_show_info_box():
    context = uebersicht_monat.handle_request(
        GetRequest(),
        uebersicht_monat.UebersichtMonatContext(einzelbuchungen=Einzelbuchungen())
    )
    assert_info_message_keine_buchungen_erfasst_in_context(result=context)


def test_with_data__should_not_show_info_box():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(
        datum=datum('01.01.2023'),
        kategorie='test',
        wert=123,
        name='test',
        dynamisch=False
    )
    context = uebersicht_monat.handle_request(
        GetRequest(),
        uebersicht_monat.UebersichtMonatContext(einzelbuchungen=einzelbuchungen)
    )
    assert_keine_message_set(result=context)


def teste__mit_mehr_ausgaben_als_einnahmen():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)
    einzelbuchungen.add(datum('10.10.2010'), 'eine einnahme kategorie', 'some name', 10)

    result_context = uebersicht_monat.handle_request(
        PostRequest({'date': '2010_10'}),
        context=uebersicht_monat.UebersichtMonatContext(einzelbuchungen=einzelbuchungen)
    )

    assert result_context.get('gesamt') == Betrag(-100)
    assert result_context.get('gesamt_einnahmen') == Betrag(10)

    assert result_context.get('einnahmen') == [
        {
            'kategorie': 'eine einnahme kategorie',
            'wert': Betrag(10.00),
            'color': '#3c8dbc'
        }
    ]
    assert result_context.get('einnahmen_labels') == ['eine einnahme kategorie']
    assert result_context.get('einnahmen_data') == BetragListe([Betrag(10)])

    assert result_context.get('ausgaben') == [
        {
            'kategorie': 'some kategorie',
            'wert': Betrag(-100.00),
            'color': '#f56954'
        }]
    assert result_context.get('ausgaben_labels') == ['some kategorie']
    assert result_context.get('ausgaben_data') == BetragListe([Betrag(100)])


def teste_gleitkommadarstellung_monats_zusammenfassung():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)

    result_context = uebersicht_monat.handle_request(
        PostRequest({'date': '2010_10'}),
        uebersicht_monat.UebersichtMonatContext(einzelbuchungen=einzelbuchungen)
    )

    assert result_context.get('wert_uebersicht_gruppe_1') == Betrag(0)
    assert result_context.get('wert_uebersicht_gruppe_2') == Betrag(100)


def teste_gleitkommadarstellung_jahres_zusammenfassung():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)

    result_context = uebersicht_monat.handle_request(
        PostRequest({'date': '2010_10'}),
        context=uebersicht_monat.UebersichtMonatContext(einzelbuchungen=einzelbuchungen)
    )

    assert result_context.get('wert_uebersicht_jahr_gruppe_1') == Betrag(0)
    assert result_context.get('wert_uebersicht_jahr_gruppe_2') == Betrag(100)


def teste__mit_unterschiedlichen_monaten__should_select_neuster_monat():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)
    einzelbuchungen.add(datum('10.10.2011'), 'eine einnahme kategorie', 'some name', 10)

    result_context = uebersicht_monat.handle_request(
        GetRequest(),
        context=uebersicht_monat.UebersichtMonatContext(einzelbuchungen=einzelbuchungen)
    )

    assert result_context.get('selected_date') == '2011_10'


def teste_datumsdarstellung_einzelbuchungsliste():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('10.10.2011'), 'eine einnahme kategorie', 'some name', 10)

    result_context = uebersicht_monat.handle_request(
        GetRequest(),
        context=uebersicht_monat.UebersichtMonatContext(einzelbuchungen=einzelbuchungen)
    )

    assert result_context.get('zusammenfassung')[0][0] == '10.10.2011'


def test_index_should_be_secured_by_request_handler():
    def index():
        uebersicht_monat.index(GetRequest())

    result = run_in_mocked_handler(index_handle=index)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['einzelbuchungen/uebersicht_monat.html']


def test_context_should_not_be_transactional():
    result = uebersicht_monat. \
        handle_request(GetRequest(), context=uebersicht_monat.UebersichtMonatContext(Einzelbuchungen()))
    assert not result.is_transactional()

from butler_offline.test.RequestStubs import GetRequest, PostRequest
from butler_offline.views.einzelbuchungen import uebersicht_monat
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler


def test_init():
    uebersicht_monat.handle_request(
        GetRequest(),
        uebersicht_monat.UebersichtMonatContext(einzelbuchungen=Einzelbuchungen())
    )


def test__with_no_data__should_generate_error_page():
    context = uebersicht_monat.handle_request(
        GetRequest(),
        uebersicht_monat.UebersichtMonatContext(einzelbuchungen=Einzelbuchungen())
    )
    assert context.is_error()
    assert context.error_text() == 'Keine Ausgaben erfasst'


def teste__mit_mehr_ausgaben_als_einnahmen():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)
    einzelbuchungen.add(datum('10.10.2010'), 'eine einnahme kategorie', 'some name', 10)

    result_context = uebersicht_monat.handle_request(
        PostRequest({'date': '2010_10'}),
        context=uebersicht_monat.UebersichtMonatContext(einzelbuchungen=einzelbuchungen)
    )

    assert result_context.get('gesamt') == '-100.00'
    assert result_context.get('gesamt_einnahmen') == '10.00'

    assert result_context.get('einnahmen') == [('eine einnahme kategorie', '10.00', '#3c8dbc')]
    assert result_context.get('einnahmen_labels') == ['eine einnahme kategorie']
    assert result_context.get('einnahmen_data') == ['10.00']

    assert result_context.get('ausgaben') == [('some kategorie', '-100.00', '#f56954')]
    assert result_context.get('ausgaben_labels') == ['some kategorie']
    assert result_context.get('ausgaben_data') == ['100.00']


def teste_gleitkommadarstellung_monats_zusammenfassung():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)

    result_context = uebersicht_monat.handle_request(
        PostRequest({'date': '2010_10'}),
        uebersicht_monat.UebersichtMonatContext(einzelbuchungen=einzelbuchungen)
    )

    assert result_context.get('wert_uebersicht_gruppe_1') == '0.00'
    assert result_context.get('wert_uebersicht_gruppe_2') == '100.00'


def teste_gleitkommadarstellung_jahres_zusammenfassung():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)

    result_context = uebersicht_monat.handle_request(
        PostRequest({'date': '2010_10'}),
        context=uebersicht_monat.UebersichtMonatContext(einzelbuchungen=einzelbuchungen)
    )

    assert result_context.get('wert_uebersicht_jahr_gruppe_1') == '0.00'
    assert result_context.get('wert_uebersicht_jahr_gruppe_2') == '100.00'


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
    result = uebersicht_monat.\
        handle_request(GetRequest(), context=uebersicht_monat.UebersichtMonatContext(Einzelbuchungen()))
    assert not result.is_transactional()

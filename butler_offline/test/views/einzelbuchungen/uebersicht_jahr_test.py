from butler_offline.test.RequestStubs import GetRequest, PostRequest
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.views.einzelbuchungen import uebersicht_jahr
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler


def test_init():
    uebersicht_jahr.handle_request(GetRequest(), context=uebersicht_jahr.UebersichtJahrContext(Einzelbuchungen()))


def teste__context_values__with_single_einnahme_and_single_ausgabe():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)
    einzelbuchungen.add(datum('10.10.2010'), 'eine einnahme kategorie', 'some name', 10)

    result_context = uebersicht_jahr.handle_request(
        PostRequest({'date': '2010', 'mode': ''}),
        uebersicht_jahr.UebersichtJahrContext(einzelbuchungen=einzelbuchungen)
    )

    assert result_context.get('zusammenfassung_ausgaben') == [['some kategorie', '-100.00', '#f56954']]
    assert result_context.get('zusammenfassung_einnahmen') == [['eine einnahme kategorie', '10.00', '#3c8dbc']]
    assert 'eine einnahme kategorie' in result_context.get('einnahmen')
    assert result_context.get('einnahmen')['eine einnahme kategorie']['values'] == '[10.00]'
    assert result_context.get('jahre') == [2010]
    assert result_context.get('selected_date') == 2010


def teste__context_values__with_mutlible_einnahme_and_ausgabe():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)
    einzelbuchungen.add(datum('10.10.2010'), 'eine einnahme kategorie', 'some name', 10)
    einzelbuchungen.add(datum('10.10.2010'), 'some kategorie', 'some name', -100)
    einzelbuchungen.add(datum('10.10.2010'), 'eine einnahme kategorie', 'some name', 10)
    einzelbuchungen.add(datum('10.10.2010'), 'some kategorie2', 'some name', -100)
    einzelbuchungen.add(datum('10.10.2010'), 'eine einnahme kategorie2', 'some name', 10)

    result_context = uebersicht_jahr.handle_request(
        PostRequest({'date': '2010', 'mode': ''}),
        uebersicht_jahr.UebersichtJahrContext(einzelbuchungen=einzelbuchungen)
    )

    assert result_context.get('zusammenfassung_ausgaben') == [['some kategorie', '-200.00', '#00a65a'],
                                                              ['some kategorie2', '-100.00', '#00c0ef']]
    assert result_context.get('zusammenfassung_einnahmen') == [['eine einnahme kategorie', '20.00', '#3c8dbc'],
                                                               ['eine einnahme kategorie2', '10.00', '#f56954']]
    assert result_context.get('buchungen')[0]['wert'] == ['30.00']
    assert result_context.get('buchungen')[1]['wert'] == ['300.00']


def test_index_should_be_secured_by_request_handler():
    def index():
        uebersicht_jahr.index(GetRequest())

    result = run_in_mocked_handler(index_handle=index)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['einzelbuchungen/uebersicht_jahr.html']


def test_context_should_not_be_transactional():
    result = uebersicht_jahr.\
        handle_request(GetRequest(), context=uebersicht_jahr.UebersichtJahrContext(Einzelbuchungen()))
    assert not result.is_transactional()

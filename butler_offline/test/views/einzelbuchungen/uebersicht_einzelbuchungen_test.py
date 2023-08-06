from butler_offline.test.RequestStubs import GetRequest,  VersionedPostRequest
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.views.einzelbuchungen import uebersicht_einzelbuchungen
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler


def test_transaction_id_should_be_in_context():
    context = uebersicht_einzelbuchungen.handle_request(
        GetRequest(),
        context=uebersicht_einzelbuchungen.UebersichtEinzelbuchungenContext(
            einzelbuchungen=Einzelbuchungen()
        ))
    assert context.is_transactional()


def get_test_data():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('12.12.2012'), 'Test einnahme kategorie', 'test einnahme name', 100)
    einzelbuchungen.add(datum('13.12.2012'), 'Test ausgabe kategorie', 'test azsgabe name', -100)
    return uebersicht_einzelbuchungen.UebersichtEinzelbuchungenContext(einzelbuchungen=einzelbuchungen)


def test_init_with_empty_database():
    uebersicht_einzelbuchungen.handle_request(
        GetRequest(),
      context=uebersicht_einzelbuchungen.UebersichtEinzelbuchungenContext(einzelbuchungen=Einzelbuchungen()))


def test_init_filled_database():
    uebersicht_einzelbuchungen.handle_request(
        GetRequest(),
        context=get_test_data())


def test_with_entry_should_return_german_date_format():
    result = uebersicht_einzelbuchungen.handle_request(GetRequest(), context=get_test_data())
    assert result.get('alles')['2012.12'][0]['datum'] == '12.12.2012'


def test_get_request_with_einnahme_should_return_edit_link_of_einnahme():
    result = uebersicht_einzelbuchungen.handle_request(GetRequest(), get_test_data())
    item = result.get('alles')['2012.12'][0]
    assert item['wert'] == '100,00'
    assert item['link'] == 'addeinnahme'
    item = result.get('alles')['2012.12'][1]
    assert item['wert'] == '-100,00'
    assert item['link'] == 'addausgabe'


def test_get_request_should_filter_year():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('1.12.2011'), 'please dont show me', 'please dont show me', 999)
    einzelbuchungen.add(datum('12.12.2012'), 'Test einnahme kategorie', 'test einnahme name', 100)
    einzelbuchungen.add(datum('1.12.2013'), 'please dont show me', 'please dont show me', 999)

    result = uebersicht_einzelbuchungen.handle_request(
        GetRequest(),
        uebersicht_einzelbuchungen.UebersichtEinzelbuchungenContext(einzelbuchungen=einzelbuchungen)
    )
    assert len(result.get('alles')) == 1
    assert result.get('jahre') == [2013, 2012, 2011]
    assert result.get('selected_date') == 2013


def test_delete():
    context = get_test_data()
    uebersicht_einzelbuchungen.handle_request(
        VersionedPostRequest({'action': 'delete', 'delete_index': '1'}),
        context=context
    )
    assert context.einzelbuchungen().select().sum() == 100


def test_index_should_be_secured_by_request_handler():
    def index():
        uebersicht_einzelbuchungen.index(GetRequest())

    result = run_in_mocked_handler(index_handle=index)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['einzelbuchungen/uebersicht.html']

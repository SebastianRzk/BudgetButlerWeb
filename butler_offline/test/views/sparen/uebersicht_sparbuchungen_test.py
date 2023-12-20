from butler_offline.core.database.sparen.sparbuchungen import Sparbuchungen
from butler_offline.test.request_stubs import GetRequest
from butler_offline.test.request_stubs import PostRequest
from butler_offline.test.test import assert_info_message_keine_sparbuchungen_erfasst_in_context, \
    assert_keine_message_set
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore.renderhelper import Betrag
from butler_offline.viewcore.state import persisted_state
from butler_offline.views.sparen import uebersicht_sparbuchungen


def generate_base_context(sparbuchungen: Sparbuchungen = Sparbuchungen()):
    return uebersicht_sparbuchungen.UebersichtSparbuchungenContext(
        sparbuchungen=sparbuchungen
    )


def generate_testdata_context():
    sparbuchungen = Sparbuchungen()
    sparbuchungen.add(datum('12.12.2012'), 'sparen', 100, sparbuchungen.TYP_MANUELLER_AUFTRAG, 'Demokonto')
    sparbuchungen.add(datum('13.12.2012'), 'auszahlen', -100, sparbuchungen.TYP_MANUELLER_AUFTRAG, 'Demokonto')
    return generate_base_context(
        sparbuchungen=sparbuchungen
    )


def test_transaction_id_should_be_in_context():
    context = uebersicht_sparbuchungen.handle_request(
        request=GetRequest(),
        context=generate_base_context()
    )
    assert context.is_ok()
    assert context.is_transactional()


def test_init_with_empty_database_should_show_info_message():
    result = uebersicht_sparbuchungen.handle_request(GetRequest(), generate_base_context())
    assert result.is_ok()
    assert_info_message_keine_sparbuchungen_erfasst_in_context(result=result)


def test_init_filled_database_should_show_no_message():
    result = uebersicht_sparbuchungen.handle_request(
        request=GetRequest(),
        context=generate_testdata_context()
    )
    assert result.is_ok()
    assert_keine_message_set(result=result)


def test_with_entry_should_return_german_date_format():
    result = uebersicht_sparbuchungen.handle_request(GetRequest(), generate_testdata_context())
    assert result.get('alles')['2012.12'][0]['datum'] == '12.12.2012'


def test_get_request__with_einnahme__should_return_edit_link_of_einnahme():
    result = uebersicht_sparbuchungen.handle_request(
        request=GetRequest(),
        context=generate_testdata_context()
    )
    first_item = result.get('alles')['2012.12'][0]
    assert first_item['wert'] == Betrag(100)
    assert first_item['name'] == 'sparen'
    assert first_item['typ'] == persisted_state.database_instance().sparbuchungen.TYP_MANUELLER_AUFTRAG
    assert first_item['konto'] == 'Demokonto'

    second_item = result.get('alles')['2012.12'][0]
    assert second_item['wert'] == Betrag(100)
    assert second_item['name'] == 'sparen'
    assert second_item['typ'] == persisted_state.database_instance().sparbuchungen.TYP_MANUELLER_AUFTRAG
    assert second_item['konto'] == 'Demokonto'


def test_delete():
    context = generate_testdata_context()
    uebersicht_sparbuchungen.handle_request(
        request=PostRequest({'action': 'delete', 'delete_index': '1'}),
        context=context
    )
    sparbuchungen = context.sparbuchungen()
    assert sparbuchungen.select().count() == 1
    assert sparbuchungen.get(0) == {'Datum': datum('12.12.2012'),
                                    'Dynamisch': False,
                                    'Konto': 'Demokonto',
                                    'Name': 'sparen',
                                    'Typ': 'Manueller Auftrag',
                                    'Wert': 100,
                                    'index': 0}


def test_index_should_be_secured_by_request_handler():
    def index():
        uebersicht_sparbuchungen.index(GetRequest())

    result = run_in_mocked_handler(index_handle=index)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['sparen/uebersicht_sparbuchungen.html']

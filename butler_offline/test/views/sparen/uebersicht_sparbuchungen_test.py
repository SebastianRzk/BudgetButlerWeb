from butler_offline.viewcore.state import persisted_state
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.test.RequestStubs import VersionedPostRequest, PostRequest
from butler_offline.test.database_util import untaint_database
from butler_offline.core import file_system
from butler_offline.views.sparen import uebersicht_sparbuchungen
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore import request_handler


def set_up():
    file_system.INSTANCE = FileSystemStub()
    persisted_state.DATABASE_INSTANCE = None
    request_handler.stub_me()


def test_transaction_id_should_be_in_context():
    set_up()
    context = uebersicht_sparbuchungen.index(GetRequest())
    assert 'ID' in context


def add_test_data():
    sparbuchungen = persisted_state.database_instance().sparbuchungen
    sparbuchungen.add(datum('12.12.2012'), 'sparen', 100, sparbuchungen.TYP_MANUELLER_AUFTRAG, 'Demokonto')
    sparbuchungen.add(datum('13.12.2012'), 'auszahlen', -100, sparbuchungen.TYP_MANUELLER_AUFTRAG, 'Demokonto')
    untaint_database(database=persisted_state.database_instance())


def test_init_with_empty_database():
    set_up()
    uebersicht_sparbuchungen.index(GetRequest())


def test_with_entry_should_return_german_date_format():
    set_up()
    add_test_data()
    result = uebersicht_sparbuchungen.index(GetRequest())
    assert result['alles']['2012.12'][0]['datum'] == '12.12.2012'


def test_init_filled_database():
    set_up()
    add_test_data()
    uebersicht_sparbuchungen.index(GetRequest())


def test_get_request__with_einnahme__should_return_edit_link_of_einnahme():
    set_up()
    add_test_data()
    result = uebersicht_sparbuchungen.index(GetRequest())
    first_item = result['alles']['2012.12'][0]
    assert first_item['wert'] == '100,00'
    assert first_item['name'] == 'sparen'
    assert first_item['typ'] == persisted_state.database_instance().sparbuchungen.TYP_MANUELLER_AUFTRAG
    assert first_item['konto'] == 'Demokonto'

    second_item = result['alles']['2012.12'][0]
    assert second_item['wert'] == '100,00'
    assert second_item['name'] == 'sparen'
    assert second_item['typ'] == persisted_state.database_instance().sparbuchungen.TYP_MANUELLER_AUFTRAG
    assert second_item['konto'] == 'Demokonto'


def test_delete():
    set_up()
    add_test_data()
    uebersicht_sparbuchungen.index(VersionedPostRequest({'action': 'delete', 'delete_index': '1'}))
    sparbuchungen = persisted_state.database_instance().sparbuchungen
    assert sparbuchungen.select().count() == 1
    assert sparbuchungen.get(0) == {'Datum': datum('12.12.2012'),
                                    'Dynamisch': False,
                                    'Konto': 'Demokonto',
                                    'Name': 'sparen',
                                    'Typ': 'Manueller Auftrag',
                                    'Wert': 100,
                                    'index': 0}


def test_delete_should_only_fire_once():
    set_up()
    add_test_data()
    next_id = persisted_state.current_database_version()

    assert persisted_state.database_instance().sparbuchungen.select().count() == 2
    uebersicht_sparbuchungen.index(PostRequest({'action': 'delete', 'delete_index': '1', 'ID': next_id}))
    assert persisted_state.database_instance().sparbuchungen.select().count() == 1
    uebersicht_sparbuchungen.index(PostRequest({'action': 'delete', 'delete_index': '1', 'ID': next_id}))
    assert persisted_state.database_instance().sparbuchungen.select().count() == 1

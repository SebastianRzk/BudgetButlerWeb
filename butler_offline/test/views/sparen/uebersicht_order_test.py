from butler_offline.viewcore.state import persisted_state
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.test.RequestStubs import VersionedPostRequest, PostRequest
from butler_offline.test.database_util import untaint_database
from butler_offline.core import file_system
from butler_offline.views.sparen import uebersicht_order
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.converter import datum_from_german


def set_up():
    file_system.INSTANCE = FileSystemStub()
    persisted_state.DATABASE_INSTANCE = None
    request_handler.stub_me()


def test_transaction_id_should_be_in_context():
    set_up()
    context = uebersicht_order.index(GetRequest())
    assert 'ID' in context


def add_test_data():
    depotwerte = persisted_state.database_instance().depotwerte
    depotwerte.add(name='depotwert1', isin='isin1', typ=depotwerte.TYP_ETF)

    order = persisted_state.database_instance().order
    order.add(datum_from_german('01.01.2020'), '1name', '1konto', 'isin1', 100)
    order.add(datum_from_german('02.02.2020'), '2name', '2konto', 'isin1', -200)

    untaint_database(database=persisted_state.database_instance())


def test_should_list_order():
    set_up()
    add_test_data()

    result = uebersicht_order.index(GetRequest())

    assert result['order'] == [
        {'Datum': '01.01.2020',
         'Depotwert': 'depotwert1 (isin1)',
         'Konto': '1konto',
         'Name': '1name',
         'Typ': 'Kauf',
         'index': 0,
         'Wert': '100,00',
         'Dynamisch': False},
        {'Datum': '02.02.2020',
         'Depotwert': 'depotwert1 (isin1)',
         'Konto': '2konto',
         'Name': '2name',
         'Typ': 'Verkauf',
         'index': 1,
         'Wert': '200,00',
         'Dynamisch': False},
    ]

def test_init_withEmptyDatabase():
    set_up()
    uebersicht_order.index(GetRequest())


def test_init_filledDatabase():
    set_up()
    add_test_data()
    uebersicht_order.index(GetRequest())


def test_delete():
    set_up()
    add_test_data()
    uebersicht_order.index(VersionedPostRequest({'action': 'delete', 'delete_index': '1'}))
    order = persisted_state.database_instance().order
    assert len(order.content) == 1
    assert order.get(0) == {
        'Datum': datum_from_german('01.01.2020'),
        'Depotwert': 'isin1',
        'Konto': '1konto',
        'Name': '1name',
        'Wert': 100,
        'index': 0,
        'Dynamisch': False
        }


def test_delete_should_only_fire_once():
    set_up()
    add_test_data()
    next_id = persisted_state.current_database_version()

    assert len(persisted_state.database_instance().order.content) == 2
    uebersicht_order.index(PostRequest({'action': 'delete', 'delete_index': '1', 'ID': next_id}))
    assert len(persisted_state.database_instance().order.content) == 1
    uebersicht_order.index(PostRequest({'action': 'delete', 'delete_index': '1', 'ID': next_id}))
    assert len(persisted_state.database_instance().order.content) == 1

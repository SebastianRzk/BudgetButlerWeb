from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest, VersionedPostRequest
from butler_offline.core import file_system
from butler_offline.views.sparen import uebersicht_orderdauerauftrag
from butler_offline.test.database_util import untaint_database
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore import request_handler


def set_up():
    file_system.INSTANCE = FileSystemStub()
    persisted_state.DATABASE_INSTANCE = None
    request_handler.stub_me()


def test_init():
    set_up()
    uebersicht_orderdauerauftrag.index(GetRequest())


def test_transaction_id_should_be_in_context():
    set_up()
    context = uebersicht_orderdauerauftrag.index(GetRequest())
    assert 'ID' in context


def test_delete():
    set_up()
    orderdauerauftrag = persisted_state.database_instance().orderdauerauftrag

    orderdauerauftrag.add(datum('01.01.2011'), datum('01.01.2011'), 'monatlich', '1name', '1konto ', '1depotwert', 11)
    orderdauerauftrag.add(datum('01.01.2011'), datum('01.01.2011'), 'monatlich', '2name', '1konto ', '1depotwert', 11)

    untaint_database(persisted_state.database_instance())

    uebersicht_orderdauerauftrag.index(VersionedPostRequest({'action': 'delete', 'delete_index': '1'}))

    assert len(orderdauerauftrag.content) == 1
    assert orderdauerauftrag.content.Name.tolist() == ['1name']


def test_german_datum():
    set_up()
    orderdauerauftrag = persisted_state.database_instance().orderdauerauftrag
    orderdauerauftrag.add(datum('01.01.2011'), datum('01.01.2011'), 'monatlich', '1name', '1konto ', '1depotwert', 11)
    untaint_database(database=persisted_state.database_instance())

    result = uebersicht_orderdauerauftrag.index(GetRequest())

    result_dauerauftrag = result['dauerauftraege']['Vergangene  Daueraufträge'][0]
    assert result_dauerauftrag['Startdatum'] == '01.01.2011'
    assert result_dauerauftrag['Endedatum'] == '01.01.2011'

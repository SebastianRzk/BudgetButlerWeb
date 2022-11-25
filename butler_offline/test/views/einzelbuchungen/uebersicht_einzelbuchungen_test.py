from butler_offline.viewcore.state import persisted_state
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest,  VersionedPostRequest, PostRequest
from butler_offline.test.database_util import untaint_database
from butler_offline.core import file_system
from butler_offline.views.einzelbuchungen import uebersicht_einzelbuchungen
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore import request_handler
from butler_offline.core import time

def set_up():
    file_system.INSTANCE = FileSystemStub()
    persisted_state.DATABASE_INSTANCE = None
    request_handler.stub_me()
    time.stub_today_with(datum("30.12.2012"))

def test_transaction_id_should_be_in_context():
    set_up()
    context = uebersicht_einzelbuchungen.index(GetRequest())
    assert 'ID' in context


def add_test_data():
    einzelbuchungen = persisted_state.database_instance().einzelbuchungen
    einzelbuchungen.add(datum('12.12.2012'), 'Test einnahme kategorie', 'test einnahme name', 100)
    einzelbuchungen.add(datum('13.12.2012'), 'Test ausgabe kategorie', 'test azsgabe name', -100)
    untaint_database(database=persisted_state.database_instance())


def test_init_withEmptyDatabase():
    set_up()
    uebersicht_einzelbuchungen.index(GetRequest())


def test_withEntry_shouldReturnGermanDateFormat():
    set_up()
    add_test_data()
    result = uebersicht_einzelbuchungen.index(GetRequest())
    assert result['alles']['2012.12'][0]['datum'] == '12.12.2012'


def test_init_filledDatabase():
    set_up()
    add_test_data()
    uebersicht_einzelbuchungen.index(GetRequest())


def test_getRequest_withEinnahme_shouldReturnEditLinkOfEinnahme():
    set_up()
    add_test_data()
    result = uebersicht_einzelbuchungen.index(GetRequest())
    item = result['alles']['2012.12'][0]
    assert item['wert'] == '100,00'
    assert item['link'] == 'addeinnahme'
    item = result['alles']['2012.12'][1]
    assert item['wert'] == '-100,00'
    assert item['link'] == 'addausgabe'


def test_getRequest_should_filter_year():
    set_up()
    einzelbuchungen = persisted_state.database_instance().einzelbuchungen
    einzelbuchungen.add(datum('1.12.2011'), 'please dont show me', 'please dont show me', 999)
    einzelbuchungen.add(datum('12.12.2012'), 'Test einnahme kategorie', 'test einnahme name', 100)
    einzelbuchungen.add(datum('1.12.2013'), 'please dont show me', 'please dont show me', 999)
    untaint_database(database=persisted_state.database_instance())

    result = uebersicht_einzelbuchungen.index(GetRequest())
    assert len(result['alles']) == 1
    assert result['jahre'] == [2013, 2012, 2011]
    assert result['selected_date'] == 2013


def test_delete():
    set_up()
    add_test_data()
    uebersicht_einzelbuchungen.index(VersionedPostRequest({'action': 'delete', 'delete_index': '1'}))
    einzelbuchungen = persisted_state.database_instance().einzelbuchungen
    assert einzelbuchungen.select().sum() == 100


def test_delete_should_only_trigger_one():
    set_up()
    add_test_data()
    next_id = request_handler.persisted_state.current_database_version()

    assert len(persisted_state.database_instance().einzelbuchungen.content) == 2
    uebersicht_einzelbuchungen.index(PostRequest({'action': 'delete', 'delete_index': '1', 'ID': next_id}))
    assert len(persisted_state.database_instance().einzelbuchungen.content) == 1
    uebersicht_einzelbuchungen.index(PostRequest({'action': 'delete', 'delete_index': '1', 'ID': next_id}))
    assert len(persisted_state.database_instance().einzelbuchungen.content) == 1

from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest, PostRequest, VersionedPostRequest
from butler_offline.test.database_util import untaint_database
from butler_offline.views.gemeinsame_buchungen import addgemeinsam
from butler_offline.core import file_system
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore.converter import german_to_rfc as rfc


def set_up():
    file_system.INSTANCE = FileSystemStub()
    persisted_state.DATABASE_INSTANCE = None
    request_handler.stub_me()


def test_init():
    set_up()
    context = addgemeinsam.index(GetRequest())
    assert context['approve_title'] == 'Gemeinsame Ausgabe hinzufügen'


def test__edit_call_from_uebersicht__should_preset_values__and_rename_button():
    set_up()
    db = persisted_state.database_instance()
    db.gemeinsamebuchungen.add(datum('10.10.2010'), 'kategorie', 'ausgaben_name', -10, 'Sebastian')
    untaint_database(database=db)

    context = addgemeinsam.index(PostRequest({'action': 'edit', 'edit_index': '0'}))

    assert context['approve_title'] == 'Gemeinsame Ausgabe aktualisieren'
    preset = context['default_item']
    assert preset['datum'] == rfc('10.10.2010')
    assert preset['edit_index'] == '0'
    assert preset['kategorie'] == 'kategorie'
    assert preset['name'] == 'ausgaben_name'
    assert preset['wert'] == '10,00'
    assert preset['person'] == 'Sebastian'


def test_transaction_id_should_be_in_context():
    set_up()
    context = addgemeinsam.index(GetRequest())
    assert 'ID' in context


def test_add_should_add_gemeinsame_buchung():
    set_up()
    addgemeinsam.index(VersionedPostRequest(
        {'action': 'add',
         'date': rfc('1.1.2017'),
         'kategorie': 'Essen',
         'name': 'testname',
         'person': 'testperson',
         'wert': '2,00'
         }
    ))
    testdb = persisted_state.database_instance()
    assert testdb.gemeinsamebuchungen.get(0) == {
        'Wert': -1 * float('2.00'),
        'Name': 'testname',
        'Kategorie': 'Essen',
        'Datum': datum('1.1.2017'),
        'Person': 'testperson',
        'index': 0
    }


def test_add_gemeinsame_ausgabe_should_show_in_recently_added():
    set_up()
    result = addgemeinsam.handle_request(VersionedPostRequest(
        {'action': 'add',
         'date': rfc('1.1.2017'),
         'kategorie': 'Essen',
         'name': 'testname',
         'wert': '-2,00',
         'person': 'testperson'
         }
    ))

    result_element = list(result['letzte_erfassung'])[0]

    assert result_element['fa'] == 'plus'
    assert result_element['datum'] == '01.01.2017'
    assert result_element['kategorie'] == 'Essen'
    assert result_element['name'] == 'testname'
    assert result_element['wert'] == '2,00'
    assert result_element['person'] == 'testperson'


def test_add_should_add_dynamic_einzelbuchung():
    set_up()
    addgemeinsam.index(VersionedPostRequest(
        {'action': 'add',
         'date': rfc('1.1.2017'),
         'kategorie': 'Essen',
         'name': 'testname',
         'person': 'testperson',
         'wert': '2,00'
         }
    ))
    testdb = persisted_state.database_instance()
    assert testdb.einzelbuchungen.get(0) == {
        'Wert': -0.5 * float('2.00'),
        'Name': 'testname (noch nicht abgerechnet, von testperson)',
        'Kategorie': 'Essen',
        'Datum': datum('1.1.2017'),
        'index': 0,
        'Tags': [],
        'Dynamisch': True
    }


def test_add_should_only_fire_once():
    set_up()
    next_id = persisted_state.current_database_version()
    addgemeinsam.index(PostRequest(
        {'action': 'add',
         'ID': next_id,
         'date': rfc('1.1.2017'),
         'kategorie': 'Essen',
         'name': 'testname',
         'person': 'testperson',
         'wert': '2,00'
         }
    ))
    addgemeinsam.index(PostRequest(
        {'action': 'add',
         'ID': next_id,
         'date': rfc('1.1.2017'),
         'kategorie': 'overwritten',
         'name': 'overwritten',
         'person': 'overwritten',
         'wert': '0,00'
         }
    ))
    testdb = persisted_state.database_instance()
    assert testdb.gemeinsamebuchungen.select().count() == 1


def test_edit_ausgabe():
    set_up()

    addgemeinsam.index(VersionedPostRequest(
        {'action': 'add',
         'date': rfc('1.1.2017'),
         'kategorie': 'Essen',
         'name': 'testname',
         'person': 'testperson',
         'wert': '2,00'
         }
    ))

    addgemeinsam.index(VersionedPostRequest(
        {'action': 'add',
         'edit_index': '0',
         'date': rfc('5.1.2017'),
         'kategorie': 'Essen',
         'name': 'testname',
         'person': 'testperson2',
         'wert': '2,50'
         }
    ))

    testdb = persisted_state.database_instance()
    assert testdb.gemeinsamebuchungen.content.Wert[0] == -1 * float('2.50')
    assert testdb.gemeinsamebuchungen.content.Name[0] == 'testname'
    assert testdb.gemeinsamebuchungen.content.Kategorie[0] == 'Essen'
    assert testdb.gemeinsamebuchungen.content.Datum[0] == datum('5.1.2017')
    assert testdb.gemeinsamebuchungen.content.Person[0] == 'testperson2'


def test__personen_option__should_contain_names():
    set_up()
    result = addgemeinsam.index(GetRequest())

    assert persisted_state.database_instance().name in result['personen']
    assert viewcore.name_of_partner() in result['personen']
    assert len(result['personen']) == 2


def test_edit_should_only_fire_once():
    set_up()

    addgemeinsam.index(VersionedPostRequest(
        {'action': 'add',
         'date': rfc('1.1.2017'),
         'kategorie': 'Essen',
         'name': 'testname',
         'person': 'testperson',
         'wert': '2,00'
         }
    ))

    next_id = persisted_state.current_database_version()
    addgemeinsam.index(PostRequest(
        {'action': 'add',
         'ID': next_id,
         'edit_index': '0',
         'date': rfc('5.1.2017'),
         'kategorie': 'Essen',
         'name': 'testname',
         'person': 'testperson2',
         'wert': '2,50'
         }
    ))
    addgemeinsam.index(PostRequest(
        {'action': 'add',
         'ID': next_id,
         'edit_index': '0',
         'date': rfc('5.1.2017'),
         'kategorie': 'overwritten',
         'name': 'overwritten',
         'person': 'overwritten',
         'wert': '0,00'
         }
    ))
    testdb = persisted_state.database_instance()
    assert testdb.gemeinsamebuchungen.content.Wert[0] == -1 * float('2.50')
    assert testdb.gemeinsamebuchungen.content.Name[0] == 'testname'
    assert testdb.gemeinsamebuchungen.content.Kategorie[0] == 'Essen'
    assert testdb.gemeinsamebuchungen.content.Datum[0] == datum('5.1.2017')
    assert testdb.gemeinsamebuchungen.content.Person[0] == 'testperson2'

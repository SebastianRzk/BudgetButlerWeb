from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest, PostRequest, VersionedPostRequest
from butler_offline.test.database_util import untaint_database
from butler_offline.views.einzelbuchungen import adddauerauftrag
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore.converter import german_to_rfc as rfc
from butler_offline.viewcore.state.persisted_state import database_instance as db
from butler_offline.viewcore import request_handler
from butler_offline.core import file_system
from butler_offline.core.frequency import ALL_FREQUENCY_NAMES


def set_up():
    file_system.INSTANCE = FileSystemStub()
    persisted_state.DATABASE_INSTANCE = None
    request_handler.stub_me()


def test_transaction_id_should_be_in_context():
    set_up()
    context = adddauerauftrag.index(GetRequest())
    assert 'ID' in context


def test_init():
    set_up()
    context = adddauerauftrag.index(GetRequest())
    assert context['approve_title'] == 'Dauerauftrag hinzufügen'
    assert context['rhythmen'] == ALL_FREQUENCY_NAMES


def test_edit_call_from_ueberischt_presets_values():
    set_up()
    db().dauerauftraege.add(datum('10.10.2010'), datum('10.10.2011'), '0kategorie', '0name', 'monatlich', 10)
    untaint_database(database=db())

    context = adddauerauftrag.index(VersionedPostRequest({'action': 'edit', 'edit_index': '0'}))

    assert context['approve_title'] == 'Dauerauftrag aktualisieren'

    preset = context['default_item']
    assert preset['Name'] == '0name'
    assert preset['Startdatum'] == rfc('10.10.2010')
    assert preset['Endedatum'] == rfc('10.10.2011')
    assert preset['Kategorie'] == '0kategorie'
    assert preset['Wert'] == '10,00'
    assert preset['typ'] == 'Einnahme'
    assert preset['Rhythmus'] == 'monatlich'

    db().dauerauftraege.add(datum('10.10.2015'), datum('10.10.2015'), '0kategorie', '0name', 'jaehrlich', -10)
    context = adddauerauftrag.handle_request(PostRequest({'action': 'edit', 'edit_index': '1'}))
    preset = context['default_item']
    assert preset['Startdatum'] == rfc('10.10.2015')
    assert preset['Wert'] == '10,00'
    assert preset['typ'] == 'Ausgabe'
    assert preset['Rhythmus'] == 'jaehrlich'


def test_add_dauerauftrag():
    set_up()
    adddauerauftrag.index(VersionedPostRequest(
        {'action': 'add',
         'startdatum': rfc('1.1.2017'),
         'endedatum': rfc('6.1.2017'),
         'kategorie': 'Essen',
         'typ': 'Ausgabe',
         'rhythmus': 'monatlich',
         'name': 'testname',
         'wert': '2,00'
         }
     ))

    assert len(db().dauerauftraege.content) == 1
    assert db().dauerauftraege.content.Wert[0] == -1 * float('2.00')
    assert db().dauerauftraege.content.Name[0] == 'testname'
    assert db().dauerauftraege.content.Kategorie[0] == 'Essen'
    assert db().dauerauftraege.content.Startdatum[0] == datum('1.1.2017')
    assert db().dauerauftraege.content.Endedatum[0] == datum('6.1.2017')
    assert db().dauerauftraege.content.Rhythmus[0] == 'monatlich'


def test_add_dauerauftrag_should_show_in_recently_added():
    set_up()
    result = adddauerauftrag.handle_request(VersionedPostRequest(
        {'action': 'add',
         'startdatum': rfc('1.1.2017'),
         'endedatum': rfc('6.1.2017'),
         'typ': 'Ausgabe',
         'kategorie': 'Essen',
         'name': 'testname',
         'rhythmus': 'monatlich',
         'wert': '-2,00'
         }
     ))

    result_element = list(result['letzte_erfassung'])[0]

    assert result_element['fa'] == 'plus'
    assert result_element['startdatum'] == '01.01.2017'
    assert result_element['endedatum'] == '06.01.2017'
    assert result_element['kategorie'] == 'Essen'
    assert result_element['name'] == 'testname'
    assert result_element['rhythmus'] == 'monatlich'
    assert result_element['wert'] == '2,00'


def test_add_dauerauftrag_einnahme():
    set_up()
    adddauerauftrag.index(VersionedPostRequest(
        {'action': 'add',
         'startdatum': rfc('1.1.2017'),
         'endedatum': rfc('6.1.2017'),
         'kategorie': 'Essen',
         'typ': 'Einnahme',
         'rhythmus': 'monatlich',
         'name': 'testname',
         'wert': '2,00'
         }
     ))

    assert len(db().dauerauftraege.content) == 1
    assert db().dauerauftraege.content.Wert[0] == float('2.00')
    assert db().dauerauftraege.content.Name[0] == 'testname'
    assert db().dauerauftraege.content.Kategorie[0] == 'Essen'
    assert db().dauerauftraege.content.Startdatum[0] == datum('1.1.2017')
    assert db().dauerauftraege.content.Endedatum[0] == datum('6.1.2017')
    assert db().dauerauftraege.content.Rhythmus[0] == 'monatlich'


def test_edit_dauerauftrag():
    set_up()

    adddauerauftrag.index(VersionedPostRequest(
        {'action': 'add',
         'startdatum': rfc('1.1.2017'),
         'endedatum': rfc('6.1.2017'),
         'kategorie': 'Essen',
         'typ': 'Ausgabe',
         'rhythmus': 'monatlich',
         'name': 'testname',
         'wert': '2,00'
         }
     ))

    adddauerauftrag.index(VersionedPostRequest(
        {'action': 'add',
         'edit_index': '0',
         'startdatum': rfc('2.1.2017'),
         'endedatum': rfc('5.1.2017'),
         'kategorie': 'Essen',
         'typ': 'Ausgabe',
         'rhythmus': 'monatlich',
         'name': 'testname',
         'wert': '2,50'
         }
     ))

    assert len(db().dauerauftraege.content) == 1
    assert db().dauerauftraege.content.Wert[0] == -1 * float('2.50')
    assert db().dauerauftraege.content.Name[0] == 'testname'
    assert db().dauerauftraege.content.Kategorie[0] == 'Essen'
    assert db().dauerauftraege.content.Startdatum[0] == datum('2.1.2017')
    assert db().dauerauftraege.content.Endedatum[0] == datum('5.1.2017')


def test_edit_dauerauftrag_ausgabe_to_einnahme():
    set_up()

    adddauerauftrag.index(VersionedPostRequest(
        {'action': 'add',
         'startdatum': rfc('1.1.2017'),
         'endedatum': rfc('6.1.2017'),
         'kategorie': 'Essen',
         'typ': 'Ausgabe',
         'rhythmus': 'monatlich',
         'name': 'testname',
         'wert': '2,00'
         }
     ))

    adddauerauftrag.index(VersionedPostRequest(
        {'action': 'add',
         'edit_index': '0',
         'startdatum': rfc('2.1.2017'),
         'endedatum': rfc('5.1.2017'),
         'kategorie': 'Essen',
         'typ': 'Einnahme',
         'rhythmus': 'monatlich',
         'name': 'testname',
         'wert': '2,50'
         }
     ))

    assert len(db().dauerauftraege.content) == 1
    assert db().dauerauftraege.content.Wert[0] == float('2.50')
    assert db().dauerauftraege.content.Name[0] == 'testname'
    assert db().dauerauftraege.content.Kategorie[0] == 'Essen'
    assert db().dauerauftraege.content.Startdatum[0] == datum('2.1.2017')
    assert db().dauerauftraege.content.Endedatum[0] == datum('5.1.2017')


def test_edit_dauerauftrag_should_only_fire_once():
    set_up()

    adddauerauftrag.index(VersionedPostRequest(
        {'action': 'add',
         'startdatum': rfc('1.1.2017'),
         'endedatum': rfc('6.1.2017'),
         'kategorie': 'Essen',
         'typ': 'Ausgabe',
         'rhythmus': 'monatlich',
         'name': 'testname',
         'wert': '2,00'
         }
     ))
    next_id = persisted_state.current_database_version()
    adddauerauftrag.index(PostRequest(
        {'action': 'add',
         'ID': next_id,
         'edit_index': '0',
         'startdatum': rfc('2.1.2017'),
         'endedatum': rfc('5.1.2017'),
         'kategorie': 'Essen',
         'typ': 'Ausgabe',
         'rhythmus': 'monatlich',
         'name': 'testname',
         'wert': '2,50'
         }
     ))

    adddauerauftrag.index(PostRequest(
        {'action': 'add',
         'ID': next_id,
         'edit_index': '0',
         'startdatum': rfc('2.1.2017'),
         'endedatum': rfc('5.1.2017'),
         'kategorie': 'overwritten',
         'typ': 'Ausgabe',
         'rhythmus': 'overwritten',
         'name': 'overwritten',
         'wert': '0,00'
         }
     ))

    assert len(db().dauerauftraege.content) == 1
    assert db().dauerauftraege.content.Wert[0] == -1 * float('2.50')
    assert db().dauerauftraege.content.Name[0] == 'testname'
    assert db().dauerauftraege.content.Kategorie[0] == 'Essen'
    assert db().dauerauftraege.content.Startdatum[0] == datum('2.1.2017')
    assert db().dauerauftraege.content.Endedatum[0] == datum('5.1.2017')


def test_add_dauerauftrag_should_only_fire_once():
    set_up()

    next_id = persisted_state.current_database_version()
    adddauerauftrag.index(PostRequest(
        {'action': 'add',
         'ID': next_id,
         'startdatum': rfc('2.1.2017'),
         'endedatum': rfc('5.1.2017'),
         'kategorie': 'Essen',
         'typ': 'Ausgabe',
         'rhythmus': 'monatlich',
         'name': 'testname',
         'wert': '2,50'
         }
     ))

    adddauerauftrag.index(PostRequest(
        {'action': 'add',
         'ID': next_id,
         'startdatum': rfc('2.1.2017'),
         'endedatum': rfc('5.1.2017'),
         'kategorie': 'overwritten',
         'typ': 'Ausgabe',
         'rhythmus': 'overwritten',
         'name': 'overwritten',
         'wert': '0,00'
         }
     ))

    assert len(db().dauerauftraege.content) == 1
    assert db().dauerauftraege.content.Wert[0] == -1 * float('2.50')
    assert db().dauerauftraege.content.Name[0] == 'testname'
    assert db().dauerauftraege.content.Kategorie[0] == 'Essen'
    assert db().dauerauftraege.content.Startdatum[0] == datum('2.1.2017')
    assert db().dauerauftraege.content.Endedatum[0] == datum('5.1.2017')

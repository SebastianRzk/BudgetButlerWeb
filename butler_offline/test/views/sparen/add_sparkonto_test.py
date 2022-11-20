from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.test.RequestStubs import PostRequest
from butler_offline.test.RequestStubs import VersionedPostRequest
from butler_offline.views.sparen import add_sparkoto
from butler_offline.core import file_system
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.context import get_error_message


def set_up():
    file_system.INSTANCE = FileSystemStub()
    persisted_state.DATABASE_INSTANCE = None
    request_handler.stub_me()


def test_init():
    set_up()
    context = add_sparkoto.index(GetRequest())
    assert context['approve_title'] == 'Sparkonto hinzufügen'


def test_transaction_id_should_be_in_context():
    set_up()
    context = add_sparkoto.index(GetRequest())
    assert 'ID' in context


def test_add_should_add_sparkonto():
    set_up()
    add_sparkoto.index(VersionedPostRequest(
        {'action': 'add',
         'kontotyp': '1typ',
         'kontoname': '1name'
         }
     ))

    db = persisted_state.database_instance()
    assert len(db.sparkontos.content) == 1
    assert db.sparkontos.content.Kontoname[0] == '1name'
    assert db.sparkontos.content.Kontotyp[0] == '1typ'


def test_add_with_underscore_in_name_should_return_error():
    set_up()
    result = add_sparkoto.index(VersionedPostRequest(
        {'action': 'add',
         'kontotyp': '1typ',
         'kontoname': '1_name'
         }
     ))

    assert get_error_message(result) == 'Kontoname darf kein Unterstrich "_" enthalten.'


def test_add_sparkonto_should_show_in_recently_added():
    set_up()
    result = add_sparkoto.index(VersionedPostRequest(
        {'action': 'add',
         'kontotyp': '1typ',
         'kontoname': '1name'
         }
     ))
    result_element = list(result['letzte_erfassung'])[0]

    assert result_element['fa'] == 'plus'
    assert result_element['Kontotyp'] == '1typ'
    assert result_element['Kontoname'] == '1name'


def test_add_should_only_fire_once():
    set_up()
    next_id = persisted_state.current_database_version()
    add_sparkoto.index(PostRequest(
        {'action': 'add',
         'ID': next_id,
         'kontotyp': '1typ',
         'kontoname': '1name'
         }
     ))
    add_sparkoto.index(PostRequest(
        {'action': 'add',
         'ID': next_id,
         'kontotyp': 'overwritten',
         'kontoname': 'overwritten'
         }
     ))
    db = persisted_state.database_instance()
    assert len(db.sparkontos.content) == 1
    assert db.sparkontos.content.Kontoname[0] == '1name'
    assert db.sparkontos.content.Kontotyp[0] == '1typ'


def test_edit_sparkonto():
    set_up()
    add_sparkoto.index(VersionedPostRequest(
        {'action': 'add',
         'kontotyp': '1typ',
         'kontoname': '1name'
         }
    ))

    result = add_sparkoto.index(VersionedPostRequest(
        {'action': 'add',
         'edit_index': 0,
         'kontotyp': '2typ',
         'kontoname': '2name'
         }
    ))

    db = persisted_state.database_instance()
    assert len(db.sparkontos.content) == 1
    assert db.sparkontos.content.Kontoname[0] == '2name'
    assert db.sparkontos.content.Kontotyp[0] == '2typ'

    result_element = list(result['letzte_erfassung'])[0]

    assert result_element['fa'] == 'pencil'
    assert result_element['Kontotyp'] == '2typ'
    assert result_element['Kontoname'] == '2name'


def test_edit_sparkonto_should_only_fire_once():
    set_up()
    add_sparkoto.index(VersionedPostRequest(
        {'action': 'add',
         'kontotyp': '1typ',
         'kontoname': '1name'
         }
    ))

    next_id = persisted_state.current_database_version()
    add_sparkoto.index(PostRequest(
        {'action': 'add',
         'ID': next_id,
         'edit_index': 0,
         'kontotyp': '2typ',
         'kontoname': '2name'
         }
    ))
    add_sparkoto.index(PostRequest(
        {'action': 'add',
         'ID': next_id,
         'edit_index': 0,
         'kontotyp': 'overwritten',
         'kontoname': 'overwritten'
         }
    ))

    db = persisted_state.database_instance()
    assert len(db.sparkontos.content) == 1
    assert db.sparkontos.content.Kontoname[0] == '2name'
    assert db.sparkontos.content.Kontotyp[0] == '2typ'

def test_edit_call_from_ueberischt_should_preset_values_and_rename_button():
    set_up()
    add_sparkoto.index(VersionedPostRequest(
        {'action': 'add',
         'kontotyp': '1typ',
         'kontoname': '1name'
         }
    ))

    context = add_sparkoto.index(PostRequest({'action': 'edit', 'edit_index': '0'}))
    assert context['approve_title'] == 'Sparkonto aktualisieren'
    preset = context['default_item']

    assert preset['edit_index'] == '0'
    assert preset['kontotyp'] == '1typ'
    assert preset['kontoname'] == '1name'


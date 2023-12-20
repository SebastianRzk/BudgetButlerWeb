from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.request_stubs import GetRequest, PostRequest
from butler_offline.views.einzelbuchungen import addeinnahme
from butler_offline.core import file_system
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore.converter import german_to_rfc as rfc
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler
from butler_offline.viewcore.state import non_persisted_state
from butler_offline.viewcore.renderhelper import Betrag
from butler_offline.viewcore.state.non_persisted_state.einzelbuchungen import EinzelbuchungAddedChange
from butler_offline.viewcore.state.non_persisted_state import NonPersistedContext

file_system.INSTANCE = FileSystemStub()


def test_transaction_id_should_be_in_context():
    context = addeinnahme.handle_request(GetRequest(), context=addeinnahme.AddEinnahmeContext(
        einzelbuchungen=Einzelbuchungen()))
    assert context.is_transactional()


def test_init_should_have_title_einnahme_hinzufuegen():
    context = addeinnahme.handle_request(GetRequest(), context=addeinnahme.AddEinnahmeContext(
        einzelbuchungen=Einzelbuchungen()
    ))
    assert context.get('approve_title') == 'Einnahme hinzufügen'


def test__edit_call_from_ueberischt__should_name_button_edit():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('10.10.2010'), 'kategorie', 'name', 10.00)

    context = addeinnahme.handle_request(request=PostRequest({'action': 'edit', 'edit_index': '0'}),
                                         context=addeinnahme.AddEinnahmeContext(einzelbuchungen=einzelbuchungen))

    assert context.get('approve_title') == 'Einnahme aktualisieren'


def test_add_ausgabe():
    einzelbuchungen = Einzelbuchungen()
    addeinnahme.handle_request(PostRequest(
        {'action': 'add',
         'date': rfc('1.1.2017'),
         'kategorie': 'Essen',
         'name': 'testname',
         'wert': '2,00'
         }),
        context=addeinnahme.AddEinnahmeContext(einzelbuchungen=einzelbuchungen))

    assert einzelbuchungen.select().count() == 1
    assert einzelbuchungen.get(0) == {
        'Wert': float('2.00'),
        'Name': 'testname',
        'Kategorie': 'Essen',
        'Datum': datum('01.01.2017'),
        'Dynamisch': False,
        'Tags': [],
        'index': 0
    }


def test_index_should_be_secured_by_request_handler():
    def index():
        addeinnahme.index(GetRequest())

    result = run_in_mocked_handler(index_handle=index)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['einzelbuchungen/add_einnahme.html']


def test_add_einnahme_should_show_in_recently_added():
    non_persisted_state.CONTEXT = NonPersistedContext()
    result = addeinnahme.handle_request(PostRequest(
        {'action': 'add',
         'date': rfc('1.1.2017'),
         'kategorie': 'Essen',
         'name': 'testname',
         'wert': '2,00'
         }
    ),
        context=addeinnahme.AddEinnahmeContext(einzelbuchungen=Einzelbuchungen()))

    assert list(result.get('letzte_erfassung')) == [
        EinzelbuchungAddedChange(
            datum='01.01.2017',
            kategorie='Essen',
            name='testname',
            wert=Betrag(2)
        )]


def test_edit_ausgabe():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(
        datum=datum('1.1.2017'),
        kategorie='Essen',
        name='testname',
        wert=float('2.00')
    )

    addeinnahme.handle_request(PostRequest(
        {'action': 'add',
         'edit_index': '0',
         'date': rfc('5.1.2017'),
         'kategorie': 'Essen',
         'name': 'testname',
         'wert': '2,50'
         }
    ), context=addeinnahme.AddEinnahmeContext(einzelbuchungen=einzelbuchungen))

    assert einzelbuchungen.select().count() == 1
    assert einzelbuchungen.get(0) == {
        'Name': 'testname',
        'Kategorie': 'Essen',
        'Datum': datum('05.01.2017'),
        'Wert': float('2.50'),
        'index': 0,
        'Dynamisch': False,
        'Tags': []
    }


def test_edit_einzelbuchung__should_load_input_values():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(
        datum=datum('1.1.2017'),
        kategorie='Essen',
        name='testname',
        wert=float('2.34')
    )

    result = addeinnahme.handle_request(PostRequest(
        {'action': 'edit',
         'edit_index': '0'
         }
    ),
        context=addeinnahme.AddEinnahmeContext(einzelbuchungen=einzelbuchungen))

    assert result.get('edit_index') == 0
    assert result.get('default_item') == {'Datum': '2017-01-01',
                                          'Dynamisch': False,
                                          'Kategorie': 'Essen',
                                          'Name': 'testname',
                                          'Tags': [],
                                          'Wert': '2,34',
                                          'index': 0}

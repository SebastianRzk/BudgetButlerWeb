from butler_offline.test.request_stubs import GetRequest
from butler_offline.test.request_stubs import PostRequest
from butler_offline.views.einzelbuchungen import addausgabe
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore.converter import german_to_rfc as rfc
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler
from butler_offline.core import file_system
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.viewcore.state.non_persisted_state.einzelbuchungen import EinzelbuchungAddedChange
from butler_offline.viewcore.renderhelper import Betrag


file_system.INSTANCE = FileSystemStub()


def test_init():
    context = addausgabe.handle_request(
        request=GetRequest(),
        context=addausgabe.AddAusgabeContext(einzelbuchungen=Einzelbuchungen()))
    assert context.get('approve_title') == 'Ausgabe hinzufügen'


def test_transaction_id_should_be_in_context():
    context = addausgabe.handle_request(
        request=GetRequest(),
        context=addausgabe.AddAusgabeContext(einzelbuchungen=Einzelbuchungen()))
    assert context.is_transactional()


def test__edit_call_from_uebersicht__should_name_button_edit():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(datum('10.10.2010'), 'kategorie', 'name', 10.00)

    context = addausgabe.handle_request(
        request=PostRequest({'action': 'edit', 'edit_index': '0'}),
        context=addausgabe.AddAusgabeContext(einzelbuchungen=einzelbuchungen)
    )
    assert context.get('approve_title') == 'Ausgabe aktualisieren'


def test_add_ausgabe():
    einzelbuchungen = Einzelbuchungen()
    addausgabe.handle_request(
        request=PostRequest(
            {'action': 'add',
             'date': rfc('1.1.2017'),
             'kategorie': 'Essen',
             'name': 'testname',
             'wert': '2,00'
             }
        ),
        context=addausgabe.AddAusgabeContext(einzelbuchungen=einzelbuchungen)
        )

    assert einzelbuchungen.select().count() == 1
    assert einzelbuchungen.get(0) == {
        'index': 0,
        'Wert': float('-2.00'),
        'Name': 'testname',
        'Kategorie': 'Essen',
        'Datum': datum('01.01.2017'),
        'Tags': [],
        'Dynamisch': False
    }


def test_add_ausgabe_should_show_in_recently_added():
    result = addausgabe.handle_request(
        request=PostRequest(
            {'action': 'add',
             'date': rfc('1.1.2017'),
             'kategorie': 'Essen',
             'name': 'testname',
             'wert': '2,00'
             }
        ),
        context=addausgabe.AddAusgabeContext(einzelbuchungen=Einzelbuchungen())
    )

    result_element = list(result.get('letzte_erfassung'))[0]

    assert result_element == EinzelbuchungAddedChange(
        datum='01.01.2017',
        kategorie='Essen',
        name='testname',
        wert=Betrag(-2)
    )


def test_edit_ausgabe():
    einzelbuchungen = Einzelbuchungen()

    einzelbuchungen.add(
        datum=datum('01.01.2017'),
        name='testname',
        kategorie='Essen',
        wert=float(-2.00),
    )

    addausgabe.handle_request(
        request=PostRequest(
            {'action': 'add',
             'edit_index': '0',
             'date': rfc('5.1.2017'),
             'kategorie': 'Essen2',
             'name': 'testname2',
             'wert': '2,50'
             }
        ),
        context=addausgabe.AddAusgabeContext(
            einzelbuchungen=einzelbuchungen
        )
    )

    assert einzelbuchungen.select().count() == 1
    assert einzelbuchungen.get(0) == {
        'Datum': datum('5.1.2017'),
        'Kategorie': 'Essen2',
        'Name': 'testname2',
        'Wert': float(-2.50),
        'index': 0,
        'Dynamisch': False,
        'Tags': []
         }


def test_edit_einzelbuchung__should_load_input_values__and__invert_wert():
    einzelbuchungen = Einzelbuchungen()

    einzelbuchungen.add(
        datum=datum('01.01.2017'),
        name='testname',
        kategorie='Essen',
        wert=float(-2.00),
    )

    result = addausgabe.handle_request(
        request=PostRequest(
            {'action': 'edit',
             'edit_index': '0'
             }),
        context=addausgabe.AddAusgabeContext(
            einzelbuchungen=einzelbuchungen
        )
    )

    assert result.get('edit_index') == 0
    assert result.get('default_item')['Name'] == 'testname'
    assert result.get('default_item')['Wert'] == '2,00'


def index_function_should_be_secured_by_request_handler():
    def handle():
        addausgabe.index(request=GetRequest())

    result = run_in_mocked_handler(index_handle=handle)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['einzelbuchungen/add_ausgabe.html']

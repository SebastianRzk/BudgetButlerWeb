from butler_offline.test.request_stubs import GetRequest, PostRequest
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore.converter import german_to_rfc as rfc
from butler_offline.views.gemeinsame_buchungen import addgemeinsam
from butler_offline.core.database.gemeinsamebuchungen import Gemeinsamebuchungen
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler


def test_init():
    context = addgemeinsam.handle_request(
        GetRequest(),
        context=simple_add_gemeinsam_context(gemeinsame_buchungen=Gemeinsamebuchungen()))
    assert context.get('approve_title') == 'Gemeinsame Ausgabe hinzufügen'


def test__edit_call_from_uebersicht__should_preset_values__and_rename_button():
    gemeinsame_buchungen = Gemeinsamebuchungen()
    gemeinsame_buchungen.add(datum('10.10.2010'), 'kategorie', 'ausgaben_name', -10, 'Sebastian')

    context = addgemeinsam.handle_request(
        PostRequest({'action': 'edit', 'edit_index': '0'}),
        context=simple_add_gemeinsam_context(gemeinsame_buchungen)
    )

    assert context.get('approve_title') == 'Gemeinsame Ausgabe aktualisieren'
    preset = context.get('default_item')
    assert preset['datum'] == rfc('10.10.2010')
    assert preset['edit_index'] == '0'
    assert preset['kategorie'] == 'kategorie'
    assert preset['name'] == 'ausgaben_name'
    assert preset['wert'] == '10,00'
    assert preset['person'] == 'Sebastian'


def simple_add_gemeinsam_context(gemeinsame_buchungen):
    return addgemeinsam.AddGemeinsameBuchungContext(
        gemeinsame_buchungen=gemeinsame_buchungen,
        kategorien=[],
        partner_name="",
        database_name=""
    )


def test_transaction_id_should_be_in_context():
    context = addgemeinsam.handle_request(
        GetRequest(),
        context=simple_add_gemeinsam_context(Gemeinsamebuchungen())
    )
    assert context.is_transactional()


def test_add_should_add_gemeinsame_buchung():
    gemeinsame_buchungen = Gemeinsamebuchungen()

    addgemeinsam.handle_request(PostRequest(
        {'action': 'add',
         'date': rfc('1.1.2017'),
         'kategorie': 'Essen',
         'name': 'testname',
         'person': 'testperson',
         'wert': '2,00'
         }),
        context=simple_add_gemeinsam_context(gemeinsame_buchungen=gemeinsame_buchungen)
    )
    assert gemeinsame_buchungen.get(0) == {
        'Wert': '-2.00',
        'Name': 'testname',
        'Kategorie': 'Essen',
        'Datum': datum('1.1.2017'),
        'Person': 'testperson',
        'index': 0
    }


def test_add_gemeinsame_ausgabe_should_show_in_recently_added():
    gemeinsame_buchungen = Gemeinsamebuchungen()

    result = addgemeinsam.handle_request(PostRequest(
        {'action': 'add',
         'date': rfc('1.1.2017'),
         'kategorie': 'Essen',
         'name': 'testname',
         'wert': '-2,00',
         'person': 'testperson'
         }),
        simple_add_gemeinsam_context(gemeinsame_buchungen=gemeinsame_buchungen)
    )

    result_element = list(result.get('letzte_erfassung'))[0]

    assert result_element['fa'] == 'plus'
    assert result_element['datum'] == '01.01.2017'
    assert result_element['kategorie'] == 'Essen'
    assert result_element['name'] == 'testname'
    assert result_element['wert'] == '2,00'
    assert result_element['person'] == 'testperson'


def test_edit_ausgabe():
    gemeinsame_buchungen = Gemeinsamebuchungen()
    gemeinsame_buchungen.add(
        ausgaben_datum=datum('01.01.2017'),
        kategorie='Essen',
        person='testperson',
        ausgaben_name='testname',
        wert=2.00,
    )

    addgemeinsam.handle_request(PostRequest(
        {'action': 'add',
         'edit_index': '0',
         'date': rfc('5.1.2017'),
         'kategorie': 'Essen2',
         'name': 'testname2',
         'person': 'testperson2',
         'wert': '2,50'
         }),
        context=simple_add_gemeinsam_context(gemeinsame_buchungen=gemeinsame_buchungen)
    )

    assert gemeinsame_buchungen.get(0) == {
        'Wert': -2.50,
        'Name': 'testname2',
        'Person': 'testperson2',
        'Datum': datum('05.01.2017'),
        'Kategorie': 'Essen2',
        'index': 0
    }


def test__personen_option__should_contain_names():
    result = addgemeinsam.handle_request(
        GetRequest(),
        context=addgemeinsam.AddGemeinsameBuchungContext(
            gemeinsame_buchungen=Gemeinsamebuchungen(),
            partner_name="Partnername",
            database_name="Name",
            kategorien=[]
        )
    )

    assert set(result.get('personen')) == {'Name', 'Partnername'}


def test_index_should_be_secured_by_request_handler():
    def index():
        addgemeinsam.index(GetRequest())

    result = run_in_mocked_handler(index_handle=index)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['gemeinsame_buchungen/addgemeinsam.html']


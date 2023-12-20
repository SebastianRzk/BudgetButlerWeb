from butler_offline.core import file_system
from butler_offline.core.database.dauerauftraege import Dauerauftraege
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.core.frequency import ALL_FREQUENCY_NAMES
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.request_stubs import GetRequest, PostRequest
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore.converter import german_to_rfc as rfc
from butler_offline.viewcore.state import non_persisted_state
from butler_offline.viewcore.state.non_persisted_state import NonPersistedContext
from butler_offline.viewcore.state.non_persisted_state.dauerauftraege import DauerauftragAddedChange
from butler_offline.views.einzelbuchungen import adddauerauftrag
from butler_offline.viewcore.renderhelper import Betrag

file_system.INSTANCE = FileSystemStub()


def test_transaction_id_should_be_in_context():
    context = adddauerauftrag.handle_request(GetRequest(), adddauerauftrag.AddDauerauftragContext(
        dauerauftraege=Dauerauftraege(),
        einzelbuchungen=Einzelbuchungen()
    ))
    assert context.is_transactional()


def test_init():
    context = adddauerauftrag.handle_request(GetRequest(), adddauerauftrag.AddDauerauftragContext(
        dauerauftraege=Dauerauftraege(),
        einzelbuchungen=Einzelbuchungen()
    ))
    assert context.get('approve_title') == 'Dauerauftrag hinzufügen'
    assert context.get('rhythmen') == ALL_FREQUENCY_NAMES


def test_edit_call_from_ueberischt_presets_values():
    dauerauftraege = Dauerauftraege()
    dauerauftraege.add(datum('10.10.2010'), datum('10.10.2011'), '0kategorie', '0name', 'monatlich', 10)

    context = adddauerauftrag.handle_request(PostRequest({'action': 'edit', 'edit_index': '0'}),
                                             context=adddauerauftrag.AddDauerauftragContext(
                                                 dauerauftraege=dauerauftraege,
                                                 einzelbuchungen=Einzelbuchungen()
                                             ))

    assert context.get('approve_title') == 'Dauerauftrag aktualisieren'

    preset = context.get('default_item')
    assert preset['Name'] == '0name'
    assert preset['Startdatum'] == rfc('10.10.2010')
    assert preset['Endedatum'] == rfc('10.10.2011')
    assert preset['Kategorie'] == '0kategorie'
    assert preset['Wert'] == '10,00'
    assert preset['typ'] == 'Einnahme'
    assert preset['Rhythmus'] == 'monatlich'

    dauerauftraege.add(datum('10.10.2015'), datum('10.10.2015'), '0kategorie', '0name', 'jaehrlich', -10)
    context = adddauerauftrag.handle_request(PostRequest({'action': 'edit', 'edit_index': '1'}),
                                             context=adddauerauftrag.AddDauerauftragContext(
                                                 dauerauftraege=dauerauftraege,
                                                 einzelbuchungen=Einzelbuchungen()
                                             ))
    preset = context.get('default_item')
    assert preset['Startdatum'] == rfc('10.10.2015')
    assert preset['Wert'] == '10,00'
    assert preset['typ'] == 'Ausgabe'
    assert preset['Rhythmus'] == 'jaehrlich'


def test_add_dauerauftrag():
    dauerauftraege = Dauerauftraege()
    adddauerauftrag.handle_request(PostRequest(
        {'action': 'add',
         'startdatum': rfc('1.1.2017'),
         'endedatum': rfc('6.1.2017'),
         'kategorie': 'Essen',
         'typ': 'Ausgabe',
         'rhythmus': 'monatlich',
         'name': 'testname',
         'wert': '2,00'
         }
    ),
        context=adddauerauftrag.AddDauerauftragContext(
            dauerauftraege=dauerauftraege,
            einzelbuchungen=Einzelbuchungen()
        )
    )

    assert dauerauftraege.select().count() == 1
    assert dauerauftraege.get(0) == {
        'Wert': -1 * float('2.00'),
        'Name': 'testname',
        'Startdatum': datum('01.01.2017'),
        'Endedatum': datum('06.01.2017'),
        'Rhythmus': 'monatlich',
        'Kategorie': 'Essen',
        'index': 0
    }


def test_add_dauerauftrag_should_show_in_recently_added():
    non_persisted_state.CONTEXT = NonPersistedContext()
    result = adddauerauftrag.handle_request(PostRequest(
        {'action': 'add',
         'startdatum': rfc('1.1.2017'),
         'endedatum': rfc('6.1.2017'),
         'kategorie': 'Essen',
         'typ': 'Ausgabe',
         'rhythmus': 'monatlich',
         'name': 'testname',
         'wert': '2,00'
         }
    ),
        context=adddauerauftrag.AddDauerauftragContext(
            dauerauftraege=Dauerauftraege(),
            einzelbuchungen=Einzelbuchungen()
        )
    )

    result_element = list(result.get('letzte_erfassung'))
    assert result_element == [DauerauftragAddedChange(
        ende_datum='06.01.2017',
        kategorie='Essen',
        name='testname',
        rhythmus='monatlich',
        start_datum='01.01.2017',
        wert=Betrag(-2))]


def test_add_dauerauftrag_einnahme():
    dauerauftraege = Dauerauftraege()
    adddauerauftrag.handle_request(PostRequest(
        {'action': 'add',
         'startdatum': rfc('1.1.2017'),
         'endedatum': rfc('6.1.2017'),
         'kategorie': 'Essen',
         'typ': 'Einnahme',
         'rhythmus': 'monatlich',
         'name': 'testname',
         'wert': '2,00'
         }
    ),
        context=adddauerauftrag.AddDauerauftragContext(
            dauerauftraege=dauerauftraege,
            einzelbuchungen=Einzelbuchungen()
        )
    )

    assert dauerauftraege.select().count() == 1
    assert dauerauftraege.get(0) == {'Endedatum': datum('6.1.2017'),
                                     'Kategorie': 'Essen',
                                     'Name': 'testname',
                                     'Rhythmus': 'monatlich',
                                     'Startdatum': datum('1.1.2017'),
                                     'Wert': 2.0,
                                     'index': 0}


def test_edit_dauerauftrag():
    dauerauftraege = Dauerauftraege()
    dauerauftraege.add(
        startdatum=datum('01.01.2017'),
        endedatum=datum('06.01.2017'),
        kategorie='Essen',
        name='testname',
        rhythmus='monatlich',
        wert=-2.00,
    )

    adddauerauftrag.handle_request(PostRequest(
        {'action': 'add',
         'edit_index': '0',
         'startdatum': rfc('2.1.2017'),
         'endedatum': rfc('5.1.2017'),
         'kategorie': 'Essen2',
         'typ': 'Einnahme',
         'rhythmus': 'jaehrlich',
         'name': 'testname2',
         'wert': '2,50'
         }
    ),
        context=adddauerauftrag.AddDauerauftragContext(
            dauerauftraege=dauerauftraege,
            einzelbuchungen=Einzelbuchungen()
        ))

    assert dauerauftraege.select().count() == 1
    assert dauerauftraege.get(0) == {
        'Wert': 2.50,
        'Name': 'testname2',
        'Kategorie': 'Essen2',
        'Startdatum': datum('02.01.2017'),
        'Endedatum': datum('05.01.2017'),
        'Rhythmus': 'jaehrlich',
        'index': 0
    }


def test_index_should_be_secured_by_request_handler():
    def index():
        adddauerauftrag.index(GetRequest())

    result = run_in_mocked_handler(index_handle=index)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['einzelbuchungen/add_dauerauftrag.html']

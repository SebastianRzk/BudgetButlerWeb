from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.test.RequestStubs import PostRequest
from butler_offline.test.RequestStubs import VersionedPostRequest
from butler_offline.views.sparen import add_depotauszug
from butler_offline.core import file_system
from butler_offline.core.database.sparen.kontos import Kontos
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore.converter import german_to_rfc as rfc
from butler_offline.viewcore.converter import datum_to_string
from butler_offline.core.database.sparen.depotauszuege import Depotauszuege
from datetime import date


def set_up():
    file_system.INSTANCE = FileSystemStub()
    persisted_state.DATABASE_INSTANCE = None
    depotwerte = persisted_state.database_instance().depotwerte
    persisted_state.database_instance().sparkontos.add('1demokonto', Kontos.TYP_DEPOT)
    persisted_state.database_instance().sparkontos.add('2demokonto', Kontos.TYP_DEPOT)
    depotwerte.add(name='1demowert', isin='1demoisin', typ=depotwerte.TYP_ETF)
    depotwerte.add(name='2demowert', isin='2demoisin', typ=depotwerte.TYP_ETF)
    depotwerte.add(name='3demowert', isin='3demoisin', typ=depotwerte.TYP_ETF)

    # old depotauszug, alle isins gebucht
    persisted_state.database_instance().depotauszuege.add(datum('01.01.2020'), '1demoisin', '1demokonto', 1)
    persisted_state.database_instance().depotauszuege.add(datum('01.01.2020'), '2demoisin', '1demokonto', 1)
    persisted_state.database_instance().depotauszuege.add(datum('01.01.2020'), '3demoisin', '1demokonto', 1)
    persisted_state.database_instance().depotauszuege.add(datum('01.01.2020'), '1demoisin', '2demokonto', 1)
    persisted_state.database_instance().depotauszuege.add(datum('01.01.2020'), '2demoisin', '2demokonto', 1)
    persisted_state.database_instance().depotauszuege.add(datum('01.01.2020'), '3demoisin', '2demokonto', 1)

    # new depotauszug
    persisted_state.database_instance().depotauszuege.add(datum('02.01.2020'), '1demoisin', '1demokonto', 20)
    persisted_state.database_instance().depotauszuege.add(datum('02.01.2020'), '2demoisin', '2demokonto', 30)
    persisted_state.database_instance().depotauszuege.add(datum('02.01.2020'), '3demoisin', '2demokonto', 40)

    request_handler.stub_me()


def test_init():
    set_up()
    context = add_depotauszug.index(GetRequest())
    assert context['approve_title'] == 'Depotauszug hinzufügen'
    assert context['default_items'] == [
        {
            'datum': datum_to_string(date.today()),
            'empty_items': [
                {'description': '2demowert (2demoisin)',
                 'isin': '2demoisin',
                 'wert': 0},
                {'description': '3demowert (3demoisin)',
                 'isin': '3demoisin',
                 'wert': 0}
            ],
            'filled_items': [
                {'description': '1demowert (1demoisin)',
                 'isin': '1demoisin',
                 'wert': 20}],
            'konto': '1demokonto'},
        {
            'datum': datum_to_string(date.today()),
            'empty_items': [
                {'description': '1demowert (1demoisin)',
                 'isin': '1demoisin',
                 'wert': 0}
            ],
            'filled_items': [
                {'description': '2demowert (2demoisin)',
                 'isin': '2demoisin',
                 'wert': 30},
                {'description': '3demowert (3demoisin)',
                 'isin': '3demoisin',
                 'wert': 40}],
            'konto': '2demokonto'},

    ]


def test_init_with_empty_depotauszuege_should_flip_filled_and_empty():
    set_up()
    persisted_state.database_instance().depotauszuege = Depotauszuege()
    context = add_depotauszug.index(GetRequest())
    assert context['approve_title'] == 'Depotauszug hinzufügen'
    assert context['default_items'] == [
        {
            'datum': datum_to_string(date.today()),
            'empty_items': [],
            'filled_items': [
                {'description': '1demowert (1demoisin)',
                 'isin': '1demoisin',
                 'wert': 0},
                {'description': '2demowert (2demoisin)',
                 'isin': '2demoisin',
                 'wert': 0},
                {'description': '3demowert (3demoisin)',
                 'isin': '3demoisin',
                 'wert': 0}],
            'konto': '1demokonto'},
        {
            'datum': datum_to_string(date.today()),
            'empty_items': [],
            'filled_items': [
                {'description': '1demowert (1demoisin)',
                 'isin': '1demoisin',
                 'wert': 0},
                {'description': '2demowert (2demoisin)',
                 'isin': '2demoisin',
                 'wert': 0},
                {'description': '3demowert (3demoisin)',
                 'isin': '3demoisin',
                 'wert': 0}],
            'konto': '2demokonto'},

    ]


def test_init_with_already_empty_should_handle_like_empty():
    set_up()

    persisted_state.database_instance().depotauszuege.add(datum('03.01.2020'), '1demoisin', '1demokonto', 0)
    persisted_state.database_instance().depotauszuege.add(datum('03.01.2020'), '2demoisin', '1demokonto', 0)
    persisted_state.database_instance().depotauszuege.add(datum('03.01.2020'), '3demoisin', '1demokonto', 0)
    persisted_state.database_instance().depotauszuege.add(datum('03.01.2020'), '1demoisin', '2demokonto', 0)
    persisted_state.database_instance().depotauszuege.add(datum('03.01.2020'), '2demoisin', '2demokonto', 0)
    persisted_state.database_instance().depotauszuege.add(datum('03.01.2020'), '3demoisin', '2demokonto', 0)

    context = add_depotauszug.index(GetRequest())
    assert context['approve_title'] == 'Depotauszug hinzufügen'
    assert context['default_items'] == [
        {
            'datum': datum_to_string(date.today()),
            'empty_items': [],
            'filled_items': [
                {'description': '1demowert (1demoisin)',
                 'isin': '1demoisin',
                 'wert': 0},
                {'description': '2demowert (2demoisin)',
                 'isin': '2demoisin',
                 'wert': 0},
                {'description': '3demowert (3demoisin)',
                 'isin': '3demoisin',
                 'wert': 0}],
            'konto': '1demokonto'},
        {
            'datum': datum_to_string(date.today()),
            'empty_items': [],
            'filled_items': [
                {'description': '1demowert (1demoisin)',
                 'isin': '1demoisin',
                 'wert': 0},
                {'description': '2demowert (2demoisin)',
                 'isin': '2demoisin',
                 'wert': 0},
                {'description': '3demowert (3demoisin)',
                 'isin': '3demoisin',
                 'wert': 0}],
            'konto': '2demokonto'},

    ]


def test_init_empty_should_return_error():
    set_up()
    persisted_state.DATABASE_INSTANCE = None

    context = add_depotauszug.index(GetRequest())

    assert '%Errortext' in context
    assert context['%Errortext'] == 'Bitte erfassen Sie zuerst ein Sparkonto vom Typ "Depot".'


def test_init_without_depotwert_should_return_error():
    set_up()
    persisted_state.DATABASE_INSTANCE = None
    sparkontos = persisted_state.database_instance().sparkontos
    sparkontos.add('1name', sparkontos.TYP_DEPOT)

    context = add_depotauszug.index(GetRequest())

    assert '%Errortext' in context
    assert context['%Errortext'] == 'Bitte erfassen Sie zuerst ein Depotwert.'


def test_transaction_id_should_be_in_context():
    set_up()
    context = add_depotauszug.index(GetRequest())
    assert 'ID' in context


def test_add():
    set_up()
    assert len(persisted_state.database_instance().depotauszuege.content) == 9

    add_depotauszug.index(VersionedPostRequest(
        {'action': 'add',
         'datum_2demokonto': rfc('01.03.2020'),
         'konto': '2demokonto',
         'wert_2demokonto_2demoisin': '100,00',
         'wert_2demokonto_3demoisin': '200,00'
         }
     ))

    db = persisted_state.database_instance()
    assert len(db.depotauszuege.content) == 11
    buchungen = db.depotauszuege.get_by(datum('01.03.2020'), '2demokonto')
    print(buchungen)

    assert len(buchungen) == 2

    assert buchungen.Wert[9] == 100
    assert buchungen.Konto[9] == '2demokonto'
    assert buchungen.Depotwert[9] == '2demoisin'
    assert buchungen.Datum[9] == datum('01.03.2020')

    assert buchungen.Wert[10] == 200
    assert buchungen.Konto[10] == '2demokonto'
    assert buchungen.Depotwert[10] == '3demoisin'
    assert buchungen.Datum[10] == datum('01.03.2020')


def test_add_with_empty_value_should_skip():
    set_up()
    persisted_state.database_instance().depotauszuege = Depotauszuege()

    assert len(persisted_state.database_instance().depotauszuege.content) == 0

    add_depotauszug.index(VersionedPostRequest(
        {'action': 'add',
         'datum_2demokonto': rfc('01.03.2020'),
         'konto': '2demokonto',
         'wert_2demokonto_2demoisin': '0,00',
         'wert_2demokonto_3demoisin': '0,00'
         }
     ))

    db = persisted_state.database_instance()
    assert len(db.depotauszuege.content) == 0

def test_add_with_empty_datum_should_return_error_page():
    set_up()
    persisted_state.database_instance().depotauszuege = Depotauszuege()

    assert len(persisted_state.database_instance().depotauszuege.content) == 0

    result = add_depotauszug.index(VersionedPostRequest(
        {'action': 'add',
         'konto': '2demokonto',
         'wert_2demokonto_2demoisin': '10,00',
         'wert_2demokonto_3demoisin': '10,00'
         }
     ))
    assert result['%Errortext'] == 'Interner Fehler <Kein Datum gefunden>.'

def test_add_order_should_show_in_recently_added():
    set_up()

    result = add_depotauszug.index(VersionedPostRequest(
        {'action': 'add',
         'datum_2demokonto': rfc('01.03.2020'),
         'konto': '2demokonto',
         'wert_2demokonto_2demoisin': '100,00'
         }
    ))

    result_element = list(result['letzte_erfassung'])[0]

    assert result_element['fa'] == 'plus'
    assert result_element['datum'] == '01.03.2020'
    assert result_element['konto'] == '2demokonto'
    assert result_element['depotwert'] == '2demoisin'
    assert result_element['wert'] == '100,00'


def test_add_order_for_existing_auszug_should_return_error():
    set_up()

    result = add_depotauszug.index(VersionedPostRequest(
        {'action': 'add',
         'datum_2demokonto': rfc('01.01.2020'),
         'konto': '2demokonto',
         'wert_2demokonto_2demoisin': '100,00'
         }
    ))

    assert '%Errortext' in result
    assert result['%Errortext'] == 'Für es besteht bereits ein Kontoauszug für 2demokonto am 01.01.2020'

def test_add_should_only_fire_once():
    set_up()
    next_id = request_handler.current_key()
    add_depotauszug.index(PostRequest(
        {'action': 'add',
         'ID': next_id,
         'datum_2demokonto': rfc('01.03.2020'),
         'konto': '2demokonto',
         'wert_2demokonto_2demoisin': '100,00'
         }
     ))
    add_depotauszug.index(PostRequest(
        {'action': 'add',
         'ID': next_id,
         'datum_2demokonto': rfc('01.03.2020'),
         'konto': 'overwritten',
         'wert_2demokonto_2demoisin': '9999,00'
         }
     ))

    buchungen = persisted_state.database_instance().depotauszuege.content
    assert len(buchungen) == 10
    assert buchungen.Wert[9] == 100
    assert buchungen.Konto[9] == '2demokonto'
    assert buchungen.Depotwert[9] == '2demoisin'
    assert buchungen.Datum[9] == datum('01.03.2020')


def test_edit():
    set_up()
    persisted_state.database_instance().depotauszuege = Depotauszuege()
    add_depotauszug.index(VersionedPostRequest(
        {'action': 'add',
         'datum_2demokonto': rfc('01.03.2020'),
         'konto': '2demokonto',
         'wert_2demokonto_2demoisin': '100,00'
         }
     ))

    result = add_depotauszug.index(VersionedPostRequest(
        {'action': 'add',
         'edit_index': 0,
         'datum_2demokonto': rfc('01.03.2020'),
         'konto': '2demokonto',
         'wert_2demokonto_2demoisin': '200,00'
         }
     ))

    db = persisted_state.database_instance()
    assert len(db.depotauszuege.content) == 1
    assert db.depotauszuege.content.Wert[0] == 200
    assert db.depotauszuege.content.Konto[0] == '2demokonto'
    assert db.depotauszuege.content.Depotwert[0] == '2demoisin'
    assert db.depotauszuege.content.Datum[0] == datum('01.03.2020')

    result_element = list(result['letzte_erfassung'])[0]

    assert result_element['fa'] == 'pencil'
    assert result_element['datum'] == '01.03.2020'
    assert result_element['konto'] == '2demokonto'
    assert result_element['depotwert'] == '2demoisin'
    assert result_element['wert'] == '200,00'


def test_edit_should_only_fire_once():
    set_up()
    persisted_state.database_instance().depotauszuege = Depotauszuege()
    add_depotauszug.index(VersionedPostRequest(
        {'action': 'add',
         'datum_2demokonto': rfc('01.03.2020'),
         'konto': '2demokonto',
         'wert_2demokonto_2demoisin': '100,00'
         }
    ))

    next_id = request_handler.current_key()
    add_depotauszug.index(PostRequest(
        {'action': 'add',
         'ID': next_id,
         'edit_index': 0,
         'datum_2demokonto': rfc('01.03.2020'),
         'konto': '2demokonto',
         'wert_2demokonto_2demoisin': '200,00'
         }
    ))

    add_depotauszug.index(PostRequest(
        {'action': 'add',
         'ID': next_id,
         'edit_index': 0,
         'datum_2demokonto': rfc('01.03.2020'),
         'konto': 'overwritten',
         'wert_2demokonto_2demoisin': '0,00'
         }
    ))

    db = persisted_state.database_instance()
    assert len(db.depotauszuege.content) == 1
    assert db.depotauszuege.content.Wert[0] == 200
    assert db.depotauszuege.content.Konto[0] == '2demokonto'
    assert db.depotauszuege.content.Depotwert[0] == '2demoisin'
    assert db.depotauszuege.content.Datum[0] == datum('01.03.2020')


def test_edit_call_from_ueberischt_should_preset_values_and_rename_button():
    set_up()

    context = add_depotauszug.index(PostRequest({'action': 'edit', 'edit_index': '8'}))

    assert context['approve_title'] == 'Depotauszug aktualisieren'
    assert context['default_items'] == [
        {
            'datum': '2020-01-02',
            'empty_items': [
                {'description': '1demowert (1demoisin)',
                 'isin': '1demoisin',
                 'wert': 0}],
            'filled_items': [
                {'description': '2demowert (2demoisin)',
                 'isin': '2demoisin',
                 'wert': 30},
                {'description': '3demowert (3demoisin)',
                 'isin': '3demoisin',
                 'wert': 40}],
            'konto': '2demokonto'}]


from datetime import date

from butler_offline.core.database import Database
from butler_offline.core.database.sparen.depotauszuege import Depotauszuege
from butler_offline.core.database.sparen.depotwerte import Depotwerte
from butler_offline.core.database.sparen.kontos import Kontos
from butler_offline.test.request_stubs import GetRequest, PostRequest
from butler_offline.test.test import assert_info_message_keine_depots_erfasst_in_context, \
    assert_info_message_keine_depotwerte_erfasst_in_context
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore.converter import datum_to_string
from butler_offline.viewcore.converter import german_to_rfc as rfc
from butler_offline.viewcore.state import non_persisted_state
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore.state.non_persisted_state import NonPersistedContext
from butler_offline.views.sparen import add_depotauszug
from butler_offline.views.sparen.add_depotauszug import AddDepotauszugContext


def initial_database() -> Database:
    database = Database(name="test")
    sparkontos = database.sparkontos
    sparkontos.add('1demokonto', Kontos.TYP_DEPOT)
    sparkontos.add('2demokonto', Kontos.TYP_DEPOT)

    depotwerte = database.depotwerte
    depotwerte.add(name='1demowert', isin='1demoisin', typ=depotwerte.TYP_ETF)
    depotwerte.add(name='2demowert', isin='2demoisin', typ=depotwerte.TYP_ETF)
    depotwerte.add(name='3demowert', isin='3demoisin', typ=depotwerte.TYP_ETF)

    # old depotauszug, alle isins gebucht
    depotauszuege = database.depotauszuege
    depotauszuege.add(datum('01.01.2020'), '1demoisin', '1demokonto', 1)
    depotauszuege.add(datum('01.01.2020'), '2demoisin', '1demokonto', 1)
    depotauszuege.add(datum('01.01.2020'), '3demoisin', '1demokonto', 1)
    depotauszuege.add(datum('01.01.2020'), '1demoisin', '2demokonto', 1)
    depotauszuege.add(datum('01.01.2020'), '2demoisin', '2demokonto', 1)
    depotauszuege.add(datum('01.01.2020'), '3demoisin', '2demokonto', 1)

    # new depotauszug
    depotauszuege.add(datum('02.01.2020'), '1demoisin', '1demokonto', 20)
    depotauszuege.add(datum('02.01.2020'), '2demoisin', '2demokonto', 30)
    depotauszuege.add(datum('02.01.2020'), '3demoisin', '2demokonto', 40)

    return database


def test_init():
    database = initial_database()
    context = add_depotauszug.handle_request(request=GetRequest(), context=AddDepotauszugContext(
        depotauszuege=database.depotauszuege,
        depotwerte=database.depotwerte,
        kontos=database.sparkontos
    ))
    assert context.get('approve_title') == 'Depotauszug hinzufügen'
    assert context.get('default_items') == [
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
    database = initial_database()
    context = add_depotauszug.handle_request(request=GetRequest(), context=AddDepotauszugContext(
        depotauszuege=Depotauszuege(),
        depotwerte=database.depotwerte,
        kontos=database.sparkontos
    ))

    assert context.get('approve_title') == 'Depotauszug hinzufügen'
    assert context.get('default_items') == [
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
    database = initial_database()

    depotauszuege = database.depotauszuege
    depotauszuege.add(datum('03.01.2020'), '1demoisin', '1demokonto', 0)
    depotauszuege.add(datum('03.01.2020'), '2demoisin', '1demokonto', 0)
    depotauszuege.add(datum('03.01.2020'), '3demoisin', '1demokonto', 0)
    depotauszuege.add(datum('03.01.2020'), '1demoisin', '2demokonto', 0)
    depotauszuege.add(datum('03.01.2020'), '2demoisin', '2demokonto', 0)
    depotauszuege.add(datum('03.01.2020'), '3demoisin', '2demokonto', 0)

    context = add_depotauszug.handle_request(request=GetRequest(), context=AddDepotauszugContext(
        depotauszuege=Depotauszuege(),
        depotwerte=database.depotwerte,
        kontos=database.sparkontos
    ))

    assert context.get('approve_title') == 'Depotauszug hinzufügen'
    assert context.get('default_items') == [
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


def test_init_with_empty_depots_should_return_error():
    depotwerte = Depotwerte()
    depotwerte.add(
        name='test',
        typ='asdf',
        isin='asdf'
    )
    context = add_depotauszug.handle_request(request=GetRequest(), context=AddDepotauszugContext(
        depotauszuege=Depotauszuege(),
        kontos=Kontos(),
        depotwerte=depotwerte
    ))
    assert_info_message_keine_depots_erfasst_in_context(context)


def test_init_empty_should_return_ok():
    context = add_depotauszug.handle_request(request=GetRequest(), context=AddDepotauszugContext(
        depotauszuege=Depotauszuege(),
        kontos=Kontos(),
        depotwerte=Depotwerte()
    ))
    assert len(context.get_info_messages()) == 2
    assert context.is_ok()


def test_init_without_depotwert_should_return_error():
    sparkontos = Kontos()
    sparkontos.add('1name', sparkontos.TYP_DEPOT)

    context = add_depotauszug.handle_request(request=GetRequest(), context=AddDepotauszugContext(
        depotauszuege=Depotauszuege(),
        depotwerte=Depotwerte(),
        kontos=sparkontos
    ))
    assert_info_message_keine_depotwerte_erfasst_in_context(context)


def test_transaction_id_should_be_in_context():
    database = initial_database()
    context = add_depotauszug.handle_request(request=GetRequest(),
                                             context=AddDepotauszugContext(
                                                 depotauszuege=database.depotauszuege,
                                                 depotwerte=database.depotwerte,
                                                 kontos=database.sparkontos
                                             ))

    assert context.is_transactional()


def test_add():
    database = initial_database()
    assert database.depotauszuege.select().count() == 9

    add_depotauszug.handle_request(request=PostRequest(
        {'action': 'add',
         'datum_2demokonto': rfc('01.03.2020'),
         'konto': '2demokonto',
         'wert_2demokonto_2demoisin': '100,00',
         'wert_2demokonto_3demoisin': '200,00'
         }
    ), context=AddDepotauszugContext(depotauszuege=database.depotauszuege,
                                     depotwerte=database.depotwerte,
                                     kontos=database.sparkontos))

    assert database.depotauszuege.select().count() == 11
    buchungen = database.depotauszuege.get_by(datum('01.03.2020'), '2demokonto')

    assert len(buchungen) == 2

    assert buchungen.Wert[9] == 100.00
    assert buchungen.Konto[9] == '2demokonto'
    assert buchungen.Depotwert[9] == '2demoisin'
    assert buchungen.Datum[9] == datum('01.03.2020')

    assert buchungen.Wert[10] == 200.00
    assert buchungen.Konto[10] == '2demokonto'
    assert buchungen.Depotwert[10] == '3demoisin'
    assert buchungen.Datum[10] == datum('01.03.2020')


def test_add_with_empty_value_should_skip():
    database = initial_database()
    database.depotauszuege = Depotauszuege()

    assert database.depotauszuege.select().count() == 0

    add_depotauszug.handle_request(request=PostRequest(
        {'action': 'add',
         'datum_2demokonto': rfc('01.03.2020'),
         'konto': '2demokonto',
         'wert_2demokonto_2demoisin': '0,00',
         'wert_2demokonto_3demoisin': '0,00'
         }
    ), context=AddDepotauszugContext(
        depotauszuege=database.depotauszuege,
        depotwerte=database.depotwerte,
        kontos=database.sparkontos))

    assert database.depotauszuege.select().count() == 0


def test_add_with_empty_datum_should_return_error_page():
    database = initial_database()

    result = add_depotauszug.handle_request(request=PostRequest(
        {'action': 'add',
         'konto': '2demokonto',
         'wert_2demokonto_2demoisin': '10,00',
         'wert_2demokonto_3demoisin': '10,00'
         }
    ), context=AddDepotauszugContext(
        depotauszuege=database.depotauszuege,
        kontos=database.sparkontos,
        depotwerte=database.depotwerte))

    assert result.is_error()
    assert result.error_text() == 'Interner Fehler <Kein Datum gefunden>.'


def test_add_order_should_show_in_recently_added():
    database = initial_database()

    result = add_depotauszug.handle_request(request=PostRequest(
        {'action': 'add',
         'datum_2demokonto': rfc('01.03.2020'),
         'konto': '2demokonto',
         'wert_2demokonto_2demoisin': '100,00'
         }
    ),
        context=AddDepotauszugContext(
            depotauszuege=database.depotauszuege,
            kontos=database.sparkontos,
            depotwerte=database.depotwerte))

    result_element = list(result.get('letzte_erfassung'))[0]

    assert result_element['fa'] == 'plus'
    assert result_element['datum'] == '01.03.2020'
    assert result_element['konto'] == '2demokonto'
    assert result_element['depotwert'] == '2demoisin'
    assert result_element['wert'] == '100,00'


def test_add_order_for_existing_auszug_should_return_error():
    database = initial_database()

    result = add_depotauszug.handle_request(request=PostRequest(
        {'action': 'add',
         'datum_2demokonto': rfc('01.01.2020'),
         'konto': '2demokonto',
         'wert_2demokonto_2demoisin': '100,00'
         }
    ),
        context=AddDepotauszugContext(
            depotauszuege=database.depotauszuege,
            kontos=database.sparkontos,
            depotwerte=database.depotwerte))

    assert result.is_error()
    assert result.error_text() == 'Für es besteht bereits ein Kontoauszug für 2demokonto am 01.01.2020'


def test_add_should_be_secured_by_request_handler():
    def index_handle():
        add_depotauszug.index(GetRequest())

    result = run_in_mocked_handler(index_handle=index_handle)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['sparen/add_depotauszug.html']


def test_edit():
    non_persisted_state.CONTEXT = NonPersistedContext()
    database = initial_database()
    database.depotauszuege = Depotauszuege()

    persisted_state.database_instance().depotauszuege = Depotauszuege()
    add_depotauszug.handle_request(request=PostRequest(
        {'action': 'add',
         'datum_2demokonto': rfc('01.03.2020'),
         'konto': '2demokonto',
         'wert_2demokonto_2demoisin': '100,00'
         }
    ),
        context=AddDepotauszugContext(
            depotauszuege=database.depotauszuege,
            depotwerte=database.depotwerte,
            kontos=database.sparkontos
        ))

    result = add_depotauszug.handle_request(request=PostRequest(
        {'action': 'add',
         'edit_index': 0,
         'datum_2demokonto': rfc('01.03.2020'),
         'konto': '2demokonto',
         'wert_2demokonto_2demoisin': '200,00'
         }
    ),
        context=AddDepotauszugContext(
            depotauszuege=database.depotauszuege,
            depotwerte=database.depotwerte,
            kontos=database.sparkontos
        ))

    assert database.depotauszuege.select().count() == 1
    assert database.depotauszuege.get(0) == {
        'Wert': 200.00,
        'Konto': '2demokonto',
        'Depotwert': '2demoisin',
        'Datum': datum('01.03.2020'),
        'index': 0
    }

    letzte_erfassungen = list(result.get('letzte_erfassung'))
    assert len(letzte_erfassungen) == 2
    assert letzte_erfassungen[0] == {
        'fa': 'pencil',
        'datum': '01.03.2020',
        'konto': '2demokonto',
        'depotwert': '2demoisin',
        'wert': '200,00'
    }


def test_edit_should_be_secured_by_request_handler():
    def index_handle():
        add_depotauszug.index(GetRequest())

    result = run_in_mocked_handler(index_handle)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['sparen/add_depotauszug.html']


def test_edit_call_from_ueberischt_should_preset_values_and_rename_button():
    database = initial_database()

    context = add_depotauszug.handle_request(
        request=PostRequest({'action': 'edit', 'edit_index': '8'}),
        context=AddDepotauszugContext(
            depotauszuege=database.depotauszuege,
            depotwerte=database.depotwerte,
            kontos=database.sparkontos)
    )

    assert context.get('approve_title') == 'Depotauszug aktualisieren'
    assert context.get('default_items') == [
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

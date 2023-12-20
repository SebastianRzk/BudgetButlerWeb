from butler_offline.core.database.sparen.kontos import Kontos
from butler_offline.core.database.sparen.sparbuchungen import Sparbuchungen
from butler_offline.test.request_stubs import GetRequest, PostRequest
from butler_offline.test.test import assert_info_message_kein_sparkonto_erfasst_in_context, assert_keine_message_set
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore.converter import german_to_rfc as rfc
from butler_offline.views.sparen import add_sparbuchung


def basic_context_with_konto(sparbuchungen: Sparbuchungen = Sparbuchungen()) -> add_sparbuchung.AddSparbuchungContext:
    kontos = Kontos()
    kontos.add('demokonto', Kontos.TYP_SPARKONTO)
    return basic_context(
        kontos=kontos,
        sparbuchungen=sparbuchungen
    )


def basic_context(
        kontos: Kontos = Kontos(),
        sparbuchungen: Sparbuchungen = Sparbuchungen()
) -> add_sparbuchung.AddSparbuchungContext:
    return add_sparbuchung.AddSparbuchungContext(
        kontos=kontos,
        sparbuchungen=sparbuchungen
    )


def test_init():
    context = add_sparbuchung.handle_request(
        request=GetRequest(),
        context=basic_context_with_konto()
    )
    assert context.is_ok()
    assert context.get('approve_title') == 'Sparbuchung hinzufügen'
    assert context.get('kontos') == ['demokonto']


def test_init_empty_should_add_info_message():
    context = add_sparbuchung.handle_request(
        request=GetRequest(),
        context=basic_context()
    )

    assert context.is_ok()
    assert_info_message_kein_sparkonto_erfasst_in_context(context)


def test_init_with_filled_database_should_have_no_message():
    kontos = Kontos()
    kontos.add(
        kontoname='testname',
        kontotyp=Kontos.TYP_SPARKONTO
    )
    context = add_sparbuchung.handle_request(
        request=GetRequest(),
        context=basic_context(
            kontos=kontos
        )
    )
    assert_keine_message_set(context)


def test_transaction_id_should_be_in_context():
    context = add_sparbuchung.handle_request(
        request=GetRequest(),
        context=basic_context()
    )
    assert context.is_transactional()


def test_add_should_add_sparbuchung():
    sparbuchungen = Sparbuchungen()
    add_sparbuchung.handle_request(
        request=PostRequest(
            {'action': 'add',
             'datum': rfc('1.1.2017'),
             'name': 'testname',
             'wert': '2,00',
             'typ': Sparbuchungen.TYP_MANUELLER_AUFTRAG,
             'eigenschaft': add_sparbuchung.EIGENSCHAFT_EINZAHLUNG,
             'konto': 'demokonto'
             }
        ),
        context=basic_context_with_konto(
            sparbuchungen=sparbuchungen
        ))

    assert sparbuchungen.select().count() == 1
    assert sparbuchungen.get(0) == {
        'Datum': datum('1.1.2017'),
        'Wert': float('2.00'),
        'Name': 'testname',
        'Typ': Sparbuchungen.TYP_MANUELLER_AUFTRAG,
        'Konto': 'demokonto',
        'index': 0,
        'Dynamisch': False
    }


def test_add_sparbuchung_should_show_in_recently_added():
    result = add_sparbuchung.handle_request(
        request=PostRequest(
            {'action': 'add',
             'datum': rfc('1.1.2017'),
             'name': 'testname',
             'wert': '2,00',
             'typ': Sparbuchungen.TYP_MANUELLER_AUFTRAG,
             'eigenschaft': add_sparbuchung.EIGENSCHAFT_EINZAHLUNG,
             'konto': 'demokonto'
             }
        ),
        context=basic_context_with_konto())

    result_element = list(result.get('letzte_erfassung'))[0]

    assert result_element['fa'] == 'plus'
    assert result_element['datum'] == '01.01.2017'
    assert result_element['konto'] == 'demokonto'
    assert result_element['name'] == 'testname'
    assert result_element['wert'] == '2,00'
    assert result_element['typ'] == Sparbuchungen.TYP_MANUELLER_AUFTRAG


def test_edit_sparbuchung():
    sparbuchungen = Sparbuchungen()
    add_sparbuchung.handle_request(
        request=PostRequest(
            {'action': 'add',
             'datum': rfc('1.1.2017'),
             'name': 'testname',
             'wert': '2,00',
             'typ': Sparbuchungen.TYP_MANUELLER_AUFTRAG,
             'eigenschaft': add_sparbuchung.EIGENSCHAFT_EINZAHLUNG,
             'konto': 'demokonto'
             }
        ),
        context=basic_context_with_konto(sparbuchungen=sparbuchungen))

    result = add_sparbuchung.handle_request(
        request=PostRequest(
            {'action': 'add',
             'edit_index': 0,
             'datum': rfc('2.2.2012'),
             'name': 'testname2',
             'wert': '3,00',
             'typ': Sparbuchungen.TYP_MANUELLER_AUFTRAG,
             'eigenschaft': add_sparbuchung.EIGENSCHAFT_EINZAHLUNG,
             'konto': 'demokonto2'
             }
        ),
        context=basic_context_with_konto(sparbuchungen=sparbuchungen)
    )

    assert sparbuchungen.select().count() == 1
    assert sparbuchungen.get(0) == {
        'Datum': datum('2.2.2012'),
        'Wert': float('3.00'),
        'Name': 'testname2',
        'Typ': Sparbuchungen.TYP_MANUELLER_AUFTRAG,
        'Konto': 'demokonto2',
        'index': 0,
        'Dynamisch': False
    }

    result_element = list(result.get('letzte_erfassung'))[0]

    assert result_element['fa'] == 'pencil'
    assert result_element['datum'] == '02.02.2012'
    assert result_element['konto'] == 'demokonto2'
    assert result_element['name'] == 'testname2'
    assert result_element['wert'] == '3,00'
    assert result_element['typ'] == Sparbuchungen.TYP_MANUELLER_AUFTRAG


def test_edit_call_from_uebersicht_should_preset_value_and_rename_button():
    sparbuchungen = Sparbuchungen()
    add_sparbuchung.handle_request(
        request=PostRequest(
            {'action': 'add',
             'datum': rfc('1.1.2017'),
             'name': 'testname',
             'wert': '2,00',
             'typ': Sparbuchungen.TYP_MANUELLER_AUFTRAG,
             'eigenschaft': add_sparbuchung.EIGENSCHAFT_EINZAHLUNG,
             'konto': 'demokonto'
             }
        ),
        context=basic_context_with_konto(sparbuchungen=sparbuchungen)
    )

    context = add_sparbuchung.handle_request(
        request=PostRequest({'action': 'edit', 'edit_index': '0'}),
        context=basic_context_with_konto(
            sparbuchungen=sparbuchungen
        )
    )
    assert context.is_ok()
    assert context.get('approve_title') == 'Sparbuchung aktualisieren'
    preset = context.get('default_item')

    assert preset['edit_index'] == '0'
    assert preset['datum'] == '2017-01-01'
    assert preset['konto'] == 'demokonto'
    assert preset['name'] == 'testname'
    assert preset['wert'] == '2,00'
    assert preset['eigenschaft'] == 'Einzahlung'
    assert preset['typ'] == Sparbuchungen.TYP_MANUELLER_AUFTRAG


def test_edit_call_from_uebersicht_should_preset_values_auszahlung():
    sparbuchungen = Sparbuchungen()
    add_sparbuchung.handle_request(
        request=PostRequest(
            {'action': 'add',
             'datum': rfc('1.1.2017'),
             'name': 'testname',
             'wert': '2,00',
             'typ': Sparbuchungen.TYP_MANUELLER_AUFTRAG,
             'eigenschaft': add_sparbuchung.EIGENSCHAFT_AUSZAHLUNG,
             'konto': 'demokonto'
             }
        ),
        context=basic_context_with_konto(sparbuchungen=sparbuchungen)
    )

    context = add_sparbuchung.handle_request(
        request=PostRequest({'action': 'edit', 'edit_index': '0'}),
        context=basic_context_with_konto(
            sparbuchungen=sparbuchungen
        )
    )

    assert context.get('approve_title') == 'Sparbuchung aktualisieren'
    preset = context.get('default_item')

    assert preset['wert'] == '2,00'
    assert preset['eigenschaft'] == 'Auszahlung'


def test_index_should_be_secured_by_request_handler():
    def index():
        add_sparbuchung.index(GetRequest())

    result = run_in_mocked_handler(index_handle=index)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['sparen/add_sparbuchung.html']

from butler_offline.core.database.sparen.depotwerte import Depotwerte
from butler_offline.core.database.sparen.kontos import Kontos
from butler_offline.core.database.sparen.orderdauerauftrag import OrderDauerauftrag
from butler_offline.core.frequency import ALL_FREQUENCY_NAMES
from butler_offline.test.request_stubs import GetRequest, PostRequest
from butler_offline.test.test import assert_info_message_keine_depotwerte_erfasst_in_context, \
    assert_info_message_keine_depots_erfasst_in_context
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore.converter import german_to_rfc as rfc
from butler_offline.views.sparen import add_orderdauerauftrag


def basic_context_with_demo_data(
        order_dauerauftrag: OrderDauerauftrag = OrderDauerauftrag()
):
    kontos = Kontos()
    depotwerte = Depotwerte()
    kontos.add('demokonto', Kontos.TYP_DEPOT)
    depotwerte.add(name='demowert', isin='demoisin', typ=depotwerte.TYP_ETF)
    return basic_context(
        depotwerte=depotwerte,
        kontos=kontos,
        order_dauerauftrag=order_dauerauftrag
    )


def basic_context(
        depotwerte: Depotwerte = Depotwerte(),
        kontos: Kontos = Kontos(),
        order_dauerauftrag: OrderDauerauftrag = OrderDauerauftrag()
):
    return add_orderdauerauftrag.AddOrderDauerauftragContext(
        depotwerte=depotwerte,
        kontos=kontos,
        order_dauerauftrag=order_dauerauftrag
    )


def test_init():
    context = add_orderdauerauftrag.handle_request(
        request=GetRequest(),
        context=basic_context_with_demo_data()
    )
    assert context.get('approve_title') == 'Order-Dauerauftrag hinzufügen'
    assert context.get('kontos') == ['demokonto']
    assert context.get('depotwerte') == [{'description': 'demowert (demoisin)', 'isin': 'demoisin'}]
    assert context.get('typen') == [add_orderdauerauftrag.TYP_KAUF, add_orderdauerauftrag.TYP_VERKAUF]
    assert context.get('rhythmen') == ALL_FREQUENCY_NAMES


def test_init_empty_should_return_show_infos():
    context = add_orderdauerauftrag.handle_request(
        request=GetRequest(),
        context=basic_context()
    )

    assert context.is_ok()
    assert len(context.get_info_messages()) == 2


def test_init_without_depotwert_should_return_error():
    kontos = Kontos()
    kontos.add('demokonto', Kontos.TYP_DEPOT)
    context = add_orderdauerauftrag.handle_request(
        request=GetRequest(),
        context=basic_context(
            kontos=kontos
        )
    )
    assert context.is_ok()
    assert_info_message_keine_depotwerte_erfasst_in_context(context)


def test_init_without_depot_should_return_error():
    depotwerte = Depotwerte()
    depotwerte.add(
        typ=Depotwerte.TYP_ETF,
        isin='isin',
        name='testname'
    )
    context = add_orderdauerauftrag.handle_request(
        request=GetRequest(),
        context=basic_context(
            depotwerte=depotwerte
        )
    )
    assert context.is_ok()
    assert_info_message_keine_depots_erfasst_in_context(context)


def test_transaction_id_should_be_in_context():
    context = add_orderdauerauftrag.handle_request(
        request=GetRequest(),
        context=basic_context_with_demo_data()
    )
    assert context.is_transactional()


def test_add():
    order_dauerauftrag = OrderDauerauftrag()
    context = add_orderdauerauftrag.handle_request(
        request=PostRequest(
            {'action': 'add',
             'startdatum': rfc('1.1.2017'),
             'endedatum': rfc('1.1.2018'),
             'rhythmus': 'monatlich',
             'name': 'testname',
             'wert': '2,00',
             'typ': add_orderdauerauftrag.TYP_KAUF,
             'depotwert': 'demoisin',
             'konto': 'demokonto'
             }
        ),
        context=basic_context_with_demo_data(
            order_dauerauftrag=order_dauerauftrag
        )
    )

    assert context.is_ok()
    assert order_dauerauftrag.select().count() == 1
    assert order_dauerauftrag.get(0) == {
        'Startdatum': datum('1.1.2017'),
        'Endedatum': datum('1.1.2018'),
        'Rhythmus': 'monatlich',
        'Wert': 2.00,
        'Name': 'testname',
        'Depotwert': 'demoisin',
        'Konto': 'demokonto',
        'index': 0
    }


def test_add_order_should_show_in_recently_added():
    result = add_orderdauerauftrag.handle_request(
        request=PostRequest(
            {'action': 'add',
             'startdatum': rfc('1.1.2017'),
             'endedatum': rfc('1.1.2018'),
             'rhythmus': 'monatlich',
             'name': 'testname',
             'wert': '2,00',
             'typ': add_orderdauerauftrag.TYP_KAUF,
             'depotwert': 'demoisin',
             'konto': 'demokonto'
             }
        ),
        context=basic_context_with_demo_data())
    result_element = list(result.get('letzte_erfassung'))[0]

    assert result_element['fa'] == 'plus'
    assert result_element['startdatum'] == '01.01.2017'
    assert result_element['endedatum'] == '01.01.2018'
    assert result_element['rhythmus'] == 'monatlich'
    assert result_element['konto'] == 'demokonto'
    assert result_element['name'] == 'testname'
    assert result_element['wert'] == '2,00'
    assert result_element['typ'] == add_orderdauerauftrag.TYP_KAUF
    assert result_element['depotwert'] == 'demoisin'


def test_edit():
    order_dauerauftrag = OrderDauerauftrag()
    add_orderdauerauftrag.handle_request(
        request=PostRequest(
            {'action': 'add',
             'startdatum': rfc('1.1.2017'),
             'endedatum': rfc('1.1.2018'),
             'rhythmus': 'monatlich',
             'name': 'testname',
             'wert': '2,00',
             'typ': add_orderdauerauftrag.TYP_KAUF,
             'depotwert': 'demoisin',
             'konto': 'demokonto'
             }
        ),
        context=basic_context_with_demo_data(order_dauerauftrag=order_dauerauftrag))

    result = add_orderdauerauftrag.handle_request(
        request=PostRequest(
            {'action': 'add',
             'edit_index': 0,
             'startdatum': rfc('2.1.2017'),
             'endedatum': rfc('2.1.2018'),
             'rhythmus': 'monatlich',
             'name': '2testname',
             'wert': '3,00',
             'typ': add_orderdauerauftrag.TYP_VERKAUF,
             'depotwert': '2demoisin',
             'konto': '2demokonto'
             }
        ),
        context=basic_context_with_demo_data(order_dauerauftrag=order_dauerauftrag))

    assert order_dauerauftrag.select().count() == 1
    assert order_dauerauftrag.get(0) == {
        'Startdatum': datum('2.1.2017'),
        'Endedatum': datum('2.1.2018'),
        'Rhythmus': 'monatlich',
        'Wert': -3.0,
        'Name': '2testname',
        'Depotwert': '2demoisin',
        'Konto': '2demokonto',
        'index': 0
    }
    result_element = list(result.get('letzte_erfassung'))[0]
    assert result_element['fa'] == 'pencil'
    assert result_element['startdatum'] == '02.01.2017'
    assert result_element['endedatum'] == '02.01.2018'
    assert result_element['rhythmus'] == 'monatlich'
    assert result_element['konto'] == '2demokonto'
    assert result_element['name'] == '2testname'
    assert result_element['depotwert'] == '2demoisin'
    assert result_element['wert'] == '3,00'
    assert result_element['typ'] == add_orderdauerauftrag.TYP_VERKAUF


def test_edit_call_from_ueberischt_should_preset_values_and_rename_button():
    order_dauerauftrag = OrderDauerauftrag()
    add_orderdauerauftrag.handle_request(
        request=PostRequest(
            {'action': 'add',
             'startdatum': rfc('1.1.2017'),
             'endedatum': rfc('1.1.2018'),
             'rhythmus': 'monatlich',
             'name': 'testname',
             'wert': '2.00',
             'typ': add_orderdauerauftrag.TYP_KAUF,
             'depotwert': 'demoisin',
             'konto': 'demokonto'
             }
        ),
        context=basic_context_with_demo_data(order_dauerauftrag=order_dauerauftrag))

    context = add_orderdauerauftrag.handle_request(
        request=PostRequest({'action': 'edit', 'edit_index': '0'}),
        context=basic_context_with_demo_data(order_dauerauftrag=order_dauerauftrag)
    )
    assert context.get('approve_title') == 'Order-Dauerauftrag aktualisieren'
    assert context.get('default_item') == {
        'edit_index': '0',
        'startdatum': '2017-01-01',
        'endedatum': '2018-01-01',
        'rhythmus': 'monatlich',
        'name': 'testname',
        'konto': 'demokonto',
        'wert': '2,00',
        'typ': add_orderdauerauftrag.TYP_KAUF,
        'depotwert': 'demoisin'
    }


def test_edit_call_from_ueberischt_should_preset_values_verkauf():
    order_dauerauftrag = OrderDauerauftrag()
    add_orderdauerauftrag.handle_request(
        request=PostRequest(
            {'action': 'add',
             'endedatum': rfc('1.1.2017'),
             'startdatum': rfc('1.1.2018'),
             'rhythmus': 'monatlich',
             'name': 'testname',
             'wert': '2,00',
             'typ': add_orderdauerauftrag.TYP_VERKAUF,
             'depotwert': 'demoisin',
             'konto': 'demokonto'
             }
        ),
        context=basic_context_with_demo_data(order_dauerauftrag=order_dauerauftrag)
    )

    context = add_orderdauerauftrag.handle_request(
        request=PostRequest({'action': 'edit', 'edit_index': '0'}),
        context=basic_context_with_demo_data(order_dauerauftrag)
    )
    assert context.get('approve_title') == 'Order-Dauerauftrag aktualisieren'
    preset = context.get('default_item')

    assert preset['wert'] == '2,00'
    assert preset['typ'] == add_orderdauerauftrag.TYP_VERKAUF


def test_index_should_be_secured_by_request_handler():
    def index():
        add_orderdauerauftrag.index(GetRequest())

    result = run_in_mocked_handler(index_handle=index)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['sparen/add_orderdauerauftrag.html']

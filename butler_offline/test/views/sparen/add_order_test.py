from butler_offline.core.database.sparen.depotwerte import Depotwerte
from butler_offline.core.database.sparen.kontos import Kontos
from butler_offline.core.database.sparen.order import Order
from butler_offline.test.core.database.builder import order_dict
from butler_offline.test.request_stubs import GetRequest, PostRequest
from butler_offline.test.test import assert_info_message_keine_depotwerte_erfasst_in_context, \
    assert_info_message_keine_depots_erfasst_in_context
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore.converter import german_to_rfc as rfc
from butler_offline.views.sparen import add_order


def get_basic_test_data():
    sparkontos = Kontos()
    sparkontos.add('demokonto', Kontos.TYP_DEPOT)

    depotwerte = Depotwerte()
    depotwerte.add(name='demowert', isin='demoisin', typ=depotwerte.TYP_ETF)

    return add_order.AddOrderContext(
        order=Order(),
        sparkontos=sparkontos,
        depotwerte=depotwerte
    )


def test_init():
    context = add_order.handle_request(
        GetRequest(),
        context=get_basic_test_data()
    )

    assert context.get('approve_title') == 'Order hinzufügen'
    assert context.get('kontos') == ['demokonto']
    assert context.get('depotwerte') == [{'description': 'demowert (demoisin)', 'isin': 'demoisin'}]
    assert context.get('typen') == [add_order.TYP_KAUF, add_order.TYP_VERKAUF]


def test_init_empty_should_show_infos():
    context = add_order.handle_request(
        GetRequest(),
        context=add_order.AddOrderContext(
            order=Order(),
            depotwerte=Depotwerte(),
            sparkontos=Kontos()
        )
    )

    assert context.is_ok()
    assert len(context.get_info_messages()) == 2


def test_init_with_missing_depot_should_show_info():
    depotwerte = Depotwerte()
    depotwerte.add(
        isin='asdf',
        name='asdf',
        typ=Depotwerte.TYP_ETF
    )
    context = add_order.handle_request(
        GetRequest(),
        context=add_order.AddOrderContext(
            order=Order(),
            depotwerte=depotwerte,
            sparkontos=Kontos()
        )
    )

    assert context.is_ok()
    assert_info_message_keine_depots_erfasst_in_context(context)


def test_init_without_depotwert_should_show_info():
    sparkontos = Kontos()
    sparkontos.add('1name', sparkontos.TYP_DEPOT)

    context = add_order.handle_request(
        GetRequest(),
        context=add_order.AddOrderContext(
            depotwerte=Depotwerte(),
            sparkontos=sparkontos,
            order=Order()
        )
    )

    assert context.is_ok()
    assert_info_message_keine_depotwerte_erfasst_in_context(context)


def test_transaction_id_should_be_in_context():
    context = add_order.handle_request(
        GetRequest(),
        get_basic_test_data()
    )
    assert context.is_transactional()


def test_add():
    context = get_basic_test_data()

    add_order.handle_request(
        request=PostRequest(
            {'action': 'add',
             'datum': rfc('1.1.2017'),
             'name': 'testname',
             'wert': '2.00',
             'typ': add_order.TYP_KAUF,
             'depotwert': 'demoisin',
             'konto': 'demokonto'
             }),
        context=context
    )

    assert context.order().select().count() == 1
    assert context.order().get(0) == {
        'Datum': datum('1.1.2017'),
        'Wert': 2.00,
        'Name': 'testname',
        'Depotwert': 'demoisin',
        'Konto': 'demokonto',
        'index': 0,
        'Dynamisch': False
    }


def test_add_order_should_show_in_recently_added():
    result = add_order.handle_request(
        PostRequest(
            {'action': 'add',
             'datum': rfc('1.1.2017'),
             'name': 'testname',
             'wert': '2,00',
             'typ': add_order.TYP_KAUF,
             'depotwert': 'demoisin',
             'konto': 'demokonto'
             }
        ),
        context=get_basic_test_data()
    )

    result_element = list(result.get('letzte_erfassung'))[0]

    assert result_element['fa'] == 'plus'
    assert result_element['datum'] == '01.01.2017'
    assert result_element['konto'] == 'demokonto'
    assert result_element['name'] == 'testname'
    assert result_element['wert'] == '2,00'
    assert result_element['typ'] == add_order.TYP_KAUF
    assert result_element['depotwert'] == 'demoisin'


def test_edit():
    context = get_basic_test_data()
    context.order().add(
        name='testname',
        wert=float('2.00'),
        datum=datum('01.01.2017'),
        depotwert='demoisin',
        dynamisch=False,
        konto='demokonto'
    )

    result = add_order.handle_request(
        request=PostRequest(
            {'action': 'add',
             'edit_index': 0,
             'datum': rfc('2.1.2017'),
             'name': '2testname',
             'wert': '3,00',
             'typ': add_order.TYP_VERKAUF,
             'depotwert': '2demoisin',
             'konto': '2demokonto'
             }
        ),
        context=context
    )

    assert context.order().select().count() == 1
    assert context.order().get(0) == order_dict(
        datum='2.1.2017',
        depotwert='2demoisin',
        konto='2demokonto',
        name='2testname',
        wert=-3.00,
    )

    result_element = list(result.get('letzte_erfassung'))[0]

    assert result_element['fa'] == 'pencil'
    assert result_element['datum'] == '02.01.2017'
    assert result_element['konto'] == '2demokonto'
    assert result_element['name'] == '2testname'
    assert result_element['depotwert'] == '2demoisin'
    assert result_element['wert'] == '3,00'
    assert result_element['typ'] == add_order.TYP_VERKAUF


def test_edit_call_from_uebersicht_should_preset_values_and_rename_button():
    context = get_basic_test_data()
    context.order().add(
        depotwert='demoisin',
        konto='demokonto',
        datum=datum('1.1.2017'),
        name='demoname',
        wert=2.10,
        dynamisch=False,
    )

    context = add_order.handle_request(
        PostRequest({'action': 'edit', 'edit_index': '0'}),
        context=context
    )
    assert context.get('approve_title') == 'Order aktualisieren'
    assert context.get('default_item') == {
        'edit_index': '0',
        'datum': '2017-01-01',
        'konto': 'demokonto',
        'name': 'demoname',
        'wert': '2,10',
        'typ': add_order.TYP_KAUF,
        'depotwert': 'demoisin'
    }


def test_edit_call_from_ueberischt_should_preset_values_verkauf():
    context = get_basic_test_data()
    context.order().add(
        depotwert='demoisin',
        konto='demokonto',
        datum=datum('1.1.2017'),
        name='demoname',
        wert=-2.10,
        dynamisch=False,
    )

    context = add_order.handle_request(
        PostRequest({'action': 'edit', 'edit_index': '0'}),
        context=context
    )
    assert context.get('approve_title') == 'Order aktualisieren'

    assert context.get('approve_title') == 'Order aktualisieren'
    assert context.get('default_item') == {
        'edit_index': '0',
        'datum': '2017-01-01',
        'konto': 'demokonto',
        'name': 'demoname',
        'wert': '2,10',
        'typ': add_order.TYP_VERKAUF,
        'depotwert': 'demoisin'
    }


def test_index_should_be_secured_by_request_handler():
    def index():
        add_order.index(GetRequest())

    result = run_in_mocked_handler(index_handle=index)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['sparen/add_order.html']

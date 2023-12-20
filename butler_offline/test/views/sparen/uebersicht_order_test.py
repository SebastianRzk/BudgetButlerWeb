from butler_offline.test.request_stubs import GetRequest
from butler_offline.test.request_stubs import PostRequest
from butler_offline.views.sparen import uebersicht_order
from butler_offline.viewcore.converter import datum_from_german
from butler_offline.core.database.sparen.order import Order
from butler_offline.core.database.sparen.depotwerte import Depotwerte
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler
from butler_offline.viewcore.renderhelper import Betrag
from butler_offline.test.test import assert_info_message_keine_order_erfasst_in_context, assert_keine_message_set


def basic_test_context(depotwerte: Depotwerte = Depotwerte,
                       order: Order = Order()) -> uebersicht_order.UebersichtOrderContext:
    return uebersicht_order.UebersichtOrderContext(
        depotwerte=depotwerte,
        order=order
    )


def test_transaction_id_should_be_in_context():
    context = uebersicht_order.handle_request(
        request=GetRequest(),
        context=basic_test_context()
    )
    assert context.is_transactional()


def context_with_test_data() -> uebersicht_order.UebersichtOrderContext:
    depotwerte = Depotwerte()
    depotwerte.add(name='depotwert1', isin='isin1', typ=depotwerte.TYP_ETF)

    order = Order()
    order.add(datum_from_german('01.01.2020'), '1name', '1konto', 'isin1', 100)
    order.add(datum_from_german('02.02.2020'), '2name', '2konto', 'isin1', -200)

    return basic_test_context(
        depotwerte=depotwerte,
        order=order
    )


def test_should_list_order():
    result = uebersicht_order.handle_request(
        request=GetRequest(),
        context=context_with_test_data()
    )

    assert result.get('order') == [
        {'Datum': '01.01.2020',
         'Depotwert': 'depotwert1 (isin1)',
         'Konto': '1konto',
         'Name': '1name',
         'Typ': 'Kauf',
         'index': 0,
         'Wert': Betrag(100),
         'Dynamisch': False},
        {'Datum': '02.02.2020',
         'Depotwert': 'depotwert1 (isin1)',
         'Konto': '2konto',
         'Name': '2name',
         'Typ': 'Verkauf',
         'index': 1,
         'Wert': Betrag(200),
         'Dynamisch': False},
    ]


def test_init_with_empty_database_should_add_info_message():
    result = uebersicht_order.handle_request(
        request=GetRequest(),
        context=basic_test_context()
    )
    assert result.is_ok()
    assert_info_message_keine_order_erfasst_in_context(result=result)


def test_init_filled_database_should_have_no_message_set():
    result = uebersicht_order.handle_request(
        request=GetRequest(),
        context=context_with_test_data()
    )
    assert result.is_ok()
    assert_keine_message_set(result=result)


def test_delete():
    context = context_with_test_data()
    uebersicht_order.handle_request(
        request=PostRequest({'action': 'delete', 'delete_index': '1'}),
        context=context
    )

    order = context.order()
    assert order.select().count() == 1
    assert order.get(0) == {
        'Datum': datum_from_german('01.01.2020'),
        'Depotwert': 'isin1',
        'Konto': '1konto',
        'Name': '1name',
        'Wert': 100,
        'index': 0,
        'Dynamisch': False
    }


def test_index_should_be_secured_by_request_handler():
    def index():
        uebersicht_order.index(GetRequest())

    result = run_in_mocked_handler(index_handle=index)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['sparen/uebersicht_order.html']

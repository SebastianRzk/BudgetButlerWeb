from butler_offline.core.database.sparen.orderdauerauftrag import OrderDauerauftrag
from butler_offline.test.request_stubs import GetRequest, PostRequest
from butler_offline.test.test import assert_info_message_keine_order_dauerauftraege_erfasst_in_context, \
    assert_keine_message_set
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.views.sparen import uebersicht_orderdauerauftrag


def generate_basic_context(
        orderdauerauftrag: OrderDauerauftrag = OrderDauerauftrag()
) -> uebersicht_orderdauerauftrag.UbersichtOrderDauerauftragContext:
    return uebersicht_orderdauerauftrag.UbersichtOrderDauerauftragContext(
        orderdauerauftrag=orderdauerauftrag
    )


def test_init_with_empty_database_should_show_message():
    result = uebersicht_orderdauerauftrag.handle_request(request=GetRequest(), context=generate_basic_context())
    assert result.is_ok()
    assert_info_message_keine_order_dauerauftraege_erfasst_in_context(result=result)


def test_init_with_filled_database_should_show_no_message():
    orderdauerauftrag = OrderDauerauftrag()
    orderdauerauftrag.add(datum('01.01.2011'), datum('01.01.2011'), 'monatlich', '1name', '1konto ', '1depotwert', 11)
    result = uebersicht_orderdauerauftrag.handle_request(request=GetRequest(), context=generate_basic_context(
        orderdauerauftrag=orderdauerauftrag
    ))
    assert result.is_ok()
    assert_keine_message_set(result=result)


def test_transaction_id_should_be_in_context():
    context = uebersicht_orderdauerauftrag.handle_request(request=GetRequest(), context=generate_basic_context())
    assert context.is_transactional()


def test_delete():
    orderdauerauftrag = OrderDauerauftrag()
    orderdauerauftrag.add(datum('01.01.2011'), datum('01.01.2011'), 'monatlich', '1name', '1konto ', '1depotwert', 11)
    orderdauerauftrag.add(datum('01.01.2011'), datum('01.01.2011'), 'monatlich', '2name', '1konto ', '1depotwert', 11)

    uebersicht_orderdauerauftrag.handle_request(
        request=PostRequest({'action': 'delete', 'delete_index': '1'}),
        context=generate_basic_context(orderdauerauftrag=orderdauerauftrag)
    )

    assert orderdauerauftrag.select().count() == 1
    assert orderdauerauftrag.get(0)['Name'] == '1name'


def test_german_datum():
    orderdauerauftrag = OrderDauerauftrag()
    orderdauerauftrag.add(datum('01.01.2011'), datum('01.01.2011'), 'monatlich', '1name', '1konto ', '1depotwert', 11)

    result = uebersicht_orderdauerauftrag.handle_request(
        request=GetRequest(),
        context=generate_basic_context(orderdauerauftrag=orderdauerauftrag)
    )

    result_dauerauftrag = result.get('dauerauftraege')['Vergangene  Daueraufträge'][0]
    assert result_dauerauftrag['Startdatum'] == '01.01.2011'
    assert result_dauerauftrag['Endedatum'] == '01.01.2011'


def test_index_should_be_secured_by_request_handler():
    def index():
        uebersicht_orderdauerauftrag.index(GetRequest())

    result = run_in_mocked_handler(index_handle=index)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['sparen/uebersicht_orderdauerauftrag.html']

from butler_offline.core.database.sparen.orderdauerauftrag import OrderDauerauftrag
from butler_offline.core.frequency import FREQUENCY_JAEHRLICH_NAME
from butler_offline.test.request_stubs import GetRequest
from butler_offline.test.test import assert_keine_message_set, \
    assert_info_message_keine_order_dauerauftraege_erfasst_in_context
from butler_offline.viewcore.context.builder import generate_page_context, PageContext
from butler_offline.viewcore.converter import datum_from_german
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.requirements import order_dauerauftrag_needed_decorator


class OrderDauerauftragContext:
    def __init__(self, orderdauerauftrag: OrderDauerauftrag):
        self._orderdauerauftrag = orderdauerauftrag

    def orderdauerauftrag(self) -> OrderDauerauftrag:
        return self._orderdauerauftrag


@order_dauerauftrag_needed_decorator()
def _run_dektorierte_order_dauerauftrag(_: Request, context: OrderDauerauftragContext) -> PageContext:
    return generate_page_context('asdf')


def test_depotwerte_needed_decorator_with_missing_depotwerte_should_add_message():
    result = _run_dektorierte_order_dauerauftrag(GetRequest(), OrderDauerauftragContext(
        orderdauerauftrag=OrderDauerauftrag()
    ))
    assert_info_message_keine_order_dauerauftraege_erfasst_in_context(result)


def test_depotwerte_needed_decorator_with_depotwerte_should_do_nothing():
    orderdauerauftrag = OrderDauerauftrag()
    orderdauerauftrag.add(
        startdatum=datum_from_german('01.01.2023'),
        endedatum=datum_from_german('01.01.2023'),
        depotwert='asdf',
        konto='asdf',
        name='asdf',
        wert=123,
        rhythmus=FREQUENCY_JAEHRLICH_NAME
    )
    result = _run_dektorierte_order_dauerauftrag(GetRequest(),
                                                 OrderDauerauftragContext(orderdauerauftrag=orderdauerauftrag))
    assert_keine_message_set(result)

from butler_offline.core.database.sparen.order import Order
from butler_offline.test.request_stubs import GetRequest
from butler_offline.test.test import assert_keine_message_set, \
    assert_info_message_keine_order_erfasst_in_context
from butler_offline.viewcore.context.builder import generate_page_context, PageContext
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.requirements import order_needed_decorator
from butler_offline.viewcore.converter import datum_from_german


class OrderContext:
    def __init__(self, order: Order):
        self._order = order

    def order(self) -> Order:
        return self._order


@order_needed_decorator()
def _run_dektorierte_depotwerte(_: Request, context: OrderContext) -> PageContext:
    return generate_page_context('asdf')


def test_depotwerte_needed_decorator_with_missing_depotwerte_should_add_message():
    result = _run_dektorierte_depotwerte(GetRequest(), OrderContext(order=Order()))
    assert_info_message_keine_order_erfasst_in_context(result)


def test_depotwerte_needed_decorator_with_depotwerte_should_do_nothing():
    order = Order()
    order.add(
        datum=datum_from_german('01.01.2023'),
        depotwert='asdf',
        konto='asdf',
        name='asdf',
        wert=123
    )
    result = _run_dektorierte_depotwerte(GetRequest(), OrderContext(order=order))
    assert_keine_message_set(result)

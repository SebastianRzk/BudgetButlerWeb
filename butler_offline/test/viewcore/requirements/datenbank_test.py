from butler_offline.core.database.sparen.order import Order
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.test.request_stubs import GetRequest
from butler_offline.test.test import assert_keine_message_set, \
    assert_info_message_nichts_erfasst_in_context
from butler_offline.viewcore.context.builder import generate_page_context, PageContext
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.requirements import irgendwas_needed_decorator
from butler_offline.viewcore.converter import datum_from_german


class Context:
    def __init__(self, order: Order, einzelbuchungen: Einzelbuchungen):
        self._order = order
        self._einzelbuchungen = einzelbuchungen

    def order(self) -> Order:
        return self._order

    def einzelbuchungen(self) -> Einzelbuchungen:
        return self._einzelbuchungen


@irgendwas_needed_decorator()
def _run(_: Request, context: Context) -> PageContext:
    return generate_page_context('asdf')


def test_depotwerte_needed_decorator_with_missing_depotwerte_should_add_message():
    result = _run(GetRequest(), Context(order=Order(), einzelbuchungen=Einzelbuchungen()))
    assert_info_message_nichts_erfasst_in_context(result)


def test_depotwerte_needed_decorator_with_depotwerte_should_do_nothing():
    order = Order()
    order.add(
        datum=datum_from_german('01.01.2023'),
        depotwert='asdf',
        konto='asdf',
        name='asdf',
        wert=123
    )
    result = _run(GetRequest(), Context(order=order, einzelbuchungen=Einzelbuchungen()))
    assert_keine_message_set(result)

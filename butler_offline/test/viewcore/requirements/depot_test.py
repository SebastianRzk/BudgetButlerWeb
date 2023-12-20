from butler_offline.core.database.sparen.kontos import Kontos
from butler_offline.test.request_stubs import GetRequest
from butler_offline.test.test import assert_keine_message_set, \
    assert_info_message_keine_depots_erfasst_in_context
from butler_offline.viewcore.context.builder import generate_page_context, PageContext
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.requirements import depots_needed_decorator


class DepotContext:
    def __init__(self, kontos: Kontos):
        self._kontos = kontos

    def kontos(self) -> Kontos:
        return self._kontos


@depots_needed_decorator()
def _run_dektorierte_depots(_: Request, context: DepotContext) -> PageContext:
    return generate_page_context('asdf')


def test_depots_needed_decorator_with_missing_depots_should_add_message():
    result = _run_dektorierte_depots(GetRequest(), DepotContext(kontos=Kontos()))
    assert_info_message_keine_depots_erfasst_in_context(result)


def test_depots_needed_decorator_with_depot_should_do_nothing():
    kontos = Kontos()
    kontos.add(
        kontoname='Test',
        kontotyp=Kontos.TYP_DEPOT
    )
    result = _run_dektorierte_depots(GetRequest(), DepotContext(kontos=kontos))
    assert_keine_message_set(result)

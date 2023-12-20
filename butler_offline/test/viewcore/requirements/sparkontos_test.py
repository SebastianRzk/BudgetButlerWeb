from butler_offline.core.database.sparen.kontos import Kontos
from butler_offline.test.request_stubs import GetRequest
from butler_offline.test.test import assert_keine_message_set, \
    assert_info_message_kein_sparkonto_erfasst_in_context
from butler_offline.test.viewcore.requirements.depot_test import DepotContext
from butler_offline.viewcore.context.builder import generate_page_context, PageContext
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.requirements import sparkontos_needed_decorator


@sparkontos_needed_decorator()
def _run_dektorierte_sparkontos(_: Request, context: DepotContext) -> PageContext:
    return generate_page_context('asdf')


def test_sparkontos_needed_decorator_with_missing_sparkonto_should_add_message():
    result = _run_dektorierte_sparkontos(GetRequest(), DepotContext(kontos=Kontos()))
    assert_info_message_kein_sparkonto_erfasst_in_context(result)


def test_sparkontos_needed_decorator_with_sparkonto_should_do_nothing():
    kontos = Kontos()
    kontos.add(
        kontotyp=Kontos.TYP_SPARKONTO,
        kontoname='asdf'
    )

    result = _run_dektorierte_sparkontos(GetRequest(), DepotContext(kontos=kontos))
    assert_keine_message_set(result)

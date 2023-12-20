from butler_offline.core.database.sparen.depotwerte import Depotwerte
from butler_offline.test.request_stubs import GetRequest
from butler_offline.test.test import assert_keine_message_set, \
    assert_info_message_keine_depotwerte_erfasst_in_context
from butler_offline.viewcore.context.builder import generate_page_context, PageContext
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.requirements import depotwerte_needed_decorator


class DepotwerteContext:
    def __init__(self, depotwerte: Depotwerte):
        self._depotwerte = depotwerte

    def depotwerte(self) -> Depotwerte:
        return self._depotwerte


@depotwerte_needed_decorator()
def _run_dektorierte_depotwerte(_: Request, context: DepotwerteContext) -> PageContext:
    return generate_page_context('asdf')


def test_depotwerte_needed_decorator_with_missing_depotwerte_should_add_message():
    result = _run_dektorierte_depotwerte(GetRequest(), DepotwerteContext(depotwerte=Depotwerte()))
    assert_info_message_keine_depotwerte_erfasst_in_context(result)


def test_depotwerte_needed_decorator_with_depotwerte_should_do_nothing():
    depotwerte = Depotwerte()
    depotwerte.add(
        isin='isin',
        typ=Depotwerte.TYP_ETF,
        name='my name'
    )
    result = _run_dektorierte_depotwerte(GetRequest(), DepotwerteContext(depotwerte=depotwerte))
    assert_keine_message_set(result)

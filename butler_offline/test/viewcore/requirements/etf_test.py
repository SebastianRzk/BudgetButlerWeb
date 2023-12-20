from butler_offline.core.database.sparen.depotwerte import Depotwerte
from butler_offline.test.request_stubs import GetRequest
from butler_offline.test.test import assert_keine_message_set, \
    assert_info_message_keine_etfs_erfasst_in_context
from butler_offline.test.viewcore.requirements.depotwerte_test import DepotwerteContext
from butler_offline.viewcore.context.builder import generate_page_context, PageContext
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.requirements import etfs_needed_decorator


@etfs_needed_decorator()
def _run_dektorierte_etfs(_: Request, context: DepotwerteContext) -> PageContext:
    return generate_page_context('asdf')


def test_depotwerte_needed_decorator_with_missing_depotwerte_should_add_message():
    result = _run_dektorierte_etfs(GetRequest(), DepotwerteContext(depotwerte=Depotwerte()))
    assert_info_message_keine_etfs_erfasst_in_context(result)


def test_depotwerte_needed_decorator_with_depotwerte_should_do_nothing():
    depotwerte = Depotwerte()
    depotwerte.add(
        isin='isin12345512',
        typ=Depotwerte.TYP_ETF,
        name='my name'
    )
    result = _run_dektorierte_etfs(GetRequest(), DepotwerteContext(depotwerte=depotwerte))
    assert_keine_message_set(result)

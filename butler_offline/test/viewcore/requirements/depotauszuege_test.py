from butler_offline.core.database.sparen.depotauszuege import Depotauszuege
from butler_offline.test.request_stubs import GetRequest
from butler_offline.test.test import assert_keine_message_set, \
    assert_info_message_keine_depotauszuege_erfasst_in_context
from butler_offline.viewcore.context.builder import generate_page_context, PageContext
from butler_offline.viewcore.converter import datum_from_german
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.requirements import depotauszug_needed_decorator


class DepotauszuegeContext:
    def __init__(self, depotauszuege: Depotauszuege):
        self._depotauszuege = depotauszuege

    def depotauszuege(self) -> Depotauszuege:
        return self._depotauszuege


@depotauszug_needed_decorator()
def _run_dektorierte_depotauszuege(_: Request, context: DepotauszuegeContext) -> PageContext:
    return generate_page_context('asdf')


def test_depotauszuge_needed_decorator_with_missing_depotauszug_should_add_message():
    result = _run_dektorierte_depotauszuege(GetRequest(), DepotauszuegeContext(depotauszuege=Depotauszuege()))
    assert_info_message_keine_depotauszuege_erfasst_in_context(result)


def test_depotauszuege_needed_decorator_with_depotauszuge_should_do_nothing():
    depotauszuege = Depotauszuege()
    depotauszuege.add(
        wert=123,
        datum=datum_from_german('01.01.2023'),
        depotwert='asdf',
        konto='asdf'
    )
    result = _run_dektorierte_depotauszuege(GetRequest(), DepotauszuegeContext(depotauszuege=depotauszuege))
    assert_keine_message_set(result)

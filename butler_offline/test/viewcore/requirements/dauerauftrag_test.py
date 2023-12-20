from butler_offline.core.database.dauerauftraege import Dauerauftraege
from butler_offline.core.frequency import FREQUENCY_JAEHRLICH_NAME
from butler_offline.test.request_stubs import GetRequest
from butler_offline.test.test import assert_keine_message_set, \
    assert_info_message_dauerauftraege_erfasst_in_context
from butler_offline.viewcore.context.builder import generate_page_context, PageContext
from butler_offline.viewcore.converter import datum_from_german
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.requirements import dauerauftrag_needed_decorator


class DauerauftragContext:
    def __init__(self, dauerauftraege: Dauerauftraege):
        self._dauerauftraege = dauerauftraege

    def dauerauftraege(self) -> Dauerauftraege:
        return self._dauerauftraege


@dauerauftrag_needed_decorator()
def _run_dektorierte_dauerauftraege(_: Request, context: DauerauftragContext) -> PageContext:
    return generate_page_context('asdf')


def test_dauerauftrag_needed_decorator_with_missing_dauerauftrag_should_add_message():
    result = _run_dektorierte_dauerauftraege(GetRequest(), DauerauftragContext(dauerauftraege=Dauerauftraege()))
    assert_info_message_dauerauftraege_erfasst_in_context(result)


def test_dauerauftrag_needed_decorator_with_dauerauftrag_should_do_nothing():
    dauerauftraege = Dauerauftraege()
    dauerauftraege.add(
        startdatum=datum_from_german('01.01.2023'),
        endedatum=datum_from_german('01.01.2023'),
        name='test',
        kategorie='test',
        wert=123,
        rhythmus=FREQUENCY_JAEHRLICH_NAME
    )
    result = _run_dektorierte_dauerauftraege(GetRequest(), DauerauftragContext(dauerauftraege=dauerauftraege))
    assert_keine_message_set(result)

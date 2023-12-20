from butler_offline.core.database.sparen.sparbuchungen import Sparbuchungen
from butler_offline.test.request_stubs import GetRequest
from butler_offline.test.test import assert_keine_message_set, \
    assert_info_message_keine_sparbuchungen_erfasst_in_context
from butler_offline.viewcore.context.builder import generate_page_context, PageContext
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.requirements import sparbuchungen_needed_decorator
from butler_offline.viewcore.converter import datum_from_german



class SparbuchungContext:
    def __init__(self, sparbuchungen: Sparbuchungen):
        self._sparbuchungen = sparbuchungen

    def sparbuchungen(self) -> Sparbuchungen:
        return self._sparbuchungen


@sparbuchungen_needed_decorator()
def _run_dektorierte_sparbuchungen(_: Request, context: SparbuchungContext) -> PageContext:
    return generate_page_context('asdf')


def test_sparkontos_needed_decorator_with_missing_sparkonto_should_add_message():
    result = _run_dektorierte_sparbuchungen(GetRequest(), SparbuchungContext(sparbuchungen=Sparbuchungen()))
    assert_info_message_keine_sparbuchungen_erfasst_in_context(result)


def test_sparkontos_needed_decorator_with_sparkonto_should_do_nothing():
    sparbuchungen = Sparbuchungen()
    sparbuchungen.add(
        konto='asdf',
        wert=123,
        name='asdf',
        typ=Sparbuchungen.TYP_ZINSEN,
        datum=datum_from_german('01.01.2023')
    )

    result = _run_dektorierte_sparbuchungen(GetRequest(), SparbuchungContext(sparbuchungen=sparbuchungen))
    assert_keine_message_set(result)

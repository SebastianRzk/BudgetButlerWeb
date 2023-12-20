from butler_offline.core.database.gemeinsamebuchungen import Gemeinsamebuchungen
from butler_offline.test.request_stubs import GetRequest
from butler_offline.test.test import assert_keine_message_set, \
    assert_info_message_keine_gemeinsame_buchungen_erfasst_in_context
from butler_offline.viewcore.context.builder import generate_page_context, PageContext
from butler_offline.viewcore.converter import datum_from_german
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.requirements import gemeinsame_buchung_needed_decorator


class GemeinsameBuchungenContext:
    def __init__(self, gemeinsamebuchungen: Gemeinsamebuchungen):
        self._gemeinsamebuchungen = gemeinsamebuchungen

    def gemeinsamebuchungen(self) -> Gemeinsamebuchungen:
        return self._gemeinsamebuchungen


@gemeinsame_buchung_needed_decorator()
def _run_dektorierte_gemeinsamebuchungen(_: Request, context: GemeinsameBuchungenContext) -> PageContext:
    return generate_page_context('asdf')


def test_gemeinsame_buchungen_needed_decorator_with_missing_gemeinsamer_buchung_should_add_message():
    result = _run_dektorierte_gemeinsamebuchungen(GetRequest(),
                                                  GemeinsameBuchungenContext(gemeinsamebuchungen=Gemeinsamebuchungen()))
    assert_info_message_keine_gemeinsame_buchungen_erfasst_in_context(result)


def test_gemeinsame_buchungen_needed_decorator_with_gemeinsamer_buchung_should_do_nothing():
    gemeinsame_buchungen = Gemeinsamebuchungen()
    gemeinsame_buchungen.add(
        ausgaben_datum=datum_from_german('01.01.2023'),
        ausgaben_name='test',
        kategorie='test',
        wert=123,
        person='Testperson'
    )
    result = _run_dektorierte_gemeinsamebuchungen(GetRequest(),
                                                  GemeinsameBuchungenContext(gemeinsamebuchungen=gemeinsame_buchungen))
    assert_keine_message_set(result)

from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.test.request_stubs import GetRequest
from butler_offline.test.test import assert_info_message_keine_buchungen_erfasst_in_context, assert_keine_message_set
from butler_offline.viewcore.context.builder import generate_page_context, PageContext
from butler_offline.viewcore.converter import datum_from_german
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.requirements import einzelbuchung_needed_decorator


class BuchungContext:
    def __init__(self, einzelbuchungen: Einzelbuchungen):
        self._einzelbuchungen = einzelbuchungen

    def einzelbuchungen(self) -> Einzelbuchungen:
        return self._einzelbuchungen


@einzelbuchung_needed_decorator()
def _run_dektorierte_buchung(_: Request, context: BuchungContext) -> PageContext:
    return generate_page_context('asdf')


def test_einzelbuchung_needed_decorator_with_missing_einzelbuchung_should_add_message():
    result = _run_dektorierte_buchung(GetRequest(), BuchungContext(einzelbuchungen=Einzelbuchungen()))
    assert_info_message_keine_buchungen_erfasst_in_context(result)


def test_einzelbuchung_needed_decorator_with_einzelbuchung_should_do_nothing():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(
        datum=datum_from_german('01.01.2023'),
        name='test',
        kategorie='test',
        wert=123,
        dynamisch=False
    )
    result = _run_dektorierte_buchung(GetRequest(), BuchungContext(einzelbuchungen=einzelbuchungen))
    assert_keine_message_set(result)


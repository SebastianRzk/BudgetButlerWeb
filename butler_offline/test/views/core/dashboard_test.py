from butler_offline.views.core import dashboard
from butler_offline.viewcore.context.builder import PageContext
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.test.request_stubs import GetRequest
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler
from datetime import date


def test_init_with_empty_database():
    dashboard.handle_request(None, dashboard.DashboardContext(
        einzelbuchungen=Einzelbuchungen(),
        today=date(2018, 2, 13)
    ))


def test_should_return_month_list():
    result: PageContext = dashboard.handle_request(None, dashboard.DashboardContext(
        einzelbuchungen=Einzelbuchungen(),
        today=date(2018, 2, 13)
    ))

    assert result.get('zusammenfassung_monatsliste') == \
           "['August', 'September', 'Oktober', 'November', 'Dezember', 'Januar', 'Februar']"


def test_with_entry_should_return_german_date():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(date(2019, 2, 16), 'eine einnahme kategorie', 'some name', 10)

    result: PageContext = dashboard.handle_request(
        None,
        dashboard.DashboardContext(
            einzelbuchungen=einzelbuchungen,
            today=date(2019, 2, 17)
        )
    )
    assert result.get('ausgaben_des_aktuellen_monats') == [
        {'index': 0, 'Datum': '16.02.2019', 'Name': 'some name', 'Kategorie': 'eine einnahme kategorie',
         'Wert': '10,00', 'Dynamisch': False, 'Tags': []}]


def test_index_should_be_secured_by_request_handler():
    def handle():
        dashboard.index(request=GetRequest())

    result = run_in_mocked_handler(handle)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['core/dashboard.html']

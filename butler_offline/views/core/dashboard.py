import datetime

from butler_offline.core import time
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.context.builder import generate_page_context
from butler_offline.viewcore.converter import to_descriptive_list


class DashboardContext:
    def __init__(self, einzelbuchungen: Einzelbuchungen, today: datetime.date):
        self._today = today
        self._einzelbuchungen = einzelbuchungen

    def einzelbuchungen(self) -> Einzelbuchungen:
        return self._einzelbuchungen

    def today(self) -> datetime.date:
        return self._today


def handle_request(_, context: DashboardContext):
    selector = context.einzelbuchungen().select()

    result_context = generate_page_context('dashboard')

    result_context.add('zusammenfassung_monatsliste', str(_monatsliste(current_month=context.today().month)))
    result_context.add('zusammenfassung_einnahmenliste',
                       str(selector
                           .select_einnahmen()
                           .inject_zeros_for_last_6_months(today=context.today())
                           .select_letzte_6_montate(today=context.today())
                           .sum_monthly()))
    result_context.add('zusammenfassung_ausgabenliste',
                       str(selector
                           .select_ausgaben()
                           .inject_zeros_for_last_6_months(today=context.today())
                           .select_letzte_6_montate(today=context.today())
                           .sum_monthly()))
    result_context.add('ausgaben_des_aktuellen_monats',
                       to_descriptive_list(selector
                                           .select_year(context.today().year)
                                           .select_month(context.today().month)
                                           .to_list()))

    return result_context


def _monatsliste(current_month: int):
    month_map = {1: 'Januar',
                 2: 'Februar',
                 3: 'März',
                 4: 'April',
                 5: 'Mai',
                 6: 'Juni',
                 7: 'Juli',
                 8: 'August',
                 9: 'September',
                 10: 'Oktober',
                 11: 'November',
                 12: 'Dezember'}
    aktueller_monat = current_month

    result_list = []

    for monat in range(0, 7):
        monat = 6 - monat

        berechneter_monat = aktueller_monat - monat
        if berechneter_monat < 1:
            berechneter_monat = berechneter_monat + 12
        result_list.append(month_map[berechneter_monat])

    return result_list


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        context_creator=lambda db: DashboardContext(einzelbuchungen=db.einzelbuchungen, today=time.today()),
        html_base_page='core/dashboard.html'
    )

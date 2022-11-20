from datetime import date

import butler_offline.viewcore.context
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore.context import generate_base_context
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.converter import to_descriptive_list
from butler_offline.core.time import today


def _handle_request(_):
    einzelbuchungen = persisted_state.database_instance().einzelbuchungen
    selector = einzelbuchungen.select()

    context = {
        'zusammenfassung_monatsliste': str(_monatsliste()),
        'zusammenfassung_einnahmenliste': str(selector.select_einnahmen().inject_zeros_for_last_6_months().select_letzte_6_montate().sum_monthly()),
        'zusammenfassung_ausgabenliste': str(selector.select_ausgaben().inject_zeros_for_last_6_months().select_letzte_6_montate().sum_monthly()),
        'ausgaben_des_aktuellen_monats': to_descriptive_list(selector.select_year(today().year).select_month(today().month).to_list())
    }
    context = {**context, **generate_base_context('dashboard')}
    return context

def _monatsliste():
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
    aktueller_monat = today().month

    result_list = []

    for monat in range(0, 7):
        monat = 6 - monat

        berechneter_monat = aktueller_monat - monat
        if berechneter_monat < 1:
            berechneter_monat = berechneter_monat + 12
        result_list.append(month_map[berechneter_monat])

    return result_list


def index(request):
    return request_handler.handle_request(request, _handle_request, 'core/dashboard.html')

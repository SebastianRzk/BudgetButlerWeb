from datetime import date

from viewcore import viewcore
from viewcore import request_handler

def _handle_request(_):
    einzelbuchungen = viewcore.database_instance().einzelbuchungen
    selector = einzelbuchungen.select()
    ausgaben_liste = []
    for row_index, row in selector.select_aktueller_monat().raw_table().iterrows():
        ausgaben_liste.append(
            {'index': row_index,
             'datum': row.Datum,
             'name': row.Name,
             'kategorie': row.Kategorie,
             'wert': '%.2f' % row.Wert
            })


    context = {
        'zusammenfassung_monatsliste': _monatsliste(),
        'zusammenfassung_einnahmenliste': _list_to_json(selector.select_einnahmen().inject_zeros_for_last_6_months().select_letzte_6_montate().sum_monthly()),
        'zusammenfassung_ausgabenliste': _list_to_json(selector.select_ausgaben().inject_zeros_for_last_6_months().select_letzte_6_montate().sum_monthly()),
        'ausgaben_des_aktuellen_monats': ausgaben_liste,
    }
    print(context)
    context = {**context, **viewcore.generate_base_context('dashboard')}
    return context


def _list_to_json(liste):
    result = '['
    for item in liste:
        if len(result) > 1:
            result = result + ', '
        result = result + str(item)
    return result + ']'

def _monatsliste():
    month_map = {1:'"Januar"', 2:'"Februar"', 3:'"März"', 4:'"April"', 5:'"Mai"',
                  6:'"Juni"', 7:'"Juli"', 8:'"August"',
                   9:'"September"', 10:'"Oktober"', 11:'"November"', 12:'"Dezember"'}
    aktueller_monat = date.today().month

    result_list = []

    for monat in range(0, 7):
        monat = 6 - monat

        berechneter_monat = aktueller_monat - monat
        if berechneter_monat < 1:
            berechneter_monat = berechneter_monat + 12
        result_list.append(month_map[berechneter_monat])

    return _list_to_json(result_list)

def index(request):
    return request_handler.handle_request(request, _handle_request, 'dashboard.html')

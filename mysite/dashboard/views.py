
from datetime import date

from django.shortcuts import render
from django.template.loader import render_to_string

from viewcore import viewcore


def handle_request():
    einzelbuchungen = viewcore.database_instance().einzelbuchungen

    ausgaben_liste = []
    for row_index, row in einzelbuchungen.select().select_aktueller_monat().raw_table().iterrows():
        ausgaben_liste.append((row_index, row.Datum, row.Name, row.Kategorie, row.Wert))

    context = {
        'zusammenfassung_monatsliste': monatsliste(),
        'zusammenfassung_einnahmenliste': str(einzelbuchungen.get_letzte_6_monate_einnahmen()),
        'zusammenfassung_ausgabenliste': str(einzelbuchungen.get_letzte_6_monate_ausgaben()),
        'ausgaben_des_aktuellen_monats': ausgaben_liste,
    }
    context = {**context, **viewcore.generate_base_context('dashboard')}
    return context

def index(request):
    context = handle_request()
    rendered_content = render_to_string('theme/dashboard.html', context, request=request)
    context['content'] = rendered_content
    return render(request, 'theme/index.html', context)


def monatsliste():
    month_map = {1:'"Januar"', 2:'"Februar"', 3:'"März"', 4:'"April"', 5:'"Mai"',
                  6:'"Juni"', 7:'"Juli"', 8:'"August"',
                   9:'"September"', 10:'"Oktober"', 11:'"November"', 12:'"Dezember"'}
    aktueller_monat = date.today().month - 1

    first = True
    result = "[ "

    for monat in range(0, 6):
        monat = 5 - monat
        if not first:
            result = result + ","
        else:
            first = False

        berechneter_monat = aktueller_monat - monat
        if berechneter_monat < 1:
            berechneter_monat = berechneter_monat + 12
        result = result + month_map[berechneter_monat]

    return result + ']'



from datetime import date

from django.http.response import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from viewcore import viewcore


def __init__(self):
    self.count = 0

def handle_request(request):
    einzelbuchungen = viewcore.database_instance().einzelbuchungen
    ausgaben_monat = einzelbuchungen.get_aktuellen_monat()[einzelbuchungen.get_aktuellen_monat().Wert < 0].Wert.sum() * -1

    ausgaben_liste = []
    for row_index, row in einzelbuchungen.get_aktuellen_monat().iterrows():
        ausgaben_liste.append((row_index, row.Datum, row.Name, row.Kategorie, row.Wert))

    context = {
        'anzahl_datensaetze':einzelbuchungen.anzahl(),
        'anzahl_dauerauftraege':len(viewcore.database_instance().dauerauftraege),
        'anzahl_stechzeiten':viewcore.database_instance().anzahl_stechzeiten(),
        'gesamt_wert': einzelbuchungen.get_all().Wert.abs().sum(),
        'rest_budget': 400,
        'prognose_monatsende': 110,
        'zusammenfassung_monatsliste': monatsliste(),
        'zusammenfassung_einnahmenliste': str(einzelbuchungen.get_letzte_6_monate_einnahmen()),
        'zusammenfassung_ausgabenliste': str(einzelbuchungen.get_letzte_6_monate_ausgaben()),
        'gesamtausgabe_diesen_monat': ausgaben_monat,
        'pro_tag_aktueller_monat': einzelbuchungen.get_ausgabe_pro_monat(0),
        'pro_tag_vergangener_monat': einzelbuchungen.get_ausgabe_pro_monat(1),
        'verganges_halbes_jahr': "%.2f" % (sum(einzelbuchungen.get_letzte_6_monate_ausgaben()) / (6 * 30 + 3)),
        'miete_grundkosten_farbe':'bg-green',

        'abrechnungen': ausgaben_liste,
    }
    context = {**context, **viewcore.generate_base_context('dashboard')}
    return context

def index(request):
    context = handle_request(request)
    rendered_content = render_to_string('theme/dashboard.html', context, request=request)
    context['content'] = rendered_content
    return render(request, 'theme/index.html', context)


def monatsliste():
    month_map = {1:'"Januar"', 2:'"Februar"', 3:'"März"', 4:'"April"', 5:'"Mai"',
                  6:'"Juni"', 7:'"Juli"', 8:'"August"',
                   9:'"September"', 10:'"Oktober"', 11:'"November"', 12:'"Dezember"'}
    aktueller_monat = date.today().month
    first = True
    result = "[ "

    for monat in range(0, 7):
        monat = 6 - monat
        if not first:
            result = result + ","
        else:
            first = False

        berechneter_monat = aktueller_monat - monat
        if berechneter_monat < 1:
            berechneter_monat = berechneter_monat + 12
        result = result + month_map[berechneter_monat]

    return result + ']'


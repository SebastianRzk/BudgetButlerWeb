
import datetime

from django.shortcuts import render
from django.template.loader import render_to_string

from viewcore import viewcore


def get_monats_namen(monat):
    return datetime.date(1900, monat, 1).strftime('%B')

def berechne_monate(tabelle):
    einzelbuchungen = viewcore.database_instance().einzelbuchungen
    alle_kategorien = set(einzelbuchungen.get_kategorien_ausgaben())

    monats_namen = []
    for _, wert_monats_gruppe in tabelle.iteritems():
        for (monat, _), _ in wert_monats_gruppe.iteritems():
            if get_monats_namen(monat) not in monats_namen:
                monats_namen.append(get_monats_namen(monat))

    print(monats_namen)

    kategorien_werte = {}
    for kategorie in alle_kategorien:
        kategorien_werte[kategorie] = '['
    umgerechnete_tabelle = _umrechnen(tabelle)
    for monat, kategorien in umgerechnete_tabelle.items():
        ausstehende_kategorien = alle_kategorien.copy()
        for kategorie, wert in kategorien.items():
            ausstehende_kategorien.remove(kategorie)
            if kategorien_werte[kategorie] == '[':
                kategorien_werte[kategorie] = kategorien_werte[kategorie] + '%.2f' % abs(wert)
            else:
                kategorien_werte[kategorie] = kategorien_werte[kategorie] + ',' + ' %.2f' % abs(wert)

        for fehllende_kategorie in ausstehende_kategorien:
            if kategorien_werte[fehllende_kategorie] == '[':
                kategorien_werte[fehllende_kategorie] = kategorien_werte[fehllende_kategorie] + '0.00'
            else:
                kategorien_werte[fehllende_kategorie] = kategorien_werte[fehllende_kategorie] + ', 0.00'

    return (monats_namen, kategorien_werte)

def _umrechnen(tabelle):
    result = {}
    for tblindex, group in tabelle.iterrows():
        print(index)
        print('###')
        print(group)
        (datum, kategorie) = tblindex
        if datum not in result:
            result[datum] = {}
        result[datum][kategorie] = group.Wert
    return result

def _computePieChartProzentual(context, jahr):
    result = viewcore.database_instance().einzelbuchungen.get_jahresausgaben_nach_kategorie_prozentual(jahr)
    ausgaben_data = []
    ausgaben_labels = []
    ausgaben_colors = []
    for kategorie, wert in result.items():
        ausgaben_data.append('%.2f' % abs(wert))
        ausgaben_labels.append(kategorie)
        ausgaben_colors.append('#' + viewcore.database_instance().einzelbuchungen.get_farbe_fuer(kategorie))

    context['pie_ausgaben_data_prozentual'] = ausgaben_data
    context['pie_ausgaben_labels'] = ausgaben_labels
    context['pie_ausgaben_colors'] = ausgaben_colors

    result = viewcore.database_instance().einzelbuchungen.get_jahreseinnahmen_nach_kategorie_prozentual(jahr)
    einnahmen_data = []
    einnahmen_labels = []
    einnahmen_colors = []
    for kategorie, wert in result.items():
        einnahmen_data.append('%.2f' % abs(wert))
        einnahmen_labels.append(kategorie)
        einnahmen_colors.append('#' + viewcore.database_instance().einzelbuchungen.get_farbe_fuer(kategorie))

    context['pie_einnahmen_data_prozentual'] = einnahmen_data
    context['pie_einnahmen_labels'] = einnahmen_labels
    context['pie_einnahmen_colors'] = einnahmen_colors


    return context

def index(request):
    context = handle_request(request)
    print(context)
    rendered_content = render_to_string('theme/uebersicht_jahr.html', context, request=request)

    context['content'] = rendered_content

    return render(request, 'theme/index.html', context)

def handle_request(request):
    today = datetime.date.today()
    year = today.year

    if 'date' in request.POST:
        year = int(float(request.POST['date']))
    einzelbuchungen = viewcore.database_instance().einzelbuchungen
    kategorien_checked_map = {}
    for kategorie in einzelbuchungen.get_alle_kategorien():
        kategorien_checked_map[kategorie] = 'checked'

    if request.method == 'POST' and request.POST['mode'] == 'change_selected':
        print('change selected')

        for kategorie in kategorien_checked_map.keys():
            if not kategorie in request.POST:
                kategorien_checked_map[kategorie] = ''

    jahresbuchungs_tabelle = einzelbuchungen.select().select_year(year)
    jahres_ausgaben = jahresbuchungs_tabelle.select_ausgaben()
    jahres_einnahmen = jahresbuchungs_tabelle.select_einnahmen()

    jahresausgaben = []
    for kategorie, jahresblock in jahres_ausgaben.group_by_kategorie().iterrows():
        jahresausgaben.append([kategorie, '%.2f' % jahresblock.Wert, kategorien_checked_map[kategorie], einzelbuchungen.get_farbe_fuer(kategorie)])

    jahreseinnahmen = []
    for kategorie, jahresblock in jahres_einnahmen.group_by_kategorie().iterrows():
        jahreseinnahmen.append([kategorie, '%.2f' % jahresblock.Wert, kategorien_checked_map[kategorie], einzelbuchungen.get_farbe_fuer(kategorie)])

    tabelle = einzelbuchungen.get_jahresausgaben_nach_monat(year)
    (monats_namen, kategorien_werte) = berechne_monate(tabelle)


    gefilterte_kategorien_werte = []
    print(kategorien_werte)
    for kategorie, wert in kategorien_werte.items():
        print(kategorien_checked_map)
        print(kategorie)
        if kategorien_checked_map[kategorie] == 'checked':
            gefilterte_kategorien_werte.append([kategorie, wert, einzelbuchungen.get_farbe_fuer(kategorie)])
            print('append:', kategorie)

    context = viewcore.generate_base_context('jahresuebersicht')

    context['durchschnitt_monat_kategorien'] = str(list(einzelbuchungen.durchschnittliche_ausgaben_pro_monat(year).keys()))
    context['durchschnittlich_monat_wert'] = str(list(einzelbuchungen.durchschnittliche_ausgaben_pro_monat(year).values()))
    context = _computePieChartProzentual(context, year)

    laenge = 12
    if year == today.year:
        laenge = today.month

    context['buchungen'] = [
        {
            'kategorie': 'Einnahmen',
            'farbe': 'rgb(210, 214, 222)',
            'wert': jahres_einnahmen.inject_zeros_for_year(year, laenge).sum_monthly()
        },
        {
            'kategorie': 'Ausgaben',
            'farbe': 'rgba(60,141,188,0.8)',
            'wert': jahres_ausgaben.inject_zeros_for_year(year, laenge).sum_monthly()
        }
    ]
    context['zusammenfassung_ausgaben'] = jahresausgaben
    context['zusammenfassung_einnahmen'] = jahreseinnahmen
    context['monats_namen'] = monats_namen
    context['selected_date'] = year
    context['ausgaben'] = gefilterte_kategorien_werte
    context['jahre'] = sorted(einzelbuchungen.get_jahre(), reverse=True)
    context['gesamt_ausgaben'] = '%.2f' % einzelbuchungen.select().select_year(year).select_ausgaben().sum()
    context['gesamt_einnahmen'] = '%.2f' % einzelbuchungen.select().select_year(year).select_einnahmen().sum()
    return context

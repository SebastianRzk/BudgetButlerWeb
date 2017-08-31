
import datetime

from django.shortcuts import render
from django.template.loader import render_to_string

from viewcore import viewcore


def get_monats_namen(monat):
    return datetime.date(1900, monat, 1).strftime('%B')

def berechne_monate(tabelle):
    print('######################')
    print(tabelle)
    print('##########################')

    einzelbuchungen = viewcore.database_instance().einzelbuchungen
    alle_kategorien = set(einzelbuchungen.get_alle_kategorien())

    monats_namen = []
    for _, wert_monats_gruppe in tabelle.iteritems():
        for (monat, _), _ in wert_monats_gruppe.iteritems():
            if get_monats_namen(monat) not in monats_namen:
                monats_namen.append(get_monats_namen(monat))

    print(monats_namen)

    kategorien_werte = {'Summe':'['}
    for kategorie in alle_kategorien:
        kategorien_werte[kategorie] = '['
    umgerechnete_tabelle = _umrechnen(tabelle)
    for monat, kategorien in umgerechnete_tabelle.items():
        ausstehende_kategorien = alle_kategorien.copy()
        monatssumme = 0
        for kategorie, wert in kategorien.items():
            ausstehende_kategorien.remove(kategorie)
            if kategorien_werte[kategorie] == '[':
                kategorien_werte[kategorie] = kategorien_werte[kategorie] + '%.2f' % abs(wert)
            else:
                kategorien_werte[kategorie] = kategorien_werte[kategorie] + ',' + ' %.2f' % abs(wert)
            if wert < 0:
                monatssumme += abs(wert)

        for fehllende_kategorie in ausstehende_kategorien:
            if kategorien_werte[fehllende_kategorie] == '[':
                kategorien_werte[fehllende_kategorie] = kategorien_werte[fehllende_kategorie] + '0.00'
            else:
                kategorien_werte[fehllende_kategorie] = kategorien_werte[fehllende_kategorie] + ', 0.00'
        if kategorien_werte['Summe'] == '[':
            kategorien_werte['Summe'] = kategorien_werte['Summe'] + '%.2f' % monatssumme
        else:
            kategorien_werte['Summe'] = kategorien_werte['Summe'] + ',' + '%.2f' % monatssumme

    return (monats_namen, kategorien_werte)

def _umrechnen(tabelle):
    result = {}
    for _, group in tabelle.iteritems():
        for tblindex, wert in group.iteritems():
            (datum, kategorie) = tblindex
            if datum not in result:
                result[datum] = {}
            result[datum][kategorie] = wert
    return result

def _computeAllesPieChartProzentual(context):
    result = viewcore.database_instance().einzelbuchungen.get_gesamtausgaben_nach_kategorie_prozentual()
    ausgaben_data = []
    ausgaben_labels = []
    ausgaben_colors = []
    for kategorie, wert in result.items():
        ausgaben_data.append('%.2f' % abs(wert))
        ausgaben_labels.append(kategorie)
        ausgaben_colors.append('#' + viewcore.database_instance().einzelbuchungen.get_farbe_fuer(kategorie))

    context['pie_alle_ausgaben_data_prozentual'] = ausgaben_data
    context['pie_ausgaben_labels'] = ausgaben_labels
    context['pie_ausgaben_colors'] = ausgaben_colors

    return context

def _computePieChartProzentual(context, jahr):
    result = viewcore.database_instance().einzelbuchungen.get_jahresausgaben_nach_kategorie_prozentual(jahr)
    ausgaben_data = []
    for _, wert in result.items():
        ausgaben_data.append('%.2f' % abs(wert))
    context['pie_ausgaben_data_prozentual'] = ausgaben_data
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
    most_important_categories = einzelbuchungen.top_kategorie_fuer_jahr(year)
    for kategorie in einzelbuchungen.get_alle_kategorien():
        if kategorie in most_important_categories:
            kategorien_checked_map[kategorie] = 'checked'
        else:
            kategorien_checked_map[kategorie] = ''

    kategorien_checked_map['Summe'] = 'checked'

    if request.method == 'POST' and request.POST['mode'] == 'change_selected':
        print('change selected')

        for kategorie in kategorien_checked_map.keys():
            if not kategorie in request.POST:
                kategorien_checked_map[kategorie] = ''


    jahresausgaben_jahr = []
    for jahr, jahresblock in einzelbuchungen.get_gesamtbuchungen_jahr(year).iteritems():
        print(jahresblock)
        for tblkategorie, tblwert in jahresblock.iteritems():
            jahresausgaben_jahr.append([tblkategorie, '%.2f' % tblwert, kategorien_checked_map[tblkategorie], einzelbuchungen.get_farbe_fuer(tblkategorie)])
        break

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

    gesamt = 0
    if not tabelle.empty:
        gesamt = tabelle.Wert.sum()


    context = viewcore.generate_base_context('jahresuebersicht')

    context = _computeAllesPieChartProzentual(context)
    context = _computePieChartProzentual(context, year)

    context['zusammenfassung'] = jahresausgaben_jahr
    context['monats_namen'] = monats_namen
    context['selected_date'] = year
    context['ausgaben'] = gefilterte_kategorien_werte
    context['jahre'] = sorted(einzelbuchungen.get_jahre(), reverse=True)
    context['gesamt'] = '%.2f' % gesamt
    context['gesamt_color'] = einzelbuchungen.get_farbe_fuer('Summe')
    context['gesamt_enabled'] = kategorien_checked_map['Summe']
    return context

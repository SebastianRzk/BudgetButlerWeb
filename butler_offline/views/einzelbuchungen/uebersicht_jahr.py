import datetime

import butler_offline.viewcore.context
from butler_offline.viewcore.state.persisted_state import database_instance
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.context import generate_base_context
from butler_offline.viewcore import request_handler


def get_monats_namen(monat):
    return datetime.date(1900, monat, 1).strftime('%B')


def _filter(liste, num_monate):
    result = []
    for monat in range(1, 13):
        if monat not in num_monate:
            continue
        result.append(liste[monat - 1])
    return result


def _computePieChartProzentual(context, jahr):
    result = database_instance().einzelbuchungen.get_jahresausgaben_nach_kategorie_prozentual(jahr)
    ausgaben_data = []
    ausgaben_labels = []
    ausgaben_colors = []
    kategorien = database_instance().einzelbuchungen.get_alle_kategorien()
    color_chooser = viewcore.get_generic_color_chooser(list(kategorien))

    for kategorie, wert in result.items():
        ausgaben_data.append('%.2f' % abs(wert))
        ausgaben_labels.append(kategorie)
        ausgaben_colors.append(color_chooser.get_for_value(kategorie))

    context['pie_ausgaben_data_prozentual'] = ausgaben_data
    context['pie_ausgaben_labels'] = ausgaben_labels
    context['pie_ausgaben_colors'] = ausgaben_colors

    result = database_instance().einzelbuchungen.get_jahreseinnahmen_nach_kategorie_prozentual(jahr)
    einnahmen_data = []
    einnahmen_labels = []
    einnahmen_colors = []
    for kategorie, wert in result.items():
        einnahmen_data.append('%.2f' % abs(wert))
        einnahmen_labels.append(kategorie)
        einnahmen_colors.append(color_chooser.get_for_value(kategorie))

    context['pie_einnahmen_data_prozentual'] = einnahmen_data
    context['pie_einnahmen_labels'] = einnahmen_labels
    context['pie_einnahmen_colors'] = einnahmen_colors

    return context


def _compile_colors(result, einzelbuchungen, num_monate, color_chooser):
    einnahmen = {}
    for month in result.keys():
        if month not in num_monate:
            continue
        for kategorie in result[month]:
            if kategorie not in einnahmen:
                einnahmen[kategorie] = {}
                einnahmen[kategorie]['values'] = '[' + result[month][kategorie]
                continue
            einnahmen[kategorie]['values'] = einnahmen[kategorie]['values'] + ',' + result[month][kategorie]

    for kategorie in einnahmen:
        einnahmen[kategorie]['values'] = einnahmen[kategorie]['values'] + ']'
        einnahmen[kategorie]['farbe'] = color_chooser.get_for_value(kategorie)

    return einnahmen


def _handle_request(request):
    today = datetime.date.today()
    year = today.year

    if request.method == 'POST' and 'date' in request.values:
        year = int(float(request.values['date']))
    einzelbuchungen = database_instance().einzelbuchungen

    jahresbuchungs_tabelle = einzelbuchungen.select().select_year(year)
    jahres_ausgaben = jahresbuchungs_tabelle.select_ausgaben()
    jahres_einnahmen = jahresbuchungs_tabelle.select_einnahmen()
    kategorien = database_instance().einzelbuchungen.get_alle_kategorien()
    color_chooser = viewcore.get_generic_color_chooser(list(kategorien))

    jahresausgaben = []
    for kategorie, jahresblock in jahres_ausgaben.group_by_kategorie().iterrows():
        jahresausgaben.append([kategorie, '%.2f' % jahresblock.Wert, color_chooser.get_for_value(kategorie)])

    jahreseinnahmen = []
    for kategorie, jahresblock in jahres_einnahmen.group_by_kategorie().iterrows():
        jahreseinnahmen.append([kategorie, '%.2f' % jahresblock.Wert, color_chooser.get_for_value(kategorie)])

    monats_namen = []
    num_monate = sorted(list(set(jahresbuchungs_tabelle.raw_table().Datum.map(lambda x: x.month))))
    for num_monat in num_monate:
        monats_namen.append(get_monats_namen(num_monat))

    context = generate_base_context('jahresuebersicht')

    context['durchschnitt_monat_kategorien'] = str(
        list(einzelbuchungen.durchschnittliche_ausgaben_pro_monat(year).keys()))
    context['durchschnittlich_monat_wert'] = str(
        list(einzelbuchungen.durchschnittliche_ausgaben_pro_monat(year).values()))
    context = _computePieChartProzentual(context, year)

    laenge = 12
    if year == today.year:
        laenge = today.month

    context['buchungen'] = [
        {
            'kategorie': 'Einnahmen',
            'farbe': 'rgb(210, 214, 222)',
            'wert': _filter(jahres_einnahmen.inject_zeros_for_year(year, laenge).sum_monthly(), num_monate)
        },
        {
            'kategorie': 'Ausgaben',
            'farbe': 'rgba(60,141,188,0.8)',
            'wert': _filter(jahres_ausgaben.inject_zeros_for_year(year, laenge).sum_monthly(), num_monate)
        }
    ]
    context['zusammenfassung_ausgaben'] = jahresausgaben
    context['zusammenfassung_einnahmen'] = jahreseinnahmen
    context['monats_namen'] = monats_namen
    context['selected_date'] = year

    context['einnahmen'] = _compile_colors(
        jahres_einnahmen.inject_zeroes_for_year_and_kategories(year).sum_kategorien_monthly(),
        einzelbuchungen,
        num_monate,
        color_chooser
    )
    context['ausgaben'] = _compile_colors(
        jahres_ausgaben.inject_zeroes_for_year_and_kategories(year).sum_kategorien_monthly(),
        einzelbuchungen,
        num_monate,
        color_chooser
    )
    context['jahre'] = sorted(einzelbuchungen.get_jahre(), reverse=True)
    context['gesamt_ausgaben'] = '%.2f' % einzelbuchungen.select().select_year(year).select_ausgaben().sum()
    context['gesamt_einnahmen'] = '%.2f' % einzelbuchungen.select().select_year(year).select_einnahmen().sum()
    return context


def index(request):
    return request_handler.handle_request(request, _handle_request, 'einzelbuchungen/uebersicht_jahr.html')

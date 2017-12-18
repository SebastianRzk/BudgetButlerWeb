
import datetime

from django.shortcuts import render
from django.template.loader import render_to_string

from viewcore import viewcore


def get_monats_namen(monat):
    return datetime.date(1900, monat, 1).strftime('%B')

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

def _compile_colors(result, einzelbuchungen):
    einnahmen = {}
    for month in result.keys():
        for kategorie in result[month]:
            if month == 1:
                einnahmen[kategorie] = {}
                einnahmen[kategorie]['values'] = '[' + result[month][kategorie]
                continue
            einnahmen[kategorie]['values'] = einnahmen[kategorie]['values'] + ',' + result[month][kategorie]

    for kategorie in einnahmen:
        einnahmen[kategorie]['values'] = einnahmen[kategorie]['values'] + ']'
        einnahmen[kategorie]['farbe'] = einzelbuchungen.get_farbe_fuer(kategorie)

    return einnahmen

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

    jahresbuchungs_tabelle = einzelbuchungen.select().select_year(year)
    jahres_ausgaben = jahresbuchungs_tabelle.select_ausgaben()
    jahres_einnahmen = jahresbuchungs_tabelle.select_einnahmen()

    jahresausgaben = []
    for kategorie, jahresblock in jahres_ausgaben.group_by_kategorie().iterrows():
        jahresausgaben.append([kategorie, '%.2f' % jahresblock.Wert, einzelbuchungen.get_farbe_fuer(kategorie)])

    jahreseinnahmen = []
    for kategorie, jahresblock in jahres_einnahmen.group_by_kategorie().iterrows():
        jahreseinnahmen.append([kategorie, '%.2f' % jahresblock.Wert, einzelbuchungen.get_farbe_fuer(kategorie)])

    num_monate = sorted(list(set(jahresbuchungs_tabelle.raw_table().Datum.map(lambda x: x.month))))
    monats_namen = []
    for num_monat in num_monate:
        monats_namen.append(get_monats_namen(num_monat))

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

    context['einnahmen'] = _compile_colors(jahres_einnahmen.inject_zeroes_for_year_and_kategories(2017).sum_kategorien_monthly(), einzelbuchungen)
    context['ausgaben'] = _compile_colors(jahres_ausgaben.inject_zeroes_for_year_and_kategories(2017).sum_kategorien_monthly(), einzelbuchungen)
    context['jahre'] = sorted(einzelbuchungen.get_jahre(), reverse=True)
    context['gesamt_ausgaben'] = '%.2f' % einzelbuchungen.select().select_year(year).select_ausgaben().sum()
    context['gesamt_einnahmen'] = '%.2f' % einzelbuchungen.select().select_year(year).select_einnahmen().sum()
    return context

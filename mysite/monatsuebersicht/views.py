
import datetime

from django.shortcuts import render
from django.template.loader import render_to_string

from viewcore import viewcore


def __init__(self):
    self.count = 0

def handle_request(request):
    context = viewcore.generate_base_context('monatsuebersicht')
    today = datetime.date.today()
    month = today.month
    year = today.year

    if request.method == "POST":
        datum = request.POST['date']
        month = int(float(datum.split("_")[1]))
        year = int(float(datum.split("_")[0]))
        print('date:', request.POST)

    context['selected_year'] = year


    einzelbuchungen = viewcore.database_instance().einzelbuchungen
    table_data_selection = einzelbuchungen.select().select_month(month).select_year(year)
    table_ausgaben = table_data_selection.select_ausgaben()
    table_einnahmen = table_data_selection.select_einnahmen()

    '''
    Berechnung der Ausgaben für das Kreisdiagramm
    '''
    ausgaben_liste = []
    ausgaben_labels = []
    ausgaben_data = []
    ausgaben_colors = []
    for kategorie, row in table_ausgaben.group_by_kategorie().iterrows():
        ausgaben_labels.append(kategorie)
        ausgaben_data.append("%.2f" % abs(row.Wert))
        ausgaben_colors.append("#" + einzelbuchungen.get_farbe_fuer(kategorie))
        ausgaben_liste.append((kategorie, "%.2f" % row.Wert, einzelbuchungen.get_farbe_fuer(kategorie)))
    context['ausgaben'] = ausgaben_liste
    context['ausgaben_labels'] = ausgaben_labels
    context['ausgaben_data'] = ausgaben_data
    context['ausgaben_colors'] = ausgaben_colors

    '''
    Berechnung der Einnahmen für das Kreisdiagramm
    '''
    einnahmen_liste = []
    einnahmen_labels = []
    einnahmen_data = []
    einnahmen_colors = []
    for kategorie, row in table_einnahmen.group_by_kategorie().iterrows():
        einnahmen_labels.append(kategorie)
        einnahmen_data.append("%.2f" % abs(row.Wert))
        einnahmen_colors.append("#" + einzelbuchungen.get_farbe_fuer(kategorie))
        einnahmen_liste.append((kategorie, "%.2f" % row.Wert, einzelbuchungen.get_farbe_fuer(kategorie)))
    context['einnahmen'] = einnahmen_liste
    context['einnahmen_labels'] = einnahmen_labels
    context['einnahmen_data'] = einnahmen_data
    context['einnahmen_colors'] = einnahmen_colors


    zusammenfassung = einzelbuchungen.get_month_summary(month, year)
    for tag, kategorien_liste in zusammenfassung:
        for einheit in kategorien_liste:
            einheit['farbe'] = einzelbuchungen.get_farbe_fuer(einheit['kategorie'])
    print(zusammenfassung)
    context['zusammenfassung'] = zusammenfassung

    ausgaben_monat = table_ausgaben.sum()
    context['gesamt'] = "%.2f" % ausgaben_monat
    einnahmen_monat = table_einnahmen.sum()
    context['gesamt_einnahmen'] = "%.2f" % einnahmen_monat


    selected_date = str(year) + "_" + str(month).rjust(2, "0")
    context['selected_date'] = selected_date
    context['monate'] = sorted(einzelbuchungen.get_monate(), reverse=True)


    if einnahmen_monat >= abs(ausgaben_monat):
        context['color_uebersicht_gruppe_1'] = "gray"
        context['name_uebersicht_gruppe_1'] = 'Gedeckte Ausgaben'
        context['wert_uebersicht_gruppe_1'] = abs(ausgaben_monat)

        context['color_uebersicht_gruppe_2'] = "lightgreen"
        context['name_uebersicht_gruppe_2'] = 'Einnahmenüberschuss'
        context['wert_uebersicht_gruppe_2'] = einnahmen_monat + ausgaben_monat

    else:
        context['color_uebersicht_gruppe_1'] = "gray"
        context['name_uebersicht_gruppe_1'] = 'Gedeckte Ausgaben'
        context['wert_uebersicht_gruppe_1'] = einnahmen_monat

        context['color_uebersicht_gruppe_2'] = "red"
        context['name_uebersicht_gruppe_2'] = 'Ungedeckte Ausgaben'
        context['wert_uebersicht_gruppe_2'] = (ausgaben_monat + einnahmen_monat) * -1

    einnahmen_jahr = einzelbuchungen.select().select_einnahmen().select_year(year).sum()
    ausgaben_jahr = einzelbuchungen.select().select_ausgaben().select_year(year).sum()
    if einnahmen_jahr >= abs(ausgaben_jahr):
        context['color_uebersicht_jahr_gruppe_1'] = "gray"
        context['name_uebersicht_jahr_gruppe_1'] = 'Gedeckte Einnahmen'
        context['wert_uebersicht_jahr_gruppe_1'] = abs(ausgaben_jahr)

        context['color_uebersicht_jahr_gruppe_2'] = "lightgreen"
        context['name_uebersicht_jahr_gruppe_2'] = 'Einnahmenüberschuss'
        context['wert_uebersicht_jahr_gruppe_2'] = einnahmen_jahr + ausgaben_jahr

    else:
        context['color_uebersicht_jahr_gruppe_1'] = "gray"
        context['name_uebersicht_jahr_gruppe_1'] = 'Gedeckte Ausgaben'
        context['wert_uebersicht_jahr_gruppe_1'] = einnahmen_jahr

        context['color_uebersicht_jahr_gruppe_2'] = "red"
        context['name_uebersicht_jahr_gruppe_2'] = 'Ungedeckte Ausgaben'
        context['wert_uebersicht_jahr_gruppe_2'] = (ausgaben_jahr + einnahmen_jahr) * -1

    return context

def index(request):
    context = handle_request(request)
    print(context)
    rendered_content = render_to_string('theme/uebersicht_monat.html', context, request=request)

    context['content'] = rendered_content

    return render(request, 'theme/index.html', context)



from mysite.viewcore import request_handler
from mysite.viewcore import viewcore
from mysite.core.ReportGenerator import ReportGenerator
from mysite.viewcore.converter import datum_to_string

def _handle_request(request):
    context = viewcore.generate_base_context('monatsuebersicht')
    einzelbuchungen = viewcore.database_instance().einzelbuchungen
    monate = sorted(einzelbuchungen.get_monate(), reverse=True)
    context['monate'] = monate

    if not monate:
        return viewcore.generate_error_context('monatsuebersicht', 'Keine Ausgaben erfasst')

    selected_item = context['monate'][0]
    if request.method == "POST":
        selected_item = request.values['date']
    month = int(float(selected_item.split("_")[1]))
    year = int(float(selected_item.split("_")[0]))

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


    zusammenfassung = table_data_selection.get_month_summary()
    for tag, kategorien_liste in zusammenfassung:
        for einheit in kategorien_liste:
            einheit['farbe'] = einzelbuchungen.get_farbe_fuer(einheit['kategorie'])
    context['zusammenfassung'] = zusammenfassung

    ausgaben_monat = table_ausgaben.sum()
    context['gesamt'] = "%.2f" % ausgaben_monat
    einnahmen_monat = table_einnahmen.sum()
    context['gesamt_einnahmen'] = "%.2f" % einnahmen_monat


    selected_date = str(year) + "_" + str(month).rjust(2, "0")
    context['selected_date'] = selected_date
    context['selected_year'] = year

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
    return request_handler.handle_request(request, _handle_request, 'uebersicht_monat.html')

def _abrechnen(request):
    context = viewcore.generate_base_context('monatsuebersicht')
    date = viewcore.today()
    year = date.year
    month = date.month
    quantity = 60

    if request.method == 'POST':
        if 'date' in request.values:
            str_year, str_month = request.values['date'].split('_')
            year = int(str_year)
            month = int(str_month)
        if 'quantity' in request.values:
            quantity = int(request.values['quantity'])

    einzelbuchungen = viewcore.database_instance().einzelbuchungen
    generator = ReportGenerator('Monatsübersicht für ' + str(month) + '/' + str(year), quantity)

    table_data_selection = einzelbuchungen.select().select_month(month).select_year(year)
    table_ausgaben = table_data_selection.select_ausgaben()
    table_einnahmen = table_data_selection.select_einnahmen()

    if _is_selected(request, 'zusammenfassung_einnahmen'):
        data = {}
        for kategorie, row in table_einnahmen.group_by_kategorie().iterrows():
            data[kategorie] = row.Wert
        generator.add_half_line_elements({'Einnahmen': data})

    if _is_selected(request, 'zusammenfassung_ausgaben'):
        data = {}
        for kategorie, row in table_ausgaben.group_by_kategorie().iterrows():
            data[kategorie] = row.Wert
        generator.add_half_line_elements({'Ausgaben': data})

    if _is_selected(request, 'einnahmen'):
        generator.add_halfline('')
        generator.add_halfline('')
        generator.add_halfline('----Einnahmen----')
        zusammenfassung = table_einnahmen.zusammenfassung()
        compiled_zusammenfassung = {}
        for tag, kategorien_liste in zusammenfassung:
            compiled_zusammenfassung[datum_to_string(tag)] = {}
            for einheit in kategorien_liste:
                compiled_zusammenfassung[datum_to_string(tag)][einheit['name']] = float(einheit['summe'])

        generator.add_half_line_elements(compiled_zusammenfassung)

    if _is_selected(request, 'ausgaben'):
        generator.add_halfline('')
        generator.add_halfline('')
        generator.add_halfline('----Ausgaben----')
        zusammenfassung = table_ausgaben.zusammenfassung()
        compiled_zusammenfassung = {}
        for tag, kategorien_liste in zusammenfassung:
            compiled_zusammenfassung[datum_to_string(tag)] = {}
            for einheit in kategorien_liste:
                compiled_zusammenfassung[datum_to_string(tag)][einheit['name']] = float(einheit['summe'])

        generator.add_half_line_elements(compiled_zusammenfassung)




    page = ''
    for line in generator.generate_pages():
        page = page + '<br>' + line
    context['abrechnungstext'] = '<pre>' + page + '</pre>'
    context['element_titel'] = 'Abrechnung vom {month}/{year}'.format(month=month, year=year)
    return context

def _is_selected(request, name):
    if request.method != 'POST':
        return True

    if 'content' not in request.values:
        return True
    print('         ', any(name == s for s in request.values.getlist('content')))
    return any(name == s for s in request.values.getlist('content'))

def abrechnen(request):
    return request_handler.handle_request(request, _abrechnen, 'present_abrechnung.html')



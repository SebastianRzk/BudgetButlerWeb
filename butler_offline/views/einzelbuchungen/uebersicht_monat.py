from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.context import generate_base_context, generate_error_context


def _handle_request(request):
    context = generate_base_context('monatsuebersicht')
    einzelbuchungen = persisted_state.database_instance().einzelbuchungen
    monate = sorted(einzelbuchungen.get_monate(), reverse=True)
    context['monate'] = monate

    if not monate:
        return generate_error_context('monatsuebersicht', 'Keine Ausgaben erfasst')

    selected_item = context['monate'][0]
    if request.method == "POST":
        selected_item = request.values['date']
    month = int(float(selected_item.split("_")[1]))
    year = int(float(selected_item.split("_")[0]))

    table_data_selection = einzelbuchungen.select().select_month(month).select_year(year)
    table_ausgaben = table_data_selection.select_ausgaben()
    table_einnahmen = table_data_selection.select_einnahmen()

    kategorien = einzelbuchungen.get_alle_kategorien()
    color_chooser = viewcore.get_generic_color_chooser(list(kategorien))

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
        ausgaben_colors.append(color_chooser.get_for_value(kategorie))
        ausgaben_liste.append((kategorie, "%.2f" % row.Wert, color_chooser.get_for_value(kategorie)))
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
        einnahmen_colors.append(color_chooser.get_for_value(kategorie))
        einnahmen_liste.append((kategorie, "%.2f" % row.Wert, color_chooser.get_for_value(kategorie)))
    context['einnahmen'] = einnahmen_liste
    context['einnahmen_labels'] = einnahmen_labels
    context['einnahmen_data'] = einnahmen_data
    context['einnahmen_colors'] = einnahmen_colors

    zusammenfassung = table_data_selection.get_month_summary()
    for tag, kategorien_liste in zusammenfassung:
        for einheit in kategorien_liste:
            einheit['farbe'] = color_chooser.get_for_value(einheit['kategorie'])
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
        context['wert_uebersicht_gruppe_1'] = '%.2f' % abs(ausgaben_monat)

        context['color_uebersicht_gruppe_2'] = "lightgreen"
        context['name_uebersicht_gruppe_2'] = 'Einnahmenüberschuss'
        context['wert_uebersicht_gruppe_2'] = '%.2f' % (einnahmen_monat + ausgaben_monat)

    else:
        context['color_uebersicht_gruppe_1'] = "gray"
        context['name_uebersicht_gruppe_1'] = 'Gedeckte Ausgaben'
        context['wert_uebersicht_gruppe_1'] = '%.2f' % einnahmen_monat

        context['color_uebersicht_gruppe_2'] = "red"
        context['name_uebersicht_gruppe_2'] = 'Ungedeckte Ausgaben'
        context['wert_uebersicht_gruppe_2'] = '%.2f' % ((ausgaben_monat + einnahmen_monat) * -1)

    einnahmen_jahr = einzelbuchungen.select().select_einnahmen().select_year(year).sum()
    ausgaben_jahr = einzelbuchungen.select().select_ausgaben().select_year(year).sum()
    if einnahmen_jahr >= abs(ausgaben_jahr):
        context['color_uebersicht_jahr_gruppe_1'] = "gray"
        context['name_uebersicht_jahr_gruppe_1'] = 'Gedeckte Einnahmen'
        context['wert_uebersicht_jahr_gruppe_1'] = '%.2f' % abs(ausgaben_jahr)

        context['color_uebersicht_jahr_gruppe_2'] = "lightgreen"
        context['name_uebersicht_jahr_gruppe_2'] = 'Einnahmenüberschuss'
        context['wert_uebersicht_jahr_gruppe_2'] = '%.2f' % (einnahmen_jahr + ausgaben_jahr)

    else:
        context['color_uebersicht_jahr_gruppe_1'] = "gray"
        context['name_uebersicht_jahr_gruppe_1'] = 'Gedeckte Ausgaben'
        context['wert_uebersicht_jahr_gruppe_1'] = '%.2f' % einnahmen_jahr

        context['color_uebersicht_jahr_gruppe_2'] = "red"
        context['name_uebersicht_jahr_gruppe_2'] = 'Ungedeckte Ausgaben'
        context['wert_uebersicht_jahr_gruppe_2'] = '%.2f' % ((ausgaben_jahr + einnahmen_jahr) * -1)

    return context


def index(request):
    return request_handler.handle_request(request, _handle_request, 'einzelbuchungen/uebersicht_monat.html')


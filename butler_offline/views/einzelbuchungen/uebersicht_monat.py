from butler_offline.viewcore import request_handler
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.context.builder import generate_page_context
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen


class UebersichtMonatContext:
    def __init__(self, einzelbuchungen: Einzelbuchungen):
        self._einzelbuchungen = einzelbuchungen

    def einzelbuchungen(self):
        return self._einzelbuchungen


def handle_request(request, context: UebersichtMonatContext):
    result_context = generate_page_context('monatsuebersicht')
    einzelbuchungen = context.einzelbuchungen()
    monate = sorted(einzelbuchungen.get_monate(), reverse=True)
    result_context.add('monate', monate)

    if not monate:
        result_context.throw_error('Keine Ausgaben erfasst')
        return result_context

    selected_item = monate[0]
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
    result_context.add('ausgaben', ausgaben_liste)
    result_context.add('ausgaben_labels', ausgaben_labels)
    result_context.add('ausgaben_data', ausgaben_data)
    result_context.add('ausgaben_colors', ausgaben_colors)

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
    result_context.add('einnahmen', einnahmen_liste)
    result_context.add('einnahmen_labels', einnahmen_labels)
    result_context.add('einnahmen_data', einnahmen_data)
    result_context.add('einnahmen_colors', einnahmen_colors)

    zusammenfassung = table_data_selection.get_month_summary()
    for tag, kategorien_liste in zusammenfassung:
        for einheit in kategorien_liste:
            einheit['farbe'] = color_chooser.get_for_value(einheit['kategorie'])
    result_context.add('zusammenfassung', zusammenfassung)

    ausgaben_monat = table_ausgaben.sum()
    result_context.add('gesamt', "%.2f" % ausgaben_monat)
    einnahmen_monat = table_einnahmen.sum()
    result_context.add('gesamt_einnahmen', "%.2f" % einnahmen_monat)

    selected_date = str(year) + "_" + str(month).rjust(2, "0")
    result_context.add('selected_date', selected_date)
    result_context.add('selected_year', year)

    if einnahmen_monat >= abs(ausgaben_monat):
        result_context.add('color_uebersicht_gruppe_1', 'gray')
        result_context.add('name_uebersicht_gruppe_1', 'Gedeckte Ausgaben')
        result_context.add('wert_uebersicht_gruppe_1', '%.2f' % abs(ausgaben_monat))

        result_context.add('color_uebersicht_gruppe_2', 'lightgreen')
        result_context.add('name_uebersicht_gruppe_2', 'Einnahmenüberschuss')
        result_context.add('wert_uebersicht_gruppe_2', '%.2f' % (einnahmen_monat + ausgaben_monat))

    else:
        result_context.add('color_uebersicht_gruppe_1', 'gray')
        result_context.add('name_uebersicht_gruppe_1', 'Gedeckte Ausgaben')
        result_context.add('wert_uebersicht_gruppe_1', '%.2f' % einnahmen_monat)

        result_context.add('color_uebersicht_gruppe_2', 'red')
        result_context.add('name_uebersicht_gruppe_2', 'Ungedeckte Ausgaben')
        result_context.add('wert_uebersicht_gruppe_2', '%.2f' % ((ausgaben_monat + einnahmen_monat) * -1))

    einnahmen_jahr = einzelbuchungen.select().select_einnahmen().select_year(year).sum()
    ausgaben_jahr = einzelbuchungen.select().select_ausgaben().select_year(year).sum()
    if einnahmen_jahr >= abs(ausgaben_jahr):
        result_context.add('color_uebersicht_jahr_gruppe_1', 'gray')
        result_context.add('name_uebersicht_jahr_gruppe_1', 'Gedeckte Einnahmen')
        result_context.add('wert_uebersicht_jahr_gruppe_1', '%.2f' % abs(ausgaben_jahr))

        result_context.add('color_uebersicht_jahr_gruppe_2', 'lightgreen')
        result_context.add('name_uebersicht_jahr_gruppe_2', 'Einnahmenüberschuss')
        result_context.add('wert_uebersicht_jahr_gruppe_2', '%.2f' % (einnahmen_jahr + ausgaben_jahr))

    else:
        result_context.add('color_uebersicht_jahr_gruppe_1', 'gray')
        result_context.add('name_uebersicht_jahr_gruppe_1', 'Gedeckte Ausgaben')
        result_context.add('wert_uebersicht_jahr_gruppe_1', '%.2f' % einnahmen_jahr)

        result_context.add('color_uebersicht_jahr_gruppe_2', 'red')
        result_context.add('name_uebersicht_jahr_gruppe_2', 'Ungedeckte Ausgaben')
        result_context.add('wert_uebersicht_jahr_gruppe_2', '%.2f' % ((ausgaben_jahr + einnahmen_jahr) * -1))

    return result_context


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        html_base_page='einzelbuchungen/uebersicht_monat.html',
        context_creator=lambda db: UebersichtMonatContext(db.einzelbuchungen)
    )

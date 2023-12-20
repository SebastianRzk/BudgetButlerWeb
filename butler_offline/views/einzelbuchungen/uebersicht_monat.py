from datetime import date

from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.viewcore import request_handler
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.context.builder import generate_page_context
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.renderhelper import Betrag, BetragListe
from butler_offline.viewcore.requirements import einzelbuchung_needed_decorator


class UebersichtMonatContext:
    def __init__(self, einzelbuchungen: Einzelbuchungen):
        self._einzelbuchungen = einzelbuchungen

    def einzelbuchungen(self):
        return self._einzelbuchungen


@einzelbuchung_needed_decorator()
def handle_request(request: Request, context: UebersichtMonatContext):
    result_context = generate_page_context('monatsuebersicht')
    einzelbuchungen = context.einzelbuchungen()
    monate = sorted(einzelbuchungen.get_monate(), reverse=True)
    result_context.add('monate', monate)

    if not monate:
        monate = [str(date.today().year) + '_' + str(date.today().month)]

    selected_item = monate[0]
    if request.is_post_request():
        selected_item = request.values['date']
    month = int(float(selected_item.split("_")[1]))
    year = int(float(selected_item.split("_")[0]))

    table_data_selection = einzelbuchungen.select().select_month(month).select_year(year)
    table_ausgaben = table_data_selection.select_ausgaben()
    table_einnahmen = table_data_selection.select_einnahmen()

    kategorien = einzelbuchungen.get_alle_kategorien()
    color_chooser = viewcore.get_generic_color_chooser(list(kategorien))

    berechne_kreisdiagramm('ausgaben', color_chooser, result_context, table_ausgaben)
    berechne_kreisdiagramm('einnahmen', color_chooser, result_context, table_einnahmen)
    berechne_zusammenfassung(color_chooser, result_context, table_data_selection)

    berechne_plus_minus_chart_aktueller_monat(month, result_context, table_ausgaben, table_einnahmen, year)

    berechne_plus_minus_chart_uebersicht_ganzes_jahr(einzelbuchungen, result_context, year)

    return result_context


def berechne_plus_minus_chart_uebersicht_ganzes_jahr(einzelbuchungen, result_context, year):
    einnahmen_jahr = einzelbuchungen.select().select_einnahmen().select_year(year).sum()
    ausgaben_jahr = einzelbuchungen.select().select_ausgaben().select_year(year).sum()
    if einnahmen_jahr >= abs(ausgaben_jahr):
        result_context.add('color_uebersicht_jahr_gruppe_1', 'gray')
        result_context.add('name_uebersicht_jahr_gruppe_1', 'Gedeckte Einnahmen')
        result_context.add('wert_uebersicht_jahr_gruppe_1', Betrag(abs(ausgaben_jahr)))

        result_context.add('color_uebersicht_jahr_gruppe_2', 'lightgreen')
        result_context.add('name_uebersicht_jahr_gruppe_2', 'Einnahmenüberschuss')
        result_context.add('wert_uebersicht_jahr_gruppe_2', Betrag(einnahmen_jahr + ausgaben_jahr))

    else:
        result_context.add('color_uebersicht_jahr_gruppe_1', 'gray')
        result_context.add('name_uebersicht_jahr_gruppe_1', 'Gedeckte Ausgaben')
        result_context.add('wert_uebersicht_jahr_gruppe_1', Betrag(einnahmen_jahr))

        result_context.add('color_uebersicht_jahr_gruppe_2', 'red')
        result_context.add('name_uebersicht_jahr_gruppe_2', 'Ungedeckte Ausgaben')
        result_context.add('wert_uebersicht_jahr_gruppe_2', Betrag(abs(ausgaben_jahr + einnahmen_jahr)))


def berechne_plus_minus_chart_aktueller_monat(month, result_context, table_ausgaben, table_einnahmen, year):
    ausgaben_monat = table_ausgaben.sum()
    result_context.add('gesamt', Betrag(ausgaben_monat))
    einnahmen_monat = table_einnahmen.sum()
    result_context.add('gesamt_einnahmen', Betrag(einnahmen_monat))
    selected_date = str(year) + "_" + str(month).rjust(2, "0")
    result_context.add('selected_date', selected_date)
    result_context.add('selected_year', year)
    if einnahmen_monat >= abs(ausgaben_monat):
        result_context.add('color_uebersicht_gruppe_1', 'gray')
        result_context.add('name_uebersicht_gruppe_1', 'Gedeckte Ausgaben')
        result_context.add('wert_uebersicht_gruppe_1', Betrag(abs(ausgaben_monat)))

        result_context.add('color_uebersicht_gruppe_2', 'lightgreen')
        result_context.add('name_uebersicht_gruppe_2', 'Einnahmenüberschuss')
        result_context.add('wert_uebersicht_gruppe_2', Betrag(einnahmen_monat + ausgaben_monat))

    else:
        result_context.add('color_uebersicht_gruppe_1', 'gray')
        result_context.add('name_uebersicht_gruppe_1', 'Gedeckte Ausgaben')
        result_context.add('wert_uebersicht_gruppe_1', Betrag(einnahmen_monat))

        result_context.add('color_uebersicht_gruppe_2', 'red')
        result_context.add('name_uebersicht_gruppe_2', 'Ungedeckte Ausgaben')
        result_context.add('wert_uebersicht_gruppe_2', Betrag(abs(ausgaben_monat + einnahmen_monat)))


def berechne_zusammenfassung(color_chooser, result_context, table_data_selection):
    zusammenfassung = table_data_selection.get_month_summary()
    for _, kategorien_liste in zusammenfassung:
        for einheit in kategorien_liste:
            einheit['farbe'] = color_chooser.get_for_value(einheit['kategorie'])
    result_context.add('zusammenfassung', zusammenfassung)


def berechne_kreisdiagramm(prefix: str, color_chooser, result_context, table_einnahmen):
    einnahmen_liste = []
    einnahmen_labels = []
    einnahmen_data = BetragListe()
    einnahmen_colors = []
    for kategorie, row in table_einnahmen.group_by_kategorie().iterrows():
        einnahmen_labels.append(kategorie)
        einnahmen_data.append(Betrag(abs(row.Wert)))
        einnahmen_colors.append(color_chooser.get_for_value(kategorie))
        einnahmen_liste.append(
            {
                'kategorie': kategorie,
                'wert': Betrag(row.Wert),
                'color': color_chooser.get_for_value(kategorie)
            })
    result_context.add(prefix, einnahmen_liste)
    result_context.add(prefix + '_labels', einnahmen_labels)
    result_context.add(prefix + '_data', einnahmen_data)
    result_context.add(prefix + '_colors', einnahmen_colors)


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        html_base_page='einzelbuchungen/uebersicht_monat.html',
        context_creator=lambda db: UebersichtMonatContext(db.einzelbuchungen)
    )

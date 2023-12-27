import datetime

from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.viewcore import request_handler
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.context.builder import PageContext
from butler_offline.viewcore.context.builder import generate_page_context
from butler_offline.viewcore.renderhelper import Betrag, BetragListe
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.requirements import einzelbuchung_needed_decorator
from butler_offline.core.time import today


class UebersichtJahrContext:
    def __init__(self, einzelbuchungen: Einzelbuchungen):
        self._einzelbuchungen = einzelbuchungen

    def einzelbuchungen(self) -> Einzelbuchungen:
        return self._einzelbuchungen


def get_monats_namen(monat):
    return datetime.date(1900, monat, 1).strftime('%B')


def _filter(liste, num_monate):
    result = []
    for monat in range(1, 13):
        if monat not in num_monate:
            continue
        result.append(liste[monat - 1])
    return result


def _compute_pie_chart_prozentual(result_context: PageContext, jahr: int, context: UebersichtJahrContext):
    result = context.einzelbuchungen().get_jahresausgaben_nach_kategorie_prozentual(jahr)
    ausgaben_data: BetragListe = BetragListe()
    ausgaben_labels = []
    ausgaben_colors = []
    kategorien = context.einzelbuchungen().get_alle_kategorien()
    color_chooser = viewcore.get_generic_color_chooser(list(kategorien))

    for kategorie, wert in result.items():
        ausgaben_data.append(Betrag(abs(wert)))
        ausgaben_labels.append(kategorie)
        ausgaben_colors.append(color_chooser.get_for_value(kategorie))

    result_context.add('pie_ausgaben_data_prozentual', ausgaben_data)
    result_context.add('pie_ausgaben_labels', ausgaben_labels)
    result_context.add('pie_ausgaben_colors', ausgaben_colors)

    result = context.einzelbuchungen().get_jahreseinnahmen_nach_kategorie_prozentual(jahr)
    einnahmen_data: BetragListe = BetragListe()
    einnahmen_labels = []
    einnahmen_colors = []
    for kategorie, wert in result.items():
        einnahmen_data.append(Betrag(abs(wert)))
        einnahmen_labels.append(kategorie)
        einnahmen_colors.append(color_chooser.get_for_value(kategorie))

    result_context.add('pie_einnahmen_data_prozentual', einnahmen_data)
    result_context.add('pie_einnahmen_labels', einnahmen_labels)
    result_context.add('pie_einnahmen_colors', einnahmen_colors)

    return result_context


def _compile_colors(result, num_monate, color_chooser):
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


@einzelbuchung_needed_decorator()
def handle_request(request: Request, context: UebersichtJahrContext):
    year = today().year

    jahre = sorted(context.einzelbuchungen().get_jahre(), reverse=True)
    if year not in jahre and len(jahre) > 0:
        year = jahre[0]

    year = request.get_post_parameter_or_default(
        key='date',
        mapping_function=lambda x: int(float(x)),
        default=year
    )

    jahresbuchungs_tabelle = context.einzelbuchungen().select().select_year(year)
    jahres_ausgaben = jahresbuchungs_tabelle.select_ausgaben()
    jahres_einnahmen = jahresbuchungs_tabelle.select_einnahmen()
    kategorien = context.einzelbuchungen().get_alle_kategorien()
    color_chooser = viewcore.get_generic_color_chooser(list(kategorien))

    jahresausgaben = []
    for kategorie, jahresblock in jahres_ausgaben.group_by_kategorie().iterrows():
        jahresausgaben.append(
            {
                'kategorie': kategorie,
                'wert': Betrag(jahresblock.Wert),
                'color': color_chooser.get_for_value(kategorie)
            })

    jahreseinnahmen = []
    for kategorie, jahresblock in jahres_einnahmen.group_by_kategorie().iterrows():
        jahreseinnahmen.append({
            'kategorie': kategorie,
            'wert': Betrag(jahresblock.Wert),
            'color': color_chooser.get_for_value(kategorie)
        })

    monats_namen = []
    num_monate = sorted(list(set(jahresbuchungs_tabelle.raw_table().Datum.map(lambda x: x.month))))
    for num_monat in num_monate:
        monats_namen.append(get_monats_namen(num_monat))

    result_context = generate_page_context('jahresuebersicht')

    result_context.add('durchschnitt_monat_kategorien', str(
        list(context.einzelbuchungen().durchschnittliche_ausgaben_pro_monat(year).keys())))
    result_context.add('durchschnittlich_monat_wert', str(
        list(context.einzelbuchungen().durchschnittliche_ausgaben_pro_monat(year).values())))
    result_context = _compute_pie_chart_prozentual(result_context, year, context)

    laenge = 12
    if year == today().year:
        laenge = today().month

    result_context.add('buchungen', [
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
    ])
    result_context.add('zusammenfassung_ausgaben', jahresausgaben)
    result_context.add('zusammenfassung_einnahmen', jahreseinnahmen)
    result_context.add('monats_namen', monats_namen)
    result_context.add('selected_date', year)

    result_context.add('einnahmen', _compile_colors(
        jahres_einnahmen.inject_zeroes_for_year_and_kategories(year).sum_kategorien_monthly(),
        num_monate,
        color_chooser
    ))
    result_context.add('ausgaben', _compile_colors(
        jahres_ausgaben.inject_zeroes_for_year_and_kategories(year).sum_kategorien_monthly(),
        num_monate,
        color_chooser
    ))
    result_context.add('jahre', jahre)
    result_context.add('gesamt_ausgaben', Betrag(
        context.einzelbuchungen()
        .select()
        .select_year(year)
        .select_ausgaben()
        .sum()
    ))
    result_context.add('gesamt_einnahmen', Betrag(
        context.einzelbuchungen()
        .select()
        .select_year(year)
        .select_einnahmen()
        .sum()
    ))
    return result_context


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        html_base_page='einzelbuchungen/uebersicht_jahr.html',
        context_creator=lambda db: UebersichtJahrContext(db.einzelbuchungen)
    )

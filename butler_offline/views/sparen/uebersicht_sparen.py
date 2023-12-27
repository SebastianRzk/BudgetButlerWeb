from datetime import date

from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.core.database.sparen.depotauszuege import Depotauszuege
from butler_offline.core.database.sparen.depotwerte import Depotwerte
from butler_offline.core.database.sparen.kontos import Kontos
from butler_offline.core.database.sparen.order import Order
from butler_offline.core.database.sparen.orderdauerauftrag import OrderDauerauftrag
from butler_offline.core.database.sparen.sparbuchungen import Sparbuchungen
from butler_offline.viewcore import request_handler
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.context.builder import generate_page_context
from butler_offline.viewcore.converter import datum_to_german
from butler_offline.viewcore.renderhelper import Betrag, BetragListe
from butler_offline.viewcore.requirements import irgendwas_needed_decorator
from butler_offline.core.time import today


class SparenUebersichtContext:
    def __init__(self,
                 einzelbuchungen: Einzelbuchungen,
                 depotauszuege: Depotauszuege,
                 kontos: Kontos,
                 order: Order,
                 orderdauerauftrag: OrderDauerauftrag,
                 depotwerte: Depotwerte,
                 sparbuchungen: Sparbuchungen):
        self._einzelbuchungen = einzelbuchungen
        self._depotauszuege = depotauszuege
        self._kontos = kontos
        self._order = order
        self._orderdauerauftrag = orderdauerauftrag
        self._depotwerte = depotwerte
        self._sparbuchungen = sparbuchungen

    def einzelbuchungen(self) -> Einzelbuchungen:
        return self._einzelbuchungen

    def depotauszeuge(self) -> Depotauszuege:
        return self._depotauszuege

    def kontos(self) -> Kontos:
        return self._kontos

    def order(self) -> Order:
        return self._order

    def order_dauerauftraege(self):
        return self._orderdauerauftrag

    def depotwerte(self) -> Depotwerte:
        return self._depotwerte

    def sparbuchungen(self) -> Sparbuchungen:
        return self._sparbuchungen


def to_piechart(data_list, gesamt_wert):
    colors = []
    labels = []
    datasets = BetragListe()

    for element in data_list:
        if gesamt_wert.value() != 0:
            prozent = Betrag((100 * element['wert'].value()) / gesamt_wert.value())
        else:
            prozent = Betrag(0)

        colors.append(element['color'])
        labels.append(element['name'])
        datasets.append(prozent)

    return {
        'colors': colors,
        'labels': labels,
        'datasets': datasets
    }


def generate_konto_uebersicht(color_kontos, color_typen,
                              sparkontos: Kontos,
                              depotwerte: Depotwerte,
                              sparbuchungen: Sparbuchungen,
                              order: Order,
                              depotauszuege: Depotauszuege):
    gesamt_kontostand = 0
    gesamt_aufbuchungen = 0
    sparkonto_liste = []

    kontotypen_werte = dict.fromkeys(sparkontos.KONTO_TYPEN, 0)
    for typ in kontotypen_werte:
        kontotypen_werte[typ] = {'gesamt': 0, 'aufbuchungen': 0}

    db = sparkontos.get_all()
    for row_index, row in db.iterrows():
        aktueller_kontostand = 0
        aufbuchungen = 0

        kontoname = row.Kontoname
        kontotyp = row.Kontotyp

        if kontotyp == sparkontos.TYP_SPARKONTO or kontotyp == sparkontos.TYP_GENOSSENSCHAFTSANTEILE:
            aktueller_kontostand = sparbuchungen.get_kontostand_fuer(kontoname)
            aufbuchungen = sparbuchungen.get_aufbuchungen_fuer(kontoname)

        if kontotyp == sparkontos.TYP_DEPOT:
            aufbuchungen = order.get_order_fuer(kontoname)
            aktueller_kontostand = depotauszuege.get_kontostand_by(kontoname)

        gesamt_kontostand += aktueller_kontostand
        gesamt_aufbuchungen += aufbuchungen

        diff = aktueller_kontostand - aufbuchungen

        kontotypen_werte[kontotyp]['gesamt'] += aktueller_kontostand
        kontotypen_werte[kontotyp]['aufbuchungen'] += aufbuchungen

        sparkonto_liste.append({
            'index': row_index,
            'color': color_kontos.get_for_value(kontoname),
            'name': kontoname,
            'kontotyp': kontotyp,
            'wert': Betrag(aktueller_kontostand),
            'difference': Betrag(diff),
            'aufbuchungen': Betrag(aufbuchungen),
            'difference_is_negativ': diff < 0
        })

    kontotypen_liste = []
    for kontotyp in kontotypen_werte:
        if kontotyp == sparkontos.TYP_DEPOT:
            continue
        diff = kontotypen_werte[kontotyp]['gesamt'] - kontotypen_werte[kontotyp]['aufbuchungen']
        kontotypen_liste.append({
            'name': kontotyp,
            'color': color_typen.get_for_value(kontotyp),
            'wert': Betrag(kontotypen_werte[kontotyp]['gesamt']),
            'aufbuchungen': Betrag(kontotypen_werte[kontotyp]['aufbuchungen']),
            'difference': Betrag(diff),
        })

    depotwerte_nach_typ = depotwerte.get_isin_nach_typ()
    for typ in depotwerte_nach_typ:
        gesamt = 0
        aufbuchungen = 0
        for isin in depotwerte_nach_typ[typ]:
            aufbuchungen += order.get_order_fuer_depotwert(isin)
            gesamt += depotauszuege.get_depotwert_by(isin)
        diff = gesamt - aufbuchungen
        kontotypen_liste.append({
            'name': typ,
            'color': color_typen.get_for_value(typ),
            'wert': Betrag(gesamt),
            'aufbuchungen': Betrag(aufbuchungen),
            'difference': Betrag(diff),
        })

    gesamt_diff = gesamt_kontostand - gesamt_aufbuchungen

    gesamt = {
        'wert': Betrag(gesamt_kontostand),
        'difference': Betrag(gesamt_diff),
        'aufbuchungen': Betrag(gesamt_aufbuchungen),
        'difference_is_negativ': gesamt_diff < 0
    }
    return gesamt, sparkonto_liste, kontotypen_liste


def get_letztes_jahr_aufbuchungen(kontoname, gesamt):
    if len(gesamt) == 0:
        return 0
    return gesamt[-1][kontoname]['aufbuchungen']


def get_letztes_jahr_kontostand(kontoname, gesamt):
    if len(gesamt) == 0:
        return 0
    return gesamt[-1][kontoname]['kontostand']


def gesamt_uebersicht(
        einzelbuchungen: Einzelbuchungen,
        sparkontos: Kontos,
        sparbuchungen: Sparbuchungen,
        depotauszuege: Depotauszuege,
        order: Order
):
    min_jahr = get_min_jahr(einzelbuchungen)
    max_jahr = today().year

    year_kontostaende = []

    gesamt_uebersicht = []
    for jahr in range(min_jahr, max_jahr + 1):
        buchungen_jahr = einzelbuchungen.select().select_year(jahr).content.copy()
        ausgaben = buchungen_jahr[buchungen_jahr.Wert < 0].copy()
        ausgaben = ausgaben[ausgaben.Kategorie != 'Sparen'].Wert.sum()
        einnahmen = buchungen_jahr[buchungen_jahr.Wert > 0].copy()
        einnahmen = einnahmen[einnahmen.Kategorie != 'Sparen'].Wert.sum()

        db = sparkontos.get_all()

        sparen_aufbuchung = 0
        gesamt_sparen = 0

        year_kontos = {}

        for _, sparkonto in db.iterrows():
            kontostand = 0
            aufbuchungen = 0

            kontoname = sparkonto.Kontoname
            kontotyp = sparkonto.Kontotyp

            if kontotyp == sparkontos.TYP_SPARKONTO or kontotyp == sparkontos.TYP_GENOSSENSCHAFTSANTEILE:
                sparbuchungen_year = sparbuchungen.select_year(jahr)
                sparbuchungen_max_year = sparbuchungen.select_max_year(jahr)
                kontostand = sparbuchungen_max_year.get_kontostand_fuer(kontoname)
                aufbuchungen = sparbuchungen_year.get_aufbuchungen_fuer(kontoname)

            if kontotyp == sparkontos.TYP_DEPOT:
                depotauszuege_year = depotauszuege.select_max_year(jahr)
                order_year = order.select_year(jahr)
                aufbuchungen = order_year.get_order_fuer(kontoname)
                kontostand = depotauszuege_year.get_kontostand_by(kontoname)

            year_kontos[kontoname] = {
                'kontostand': Betrag(kontostand),
                'aufbuchungen': Betrag(aufbuchungen),
                'name': kontoname
            }

            gesamt_sparen += kontostand
            sparen_aufbuchung += aufbuchungen

        year_kontos['Gesamt'] = {
            'kontostand': Betrag(gesamt_sparen),
            'aufbuchungen': Betrag(sparen_aufbuchung),
            'name': 'Gesamt'
        }

        year_kontostaende.append(year_kontos)

        gesamt_uebersicht.append({
            'jahr': jahr,
            'ausgaben': ausgaben,
            'einnahmen': einnahmen,
            'sparen_aufbuchung': sparen_aufbuchung,
            'gesamt_sparen': gesamt_sparen,
        })

    return gesamt_uebersicht, year_kontostaende


def get_min_jahr(einzelbuchungen):
    datae = einzelbuchungen.content.copy().Datum
    if len(datae) == 0:
        return today().year - 1
    return datae.min().year


def berechne_gesamt_tabelle(jahresdaten: list):
    if len(jahresdaten) == 0:
        return [[]]

    kontos = []
    for element in jahresdaten[0]:
        if element == 'Gesamt':
            continue
        kontos.append(element)
    kontos = sorted(kontos)
    kontos.append('Gesamt')

    kontodaten = {}

    for jahr in jahresdaten:
        for konto in jahr:
            if konto not in kontodaten:
                kontodaten[konto] = BetragListe()
            kontodaten[konto].append(jahr[konto])

    gesamt = []

    for konto in kontos:
        gesamt.append(kontodaten[konto])

    return gesamt


def berechne_diagramm(data):
    result = [
        {
            'label': 'Einnahmen',
            'color': 'rgb(210, 214, 222)',
            'datasets': BetragListe()
        },
        {
            'label': 'Ausgaben',
            'color': 'rgba(60, 141, 188, 0.8)',
            'datasets': BetragListe()
        },
        {
            'label': 'Sparen',
            'color': 'rgb(0, 166, 90)',
            'datasets': BetragListe()
        }
    ]
    labels = []

    for jahr in data:
        labels.append(jahr['jahr'])
        result[0]['datasets'].append(Betrag(jahr['einnahmen']))
        result[1]['datasets'].append(Betrag(abs(jahr['ausgaben'])))
        result[2]['datasets'].append(Betrag(jahr['sparen_aufbuchung']))

    return labels, result


def berechne_kontogesamt(data):
    data_gesamt = data[-1]

    kontostand = BetragListe()
    aufbuchungen = BetragListe()

    for year in data_gesamt.content():
        kontostand.append(year['kontostand'])
        aufbuchungen.append(year['aufbuchungen'])

    return {
        'kontostand': kontostand,
        'aufbuchungen': aufbuchungen
    }


def get_last_order_for(konto, order: Order):
    order_content = order.content.copy()
    order_for_konto = order_content[order_content.Konto == konto]
    if len(order_for_konto) == 0:
        return None
    return order_for_konto.Datum.max()


def general_infos(
        sparkontos: Kontos,
        depotauszuege: Depotauszuege,
        order: Order
):
    kontos = sparkontos.get_depots()
    info = []
    for konto in kontos:
        latest_depotauszug = depotauszuege.get_latest_datum_by(konto)
        latest_order = get_last_order_for(
            konto,
            order=order
        )

        warning = False
        print('order', latest_order, 'auszug', latest_depotauszug)
        if latest_order and latest_depotauszug and latest_depotauszug < latest_order:
            warning = True

        if not latest_order:
            latest_order = ''
        else:
            latest_order = datum_to_german(latest_order)

        if not latest_depotauszug:
            latest_depotauszug = 'fehlend'
            warning = True
        else:
            latest_depotauszug = datum_to_german(latest_depotauszug)

        info.append({
            'konto': konto,
            'letzter_auszug': latest_depotauszug,
            'letzte_order': latest_order,
            'warning': warning
        })

    return {
        'kontos': info
    }


def get_sum(df):
    if len(df) == 0:
        return 0
    return df.Wert.sum()


def get_wert_sum(df):
    if len(df) == 0:
        return 0
    return get_sum(df[df.Wert > 0])


def berechne_order_typ(dauerauftrag_order, order: Order):
    order_gesamt_raw = order.content.copy()
    order_summe = get_wert_sum(order_gesamt_raw)
    dauerauftrag_order = get_wert_sum(dauerauftrag_order)

    return {
        'manual': Betrag(order_summe - dauerauftrag_order),
        'dauerauftrag': Betrag(dauerauftrag_order),
    }


def berechne_monatlich(order_dauerauftrag: OrderDauerauftrag,
                       depotwerte: Depotwerte):
    aktuelle_dauerauftraege = order_dauerauftrag.aktuelle_raw().copy()
    aktuelle_dauerauftraege = aktuelle_dauerauftraege[aktuelle_dauerauftraege.Wert > 0]

    isins = set(aktuelle_dauerauftraege.Depotwert.tolist())

    namen = []
    colors = []
    werte = BetragListe()
    monatlich = []
    color_chooser = viewcore.get_generic_color_chooser(list(sorted(isins)))

    for isin in sorted(isins):
        name = depotwerte.get_description_for(isin)
        wert = get_sum(aktuelle_dauerauftraege[aktuelle_dauerauftraege.Depotwert == isin])
        color = color_chooser.get_for_value(isin)

        namen.append(name)
        werte.append(Betrag(wert))
        colors.append(color)
        monatlich.append({
            'name': name,
            'wert': Betrag(wert),
            'color': color
        })

    return {
        'einzelwerte': monatlich,
        'colors': colors,
        'namen': namen,
        'werte': werte
    }


@irgendwas_needed_decorator()
def handle_request(_, context: SparenUebersichtContext):
    result_context = generate_page_context(page_name='sparen')

    kontos = context.kontos().get_all().Kontoname.tolist()
    typen = context.kontos().KONTO_TYPEN
    depot_typen = context.depotwerte().TYPES

    color_kontos = viewcore.get_generic_color_chooser(kontos)
    color_typen = viewcore.get_generic_color_chooser(typen + depot_typen)

    gesamt, kontos, typen = generate_konto_uebersicht(
        color_kontos,
        color_typen,
        sparkontos=context.kontos(),
        depotauszuege=context.depotauszeuge(),
        depotwerte=context.depotwerte(),
        order=context.order(),
        sparbuchungen=context.sparbuchungen(),
    )
    diagramm_uebersicht, year_kontostaende = gesamt_uebersicht(
        sparbuchungen=context.sparbuchungen(),
        depotauszuege=context.depotauszeuge(),
        order=context.order(),
        sparkontos=context.kontos(),
        einzelbuchungen=context.einzelbuchungen(),
    )
    gesamt_tabelle = berechne_gesamt_tabelle(year_kontostaende)
    gesamt_diagramm_labels, gesamt_diagramm_data = berechne_diagramm(diagramm_uebersicht)
    gesamt_linechart = berechne_kontogesamt(gesamt_tabelle)

    order_until_today = context.order_dauerauftraege().get_all_order_until_today()

    result_context.add('kontos', kontos)
    result_context.add('typen', typen)
    result_context.add('gesamt', gesamt)
    result_context.add('monatlich', berechne_monatlich(
        order_dauerauftrag=context.order_dauerauftraege(),
        depotwerte=context.depotwerte()
    ))
    result_context.add('order_typ', berechne_order_typ(
        order_until_today,
        order=context.order(),
    ))
    result_context.add('general_infos', general_infos(
        sparkontos=context.kontos(),
        depotauszuege=context.depotauszeuge(),
        order=context.order()
    ))
    result_context.add('konto_diagramm', to_piechart(kontos, gesamt['wert']))
    result_context.add('typen_diagramm', to_piechart(typen, gesamt['wert']))
    result_context.add('gesamt_diagramm_labels', gesamt_diagramm_labels)
    result_context.add('gesamt_diagramm_data', gesamt_diagramm_data)
    result_context.add('gesamt_linechart', gesamt_linechart)
    return result_context


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        context_creator=lambda db: SparenUebersichtContext(
            einzelbuchungen=db.einzelbuchungen,
            order=db.order,
            sparbuchungen=db.sparbuchungen,
            depotauszuege=db.depotauszuege,
            depotwerte=db.depotwerte,
            kontos=db.sparkontos,
            orderdauerauftrag=db.orderdauerauftrag
        ),
        html_base_page='sparen/uebersicht_sparen.html'
    )

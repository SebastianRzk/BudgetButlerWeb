from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.converter import from_double_to_german
from butler_offline.viewcore.converter import datum_to_german
from datetime import date


def to_piechart(data_list, gesamt_wert):
    colors = []
    labels = []
    datasets = []

    for element in data_list:
        if gesamt_wert != 0:
            prozent = '%.2f' % ((100 * element['wert']) / gesamt_wert)
        else:
            prozent = 0

        colors.append(element['color'])
        labels.append(element['name'])
        datasets.append(prozent)

    return {
        'colors': colors,
        'labels': labels,
        'datasets': datasets
    }


def generate_konto_uebersicht(color_kontos, color_typen):
    sparkontos = persisted_state.database_instance().sparkontos
    depotwerte = persisted_state.database_instance().depotwerte

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
            aktueller_kontostand = persisted_state.database_instance().sparbuchungen.get_kontostand_fuer(kontoname)
            aufbuchungen = persisted_state.database_instance().sparbuchungen.get_aufbuchungen_fuer(kontoname)

        if kontotyp == sparkontos.TYP_DEPOT:
            aufbuchungen = persisted_state.database_instance().order.get_order_fuer(kontoname)
            aktueller_kontostand = persisted_state.database_instance().depotauszuege.get_kontostand_by(kontoname)

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
            'wert': aktueller_kontostand,
            'difference': diff,
            'aufbuchungen': aufbuchungen,
            'wert_str': from_double_to_german(aktueller_kontostand),
            'difference_str': from_double_to_german(diff),
            'aufbuchungen_str': from_double_to_german(aufbuchungen),
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
            'wert': kontotypen_werte[kontotyp]['gesamt'],
            'wert_str': from_double_to_german(kontotypen_werte[kontotyp]['gesamt']),
            'aufbuchungen': kontotypen_werte[kontotyp]['aufbuchungen'],
            'aufbuchungen_str': from_double_to_german(kontotypen_werte[kontotyp]['aufbuchungen']),
            'difference': diff,
            'difference_str': from_double_to_german(diff)
        })

    depotwerte_nach_typ = depotwerte.get_isin_nach_typ()
    for typ in depotwerte_nach_typ:
        gesamt = 0
        aufbuchungen = 0
        for isin in depotwerte_nach_typ[typ]:
            aufbuchungen += persisted_state.database_instance().order.get_order_fuer_depotwert(isin)
            gesamt += persisted_state.database_instance().depotauszuege.get_depotwert_by(isin)
        diff = gesamt - aufbuchungen
        kontotypen_liste.append({
                'name': typ,
                'color': color_typen.get_for_value(typ),
                'wert': gesamt,
                'wert_str': from_double_to_german(gesamt),
                'aufbuchungen': aufbuchungen,
                'aufbuchungen_str': from_double_to_german(aufbuchungen),
                'difference': diff,
                'difference_str': from_double_to_german(diff)
            })


    gesamt_diff = gesamt_kontostand - gesamt_aufbuchungen

    gesamt = {
        'wert': gesamt_kontostand,
        'difference': gesamt_diff,
        'aufbuchungen': gesamt_aufbuchungen,
        'wert_str': from_double_to_german(gesamt_kontostand),
        'difference_str': from_double_to_german(gesamt_diff),
        'aufbuchungen_str': from_double_to_german(gesamt_aufbuchungen),
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


def gesamt_uebersicht():
    einzelbuchungen = persisted_state.database_instance().einzelbuchungen
    sparkontos = persisted_state.database_instance().sparkontos
    min_jahr = einzelbuchungen.content.copy()[einzelbuchungen.content.copy().Kategorie != 'Sparen'].Datum.min().year
    max_jahr = date.today().year

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

        for row_index, row in db.iterrows():
            kontostand = 0
            aufbuchungen = 0

            sparbuchungen_year = persisted_state.database_instance().sparbuchungen.select_year(jahr)
            sparbuchungen_max_year = persisted_state.database_instance().sparbuchungen.select_max_year(jahr)
            depotauszuege_year = persisted_state.database_instance().depotauszuege.select_max_year(jahr)
            order_year = persisted_state.database_instance().order.select_year(jahr)

            kontoname = row.Kontoname
            kontotyp = row.Kontotyp

            if kontotyp == sparkontos.TYP_SPARKONTO or kontotyp == sparkontos.TYP_GENOSSENSCHAFTSANTEILE:
                kontostand = sparbuchungen_max_year.get_kontostand_fuer(kontoname)
                aufbuchungen = sparbuchungen_year.get_aufbuchungen_fuer(kontoname)

            if kontotyp == sparkontos.TYP_DEPOT:
                aufbuchungen = order_year.get_order_fuer(kontoname)
                kontostand = depotauszuege_year.get_kontostand_by(kontoname)

            year_kontos[kontoname] = {
                'kontostand': kontostand,
                'kontostand_str': from_double_to_german(kontostand),
                'aufbuchungen': aufbuchungen,
                'aufbuchungen_str': from_double_to_german(aufbuchungen),
                'name': kontoname
            }

            gesamt_sparen += kontostand
            sparen_aufbuchung += aufbuchungen

        year_kontos['Gesamt'] = {
                'kontostand': gesamt_sparen,
                'aufbuchungen': sparen_aufbuchung,
                'kontostand_str': from_double_to_german(gesamt_sparen),
                'aufbuchungen_str': from_double_to_german(sparen_aufbuchung),
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


def berechne_gesamt_tabelle(jahresdaten):
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
                kontodaten[konto] = []
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
            'datasets': []
        },
        {
            'label': 'Ausgaben',
            'color': 'rgba(60, 141, 188, 0.8)',
            'datasets': []
        },
        {
            'label': 'Sparen',
            'color': 'rgb(0, 166, 90)',
            'datasets': []
        }
    ]
    labels = []

    for jahr in data:
        labels.append(jahr['jahr'])
        result[0]['datasets'].append('%.2f' % jahr['einnahmen'])
        result[1]['datasets'].append('%.2f' % abs(jahr['ausgaben']))
        result[2]['datasets'].append('%.2f' % jahr['sparen_aufbuchung'])

    return labels, result


def berechne_kontogesamt(data):
    data_gesamt = data[-1]

    kontostand = []
    aufbuchungen = []

    for year in data_gesamt:
        kontostand.append(year['kontostand'])
        aufbuchungen.append(year['aufbuchungen'])

    return {
        'kontostand': kontostand,
        'aufbuchungen': aufbuchungen
    }


def get_last_order_for(konto):
    order_content = persisted_state.database_instance().order.content.copy()
    order_for_konto = order_content[order_content.Konto == konto]
    if len(order_for_konto) == 0:
        return None
    return order_for_konto.Datum.max()


def general_infos():
    kontos = persisted_state.database_instance().sparkontos.get_depots()
    info = []
    for konto in kontos:
        latest_depotauszug = persisted_state.database_instance().depotauszuege.get_latest_datum_by(konto)
        latest_order = get_last_order_for(konto)

        warning = False;
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


def berechne_order_typ(dauerauftrag_order):
    order_gesamt_raw = persisted_state.database_instance().order.content.copy()
    order_summe = get_wert_sum(order_gesamt_raw)
    dauerauftrag_order = get_wert_sum(dauerauftrag_order)

    return {
        'manual': from_double_to_german(order_summe - dauerauftrag_order),
        'dauerauftrag': from_double_to_german(dauerauftrag_order),
        'manual_raw': '%.2f' % (order_summe - dauerauftrag_order),
        'dauerauftrag_raw': '%.2f' % dauerauftrag_order
    }


def berechne_monatlich():
    aktuelle_dauerauftraege = persisted_state.database_instance().orderdauerauftrag.aktuelle_raw().copy()
    aktuelle_dauerauftraege = aktuelle_dauerauftraege[aktuelle_dauerauftraege.Wert > 0]

    isins = set(aktuelle_dauerauftraege.Depotwert.tolist())

    namen = []
    colors = []
    werte = []
    monatlich = []
    color_chooser = viewcore.get_generic_color_chooser(list(sorted(isins)))

    for isin in sorted(isins):
        name = persisted_state.database_instance().depotwerte.get_description_for(isin)
        wert = get_sum(aktuelle_dauerauftraege[aktuelle_dauerauftraege.Depotwert == isin])
        color = color_chooser.get_for_value(isin)

        namen.append(name)
        werte.append('%.2f' % wert)
        colors.append(color)
        monatlich.append({
            'name': name,
            'wert': from_double_to_german(wert),
            'color': color
        })

    return {
        'einzelwerte': monatlich,
        'colors': colors,
        'namen': namen,
        'werte': werte
    }


def _handle_request(request):
    if persisted_state.database_instance().einzelbuchungen.anzahl() == 0:
        return viewcore.generate_error_context('uebersicht_sparen', 'Bitte erfassen Sie zuerst eine Einzelbuchung.')

    context = viewcore.generate_transactional_context('sparen')
    kontos = persisted_state.database_instance().sparkontos.get_all().Kontoname.tolist()
    typen = persisted_state.database_instance().sparkontos.KONTO_TYPEN
    depot_typen = persisted_state.database_instance().depotwerte.TYPES

    color_kontos = viewcore.get_generic_color_chooser(kontos)
    color_typen = viewcore.get_generic_color_chooser(typen + depot_typen)

    gesamt, kontos, typen = generate_konto_uebersicht(color_kontos, color_typen)
    diagramm_uebersicht, year_kontostaende = gesamt_uebersicht()
    gesamt_tabelle = berechne_gesamt_tabelle(year_kontostaende)
    gesamt_diagramm_labels, gesamt_diagramm_data = berechne_diagramm(diagramm_uebersicht)
    gesamt_linechart = berechne_kontogesamt(gesamt_tabelle)

    order_until_today = persisted_state.database_instance().orderdauerauftrag.get_all_order_until_today()

    context['kontos'] = kontos
    context['typen'] = typen
    context['gesamt'] = gesamt
    context['monatlich'] = berechne_monatlich()
    context['order_typ'] = berechne_order_typ(order_until_today)
    context['general_infos'] = general_infos()
    context['konto_diagramm'] = to_piechart(kontos, gesamt['wert'])
    context['typen_diagramm'] = to_piechart(typen, gesamt['wert'])
    context['gesamt_diagramm_labels'] = gesamt_diagramm_labels
    context['gesamt_diagramm_data'] = gesamt_diagramm_data
    context['gesamt_linechart'] = gesamt_linechart
    return context


def index(request):
    return request_handler.handle_request(request, _handle_request, 'sparen/uebersicht_sparen.html')


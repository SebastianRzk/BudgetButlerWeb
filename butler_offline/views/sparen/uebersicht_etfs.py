import gettext
import traceback

import pycountry

from butler_offline.core import time
from butler_offline.core.database.sparen.depotauszuege import Depotauszuege
from butler_offline.core.database.sparen.depotwerte import Depotwerte
from butler_offline.online_services.shares import etf_data
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.context.builder import generate_transactional_page_context, PageContext
from butler_offline.viewcore.converter import datum_to_german
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore.state.persisted_state import SharesInfo
from butler_offline.views.sparen import language
from butler_offline.viewcore.requirements import etfs_needed_decorator


class UebersichtEtfsContext:
    def __init__(self, depotauszuege: Depotauszuege, depotwerte: Depotwerte, shares_info: SharesInfo):
        self._depotauszuege = depotauszuege
        self._depotwerte = depotwerte
        self._shares_info = shares_info

    def depotwerte(self) -> Depotwerte:
        return self._depotwerte

    def depotauszuege(self) -> Depotauszuege:
        return self._depotauszuege

    def shares_info(self) -> SharesInfo:
        return self._shares_info


PAGE_NAME = 'uebersicht_etfs'


@etfs_needed_decorator()
def handle_request(request: Request, context: UebersichtEtfsContext):
    result_context = generate_transactional_page_context(PAGE_NAME)
    if request.post_action_is('update_data'):
        result_context = _update_data(request.values['isin'], result_context, shares_info=context.shares_info())
    return _generate_content(result_context, context=context)


def _update_data(isin, context: PageContext, shares_info: SharesInfo) -> PageContext:
    try:
        data = etf_data.get_data_for(isin)
        date = datum_to_german(time.today())
        shares_info.save(isin, date, etf_data.SOURCE, data)
        context.add_user_success_message(language.SHARES_DATA_UPDATED.format(isin=isin))
    except:
        traceback.print_exc()
        context.add_user_error_message(language.SHARES_DATA_NOT_UPDATED.format(isin=isin))
    return context


def _translate(region_code, lang):
    region = pycountry.countries.get(alpha_3=region_code)
    if not region:
        print('Region nicht gefunden für code:', region_code)
        return region_code
    translation = lang.gettext(region)
    if not translation:
        print('Region konnte nicht übersetzt werden', region)
        return region
    return translation.name


def get_data(shares_info_resolver, isins_with_data, wert_resolver, depotwerte, translator):
    if not isins_with_data:
        return None
    order = []
    regions = []
    gesamt_betrag = 0

    for isin_index in range(0, len(isins_with_data)):
        isin = isins_with_data[isin_index]
        data = shares_info_resolver(isin)
        wert = wert_resolver(isin)
        gesamt_betrag += wert

        for region in data.keys():
            data_to_present = {
                'euro': 0,
                'euro_str': '0,00',
                'percent': 0,
                'percent_str': '0,00'
            }

            if region in data:
                region_percent = data[region]
                data_to_present = {
                    'euro': (region_percent * wert) / 100,
                    'euro_str': '%.2f' % ((region_percent * wert) / 100),
                    'percent': region_percent,
                    'percent_str': '%.2f' % region_percent
                }

            if region not in order:
                order.append(region)
                regions.append([{
                    'euro': 0,
                    'euro_str': '0,00',
                    'percent': 0,
                    'percent_str': '0,00'
                } for _ in range(0, isin_index)])

            region_index_in_list = order.index(region)
            regions[region_index_in_list].append(data_to_present)

        # Fill empty regions
        for r in regions:
            if len(r) == isin_index + 1:
                continue
            r.append({
                'euro': 0,
                'euro_str': '0,00',
                'percent': 0,
                'percent_str': '0,00'
            })
    # Compute gesamt
    for region_index in range(0, len(regions)):
        region = regions[region_index]
        wert = 0
        for share in region:
            wert += share['euro']

        prozent = 0
        if gesamt_betrag:
            prozent = ((wert * 100) / gesamt_betrag)

        region.insert(0,
                      {
                          'euro': wert,
                          'euro_str': '%.2f' % wert,
                          'percent': prozent,
                          'percent_str': '%.2f' % prozent
                      })
        region.insert(0, translator(order[region_index]))

    regions = list(reversed(sorted(regions, key=lambda x: x[1]['euro'])))

    return {
        'header': ['Gesamt'] + [depotwerte.get_description_for(e) for e in isins_with_data],
        'data': regions
    }


def _get_costs(shares_data, isins_with_data, wert_resolver, depotwerte):
    if not isins_with_data:
        return None

    total_cost_eur = 0
    total_eur = 0
    data = []

    for isin in isins_with_data:
        wert = wert_resolver(isin)
        cost_percent = shares_data.get_latest_data_for(isin)[SharesInfo.KOSTEN]
        cost_eur = wert * (cost_percent / 100)
        total_cost_eur += cost_eur
        total_eur += wert

        data.append({
            'name': depotwerte.get_description_for(isin),
            'costs_percent': '%.2f' % cost_percent,
            'costs_eur': '%.2f' % cost_eur
        })
    cost_percent = 0
    if total_eur:
        cost_percent = (total_cost_eur * 100) / total_eur

    gesamt = {
        'name': 'Gesamt',
        'costs_percent': '%.2f' % cost_percent,
        'costs_eur': '%.2f' % total_cost_eur
    }

    return {'data': data,
            'gesamt': gesamt}


def _generate_content(result_context: PageContext, context: UebersichtEtfsContext):
    depotwerte = context.depotwerte()
    shares_info = context.shares_info()
    depotauszuege = context.depotauszuege()
    isins = depotwerte.get_valid_isins()
    etfs = []
    for isin in isins:
        isin_datum = 'Noch keine Daten'
        if shares_info.get_last_changed_date_for(isin):
            isin_datum = shares_info.get_last_changed_date_for(isin)

        etfs.append(
            {
                'Name': depotwerte.get_description_for(isin),
                'Datum': isin_datum,
                'ISIN': isin
            }
        )

    all_relevant_isins = depotauszuege.get_isins_invested_by()
    isins_with_data = shares_info.filter_out_isins_without_data(all_relevant_isins)

    german = gettext.translation('iso3166-3', pycountry.LOCALES_DIR, languages=['de'])

    result_context.add('etfs', etfs)
    result_context.add('regions', get_data(
        lambda x: shares_info.get_latest_data_for(x)[SharesInfo.REGIONEN],
        isins_with_data,
        lambda x: depotauszuege.get_depotwert_by(x),
        depotwerte,
        lambda x: _translate(x, german)
    ))
    result_context.add('sectors', get_data(
        lambda x: shares_info.get_latest_data_for(x)[SharesInfo.SEKTOREN],
        isins_with_data,
        lambda x: depotauszuege.get_depotwert_by(x),
        depotwerte,
        lambda x: x
    ))
    result_context.add('costs',
                       _get_costs(shares_info, isins_with_data, lambda x: depotauszuege.get_depotwert_by(x),
                                  depotwerte))

    return result_context


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        html_base_page='sparen/uebersicht_etfs.html',
        context_creator=lambda db: UebersichtEtfsContext(
            depotwerte=db.depotwerte,
            depotauszuege=db.depotauszuege,
            shares_info=persisted_state.shares_data()
        )
    )

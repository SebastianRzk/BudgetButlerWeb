from butler_offline.viewcore import request_handler
from butler_offline.core import time
from butler_offline.views.sparen.language import NO_VALID_ISIN_IN_DB
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore.converter import datum_to_german
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.online_services.shares import etf_data
from butler_offline.viewcore import base_html
from butler_offline.core.shares import SharesInfo
import gettext
import pycountry
import traceback
from butler_offline.views.sparen import language
from butler_offline.viewcore.context import generate_transactional_context, generate_error_context

PAGE_NAME = 'uebersicht_etfs'


def _handle_request(request):
    context = generate_transactional_context(PAGE_NAME)
    if post_action_is(request, 'update_data'):
        context = _update_data(request.values['isin'], context)
    return _generate_content(context)


def _update_data(isin, context):
    try:
        data = etf_data.get_data_for(isin)
        date = datum_to_german(time.today())
        persisted_state.shares_data().save(isin, date, etf_data.SOURCE, data)
        return base_html.set_success_message(context, language.SHARES_DATA_UPDATED.format(isin=isin))
    except:
        traceback.print_exc()
        return base_html.set_error_message(
            context,
            language.SHARES_DATA_NOT_UPDATED.format(isin=isin))


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
                    'euro_str': '%.2f' % ((region_percent * wert)/100),
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
        cost_eur = wert*(cost_percent / 100)
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


def _generate_content(context):
    depotwerte = persisted_state.database_instance().depotwerte
    shares_info = persisted_state.shares_data()
    depotauszuege = persisted_state.database_instance().depotauszuege
    isins = depotwerte.get_valid_isins()
    if not isins:
        return generate_error_context(PAGE_NAME, NO_VALID_ISIN_IN_DB)

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

    german = gettext.translation('iso3166', pycountry.LOCALES_DIR, languages=['de'])

    context['etfs'] = etfs
    context['regions'] = get_data(
        lambda x: shares_info.get_latest_data_for(x)[SharesInfo.REGIONEN],
        isins_with_data,
        lambda x: depotauszuege.get_depotwert_by(x),
        depotwerte,
        lambda x: _translate(x, german)
    )
    context['sectors'] = get_data(
        lambda x: shares_info.get_latest_data_for(x)[SharesInfo.SEKTOREN],
        isins_with_data,
        lambda x: depotauszuege.get_depotwert_by(x),
        depotwerte,
        lambda x: x
    )
    context['costs'] = _get_costs(shares_info, isins_with_data, lambda x: depotauszuege.get_depotwert_by(x), depotwerte)

    return context


def index(request):
    return request_handler.handle_request(request, _handle_request, 'sparen/uebersicht_etfs.html')


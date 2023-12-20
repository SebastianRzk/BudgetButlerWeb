from butler_offline.views.sparen.uebersicht_etfs import handle_request, UebersichtEtfsContext
from butler_offline.test.request_stubs import GetRequest
from butler_offline.core.time import today
from butler_offline.core.shares import sectors
from butler_offline.viewcore.converter import datum_to_string, datum_to_german
from butler_offline.viewcore import requester
from butler_offline.test.requester_stub import RequesterStub
from butler_offline.test.request_stubs import PostRequestAction
from butler_offline.views.sparen import language
from butler_offline.core.shares.shares_manager import SharesInfo
from butler_offline.core.database.sparen.depotwerte import Depotwerte
from butler_offline.core.database.sparen.depotauszuege import Depotauszuege
from butler_offline.test.test import assert_info_message_keine_etfs_erfasst_in_context, assert_keine_message_set


def basic_context(
        shares_info: SharesInfo = SharesInfo({}),
        depotwerte: Depotwerte = Depotwerte(),
        depotauszuege: Depotauszuege = Depotauszuege()
) -> UebersichtEtfsContext:
    return UebersichtEtfsContext(
        depotauszuege=depotauszuege,
        shares_info=shares_info,
        depotwerte=depotwerte
    )


def test_load_page_without_data_should_render_with_info_message():
    context = handle_request(
        request=GetRequest(),
        context=basic_context())

    assert context.is_ok()
    assert_info_message_keine_etfs_erfasst_in_context(result=context)


def test_load_page_with_data_should_show_no_message():
    context = handle_request(
        request=GetRequest(),
        context=context_with_test_data()
    )
    assert_keine_message_set(result=context)


def test_load_page_without_shares_data():
    context = handle_request(
        request=GetRequest(),
        context=context_with_test_data()
    )

    assert context.get('etfs') == [
        {
            'Name': 'some name (isin56789012)',
            'Datum': 'Noch keine Daten',
            'ISIN': 'isin56789012'
        }
    ]


def context_with_test_data():
    return basic_context(depotwerte=(get_test_data()))


def get_test_data():
    depotwerte = Depotwerte()
    depotwerte.add(name='some name', isin='isin56789012', typ=depotwerte.TYP_ETF)
    return depotwerte


def test_content():
    depotwerte = Depotwerte()
    depotwerte.add(name='large_etf', isin='1isin6789012', typ=depotwerte.TYP_ETF)
    depotwerte.add(name='small_etf', isin='2isin6789012', typ=depotwerte.TYP_ETF)

    depotauszuege = Depotauszuege()
    depotauszuege.add(depotwert='1isin6789012', datum=today(), konto='', wert=900)
    depotauszuege.add(depotwert='2isin6789012', datum=today(), konto='', wert=100)

    shares_data = SharesInfo({})
    shares_data.save(
        isin='1isin6789012',
        source='',
        date=datum_to_string(today()),
        data={
            SharesInfo.REGIONEN: {
                'DEU': 0.40,
                'USA': 0.60
            },
            SharesInfo.SEKTOREN: {
                sectors.BASISKONSUMGUETER: 50,
                sectors.ENERGIE: 50
            },
            SharesInfo.KOSTEN: 0.20
        }
    )
    shares_data.save(
        isin='2isin6789012',
        source='',
        date=datum_to_string(today()),
        data={
            SharesInfo.REGIONEN: {
                'NOR': 0.10,
                'DEU': 0.90
            },
            SharesInfo.SEKTOREN: {
                sectors.BASISKONSUMGUETER: 50,
                sectors.IMMOBILIEN: 50
            },
            SharesInfo.KOSTEN: 1.5,
        }
    )

    result = handle_request(
        request=GetRequest(),
        context=basic_context(shares_info=shares_data,
                              depotwerte=depotwerte,
                              depotauszuege=depotauszuege)
    )

    assert result.get('regions') == {
        'header': ['Gesamt',
                   'large_etf (1isin6789012)',
                   'small_etf (2isin6789012)'],
        'data': [
            ['United States',
             {'euro': 5.4,
              'euro_str': '5.40',
              'percent': 0.54,
              'percent_str': '0.54'},
             {'euro': 5.4,
              'euro_str': '5.40',
              'percent': 0.6,
              'percent_str': '0.60'},
             {'euro': 0,
              'euro_str': '0,00',
              'percent': 0,
              'percent_str': '0,00'}],
            ['Germany',
             {'euro': 4.5,
              'euro_str': '4.50',
              'percent': 0.45,
              'percent_str': '0.45'},
             {'euro': 3.6,
              'euro_str': '3.60',
              'percent': 0.4,
              'percent_str': '0.40'},
             {'euro': 0.9,
              'euro_str': '0.90',
              'percent': 0.9,
              'percent_str': '0.90'}],
            ['Norway',
             {'euro': 0.1,
              'euro_str': '0.10',
              'percent': 0.01,
              'percent_str': '0.01'},
             {'euro': 0,
              'euro_str': '0,00',
              'percent': 0,
              'percent_str': '0,00'},
             {'euro': 0.1,
              'euro_str': '0.10',
              'percent': 0.1,
              'percent_str': '0.10'}]],
    }

    assert result.get('sectors') == {
        'data': [[
            'Basiskonsumgüter',
            {'euro': 500.0,
             'euro_str': '500.00',
             'percent': 50.0,
             'percent_str': '50.00'},
            {'euro': 450.0,
             'euro_str': '450.00',
             'percent': 50,
             'percent_str': '50.00'},
            {'euro': 50.0,
             'euro_str': '50.00',
             'percent': 50,
             'percent_str': '50.00'}],
            ['Energie',
             {'euro': 450.0,
              'euro_str': '450.00',
              'percent': 45.0,
              'percent_str': '45.00'},
             {'euro': 450.0,
              'euro_str': '450.00',
              'percent': 50,
              'percent_str': '50.00'},
             {'euro': 0,
              'euro_str': '0,00',
              'percent': 0,
              'percent_str': '0,00'}],
            ['Immobilien',
             {'euro': 50.0,
              'euro_str': '50.00',
              'percent': 5.0,
              'percent_str': '5.00'},
             {'euro': 0,
              'euro_str': '0,00',
              'percent': 0,
              'percent_str': '0,00'},
             {'euro': 50.0,
              'euro_str': '50.00',
              'percent': 50,
              'percent_str': '50.00'}]],
        'header': ['Gesamt', 'large_etf (1isin6789012)', 'small_etf (2isin6789012)']}
    assert result.get('costs') == {
        'data': [{'costs_eur': '1.80',
                  'costs_percent': '0.20',
                  'name': 'large_etf (1isin6789012)'},
                 {'costs_eur': '1.50',
                  'costs_percent': '1.50',
                  'name': 'small_etf (2isin6789012)'}],
        'gesamt': {'costs_eur': '3.30',
                   'costs_percent': '0.33',
                   'name': 'Gesamt'},
    }


DEMO_DATA = '''
{
   "totalFee":0.38,
   "indexName":"WisdomTree Europe Small Cap Dividend Index",
   "name":"WisdomTree Europe SmallCap Dividend UCITS ETF",
   "isin":"DE000A14ND46",
   "provider":"WisdomTree",
   "listings":[

   ],
   "regions":[
      {
         "country":"GBR",
         "percentage":29.52
      },
      {
         "country":"NOR",
         "percentage":12.55
      }
   ],
   "sectors":[
      {
         "sector":"INDUSTRIALS",
         "percentage":20.61
      }
   ]
}
'''


def test_refresh_data():
    shares_info = SharesInfo({})
    requester.INSTANCE = RequesterStub(
        {
            'https://api.etf-data.com/product/DE000A14ND46': DEMO_DATA
        }
    )

    result = handle_request(
        request=PostRequestAction('update_data', {'isin': 'DE000A14ND46'}),
        context=basic_context(shares_info=shares_info)
    )
    assert result.user_success_message()
    assert result.user_success_message().content() == language.SHARES_DATA_UPDATED.format(isin='DE000A14ND46')
    assert shares_info.get_last_changed_date_for('DE000A14ND46') == datum_to_german(today())

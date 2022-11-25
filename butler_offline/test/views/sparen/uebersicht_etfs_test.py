from butler_offline.core import file_system
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.viewcore.state.persisted_state import persisted_state
from butler_offline.viewcore import request_handler
from butler_offline.views.sparen.uebersicht_etfs import index
from butler_offline.views.sparen.language import NO_VALID_ISIN_IN_DB
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.core.time import today
from butler_offline.core.shares import SharesInfo
from butler_offline.core.shares import sectors
from butler_offline.viewcore.converter import datum_to_string,datum_to_german
from butler_offline.viewcore import requester
from butler_offline.test.RequesterStub import RequesterStub
from butler_offline.test.RequestStubs import VersionedPostRequestAction
from butler_offline.test.database_util import untaint_database
from butler_offline.views.sparen import language
from butler_offline.viewcore.context import get_error_message

def set_up():
    file_system.INSTANCE = FileSystemStub()
    persisted_state.DATABASE_INSTANCE = None
    persisted_state.SHARES_DATA = None
    request_handler.stub_me()


def test_load_page_without_data():
    set_up()
    context = index(GetRequest())

    assert get_error_message(context) == NO_VALID_ISIN_IN_DB


def test_load_page_without_shares_data():
    set_up()
    depotwerte = persisted_state.database_instance().depotwerte
    depotwerte.add(name='some name', isin='isin56789012', typ=depotwerte.TYP_ETF)
    untaint_database(database=persisted_state.database_instance())

    context = index(GetRequest())

    assert context['etfs'] == [
        {
            'Name': 'some name (isin56789012)',
            'Datum': 'Noch keine Daten',
            'ISIN': 'isin56789012'
        }
    ]


def test_content():
    set_up()

    depotwerte = persisted_state.database_instance().depotwerte
    depotwerte.add(name='large_etf', isin='1isin6789012', typ=depotwerte.TYP_ETF)
    depotwerte.add(name='small_etf', isin='2isin6789012', typ=depotwerte.TYP_ETF)

    persisted_state.database_instance().depotauszuege.add(depotwert='1isin6789012', datum=today(), konto='', wert=900)
    persisted_state.database_instance().depotauszuege.add(depotwert='2isin6789012', datum=today(), konto='', wert=100)

    persisted_state.shares_data().save(
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
    persisted_state.shares_data().save(
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
    untaint_database(database=persisted_state.database_instance())

    result = index(GetRequest())

    assert result['regions'] == {
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

    assert result['sectors'] == {
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
    assert result['costs'] == {
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
    requester.INSTANCE = RequesterStub(
        {
            'https://api.etf-data.com/product/DE000A14ND46': DEMO_DATA
        }
    )

    result = index(VersionedPostRequestAction('update_data', {'isin': 'DE000A14ND46'}))
    assert result['message']
    assert result['message_type'] == 'success'
    assert result['message_content'] == language.SHARES_DATA_UPDATED.format(isin='DE000A14ND46')
    assert persisted_state.shares_data().get_last_changed_date_for('DE000A14ND46') == datum_to_german(today())




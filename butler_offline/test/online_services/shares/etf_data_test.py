from butler_offline.online_services.shares.etf_data import get_data_for
from butler_offline.test.requester_stub import RequesterStub
from butler_offline.viewcore import requester

DEMO_DATA = '''
{
   "totalFee":0.38,
   "indexName":"WisdomTree Europe Small Cap Dividend Index",
   "name":"WisdomTree Europe SmallCap Dividend UCITS ETF",
   "isin":"DE000A14ND46",
   "provider":"WisdomTree",
   "domicile":"IRL",
   "baseCurrency":"EUR",
   "assetClass":"EQUITY",
   "replicationMethod":"PHYSICAL",
   "distributionFrequency":"SEMI_ANNUALLY",
   "distributionType":"DISTRIBUTING",
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
      },
      {
         "sector":"FINANCIALS",
         "percentage":16.35
      },
      {
         "sector":"CONSUMER_DISCRETIONARY",
         "percentage":11.4
      },
      {
         "sector":"MATERIALS",
         "percentage":8.11
      },
      {
         "sector":"ENERGY",
         "percentage":7.43
      },
      {
         "sector":"HEALTH_CARE",
         "percentage":6.99
      },
      {
         "sector":"INFORMATION_TECHNOLOGY",
         "percentage":6.75
      },
      {
         "sector":"UTILITIES",
         "percentage":6.55
      },
      {
         "sector":"REAL_ESTATE",
         "percentage":6.19
      },
      {
         "sector":"CONSUMER_STAPLES",
         "percentage":5.87
      },
      {
         "sector":"COMMUNICATION_SERVICES",
         "percentage":3.7
      }
   ]
}
'''


def test_parse_json():
    requester.INSTANCE = RequesterStub(
        {
            'https://api.etf-data.com/product/DE000A14ND46': DEMO_DATA
        }
    )

    result = get_data_for('DE000A14ND46')

    assert result == {'IndexName': 'WisdomTree Europe Small Cap Dividend Index',
                      'Kosten': 0.38,
                      'Name': 'WisdomTree Europe SmallCap Dividend UCITS ETF',
                      'Regionen': {'GBR': 29.52, 'NOR': 12.55},
                      'Sektoren': {'Basiskonsumgüter': 5.87,
                                   'Energie': 7.43,
                                   'Finanzen': 16.35,
                                   'Gesundheitswesen': 6.99,
                                   'Immobilien': 6.19,
                                   'Industriegüter': 20.61,
                                   'Informationstechnologie': 6.75,
                                   'Kommunikationsdienste': 3.70,
                                   'Konsumgüter': 11.40,
                                   'Roh- und Grundstoffe': 8.11,
                                   'Sonstiges': 0.05,
                                   'Versorgungsunternehmen': 6.55}}

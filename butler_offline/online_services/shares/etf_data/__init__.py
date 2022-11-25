from butler_offline.viewcore import requester
from butler_offline.core.shares import sectors
from butler_offline.core.shares import SharesInfo
from textwrap import shorten
import json
import logging

URL = 'https://api.etf-data.com/product/{isin}'
SOURCE = 'api.etf-data.com'


def get_data_for(isin):
    data = json.loads(requester.instance().get(URL.format(isin=isin)))
    logging.debug('loaded etf data: %s', data)
    return _map_data(data)


_KEY_REGIONS = 'regions'
_KEY_PERCENTAGE = 'percentage'
_KEY_REGION_NAME = 'country'

_KEY_SECTORS = 'sectors'
_KEY_SECTORS_NAME = 'sector'

_SECTORS_MAPPING = {
    'CONSUMER_DISCRETIONARY': sectors.KONSUMGUETER,
    'CONSUMER_STAPLES': sectors.BASISKONSUMGUETER,
    'ENERGY': sectors.ENERGIE,
    'MATERIALS': sectors.ROHSTOFFE,
    'INDUSTRIALS': sectors.INDUSTRIEGUETER,
    'HEALTH_CARE': sectors.GESUNDHEITSWESEN,
    'FINANCIALS': sectors.FINANZEN,
    'INFORMATION_TECHNOLOGY': sectors.INFORMATIONSTECHNOLOGIE,
    'REAL_ESTATE': sectors.IMMOBILIEN,
    'COMMUNICATION_SERVICES': sectors.KOMMUNIKATIONSDIENSTE,
    'UTILITIES': sectors.VERSORGUNGSUNTERNEHMEN,
    'OTHER': sectors.SONSTIGES
}


def _to_float(number):
    return round(number, 2)


def _map_data(json_data):
    regions = {}
    for region in json_data[_KEY_REGIONS]:
        region_str = str(region[_KEY_REGION_NAME])[:3]
        percent = _to_float(region[_KEY_PERCENTAGE])
        regions[region_str] = percent

    _sectors = {}
    sum_percent = 0
    for sector in json_data[_KEY_SECTORS]:
        name = _SECTORS_MAPPING[sector[_KEY_SECTORS_NAME]]
        percent = _to_float(sector[_KEY_PERCENTAGE])
        _sectors[name] = percent
        sum_percent += percent
    _sectors[sectors.SONSTIGES] = round(100.00 - sum_percent, 2)

    return {
        SharesInfo.NAME: shorten(str(json_data['name']), 60),
        SharesInfo.INDEX_NAME: shorten(str(json_data['indexName']), 60),
        SharesInfo.KOSTEN: _to_float(json_data['totalFee']),
        SharesInfo.REGIONEN: regions,
        SharesInfo.SEKTOREN: _sectors
    }

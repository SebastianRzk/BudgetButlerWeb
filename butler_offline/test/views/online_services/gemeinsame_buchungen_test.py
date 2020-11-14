
from butler_offline.viewcore import requester
from butler_offline.views.online_services.gemeinsame_buchungen import get_gemeinsame_buchungen,\
    upload_gemeinsame_buchungen, delete_gemeinsame_buchungen
from butler_offline.test.RequesterStub import RequesterStub
from butler_offline.views.online_services.session import OnlineAuth



_JSON_IMPORT_DATA = '''
[
{"id":"122","datum":"2019-07-15","name":"Testausgabe1","kategorie":"Essen","wert":"-1.3", "user":"Sebastian", "zielperson":"Sebastian"},
{"id":"123","datum":"2019-07-11","name":"Testausgabe2","kategorie":"Essen","wert":"-0.9", "user":"other", "zielperson":"other"}
]
'''

_RESULT_OK = '''
{
    "result": "OK"
}
'''


def test_get_gemeinsame_buchungen():
    requester.INSTANCE = RequesterStub({'https://test.test/api/gemeinsamebuchung.php': _JSON_IMPORT_DATA})

    result = get_gemeinsame_buchungen('https://test.test/api', OnlineAuth(None, None, None))

    assert result[0]["id"] == "122"
    assert result[0]["name"] == "Testausgabe1"
    assert result[0]["user"] == "Sebastian"
    assert result[0]["zielperson"] == "Sebastian"
    assert result[1]["id"] == "123"
    assert result[1]["name"] == "Testausgabe2"
    assert result[1]["user"] == "other"
    assert result[1]["zielperson"] == "other"


def test_upload_gemeinsame_buchungen():
    api_url = 'https://test.test/api/gemeinsamebuchung.php'
    data = ['Gemeinsame Buchungen']
    requester.INSTANCE = RequesterStub({api_url: _RESULT_OK}, auth_cookies='auth_cookies')

    result = upload_gemeinsame_buchungen('https://test.test/api', data, OnlineAuth('', '', 'auth_cookies'))

    assert result
    assert requester.INSTANCE.data_of_request(api_url) == [data]


def test_delete_gemeinsame_buchugen():
    requester.INSTANCE = RequesterStub({'https://test.test/deletegemeinsam.php': 'ok'})

    delete_gemeinsame_buchungen('https://test.test', auth_container=OnlineAuth(None, None, None))

    assert requester.INSTANCE.call_count_of('https://test.test/deletegemeinsam.php') == 1


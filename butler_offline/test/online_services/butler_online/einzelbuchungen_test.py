
from butler_offline.viewcore import requester
from butler_offline.online_services.butler_online.einzelbuchungen import get_einzelbuchungen, delete_einzelbuchungen
from butler_offline.test.requester_stub import RequesterStub
from butler_offline.online_services.butler_online.session import OnlineAuth

_JSON_IMPORT_DATA = '''
[
{"id":"122","datum":"2019-07-15","name":"Testausgabe1","kategorie":"Essen","wert":"-1.3"},
{"id":"123","datum":"2019-07-11","name":"Testausgabe2","kategorie":"Essen","wert":"-0.9"}
]
'''


def test_import_einzelbuchungen():

    requester.INSTANCE = RequesterStub({'https://test.test/api/einzelbuchungen': _JSON_IMPORT_DATA})
    result = get_einzelbuchungen('https://test.test/', auth_container=OnlineAuth(None, None))

    assert result[0]["id"] == "122"
    assert result[0]["name"] == "Testausgabe1"
    assert result[1]["id"] == "123"
    assert result[1]["name"] == "Testausgabe2"


def test_delete_einzelbuchhungen():
    requester.INSTANCE = RequesterStub({'https://test.test/api/einzelbuchungen': 'ok'})

    delete_einzelbuchungen('https://test.test/', auth_container=OnlineAuth(None, None))

    assert requester.INSTANCE.call_count_of('https://test.test/api/einzelbuchungen') == 1


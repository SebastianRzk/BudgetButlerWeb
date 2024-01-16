from butler_offline.online_services.butler_online.session import OnlineAuth
from butler_offline.online_services.butler_online.settings import set_kategorien
from butler_offline.test.requester_stub import RequesterStub
from butler_offline.viewcore import requester


def test_set_kategorien():
    requester.INSTANCE = RequesterStub({'https://test.test/api/kategorien/batch': 'ok'})

    set_kategorien('https://test.test/', ['kategorie1', 'kategorie2'], auth_container=OnlineAuth(None, None))

    assert requester.INSTANCE.call_count_of('https://test.test/api/kategorien/batch') == 1
    assert requester.INSTANCE.data_of_request('https://test.test/api/kategorien/batch') == [['kategorie1', 'kategorie2']]

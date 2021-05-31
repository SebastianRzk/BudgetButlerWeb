
from butler_offline.viewcore import requester
from butler_offline.online_services.butler_online.settings import set_kategorien
from butler_offline.test.RequesterStub import RequesterStub
from butler_offline.online_services.butler_online.session import OnlineAuth


def test_set_kategorien():
    requester.INSTANCE = RequesterStub({'https://test.test/setkategorien.php': 'ok'})

    set_kategorien('https://test.test', 'kategorie1,kategorie2', auth_container=OnlineAuth(None, None, None))

    assert requester.INSTANCE.call_count_of('https://test.test/setkategorien.php') == 1
    assert requester.INSTANCE.data_of_request('https://test.test/setkategorien.php') == [{'kategorien': 'kategorie1,kategorie2'}]

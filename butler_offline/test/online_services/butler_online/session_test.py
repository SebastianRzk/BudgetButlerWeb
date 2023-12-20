
from butler_offline.viewcore import requester
from butler_offline.online_services.butler_online.session import get_partnername, login
from butler_offline.test.requester_stub import RequesterStub, MockedResponse
from butler_offline.online_services.butler_online.session import OnlineAuth


PARTNERNAME_RESPONSE = '''
{
    "partnername": "Partner1"
}
'''

LOGIN_RESPONSE = MockedResponse('data', 'login cookies')

DECODED_LOGIN_DATA = '''{
    "username": "online user name"
}'''


def test_get_partnername():
    requester.INSTANCE = RequesterStub({'https://test.test/api/partner.php': PARTNERNAME_RESPONSE})

    assert get_partnername('https://test.test/api', OnlineAuth(None, None, None)) == 'Partner1'


def test_login():
    requester.INSTANCE = RequesterStub({'https://test.test/api/login.php': LOGIN_RESPONSE},
                                       DECODED_LOGIN_DATA)

    auth_container = login('https://test.test/api', '', '')

    assert auth_container.cookies() == 'login cookies'
    assert auth_container.online_name() == 'online user name'


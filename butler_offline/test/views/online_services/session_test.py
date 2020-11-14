
from butler_offline.viewcore import requester
from butler_offline.views.online_services.session import get_partnername, login
from butler_offline.test.RequesterStub import RequesterStub, MockedResponse
from butler_offline.views.online_services.session import OnlineAuth

auth_response = '''
{
    "username": "Sebastian",
    "token": "0x00",
    "role": "User"
}
'''

partnername_response = '''
{
    "partnername": "Partner1"
}
'''

login_response = MockedResponse('data', 'login cookies')

decoded_login_data = '''{
    "username": "online user name"
}'''

def test_get_partnername():
    requester.INSTANCE = RequesterStub({'https://test.test/api/partner.php': partnername_response})

    assert get_partnername('https://test.test/api', OnlineAuth(None, None, None)) == 'Partner1'


def test_login():
    requester.INSTANCE = RequesterStub({'https://test.test/api/login.php': login_response},
                                       decoded_login_data)

    auth_container = login('https://test.test/api', '', '')

    assert auth_container.cookies() == 'login cookies'
    assert auth_container.online_name() == 'online user name'


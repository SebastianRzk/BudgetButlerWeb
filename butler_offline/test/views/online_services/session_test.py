
from butler_offline.viewcore import requester
from butler_offline.views.online_services.session import get_username, get_partnername, login
from butler_offline.test.RequesterStub import RequesterStub, MockedResponse
from unittest import TestCase

class TestSession(TestCase):
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

    def test_get_username(self):
        requester.INSTANCE = RequesterStub({'https://test.test/api/login.php': self.auth_response})

        assert get_username('https://test.test/api', '', '') == 'Sebastian'

    def test_get_partnername(self):
        requester.INSTANCE = RequesterStub({'https://test.test/api/partner.php': self.partnername_response})

        assert get_partnername('https://test.test/api', '', '') == 'Partner1'

    def test_login(self):
        requester.INSTANCE = RequesterStub({'https://test.test/api/login.php': self.login_response},
                                           self.decoded_login_data)

        auth_container = login('https://test.test/api', '', '')

        assert auth_container.cookies() == 'login cookies'
        assert auth_container.online_name() == 'online user name'


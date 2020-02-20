
from butler_offline.viewcore import requester
from butler_offline.views.online_services.session import get_username
from butler_offline.views.online_services.session import get_partnername
from butler_offline.test.RequesterStub import RequesterStub
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

    def test_get_username(self):
        requester.INSTANCE = RequesterStub({'https://test.test/api/login.php': self.auth_response})

        assert get_username('https://test.test/api', '', '') == 'Sebastian'

    def test_get_partnername(self):
        requester.INSTANCE = RequesterStub({'https://test.test/api/partner.php': self.partnername_response})

        assert get_partnername('https://test.test/api', '', '') == 'Partner1'


from butler_offline.viewcore import requester
from butler_offline.views.online_services.session import get_username
from butler_offline.test.RequesterStub import RequesterStub
from unittest import TestCase

class TesteAddEinzelbuchungView(TestCase):
    auth_response = '''
    {
        "username": "Sebastian",
        "token": "0x00",
        "role": "User"
    }
    '''

    def test_get_username(self):
        requester.INSTANCE = RequesterStub({'https://test.test/login.php': self.auth_response})

        assert get_username('https://test.test','','') == 'Sebastian'

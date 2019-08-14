
from butler_offline.viewcore import requester
from butler_offline.views.online_services.einzelbuchungen import get_einzelbuchungen
from butler_offline.test.RequesterStub import RequesterStub
from unittest import TestCase
import json

class TestEinzelbuchungen(TestCase):
    _JSON_IMPORT_DATA = '''
    [
    {"id":"122","datum":"2019-07-15","name":"Testausgabe1","kategorie":"Essen","wert":"-1.3"},
    {"id":"123","datum":"2019-07-11","name":"Testausgabe2","kategorie":"Essen","wert":"-0.9"}
    ]
    '''

    def test_get_username(self):
        requester.INSTANCE = RequesterStub({'https://test.test/einzelbuchung.php': self._JSON_IMPORT_DATA})

        result =  get_einzelbuchungen('https://test.test','','')

        assert result[0]["id"] == "122"
        assert result[0]["name"] == "Testausgabe1"
        assert result[1]["id"] == "123"
        assert result[1]["name"] == "Testausgabe2"

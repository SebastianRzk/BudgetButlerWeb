
from butler_offline.viewcore import requester
from butler_offline.views.online_services.gemeinsame_buchungen import get_gemeinsame_buchungen
from butler_offline.test.RequesterStub import RequesterStub
from unittest import TestCase
import json

class TestGemeinsameBuchungen(TestCase):
    _JSON_IMPORT_DATA = '''
    [
    {"id":"122","datum":"2019-07-15","name":"Testausgabe1","kategorie":"Essen","wert":"-1.3", "user":"Sebastian", "zielperson":"Sebastian"},
    {"id":"123","datum":"2019-07-11","name":"Testausgabe2","kategorie":"Essen","wert":"-0.9", "user":"other", "zielperson":"other"}
    ]
    '''

    def test_get_username(self):
        requester.INSTANCE = RequesterStub({'https://test.test/gemeinsamebuchung.php': self._JSON_IMPORT_DATA})

        result =  get_gemeinsame_buchungen('https://test.test','','')

        assert result[0]["id"] == "122"
        assert result[0]["name"] == "Testausgabe1"
        assert result[0]["user"] == "Sebastian"
        assert result[0]["zielperson"] == "Sebastian"
        assert result[1]["id"] == "123"
        assert result[1]["name"] == "Testausgabe2"
        assert result[1]["user"] == "other"
        assert result[1]["zielperson"] == "other"

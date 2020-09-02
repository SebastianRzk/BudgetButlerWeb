import unittest

from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.core import file_system
from butler_offline.views.gemeinsame_buchungen import uebersicht_abrechnungen
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler


class TestUebersichtAbrechnungen(unittest.TestCase):
    ABRECHNUNG_A_CONTENT = '''
#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Dynamisch
2017-03-06,Abrechung,Abrechung,-10.0,True
#######MaschinenimportEnd'''
    IMPORT_A_CONTENT = '''
#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Dynamisch
2017-04-06,Import,Import,-10.0,True
2017-04-06,Import,Import,-10.0,True
#######MaschinenimportEnd'''

    def set_up(self):
        file_system.INSTANCE = FileSystemStub()
        file_system.instance().write(file_system.ABRECHNUNG_PATH+'*Abrechnung_A', self.ABRECHNUNG_A_CONTENT)
        file_system.instance().write(file_system.IMPORT_PATH+'*Import_A', self.IMPORT_A_CONTENT)

        persisted_state.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        context = uebersicht_abrechnungen.index(GetRequest())
        assert context['zusammenfassungen'] == [{
            'jahr': '2017',
            'monate': [0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0]
        }]
        assert context['abrechnungen'] == [
            {
                'content': self.ABRECHNUNG_A_CONTENT,
                'name': '../Abrechnungen/*Abrechnung_A'
            },
            {
                'content': self.IMPORT_A_CONTENT,
                'name': '../Import/*Import_A'
            }
        ]


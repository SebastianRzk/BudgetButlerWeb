from datetime import date
import os
import sys
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from test import DBManagerStub
from test.RequestStubs import GetRequest
from test.RequestStubs import PostRequest
from core.DatabaseModule import Database
from importd import views
from viewcore import viewcore
from viewcore.converter import datum
from viewcore import request_handler




# Create your tests here.
class Importd(unittest.TestCase):

    def set_up(self):
        DBManagerStub.setup_db_for_test()
        request_handler.stub_me()

    def test_init_shouldReturnIndexPage(self):
        self.set_up()
        context = views.index(GetRequest())
        assert context['content'] == 'import.html'

    _IMPORT_DATA = '''
    #######MaschinenimportStart
    Datum,Kategorie,Name,Wert,Dynamisch
    2017-03-06,Essen,Edeka,-10.0,True
    #######MaschinenimportEnd
    '''
    def test_addePassendeKategorie_shouldImportValue(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01/01/2017'), 'Essen', 'some name', -1.54)

        context = views.index(PostRequest({'import':self._IMPORT_DATA}))
        assert context['content'] == 'import.html'
        assert einzelbuchungen.select().select_year(2017).sum() == -11.54


    def test_addeUnpassendenKategorie_shouldShowImportMappingPage(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01/01/2017'), 'unbekannt', 'some name', -1.54)

        context = views.index(PostRequest({'import':self._IMPORT_DATA}))
        assert context['content'] == 'import_mapping.html'

    def test_addeUnpassendenKategorie_mitPassendemMapping_shouldImportValue(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01/01/2017'), 'Unpassend', 'some name', -1.54)

        context = views.index(PostRequest({'import':self._IMPORT_DATA, 'Essen_mapping':'als Unpassend importieren'}))
        assert context['content'] == 'import.html'
        assert einzelbuchungen.select().select_year(2017).sum() == -11.54
